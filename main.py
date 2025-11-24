"""
This is a Telegram bot that provides real-time prices for gold, currencies,
and the cryptocurrency market.
"""
# NOTE:
# Please create a `.env` file in your project root
# and add the following environment variables:
#
# API_TOKEN=your_telegram_bot_token
# API_URL=your_api_endpoint_url

import logging
from logging.handlers import RotatingFileHandler
import os
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from API.data import (
    get_gold_prices,
    get_currency_prices,
    get_cryptocurrency_prices
)

from CONTENT import text_resources as TX
from CONTENT.text_resources import (
    get_gold_message_text,
    get_currency_message_text,
    get_cryptocurrency_message_text
)

# Load .env File
load_dotenv()

# Initialize bot with token
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable is not set.")

bot = telebot.TeleBot(API_TOKEN)

# ------------------------------
# Logging Module Configuration
# ------------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)
if not os.path.exists('logs'):
    os.mkdir('logs')

# main.py RotatingFileHandler
handler = RotatingFileHandler(
    filename='logs/bot.log',
    encoding='utf-8',
    mode='a',
    maxBytes=10480000,
    backupCount=2,
)
handler.setLevel(logging.WARNING)
LOG_FORMAT = '[%(asctime)s] %(levelname)-8s | %(filename)s:%(lineno)d  --->  %(message)s'
handler.setFormatter(logging.Formatter(LOG_FORMAT))

# API.py FileHandler
API_handler = logging.FileHandler('logs/api.log')
API_handler.setLevel(logging.WARNING)
LOG_FORMAT = '[%(asctime)s] %(levelname)-8s | %(filename)s:%(lineno)d  --->  %(message)s'
API_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)
logger.addHandler(API_handler)


# ------------------------------
# Command Handlers
# ------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Handle the /start command.

    Creates a custom reply keyboard with several main options:
    - Gold and coin prices
    - Currency exchange rates
    - Cryptocurrency market
    - Help section

    Sends a welcome message to the user and logs basic user information.
    """

    user_id = message.from_user.id
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    username = message.from_user.username or ""

    users_file = 'logs/users.json'

    # Create the file if it doesn't exist
    if not os.path.exists(users_file):
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)

    # Open the file and add the user if not already present
    with open(users_file, 'r+', encoding='utf-8') as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = []
        # Check if the user already exists by ID
        exists = any(user.get("id") == user_id for user in users)
        # Add new user if not found
        if not exists:
            users.append({
                "id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username
            })
            # Write updated data back to file
            f.seek(0)
            json.dump(users, f, ensure_ascii=False, indent=4)
            f.truncate()

    # Send welcome message
    markup = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='انتخاب کنید')
    gold_btn = KeyboardButton('قیمت طلا و سکه')
    currency_btn = KeyboardButton('نرخ ارز')
    cryptocurrency_btn = KeyboardButton('بازار کریپتوکارنسی')
    help_btn = KeyboardButton('راهنمایی')

    markup.add(currency_btn, gold_btn)
    markup.add(help_btn, cryptocurrency_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    logger.warning(message)
    bot.send_message(message.chat.id, TX.START_TEXT, reply_markup=markup, parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'قیمت طلا و سکه')
def send_gold_price(message):
    """
    Handle 'قیمت طلا و سکه' button press.
    Retrieves gold and coin prices from the API data source in real-time.
    """
    try:

        gold_data = get_gold_prices()
    except Exception as e:
        logger.error("Error fetching gold API data in main.py", exc_info=e)
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد! لطفا ساعاتی دیگر امتحان کنید')
        return

    if not gold_data:
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد یا خالی است! /'
                                          ' لطفا ساعاتی دیگر امتحان کنید')
        return

    gold_message_text = get_gold_message_text()
    for gold_name, gold_price in gold_data.items():
        if gold_name == "سکه یک گرمی":
            gold_message_text += '\n'

        try:
            price = int(gold_price)
            formatted_price = f"{price:,}"
        except (ValueError, TypeError):
            formatted_price = str(gold_price) if gold_price else "نامشخص"
            logger.warning("Invalid price format for %s: %s", gold_name, gold_price)

        gold_message_text += f"- {gold_name}: {formatted_price} \n"

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, gold_message_text, parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'نرخ ارز')
def send_currency_price(message):
    """
    Handle 'نرخ ارز' button press.
    Retrieves currency exchange rates in real-time.
    renames 'دلار تتر' to 'تتر' for better clarity,
    and sends a formatted message including all currency prices in Toman.
    """
    try:
        currency_data = get_currency_prices()
    except Exception as e:
        logger.error("Error fetching currency API data in main.py", exc_info=e)
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد! لطفا ساعاتی دیگر امتحان کنید')
        return

    if not currency_data:
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد یا خالی است! /'
                                          ' لطفا ساعاتی دیگر امتحان کنید')
        return

    currency_message_text = get_currency_message_text()
    for currency_name, currency_price in currency_data.items():
        if currency_name == 'دلار تتر':
            currency_name = 'تتر'

        try:
            price = int(currency_price)
            formatted_price = f"{price:,}"
        except (ValueError, TypeError):
            formatted_price = str(currency_price) if currency_price else "نامشخص"
            logger.warning("Invalid price format for %s: %s", currency_name, currency_price)

        currency_message_text += f"- {currency_name}: {formatted_price} \n"

    currency_message_text += '\n (<b>قیمت‌ها به تومان است</b>)'
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, currency_message_text, parse_mode='HTML')


@bot.message_handler(func=lambda message: message.text == 'بازار کریپتوکارنسی')
def send_cryptocurrency_price(message):
    """
    Handle 'بازار کریپتوکارنسی' button press.
    Fetches cryptocurrency prices in real-time.
    renames 'دلار تتر' to 'تتر' for better clarity,
    and sends a formatted message including all currency prices in Toman.
    """
    try:
        cryptocurrency_data = get_cryptocurrency_prices()
    except Exception as e:
        logger.error("Error fetching crypto API data in main.py", exc_info=e)
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد! لطفا ساعاتی دیگر امتحان کنید')
        return

    if not cryptocurrency_data:
        bot.send_message(message.chat.id, 'دیتا از API فراخوانی نشد یا خالی است! /'
                                          ' لطفا ساعاتی دیگر امتحان کنید')
        return

    cryptocurrency_message_text = get_cryptocurrency_message_text()
    for cryptocurrency_name, cryptocurrency_price in cryptocurrency_data.items():
        if cryptocurrency_name in ('تتر', 'استلار'):
            continue

        try:
            price = float(cryptocurrency_price)
            formatted_price = f"{price:,}"
        except (ValueError, TypeError):
            formatted_price = str(cryptocurrency_price) if cryptocurrency_price else "نامشخص"
            logger.warning("Invalid price format %s: %s",cryptocurrency_name, cryptocurrency_price)

        cryptocurrency_message_text += f"- {cryptocurrency_name}: {formatted_price} \n"

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, cryptocurrency_message_text, parse_mode='HTML')


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == 'راهنمایی')
def send_help(message):
    """
    Handle both /help command and 'راهنمایی' button.
    Sends a help message containing usage information
    and available bot commands.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, TX.HELP_TEXT)


@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda message: message.text == 'درباره ما')
def send_about_us(message):
    """
    Handle both /about command and 'درباره ما' button.
    Sends information about the bot, such as purpose and creator details.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, TX.ABOUT_TEXT)


@bot.message_handler(commands=['contact'])
@bot.message_handler(func=lambda message: message.text == 'تماس با ما')
def send_contact_us(message):
    """
    Handle both /contact command and 'تماس با ما' button.
    Sends contact information for support or feedback.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, TX.CONTACT_TEXT)


@bot.message_handler(func=lambda message: True)
def send_hint(message):
    """
    Fallback handler for unrecognized text messages.
    Informs the user to use available buttons or restart the bot.
    """
    bot.send_message(
        message.chat.id,
        'لطفا از یکی از دکمه‌های پایین صفحه استفاده کنید یا دستور /start را بزنید.'
    )


# ------------------------------
# Bot Polling (main loop)
# ------------------------------
bot.infinity_polling()
