# main.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, render_template
import threading
import config

# Telegram Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Visit my site: {config.SITE_URL}")

def run_bot():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Flask Web Server
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        return render_template("index.html", submitted_url=url)
    return render_template("index.html", submitted_url=None)

def run_flask():
    flask_app.run(host="0.0.0.0", port=80)

# Run both bot and Flask server
if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # Start Telegram bot
    run_bot()
