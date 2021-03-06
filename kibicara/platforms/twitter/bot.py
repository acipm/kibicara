# Copyright (C) 2020 by Cathy Hu <cathy.hu@fau.de>
# Copyright (C) 2020 by Martin Rey <martin.rey@mailbox.org>
#
# SPDX-License-Identifier: 0BSD

from asyncio import CancelledError, gather, sleep
from logging import getLogger

from peony import PeonyClient, exceptions

from kibicara.config import config
from kibicara.platformapi import Censor, Message, Spawner
from kibicara.platforms.twitter.model import Twitter

logger = getLogger(__name__)


class TwitterBot(Censor):
    def __init__(self, twitter_model):
        super().__init__(twitter_model.hood)
        self.twitter_model = twitter_model
        self.enabled = self.twitter_model.enabled
        self.polling_interval_sec = 60
        self.mentions_since_id = self.twitter_model.mentions_since_id
        self.dms_since_id = self.twitter_model.dms_since_id

    @classmethod
    async def destroy_hood(cls, hood):
        """Removes all its database entries."""
        for twitter in await Twitter.objects.filter(hood=hood).all():
            await twitter.delete()

    async def run(self):
        try:
            if not self.twitter_model.verified:
                raise ValueError('Oauth Handshake not completed')
            self.client = PeonyClient(
                consumer_key=config['twitter']['consumer_key'],
                consumer_secret=config['twitter']['consumer_secret'],
                access_token=self.twitter_model.access_token,
                access_token_secret=self.twitter_model.access_token_secret,
            )
            if self.twitter_model.mentions_since_id is None:
                logger.debug('since_id is None in model, fetch newest mention id')
                await self._poll_mentions()
            if self.twitter_model.dms_since_id is None:
                logger.debug('since_id is None in model, fetch newest dm id')
                await self._poll_direct_messages()
            user = await self.client.user
            if user.screen_name:
                await self.twitter_model.update(username=user.screen_name)
            logger.debug(
                'Starting Twitter bot: {0}'.format(self.twitter_model.__dict__)
            )
            await gather(self.poll(), self.push())
        except CancelledError:
            logger.debug(
                'Bot {0} received Cancellation.'.format(self.twitter_model.hood.name)
            )
        except exceptions.Unauthorized:
            logger.debug(
                'Bot {0} has invalid auth token.'.format(self.twitter_model.hood.name)
            )
            await self.twitter_model.update(enabled=False)
            self.enabled = self.twitter_model.enabled
        except (KeyError, ValueError, exceptions.NotAuthenticated):
            logger.warning('Missing consumer_keys for Twitter in your configuration.')
            await self.twitter_model.update(enabled=False)
            self.enabled = self.twitter_model.enabled
        finally:
            logger.debug('Bot {0} stopped.'.format(self.twitter_model.hood.name))

    async def poll(self):
        while True:
            dms = await self._poll_direct_messages()
            logger.debug(
                'Polled dms ({0}): {1}'.format(self.twitter_model.hood.name, str(dms))
            )
            mentions = await self._poll_mentions()
            logger.debug(
                'Polled mentions ({0}): {1}'.format(
                    self.twitter_model.hood.name, str(mentions)
                )
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
        filtered_text = ''
        for index, character in enumerate(text):
            if index not in remove_indices:
                filtered_text += character
        return filtered_text.strip()

    async def push(self):
        while True:
            message = await self.receive()
            logger.debug(
                'Received message from censor ({0}): {1}'.format(
                    self.twitter_model.hood.name, message.text
                )
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
