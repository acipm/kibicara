# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
#
# SPDX-License-Identifier: 0BSD

from asyncio import gather, sleep
from kibicara.config import config
from kibicara.platformapi import Censor, Message, Spawner
from kibicara.platforms.twitter.model import Twitter
from logging import getLogger
from peony import PeonyClient


logger = getLogger(__name__)


class TwitterBot(Censor):
    def __init__(self, twitter_model):
        super().__init__(twitter_model.hood)
        self.twitter_model = twitter_model
        self.tokens = {
            'consumer_key': config['twitter_consumer_key'],
            'consumer_secret': config['twitter_consumer_secret'],
            'access_token': twitter_model.access_token,
            'access_token_secret': twitter_model.access_token_secret,
        }
        self.client = PeonyClient(**self.tokens)
        self.polling_interval_sec = 60
        self.mentions_since_id = self.twitter_model.mentions_since_id
        self.dms_since_id = self.twitter_model.dms_since_id

    async def run(self):
        if self.twitter_model.successful_verified:
            if self.twitter_model.mentions_since_id is None:
                logger.debug('since_id is None in model, fetch newest mention id')
                mentions = await self._poll_mentions()
            if self.twitter_model.dms_since_id is None:
                logger.debug('since_id is None in model, fetch newest dm id')
                dms = await self._poll_direct_messages()
            logger.debug('Starting Twitter bot: %s' % self.twitter_model.__dict__)
            await gather(self.poll(), self.push())
        else:
            logger.debug('Twitter Bot not started: Oauth Handshake not completed')

    async def poll(self):
        while True:
            dms = await self._poll_direct_messages()
            logger.debug(
                'Polled dms (%s): %s' % (self.twitter_model.hood.name, str(dms))
            )
            mentions = await self._poll_mentions()
            logger.debug(
                'Polled mentions (%s): %s'
                % (self.twitter_model.hood.name, str(mentions))
            )
            await self.twitter_model.update(
                dms_since_id=self.dms_since_id, mentions_since_id=self.mentions_since_id
            )
            for message in dms:
                await self.publish(Message(message))
            for message_id, message in mentions:
                await self.publish(Message(message, twitter_mention_id=message_id))
            await sleep(self.polling_interval_sec)

    async def _poll_direct_messages(self):
        dms = await self.client.api.direct_messages.events.list.get()
        dms = dms.events
        # TODO check for next_cursor (see twitter api)
        dms_filtered = []
        if dms:
            for dm in dms:
                if int(dm.id) == self.dms_since_id:
                    break
                dms_filtered.append(dm)
            self.dms_since_id = int(dms[0].id)
        messages = []
        for dm in dms_filtered:
            filtered_text = await self._filter_text(
                dm.message_create.message_data.entities,
                dm.message_create.message_data.text,
            )
            if not filtered_text:
                continue
            messages.append(filtered_text)
        return messages

    async def _poll_mentions(self):
        mentions = await self.client.api.statuses.mentions_timeline.get(
            since_id=self.mentions_since_id
        )
        if mentions:
            self.mentions_since_id = mentions[0].id
        messages = []
        for mention in mentions:
            filtered_text = await self._filter_text(mention.entities, mention.text)
            if not filtered_text:
                continue
            messages.append((mention.id, filtered_text))
        return messages

    async def _filter_text(self, entities, text):
        remove_indices = set()
        for user in entities.user_mentions:
            remove_indices.update(range(user.indices[0], user.indices[1] + 1))
        for url in entities.urls:
            remove_indices.update(range(url.indices[0], url.indices[1] + 1))
        for symbol in entities.symbols:
            remove_indices.update(range(symbol.indices[0], symbol.indices[1] + 1))
        filtered_text = ""
        for index, character in enumerate(text):
            if index not in remove_indices:
                filtered_text += character
        filtered_text = filtered_text.strip()
        return filtered_text

    async def push(self):
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor (%s): %s'
                % (self.twitter_model.hood.name, message.text)
            )
            if hasattr(message, 'twitter_mention_id'):
                await self._retweet(message.twitter_mention_id)
            else:
                await self._post_tweet(message.text)

    async def _post_tweet(self, message):
        return await self.client.api.statuses.update.post(status=message)

    async def _retweet(self, message_id):
        return await self.client.api.statuses.retweet.post(id=message_id)


spawner = Spawner(Twitter, TwitterBot)
