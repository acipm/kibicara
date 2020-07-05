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
        self.mentions_since_id = None
        self.dms_since_id = None

    async def run(self):
        await gather(self.poll(), self.push())

    async def poll(self):
        while True:
            messages = await self._poll_direct_messages()
            messages.extend(await self._poll_mentions())
            print(messages)
            # TODO hold since_ids in database
            await self.twitter_model.update(
                dms_since_id=self.dms_since_id, mentions_since_id=self.mentions_since_id
            )
            # TODO send message to censor
            for message in messages:
                await self.publish(Message(message))
            await sleep(self.polling_interval_sec)

    async def _poll_direct_messages(self):
        dms = await self.client.api.direct_messages.events.list.get()
        dms = dms.events
        # TODO check for next_cursor (see twitter api)
        dms_filtered = []
        if dms:
            for dm in dms:
                if dm.id == self.dms_since_id:
                    break
                dms_filtered.append(dm)
            self.dms_since_id = dms[0].id
        messages = []
        for dm in dms_filtered:
            filtered_text = await self._filter_text(
                dm.message_create.message_data.entities,
                dm.message_create.message_data.text,
            )
            if not filtered_text:
                continue
            messages.append(filtered_text)
        logger.debug(messages)
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
            messages.append(filtered_text)
        logger.debug(messages)
        return messages

    async def _filter_text(self, entities, text):
        remove_indices = []
        for user in entities.user_mentions:
            remove_indices.extend(list(range(user.indices[0], user.indices[1] + 1)))
        for url in entities.urls:
            remove_indices.extend(list(range(url.indices[0], url.indices[1] + 1)))
        for symbol in entities.symbols:
            remove_indices.extend(list(range(symbol.indices[0], symbol.indices[1] + 1)))
        filtered_text = ""
        for index, character in enumerate(text):
            if index not in remove_indices:
                filtered_text += character
        filtered_text = filtered_text.strip()
        return filtered_text

    async def push(self):
        while True:
            message = await self.receive()
            print('Received' + message.text)
            # TODO check if report is from twitter itself
            # _retweet(message_id)
            # else
            # _post_tweet(message)

    async def _post_tweet(self, message):
        return await self.client.api.statuses.update.post(status=message)

    async def _retweet(self, message_id):
        return await self.client.api.statuses.retweet.post(id=message_id)


spawner = Spawner(Twitter, TwitterBot)
