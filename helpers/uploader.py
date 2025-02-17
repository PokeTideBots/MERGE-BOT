import os
import time
import asyncio
from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    Message
)
from helpers.display_progress import Progress
from config import Config
from bot import userBot ,LOGCHANNEL
from __init__ import LOGGER

async def uploadVideo(
    c:Client,
    cb: CallbackQuery,
    merged_video_path,
    width,
    height,
    duration,
    video_thumbnail,
    file_size,
    upload_mode: bool,
):
    realcaption = merged_video_path.rsplit('/',1)[-1]
    realcaption = realcaption.replace("_"," ")
    # Report your errors in telegram group.
    if Config.IS_PREMIUM:
        sent_ = None
        prog = Progress(cb.from_user.id, c, cb.message)
        async with userBot:
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await userBot.send_video(
                    chat_id=int(LOGCHANNEL),
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"**{realcaption}**\n\nMerged for: {cb.from_user.mention}",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"Uploading: `{merged_video_path.rsplit('/',1)[-1]}`",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await userBot.send_document(
                    chat_id=int(LOGCHANNEL),
                    document=merged_video_path,
                    thumb=video_thumbnail,
                    caption=f"**{realcaption}**\n\nMerged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"Uploading: `{merged_video_path.rsplit('/',1)[-1]}`",
                        c_time,
                    ),
                )
            if sent_ is not None:
                await c.copy_message(
                    chat_id=cb.message.chat.id,
                    from_chat_id=sent_.chat.id ,
                    message_id=sent_.id,
                    caption=f"**{realcaption}**"
                )
                # await sent_.delete()
    else:
        try:
            sent_ = None
            prog = Progress(cb.from_user.id, c, cb.message)
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await c.send_video(
                    chat_id=cb.message.chat.id,
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"**{realcaption}**",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"Uploading: `{merged_video_path.rsplit('/',1)[-1]}`",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await c.send_document(
                    chat_id=cb.message.chat.id,
                    document=merged_video_path,
                    thumb=video_thumbnail,
                    caption=f"**{realcaption}**",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"Uploading: `{merged_video_path.rsplit('/',1)[-1]}`",
                        c_time,
                    ),
                )
        except Exception as err:
            LOGGER.info(err)
            await cb.message.edit("Failed to upload")
        if sent_ is not None:
            if Config.LOGCHANNEL is not None:
                media = sent_.video or sent_.document
                await sent_.copy(
                    chat_id=int(LOGCHANNEL),
                    caption=f"**{media.file_name}**\n\nMerged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>",
                )
