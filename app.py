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
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Bot
import warranty as warranty_script
import os

# Enable logging
logging.basicConfig(level=logging.INFO, filename='output.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    token = os.environ.get('TOKEN')
    mychat_id = os.environ.get('CHAT_ID')
except:
    print('Either TOKEN or CHAT_ID is not set!')

bot = Bot(token=token)

print('Bot started successfully.')
logging.info('Bot started successfully.')
bot.send_message(chat_id=mychat_id,text="Bot started successfully")


WARRANTY = range(1)
import os

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Type /startbot to initiate request!')

def ask_input(update, context):
    update.message.reply_text("Please send me your excel file for processing. /cancel to cancel.")
    return WARRANTY

def warranty(update, context):
    chat_id = update.message.chat_id
    mytext = 'Lenovo bot completed processing successfully.'
    file = update.message.document.get_file().download(custom_path='input.xlsx')
    update.message.reply_text('File received successfully! \n'
                              'Please wait while I process your spreadsheet.')
    warranty_script.main(chat_id)
    update.message.reply_text('Your spreadsheet is ready!')
    update.message.reply_document(document=open('result.xlsx', 'rb'))
    bot.send_message(chat_id=mychat_id,text=mytext)
    os.remove('result.xlsx')
    os.remove('input.xlsx')
    return ConversationHandler.END

def template(update, context):
    update.message.reply_text('Please use below template for me to process.')
    update.message.reply_document(document=open('Lenovo.xlsx', 'rb'))

def timeout(update, context):
    update.message.reply_text('Request timed out! /startbot to initiate request again.')

def cancel(update, context):
    update.message.reply_text('Request terminated. /startbot to initate request again.')
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
        entry_points=[CommandHandler('startbot', ask_input)],
        states={
            WARRANTY: [MessageHandler(Filters.document.mime_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), warranty)],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text, timeout)]
        },
        conversation_timeout = 60.0,
        fallbacks=[CommandHandler("cancel", cancel)]

    )

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('template', template))
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()