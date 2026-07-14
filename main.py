import telebot
import pytz
import threading
import time
import os
import requests
from datetime import datetime
from flask import Flask

BOT_TOKEN = "7965180988:AAGWjcnWZ6cL3o4p4OEJ4cofU30k8YnJzEM"
OWNER_ID = 7957605290
ALLOWED_GROUP = "fightx3xvdg"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

is_running = False
last_message_id = None
target_chat_id = None

KOLKATA_TZ = pytz.timezone('Asia/Kolkata')
# Updated start time: 14 July 2026, 5:01 PM (17:01)
START_TIME = KOLKATA_TZ.localize(datetime(2026, 7, 14, 17, 1, 0))

def to_small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    small =  "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ0123456789"
    mapping = str.maketrans(normal, small)
    return text.translate(mapping)

def uptime_loop():
    global last_message_id, is_running, target_chat_id
    
    while True:
        if is_running and target_chat_id:
            now = datetime.now(KOLKATA_TZ)
            diff = now - START_TIME
            
            total_seconds = int(diff.total_seconds())
            
            total_hours = total_seconds // 3600
            total_minutes = (total_seconds % 3600) // 60
            uptime_old = to_small_caps(f"{total_hours} HOURS {total_minutes} MINUTES")
            
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            
            if days > 0:
                uptime_new = f"{days} DAYS {hours} HOURS {minutes} MINUTES"
            else:
                uptime_new = f"{hours} HOURS {minutes} MINUTES"
                
            formatted_total = to_small_caps(uptime_new)
            
            # Updated the display text to match the new start date and time
            uptime_text = f"""<blockquote><b>┏━「 ᴅ-ʙᴀʙᴀɪ ᴠs 𝟑x-ᴀsʀᴀғᴜʟ 」</b>
<b>┣</b> 🧪 <b>ᴜᴘᴛɪᴍᴇ:</b> ᴄᴏᴅᴇ—ᴅᴇᴛᴇᴄᴛᴏʀ
<b>┣</b> ⏳ <b>sᴛᴀʀᴛ:</b> 𝟷𝟺.𝟶𝟽.𝟸𝟶𝟸𝟼 | 𝟶𝟻:𝟶𝟷 ᴘᴍ
<b>┣</b> ⏱️ <b>ᴜᴘᴛɪᴍᴇ:</b> {uptime_old}
<b>┣</b> 🗓️ <b>ᴛᴏᴛᴀʟ:</b> {formatted_total}
<b>┗━━━━━➾</b> 👨‍💻 <b>ᴅᴇᴠ:</b> Ｄｘ－Ｓｉｍｕ</blockquote>"""

            if last_message_id:
                try:
                    bot.delete_message(target_chat_id, last_message_id)
                except Exception as e:
                    pass
            
            try:
                msg = bot.send_message(target_chat_id, uptime_text, parse_mode="HTML")
                last_message_id = msg.message_id
            except Exception as e:
                print(f"Error sending message: {e}")
                
        time.sleep(60)

@bot.message_handler(commands=['on'])
def turn_on(message):
    global is_running, target_chat_id, last_message_id
    
    if message.from_user.id != OWNER_ID:
        return
        
    if message.chat.username != ALLOWED_GROUP:
        bot.reply_to(message, f"❌ ᴇʀʀᴏʀ: ᴛʜɪs ʙᴏᴛ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ Ｄａｒｋ－Ｇａｎｇ")
        return

    if not is_running:
        is_running = True
        target_chat_id = message.chat.id
        last_message_id = None
        bot.reply_to(message, "✅ ᴜᴘᴛɪᴍᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ sᴛᴀʀᴛᴇᴅ.")
    else:
        bot.reply_to(message, "⚠️ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ!")

@bot.message_handler(commands=['off'])
def turn_off(message):
    global is_running
    
    if message.from_user.id != OWNER_ID:
        return
        
    if is_running:
        is_running = False
        bot.reply_to(message, "🛑 ᴜᴘᴛɪᴍᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ sᴛᴏᴘᴘᴇᴅ.")
    else:
        bot.reply_to(message, "⚠️ ɴᴏᴛ ʀᴜɴɴɪɴɢ ᴄᴜʀʀᴇɴᴛʟʏ.")

@app.route('/')
def home():
    return "DX-CODEX Bot is Alive!"

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive_ping():
    port = int(os.environ.get('PORT', 8080))
    URL = os.environ.get('RENDER_EXTERNAL_URL', f"http://localhost:{port}")
    B = "ALIVE-PING"
    
    time.sleep(10) 
    
    while True:
        try:
            requests.get(URL)
            print(f"[{B}] Pinging server ({URL}) to stay awake...")
        except Exception as e:
            print(f"[{B}] Ping failed: {e}")
        time.sleep(300)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    ping_thread = threading.Thread(target=keep_alive_ping, daemon=True)
    ping_thread.start()
    
    uptime_thread = threading.Thread(target=uptime_loop, daemon=True)
    uptime_thread.start()
    
    print("🤖 Bot Started... Waiting for /on command in group.")
    bot.infinity_polling()
