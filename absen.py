import logging
from datetime import datetime
import os
from dotenv import load_dotenv  # Import library dotenv
from telegram import Update, BotCommand
from telegram.ext import Updater, CommandHandler, CallbackContext

# Memuat variabel lingkungan dari file .env
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Penyimpanan absensi: {tanggal: set nama pengguna}
attendance = {}

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

def absen(update: Update, context: CallbackContext):
    user = update.effective_user
    if user is None:
        update.message.reply_text("Error: Tidak dapat mengenali pengguna.")
        return

    today = get_today_date()
    if today not in attendance:
        attendance[today] = set()
    if user.full_name in attendance[today]:
        update.message.reply_text(f"Halo {user.full_name}, kamu sudah absen hari ini. Terima kasih!")
    else:
        attendance[today].add(user.full_name)
        update.message.reply_text(f"Absensi kamu dicatat, {user.full_name}. Terima kasih sudah absen!")

def absen_list(update: Update, context: CallbackContext):
    today = get_today_date()
    if today not in attendance or len(attendance[today]) == 0:
        update.message.reply_text("Belum ada yang absen hari ini.")
    else:
        list_absen = "\n".join(f"- {name}" for name in sorted(attendance[today]))
        update.message.reply_text(f"Daftar absen hari ini:\n{list_absen}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Halo! Saya adalah bot absensi grup.\n"
        "Gunakan perintah /absen untuk absen hari ini.\n"
        "Gunakan perintah /absen_list untuk melihat daftar absensi hari ini."
    )

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("Token bot tidak ditemukan! Harap atur variabel lingkungan BOT_TOKEN.")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("absen", absen))
    dp.add_handler(CommandHandler("absen_list", absen_list))

    updater.bot.set_my_commands([
        BotCommand("start", "Memulai bot dan info"),
        BotCommand("absen", "Absen hari ini"),
        BotCommand("absen_list", "Lihat daftar absen hari ini")
    ])

    updater.start_polling()
    logger.info("Bot berjalan dan siap digunakan.")
    updater.idle()

if __name__ == "__main__":
    main()
