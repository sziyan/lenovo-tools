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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = config.token
print('Bot started successfully.')
TOOL_SELECT, WARRANTY, CONVERT_DATE, FILE = range(4)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def start_tool(update,context):
    reply_keyboard = [['Get Warranty', 'Convert Dates']]

    update.message.reply_text('Select tools to use', reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TOOL_SELECT

def tool_select(update, context):
    choice = update.message.text
    print(choice)
    if choice == 'Get Warranty':
        update.message.reply_text('Please send me your excel file.')
        return WARRANTY
    elif choice == 'Convert Dates':
        return CONVERT_DATE
    else:
        update.message.reply_text('Error selecting choices')

def warranty(update, context):
    file = update.message.document.get_file().download()
    update.message.reply_text('File sent successfully!')

def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

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
        entry_points=[CommandHandler("start_tool", start_tool)],
        states={
            TOOL_SELECT: [MessageHandler(Filters.text, tool_select)],
            WARRANTY: [MessageHandler(Filters.text, warranty)],
            #CONVERT_DATE: [MessageHandler(Filters.text, convert_date)],
            #FILE: [MessageHandler(Filters.text, output_file)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]

    )

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()