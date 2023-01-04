import logging
import os
from dotenv import load_dotenv

from telegram import __version__ as TG_VER
from telegram import (
    ReplyKeyboardMarkup,
    Update,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from apis import get_surah, quran_uzbek_text, quran_uzbek_text,send_full_audio

from surahList import dict_surah

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


(ENTRY_STATE,QUESTION_STATE_AR,QUESTION_STATE_UZ,QUESTION_STATE_DICT,AUDIO_STATE_AR,AUDIO_STATE_UZ,TEXT_STATE) = range(7)


def send_dict_as_list(dictionary):
    message = ''
    for i, (key, value) in enumerate(dictionary.items()):
        message += f'{key}: {value}\n'  # Add each item to the message with its number
    while len(message) > 0:
        chunk = message[:4096]  # Get the first 4096 characters of the message
        message = message[4096:]  # Get the rest of the message

        return chunk


async def start(update: Update, context: ContextTypes):
    """Start the conversation and ask user for input."""

    button = [[KeyboardButton(text="Arabic"), KeyboardButton(text="Uzbek")],
    [KeyboardButton(text="Surah List")]]
    # reply_keyboard = ["Book", "Audio"]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        """𝗔𝘀𝘀𝗮𝗹𝗮𝗺𝘂 𝗮𝗹𝗮𝗶𝗸𝘂𝗺! 
𝗖𝗵𝗼𝗼𝘀𝗲 𝗮𝗻 𝗼𝗽𝘁𝗶𝗼𝗻 👇🏻""",
        reply_markup=reply_markup,
    )

    return ENTRY_STATE


# Second step
async def arabic(update: Update, context: ContextTypes):
    """Asks for input"""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
    button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter number of surah ",
        reply_markup=reply_markup,
    )

    return QUESTION_STATE_AR


async def uzbek(update: Update, context: ContextTypes):
    """Enters arabic book menu and asks for 2 options full and verse"""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
    button, resize_keyboard=True
    )

    await update.message.reply_text(
        "Enter number of surah ",
        reply_markup=reply_markup,
    )

    return QUESTION_STATE_UZ


async def surah_list(update: Update, context: ContextTypes):
    """Enters arabic book menu and asks for 2 options full and verse"""

    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
    button, resize_keyboard=True
    )

    a = send_dict_as_list(dict_surah)

    await update.message.reply_text("Processing...")
    await update.message.reply_text(a,reply_markup=reply_markup
    )

    return QUESTION_STATE_DICT

import codecs

async def pre_query_answer_handler_ar(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")], [KeyboardButton(text="Listen audio")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    
    question = update.message.text
    context.user_data['question'] = question

    if int(question)>0 and int(question)<115:

        await update.message.reply_text("Processing...")

        _surah = await get_surah(question)

        for i in range(0, len(_surah)):

            await update.message.reply_text(_surah[i],reply_markup=reply_markup)
    else:
        await update.message.reply_text("You can enter a number between 1 and 114. Try again: ")

    return QUESTION_STATE_AR



async def pre_query_answer_handler_uz(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    button = [[KeyboardButton(text="Back")], [KeyboardButton(text="Listen audio")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    question = update.message.text
    context.user_data['question'] = question

    surah_uz =   context.user_data['question'] 

    if int(question)>0 and int(question)<115:
        await update.message.reply_text("Processing...")
        await update.message.reply_text(await quran_uzbek_text(surah_uz),reply_markup=reply_markup)
    else:
        await update.message.reply_text("You can enter a number between 1 and 114! Try again: ")



    return QUESTION_STATE_UZ


#Handling the audio
async def pre_query_audio_handler_ar(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    res = await send_full_audio(context.user_data['question'])  

    if res:
        await update.message.reply_text("Downloading...")
        await update.message.reply_audio(open("file/audio.mp3", "rb"))
    else:
        await update.message.reply_text("try later")

    os.remove("file/audio.mp3")

    return QUESTION_STATE_AR


#Handling the audio
async def pre_query_audio_handler_uz(update: Update, context: ContextTypes):
    """Display the answer to the user."""

    res = await send_full_audio(context.user_data['question'])


    await update.message.reply_text("Try later")

    # if res:
    #     await update.message.reply_audio(open("file/audio.mp3", "rb"))
    # else:
    #     await update.message.reply_text("try later")

    # os.remove("file/audio.mp3")

    return QUESTION_STATE_UZ

if __name__ == '__main__':
    load_dotenv()

    def main():
        """Run the bot"""

    application =Application.builder().token(os.getenv("BOT_TOKEN")).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                ENTRY_STATE: [
                    MessageHandler(filters.Regex("^Arabic$"), arabic),
                    MessageHandler(filters.Regex("^Uzbek$"), uzbek),
                    MessageHandler(filters.Regex('^Back$'), start),
                    MessageHandler(filters.Regex("Surah List"), surah_list)
                ],
                QUESTION_STATE_AR: [
                    MessageHandler(filters.Regex('^Back$'), start),
                    MessageHandler(filters.Regex('^Listen audio$'), pre_query_audio_handler_ar),
                    MessageHandler(filters.TEXT, pre_query_answer_handler_ar),
                ],
                QUESTION_STATE_UZ: [
                    MessageHandler(filters.Regex('^Back$'), start),
                    MessageHandler(filters.Regex('^Listen audio$'), pre_query_audio_handler_uz),
                    MessageHandler(filters.TEXT, pre_query_answer_handler_uz),
                ],
                AUDIO_STATE_AR: [
                    MessageHandler(filters.Regex('^Back$'), start),
                    MessageHandler(filters.TEXT, pre_query_answer_handler_ar),
            ],
                },
            fallbacks=[],)

    application.add_handler(conv_handler)

    print("Bot started")
    application.run_polling()