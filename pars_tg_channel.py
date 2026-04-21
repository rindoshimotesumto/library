import os
from pyrogram import Client

api_id = os.getenv("MY_ACC_ID")
api_hash = os.getenv("MY_ACC_HASH")
bot_username = "@miniProjectsBot"

async def send_audio_to_bot(app: Client, chat_username: str, message_id: int):
    message = await app.get_messages(chat_username, message_id)

    if message.voice or message.audio:
        forwarded = await app.forward_messages(
            chat_id=bot_username,
            from_chat_id=chat_username,
            message_ids=message_id
        )

        # получаем file_id из пересланного сообщения
        if forwarded.voice:
            return forwarded.voice.file_id
        if forwarded.audio:
            return forwarded.audio.file_id
        if forwarded.document:
            return forwarded.document.file_id

    return None