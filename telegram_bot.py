
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from query_data import query_rag, remove_think_block
import os
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# API key
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def chatLLM(prompt: str) -> str:
    """Generate response from LLM model."""
    try:
        return remove_think_block( await query_rag(prompt))
    except Exception as e:
        logging.error(f"LLM Query Error: {e}")
        return "Sorry, I couldn't process your request."


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    user_message = update.message.text
    response = await chatLLM(user_message)
    await update.message.reply_text(response)

    
def telegram_bot_start() -> None:
    
    """Start the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot is running...")
    app.run_polling()



def main() -> None:
    telegram_bot_start() 


if __name__ == "__main__":
    main()
