#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import config
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import warranty as warranty_script
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = config.token
print('Bot started successfully.')

WARRANTY, CONVERT_DATE = range(2)
import os

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def start_tool(update,context):
    #keyboard = [[InlineKeyboardButton('Get Warranty', callback_data='warranty'), InlineKeyboardButton('Convert Dates', callback_data='convert dates')]]
    keyboard = [[InlineKeyboardButton('Get Warranty', callback_data='warranty')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select tools to use', reply_markup = reply_markup)
    return ConversationHandler.END

def tool_select(update, context):
    query = update.callback_query
    query.answer()
    choice = query.data
    if choice == 'warranty':
        query.message.reply_text('Please send me your excel file.')
        return WARRANTY
    elif choice == 'convert dates':
        return CONVERT_DATE
    else:
        query.message.reply_text('Error selecting choices')
    return WARRANTY

def warranty(update, context):
    chat_id = update.message.chat_id
    file = update.message.document.get_file().download(custom_path='input.xlsx')
    update.message.reply_text('File received successfully! \n'
                              'Please wait while I process your spreadsheet.')
    warranty_script.main(chat_id)
    update.message.reply_text('Your spreadsheet is ready!')
    update.message.reply_document(document=open('result.xlsx', 'rb'))
    os.remove('result.xlsx')
    os.remove('input.xlsx')
    encouragement_list = ['Are you sleepy yet?', 'Aiseh doing work ah?', 'Talk to me if you bored ', 'Dont forget I am always here for you.', 'Jiayou Jiayou', 'I love you oh']
    random_int = random.randint(0, len(encouragement_list)-1)   #generate random integers
    encouragement_reply_text = encouragement_list[random_int] #select random text from encouragement list to send
    update.message.reply_text(encouragement_reply_text) #send encouragement text
    return ConversationHandler.END

def convert_dates(update, context):
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(tool_select)],
        states={
            WARRANTY: [MessageHandler(Filters.document.mime_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), warranty)],
            CONVERT_DATE: [MessageHandler(Filters.all, convert_dates)],
            #FILE: [MessageHandler(Filters.text, output_file)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]

    )

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('startbot', start_tool))
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()