from typing import Optional, Union

from telethon import TelegramClient, events, sync, types
from telethon.tl.types import Channel

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
]):
    return type(tag) in [
        types.MessageEntityCashtag,
        types.MessageEntityUrl,
        types.MessageEntityBankCard,
        types.MessageEntityEmail,
        types.MessageEntityHashtag,
        types.MessageEntityMention,
        types.MessageEntityMentionName,
        types.MessageEntityTextUrl,
        types.MessageEntityUnknown,
    ]


@client.on(events.NewMessage())
async def handler(event: events.NewMessage.Event):
    global target_channel
    if target_channel is None:
        target_channel = await client.get_entity(TARGET_CHANNEL)
    message: types.Message = event.message
    print(event)

    if isinstance(event.message.peer_id, types.PeerChannel):
        channel_id = message.peer_id.channel_id
        if channel_id not in ACCEPTED_CHANNELS:
            return
        if message.entities is not None and len(
                [tag for tag in message.entities if is_ad_tag(tag)]
        ) > 0:
            await message.forward_to(TRASH_CHANNEL)
        else:
            await message.forward_to(TARGET_CHANNEL)


async def main():
    global target_channel
    print(await client.get_dialogs())
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
