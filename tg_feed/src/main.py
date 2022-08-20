import asyncio
import signal
from typing import Union

from telethon import TelegramClient, events, types
from telethon.tl.types import Message
from config import get_logger

from config import API_ID, API_HASH, ACCEPTED_CHANNELS, TARGET_CHANNEL, \
    TRASH_CHANNEL, ACCEPTED_URLS

logger = get_logger(__name__)


def is_ad_tag(tag: Union[
    types.MessageEntityBold,
    types.MessageEntityCode,
    types.MessageEntityCashtag,
    types.MessageEntityPre,
    types.MessageEntityUrl,
    types.MessageEntityBankCard,
    types.MessageEntityBlockquote,
    types.MessageEntityBotCommand,
    types.MessageEntityEmail,
    types.MessageEntityHashtag,
    types.MessageEntityItalic,
    types.MessageEntityMention,
    types.MessageEntityMentionName,
    types.MessageEntityPhone,
    types.MessageEntityStrike,
    types.MessageEntityTextUrl,
    types.MessageEntityUnderline,
    types.MessageEntityUnknown,
], message: Message):
    logger.info(f"Processing tag {tag.to_dict()} "
                f"({message.message[tag.offset:tag.offset + tag.length]}), "
                f"type {type(tag)}")
    is_mention_tag = type(tag) in [
        types.MessageEntityCashtag,
        types.MessageEntityBankCard,
        types.MessageEntityEmail,
        types.MessageEntityMention,
        types.MessageEntityMentionName,
        types.MessageEntityUnknown,
    ]
    logger.info(f"Is {'' if is_mention_tag else 'not '}a mention tag")
    is_url_tag = type(tag) in [
        types.MessageEntityTextUrl, types.MessageEntityUrl
    ]
    is_bad_url_tag = True
    if is_url_tag:
        url_part = (
            tag.url if type(tag) == types.MessageEntityTextUrl
            else message.message[tag.offset:tag.offset + tag.length]
        )
        logger.info(f"Checking if any of {ACCEPTED_URLS} is in {url_part}")
        for good_url in ACCEPTED_URLS:
            if good_url in url_part:
                is_bad_url_tag = False
                logger.info(f"{good_url} is in url_part, tag is ok")
                break
    is_ad = is_mention_tag or (is_url_tag and is_bad_url_tag)
    logger.info(
        f"Mention tag: {is_mention_tag}, url tag: {is_url_tag}, "
        f"bad url tag: {is_bad_url_tag}"
    )
    return is_ad


async def handler(client: TelegramClient, sent_group_id: set, event: events.NewMessage.Event):
    message: types.Message = event.message
    logger.info(f"Message: {str(message)}")
    if isinstance(event.message.peer_id, types.PeerChannel):
        channel_id = message.peer_id.channel_id
        if channel_id not in ACCEPTED_CHANNELS:
            logger.info(f"Not from a target channel: {channel_id}")
            return
        if message.entities is not None and len(
                [tag for tag in message.entities if is_ad_tag(tag, message)]
        ) > 0:
            logger.info("Got an ad tag, goto trash")
            await message.forward_to(TRASH_CHANNEL, as_album=True)
        else:
            logger.info("Good post, goto target")
            if message.grouped_id is not None:
                if message.grouped_id in sent_group_id:
                    logger.info("Already sent this group")
                    return
                logger.info("Hasn't sent yet")
                sent_group_id.add(message.grouped_id)
                res = await client.get_messages(channel_id, limit=10)
                logger.info("Got messages")
                to_send = []
                for elem in res:
                    if elem.grouped_id == message.grouped_id:
                        to_send.append(elem)
                logger.info(f"Sending album of {len(to_send)} media")

                await client.forward_messages(TARGET_CHANNEL, to_send)
            else:
                logger.info(f"Sending single message ")
                logger.error(
                    await message.forward_to(TARGET_CHANNEL))


async def terminate(client: TelegramClient):
    logger.info(f"Terminating...")
    await client.disconnect()


async def configure_and_start_polling():
    client = TelegramClient('tg_feed', API_ID, API_HASH)
    asyncio.get_event_loop().add_signal_handler(
        signal.SIGINT, lambda: asyncio.ensure_future(client.disconnect()))
    asyncio.get_event_loop().add_signal_handler(
        signal.SIGTERM, lambda: asyncio.ensure_future(client.disconnect()))
    await client.connect()
    sent_grouped_id = {}

    client.on(events.NewMessage())(lambda event: handler(client, sent_grouped_id, event))

    logger.info("Start polling")
    await client.run_until_disconnected()
    logger.info("Stopping...")


def main():
    asyncio.run(configure_and_start_polling())


if __name__ == "__main__":
    main()
