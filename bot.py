import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====== حط التوكن هنا ======
TOKEN = "8614603359:AAHYMsRjWP0bkxW_YSBTVZa1DT9AvDXQEJg"

# ====== بياناتك ======
PHONE = "01156406843"
USERNAME = "kirolosRADY120"

# ====== المنتجات ======
products = {
    "shoes": [
        {
            "name": "حذاء رياضي 1",
            "price": 200,
            "img": "https://i.postimg.cc/Pqqrq3vX/Whats-App-Image-2026-05-04-at-3-37-36-PM.jpg",
        },
        {
            "name": "حذاء كلاسيك 2",
            "price": 250,
            "img": "https://i.postimg.cc/xTKdpbS9/Whats-App-Image-2026-05-04-at-3-33-33-PM.jpg",
        },
    ],
    "pants": [
        {
            "name": "بنطلون شروال راجالي 1",
            "price": 300,
            "img": "https://i.postimg.cc/44Y7PddT/Whats-App-Image-2026-05-04-at-3-38-35-PM.jpg",
        },
        {
            "name": "بنطلون وايد ليج بناتي 2",
            "price": 350,
            "img": "https://i.postimg.cc/Bvhbc99R/Whats-App-Image-2026-05-04-at-3-35-34-PM.jpg",
        },
    ],
}

user_cart = {}

logging.basicConfig(level=logging.INFO)


# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👟 أحذية", callback_data="shoes")],
        [InlineKeyboardButton("👖 بناطيل", callback_data="pants")],
    ]
    await update.message.reply_text(
        "أهلاً بيك 👋 اختر القسم:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ====== عرض الأقسام ======
async def browse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data
    items = products[category]

    for i, item in enumerate(items):
        keyboard = [
            [InlineKeyboardButton("اختار الكمية", callback_data=f"qty_{category}_{i}")]
        ]

        await query.message.reply_photo(
            photo=item["img"],
            caption=f"{item['name']}\nالسعر: {item['price']} جنيه",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# ====== اختيار الكمية ======
async def choose_qty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    category = data[1]
    index = int(data[2])

    keyboard = [
        [InlineKeyboardButton("1x", callback_data=f"add_{category}_{index}_1")],
        [InlineKeyboardButton("2x", callback_data=f"add_{category}_{index}_2")],
        [InlineKeyboardButton("3x", callback_data=f"add_{category}_{index}_3")],
    ]

    await query.message.reply_text(
        "اختار الكمية:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ====== إضافة للسلة ======
async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    category = data[1]
    index = int(data[2])
    qty = int(data[3])

    user_id = query.from_user.id
    item = products[category][index]

    if user_id not in user_cart:
        user_cart[user_id] = []

    user_cart[user_id].append((item, qty))

    keyboard = [
        [InlineKeyboardButton("🛍 نعم عايز حاجة تاني", callback_data="more")],
        [InlineKeyboardButton("✅ تأكيد الطلب", callback_data="confirm")],
    ]

    await query.message.reply_text(
        "تم إضافة المنتج ✅\nهل تريد شيء آخر؟",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ====== رجوع للأقسام ======
async def more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("👟 أحذية", callback_data="shoes")],
        [InlineKeyboardButton("👖 بناطيل", callback_data="pants")],
    ]

    await query.message.reply_text(
        "اختار القسم تاني 👇", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ====== تأكيد الطلب ======
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    cart = user_cart.get(user_id, [])

    if not cart:
        await query.message.reply_text("مفيش طلبات ❌")
        return

    text = "🧾 طلبك:\n\n"
    for item, qty in cart:
        text += f"{item['name']} × {qty}\n"

    keyboard = [
        [InlineKeyboardButton("📞 تواصل على تليجرام", url=f"https://t.me/{USERNAME}")]
    ]

    await query.message.reply_text(
        text + f"\n📱 رقم التواصل: {PHONE}", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ====== تشغيل البوت ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(browse, pattern="^(shoes|pants)$"))
    app.add_handler(CallbackQueryHandler(choose_qty, pattern="^qty_"))
    app.add_handler(CallbackQueryHandler(add_to_cart, pattern="^add_"))
    app.add_handler(CallbackQueryHandler(more, pattern="^more$"))
    app.add_handler(CallbackQueryHandler(confirm, pattern="^confirm$"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
