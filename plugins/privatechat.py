from pyrogram import Client, filters
from pyrogram.types import Message

import constants
import db
from tr import tr


@Client.on_message(
    filters.command("hi")
    & filters.private
)
async def start(bot, message: Message):
    await message.reply_text(constants.start_message_text.format(message.from_user.mention()))


@Client.on_message(
    filters.command("help")
    & filters.private
)
async def help(bot, message: Message):
    await message.reply_text(constants.help_text)


@Client.on_message(
    filters.command("donate")
    & filters.private
)
async def donate(bot, message: Message):
    await message.reply_text(constants.donate_text)


@Client.on_message(filters.command("language"))
async def language(bot, message: Message):
    await message.reply_text(constants.language_text)


@Client.on_message(filters.command("lang") & filters.private)
async def setmylang(bot, message: Message):
    thelang = message.command[1]
    await message.reply(f"{thelang} has been set as your main language.")
    db.set_lang(message.chat.id, message.chat.type, thelang)


@Client.on_message(filters.private & ~filters.command("tr"))
async def main(bot, message: Message):
    userlang = db.get_lang(message.chat.id, message.chat.type)
    translation = await tr(message.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(message.text)
    await message.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")


@Client.on_message(filters.command("tr") & filters.private)
async def translateprivatetwo(bot, message: Message):
    to_translate = message.text.split(None, 2)[2]
    language = await tr.detect(message.text.split(None, 2)[2])
    tolanguage = message.command[1]
    translation = await tr(to_translate,
                           sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}"
    await message.reply(trmsgtext, parse_mode="markdown")