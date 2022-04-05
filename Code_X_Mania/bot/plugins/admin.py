# (c) @code-x-mania
import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
from Code_X_Mania.utils.broadcast_helper import send_msg
from Code_X_Mania.utils.database import Database
from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
from pyrogram import filters, Client
from pyrogram.types import Message
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
broadcast_ids = {}


@StreamBot.on_message(filters.command("status") & filters.private & filters.user(Var.OWNER_ID) & ~filters.edited)
async def sts(c: Client, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"**Kullanıcı sayısı:** `{total_users}`", parse_mode="Markdown", quote=True)


@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(Var.OWNER_ID) & filters.reply & ~filters.edited)
async def broadcast_(c, m):
    user_id=m.from_user.id
    out = await m.reply_text(
            text=f"Yayın başladı! Tüm kullanıcılar bilgilendirildiğinde günlük dosyası ile bilgilendirileceksiniz."
    )
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"yayın tamamlandı `{completed_in}`\n\nToplam kullanıcı {total_users}.\n Toplam Yapılan {done}, {success} Başarı ve {failed} başarısız.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"yayın tamamlandı `{completed_in}`\n\nToplam kullanıcı {total_users}.\nToplam Yapılan {done}, {success} başarı ve {failed} başarısız.",
            quote=True
        )
    os.remove('broadcast.txt')
