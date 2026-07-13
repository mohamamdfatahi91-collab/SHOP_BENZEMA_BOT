from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8805053771:AAFzYctAkxQecMcXUWg7-WgmPIXAmV89DAg"

ADMIN_ID = 8527824342

CARD_NUMBER = "6219 8614 5297 1103"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📦 خرید کانفیگ"],
        ["💰 قیمت‌ها"],
        ["👤 پشتیبانی"]
    ]

    await update.message.reply_text(
        "سلام 🌹\nبه فروشگاه کانفیگ خوش آمدید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📦 خرید کانفیگ":

        keyboard = [
            ["کانفیگ ۱ ماهه"],
            ["کانفیگ ۳ ماهه"],
            ["کانفیگ ۶ ماهه"]
        ]

        await update.message.reply_text(
            "مدت کانفیگ را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )


    elif text in [
        "کانفیگ ۱ ماهه",
        "کانفیگ ۳ ماهه",
        "کانفیگ ۶ ماهه"
    ]:

        context.user_data["config"] = text

        await update.message.reply_text(
            f"💳 کارت به کارت کنید:\n\n"
            f"{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید."
        )


    elif text == "💰 قیمت‌ها":

        await update.message.reply_text(
            "💰 قیمت‌ها:\n\n"
            "۱ ماهه: 100 هزار تومان\n"
            "۳ ماهه: 250 هزار تومان\n"
            "۶ ماهه: 450 هزار تومان"
        )


    elif text == "👤 پشتیبانی":

        await update.message.reply_text(
            "با ادمین در ارتباط باشید."
        )



async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    config = context.user_data.get(
        "config",
        "انتخاب نشده"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ تایید پرداخت",
                callback_data=f"ok_{user.id}"
            ),
            InlineKeyboardButton(
                "❌ رد پرداخت",
                callback_data=f"no_{user.id}"
            )
        ]
    ])


    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"""
🧾 رسید جدید

👤 نام:
{user.first_name}

🆔 آیدی:
{user.id}

📦 کانفیگ:
{config}
""",
        reply_markup=keyboard
    )


    await update.message.reply_text(
        "رسید ارسال شد ✅\nمنتظر تایید ادمین باشید."
    )



async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    if data.startswith("ok_"):

        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ پرداخت شما تایید شد.\nادمین به زودی کانفیگ را ارسال می‌کند."
        )

        await query.answer("تایید شد")


    elif data.startswith("no_"):

        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ پرداخت شما تایید نشد. لطفاً با پشتیبانی تماس بگیرید."
        )

        await query.answer("رد شد")



def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    app.add_handler(
        CallbackQueryHandler(admin_button)
    )


    print("Bot is running...")

    app.run_polling()



if __name__ == "__main__":
    main()
