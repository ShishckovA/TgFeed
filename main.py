from typing import Optional, Union

from telethon import TelegramClient, events, sync, types
from telethon.tl.types import Channel, Message
from config import logger

from config import API_ID, API_HASH, ACCEPTED_CHANNELS, TARGET_CHANNEL, \
    TRASH_CHANNEL

client = TelegramClient('tg_feed', API_ID, API_HASH)
target_channel: Optional[Channel] = None


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
                 f"({message.message[tag.offset:tag.offset + tag.length]}, "
                 f"type {type(tag)}")
    is_ad = type(tag) in [
        types.MessageEntityCashtag,
        types.MessageEntityBankCard,
        types.MessageEntityEmail,
        types.MessageEntityMention,
        types.MessageEntityMentionName,
        types.MessageEntityUnknown,
    ] or (type(tag) == types.MessageEntityTextUrl and
          'teletype' not in tag.url) \
            or (type(tag) == types.MessageEntityUrl and
                'teletype' not in message.message[
                                  tag.offset:tag.offset + tag.length])
    logger.info(f"Is {'' if is_ad else 'not '}an ad tag")
    return is_ad


@client.on(events.NewMessage())
async def handler(event: events.NewMessage.Event):
    global target_channel
    if target_channel is None:
        logger.info("Updating target_channel")
        target_channel = await client.get_entity(TARGET_CHANNEL)
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
            await message.forward_to(TRASH_CHANNEL)
        else:
            logger.info("Good post, goto target")
            await message.forward_to(TARGET_CHANNEL)


async def main():
    global target_channel
    await client.run_until_disconnected()


with client:
    logger.info("Starting...")
    client.loop.run_until_complete(main())
