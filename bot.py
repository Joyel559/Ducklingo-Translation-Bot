from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize translator
translator = GoogleTranslator(source='auto', target='en')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = (
        "👋 Welcome to the Translator Bot!\n\n"
        "Simply send me any text and I'll translate it to English.\n"
        "You can also use commands:\n"
        "/start - Show this message\n"
        "/help - Show help information"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "🔍 How to use this bot:\n\n"
        "1. Simply send any text in any language\n"
        "2. The bot will automatically translate it to English\n"
        "3. If there's an error, try sending the message again"
    )
    await update.message.reply_text(help_text)

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Translate the user message to English."""
    try:
        text = update.message.text
        if not text:
            await update.message.reply_text("Please send some text to translate.")
            return

        # Translate the text
        translation = translator.translate(text)
        
        # If translation is successful, send it back
        if translation:
            await update.message.reply_text(
                f"🔄 Translation to English:\n{translation}"
            )
        else:
            await update.message.reply_text("Sorry, I couldn't translate that text. Please try again.")
            
    except Exception as e:
        await update.message.reply_text(
            "Sorry, there was an error with the translation. Please try again."
        )
        logging.error(f"Translation error: {str(e)}")

def main():
    """Start the bot."""
    # Replace YOUR_BOT_TOKEN with your actual token from BotFather
    TOKEN = "8162879215:AAEUCm62KYbSWJ345WdYlEpJbi552Tznnwo"
    
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handler
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        translate_text
    ))

    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()