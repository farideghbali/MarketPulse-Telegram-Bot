"""
This module contains all static text templates and dynamic text generation functions
used by the Telegram bot. Dynamic functions ensure real-time date and time updates.
"""

import emoji
import jdatetime


def get_current_jalali_time():
    """Calculates and returns the current Jalali date and time."""
    now = jdatetime.datetime.now()
    return now.strftime('%Y/%m/%d'), now.strftime('%H:%M')

# --------------------------------------------------
# Gold & Coin Message Template
# --------------------------------------------------
def get_gold_message_text():
    """Generates the gold price message text with the current time."""
    date_str, time_str = get_current_jalali_time()
    return f"""
<b>{emoji.emojize(":yellow_circle:")} قیمت طلا و سکه</b>

تاریخ: {date_str}
ساعت: {time_str}

"""

# --------------------------------------------------
# Currency Exchange Message Template
# --------------------------------------------------
def get_currency_message_text():
    """Generates the currency message text with the current time."""
    date_str, time_str = get_current_jalali_time()
    return f"""
{emoji.emojize(":green_circle:")} <b> نرخ ارز </b>

تاریخ: {date_str}
ساعت: {time_str}

"""

# --------------------------------------------------
# Cryptocurrency Market Message Template
# --------------------------------------------------
def get_cryptocurrency_message_text():
    """Generates the cryptocurrency message text with the current time."""
    date_str, time_str = get_current_jalali_time()
    return f"""
{emoji.emojize(":orange_circle:")} <b>آخرین قیمت‌های بازار کریپتو:</b>

تاریخ: {date_str}
ساعت: {time_str}

"""

# Welcome Message (Triggered by /start)
START_TEXT = f"""
سلام {emoji.emojize(":man_raising_hand:")}
به ربات <b> زر‌ ارز </b> خوش اومدی!

اینجا می‌تونی قیمت لحظه‌ای طلا، سکه و ارزهای پرکاربرد رو ببینی

برای شروع، یکی از گزینه‌های زیر رو انتخاب کن {emoji.emojize(":backhand_index_pointing_down:")}
"""

# Help Message
HELP_TEXT = f"""
برای استفاده از ربات، فقط کافیه یکی از دکمه‌های زیر رو انتخاب کنید:

{emoji.emojize(":money_bag:")} قیمت طلا و سکه: نمایش لحظه‌ای قیمت انواع طلا و سکه.
{emoji.emojize(":dollar_banknote:")} نرخ ارز: مشاهده نرخ دلار، یورو و سایر ارزها.
{emoji.emojize(":coin:")} بازار کریپتوکارنسی: دریافت آخرین داده‌های بازار کریپتو به‌صورت لحظه‌ای.

{emoji.emojize(":pushpin:")} اگر ربات پاسخ نداد \
یا قیمت‌ها نمایش داده نشدن، چند ثانیه صبر کنید و دوباره امتحان کنید.

در صورت بروز مشکل، می‌تونید با پشتیبانی تماس بگیرید.
جهت ارتباط با سازنده\
 از منوی سمت چپ گزینه تماس با سازنده رو انتخاب کنید. {emoji.emojize(":folded_hands:")}
"""

# About Us Message
ABOUT_TEXT = f"""
من یک ربات هوشمند هستم که به‌صورت لحظه‌ای قیمت طلا، سکه، دلار و سایر ارزها رو نمایش می‌دم.
هدفم اینه که بدون نیاز به جست‌وجو در سایت‌ها یا کانال‌های مختلف، فقط با یک کلیک، جدیدترین قیمت‌ها رو در دسترس شما بذارم.
داده‌ها به‌صورت خودکار و مداوم به‌روزرسانی می‌شن تا همیشه جدیدترین اطلاعات رو ببینید. و به مرور امکانات دیگری هم اضافه می‌کنم.
و برای همیشه رایگان هستم {emoji.emojize(":yellow_heart:")}
"""

# Contact Us Message
CONTACT_TEXT = f"""
سلام! {emoji.emojize(":man_raising_hand:")}
من فرید اقبالی هستم، توسعه‌دهنده‌ی این ربات.

اگر پیشنهادی برای بهبود ربات داری یا مشکلی مشاهده کردی، لطفاً با ما در تماس باش.
{emoji.emojize(":envelope:")} ارتباط از طریق تلگرام: @farid_eghbali
{emoji.emojize(":e-mail:")} یا ایمیل: info@farideghbali.com

{emoji.emojize(":speech_balloon:")} پیشنهادها و نظراتتون باعث رشد ما می‌شه!
"""

# --------------------------------------------------
# Static texts alias for backwards compatibility in main.py
# --------------------------------------------------

class TextResources:
    """
    Static texts alias for backwards compatibility in main.py
    """
    START_TEXT = START_TEXT
    HELP_TEXT = HELP_TEXT
    ABOUT_TEXT = ABOUT_TEXT
    CONTACT_TEXT = CONTACT_TEXT

text_resources = TextResources()
