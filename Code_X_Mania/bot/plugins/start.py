# (c) adarsh-goel

from Code_X_Mania.bot import StreamBot
from Code_X_Mania.vars import Var
from Code_X_Mania.utils.human_readable import humanbytes
from Code_X_Mania.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
from pyshorteners import Shortener

def get_shortlink(url):
   shortlink = False 
   try:
      shortlink = Shortener().dagd.short(url)
   except Exception as err:
       print(err)
       pass
   return shortlink

@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Yeni Üye Katıldı:** \n\n__Yeni Arkadaşım__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Bot Çalışıyor !!__"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text=" Siz Yasaklandiniz \n\n @DTO_Bots **",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i> Kanala Abone ol 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Katıl 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>HATA!! </i> <b> <a href='http://t.me/DTO_Bots'> Yardım için Tıkla </a></b>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text="""
Esenlikler Sayğılar 👋,Bu Bot Video/Dosya'nızdan Anında  İndirme ve Akış Bağlantısı vermek için Tasarlanmış.

<b>Bana Bir Video / Dosya Gönderin! </b>

            """,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup( [ [InlineKeyboardButton('Yiyesi', url=f"https://t.me/iLqar_TurkSoy"),
                                                                                       InlineKeyboardButton('Takip Et ', url='https://t.me/turandizi') ] ]  ) )
                                                                                       
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**Üzgünüm , Siz Yasaklandanız , Yöneticile iletişime Geçin** @ilqar_TurkSoy",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Botu Kullanmak için Kanala Abone Olmayın Gerekir**!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Kanalimiz", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Yenile / Yeniden dene",
                                                     url=f"https://t.me/{Var.APP_NAME}.herokuapp.com/{usr_cmd}") # Chnage ur app name
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Hata Baş Verdiyi Zaman , Yöneticiye Bildirin** [iLqar TürkSoy](https://t.me/iLqar_TurkSoy).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = Var.URL + 'watch/' + str(log_msg.message_id)
        shortlink = get_shortlink(stream_link)
        if shortlink:
            stream_link = shortlink
        online_link = Var.URL + 'download/' + str(log_msg.message_id)
        shortlinka = get_shortlink(online_link)
        if shortlinka:
            online_link = shortlinka

        msg_text ="""
<i><u>Bağlantınız Oluşturuldu!</u></i>

<b>📂 Dosya Adı :</b> <i>{}</i>

<b>📦 Boyut :</b> <i>{}</i>

<b>📥 İndirmek :</b> <i>{}</i>

<b> 🖥Akış  :</b> <i>{}</i>

<b>🚸 Dikkat:  Ben silene kadar bağlantının süresi dolmayacak </b>

"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, online_link, stream_link),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥AKIŞ", url=stream_link), #Stream Link
                                                InlineKeyboardButton('İNDİRMEK📥', url=online_link)]]) #Download Link
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Yeni üye katıldı **\n\n__Yeni Arkadaşım__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Bot Çalışıyor !!__"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>    Üzgünüm Arkadaş, Yasalar İhlali Nedeniyle yasaklandınız </i>",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text=" Bot kullanmak için lütfen kanala katılın.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Kanal", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text=" Hata Baş Verdi , Yöneticiye Bildirin! [Yönetici](https://t.me/ilqar_turksoy).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
   
    await message.reply_text(
       text="Bana Telegramdan Dosya / Medya Gönder ,Harici indirme bağlantısı sağlayacağım..",
            parse_mode="HTML",
            
          reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("😇Bağış Yapmak", url="https://t.me/ilqar_turksoy")]
            ]
        )
    )
