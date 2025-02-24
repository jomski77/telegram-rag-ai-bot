from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread
import time
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import asyncio
from datetime import datetime
from query_data import query_rag, remove_think_block, clean_llm_formatting
import os
from dotenv import load_dotenv
import logging

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', transports=['polling'])
#socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', transports=['polling'])

# Global variables
bot_active = False
messages = []
responses = []


def prepend_timestamp(message: str):
    """
    Prepend the current date and time to the given message in the format [DD/Mon/YYYY HH:MM:SS]
    with proper padding.
    """
    timestamp = datetime.now().strftime('[%d/%b/%Y %H:%M:%S]')
       
    return f"{timestamp} {message}"



# Function to handle Telegram messages
async def handle_telegram_messages(update: Update, context: CallbackContext):
    global messages, responses
    ogMessage = update.message.text

    message = prepend_timestamp(f'[{update.message.from_user.id}] {update.message.chat.first_name} {update.message.chat.last_name} ({update.message.chat.username}) - {ogMessage}')
    logging.info(f"🧑‍💻 Telegram User: {message}")

    await update.message.reply_text("🤖 Processing your inquiry...")        
    
    response = remove_think_block( await query_rag(ogMessage))    
    
    response = clean_llm_formatting(response)    
    await update.message.reply_text(response)
    logging.info(f"🤖 Telegram Bot: {response}")

    response = prepend_timestamp(response)
    messages.append(message)
    responses.append(response)
       
    # Emit new message and response to the frontend
    socketio.emit('new_message', {'message': message, 'response': response})




# Background task for the Telegram bot
def start_bot():
    # Create and run a new event loop for the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_messages))
        
    #loop.create_task(application.run_polling())
    #loop.run_forever()
    loop.run_until_complete(application.run_polling())

    logging.info(f"🛠️📡 Telegram bot started.")




# Start bot in background
def start_bot_background():    
    global bot_active
        
    if not bot_active:        
        t = Thread(target=start_bot, daemon=True)
        t.start()
        bot_active = True


# WebSocket event to send initial messages
@socketio.on('connect')
def handle_connect():
    emit('initial_data', {'messages': messages, 'responses': responses})


@app.route('/')
def index():    
    return render_template('index.html')

if __name__ == '__main__':     
    start_bot_background()           
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
     
    