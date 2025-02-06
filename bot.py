import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from utils.heroku_utils import validate_heroku_api, list_heroku_apps
from utils.docker_utils import download_and_run_container, zip_and_send_files
from utils.telegram_utils import send_message_with_emoji

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# In-memory storage for API keys
user_api_keys = {}

# Command: /start
def start(update: Update, context: CallbackContext):
    send_message_with_emoji(
        update, context,
        "👋 Welcome to the Heroku Bot! Please set your Heroku API key using /setapi <your_api_key>."
    )

# Command: /setapi <api_key>
def set_api(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        send_message_with_emoji(update, context, "❌ Please provide your Heroku API key.")
        return

    api_key = context.args[0]
    user_id = update.message.from_user.id

    # Validate the API key
    if validate_heroku_api(api_key):
        user_api_keys[user_id] = api_key
        send_message_with_emoji(update, context, "✅ Heroku API key set successfully!")
    else:
        send_message_with_emoji(update, context, "❌ Invalid Heroku API key. Please try again.")

# Command: /apps
def list_apps(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_api_keys:
        send_message_with_emoji(update, context, "❌ Please set your Heroku API key using /setapi first.")
        return

    api_key = user_api_keys[user_id]
    apps = list_heroku_apps(api_key)
    send_message_with_emoji(update, context, f"📋 Heroku Apps:\n{apps}")

# Command: /container <app_name>
def run_container(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_api_keys:
        send_message_with_emoji(update, context, "❌ Please set your Heroku API key using /setapi first.")
        return

    if len(context.args) == 0:
        send_message_with_emoji(update, context, "❌ Please provide the Heroku app name.")
        return

    app_name = context.args[0]
    api_key = user_api_keys[user_id]

    # Download and run the container
    container_id = download_and_run_container(app_name, api_key)
    if container_id:
        send_message_with_emoji(update, context, f"🐳 Container started with ID: {container_id}")
        # Zip and send files
        zip_and_send_files(update, context, app_name)
    else:
        send_message_with_emoji(update, context, "❌ Failed to start the container.")

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("Please set the TELEGRAM_TOKEN environment variable.")

    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("setapi", set_api))
    dispatcher.add_handler(CommandHandler("apps", list_apps))
    dispatcher.add_handler(CommandHandler("container", run_container))

    # Start the bot
    updater.start_polling()
    updater.idle()

if _name_ == "_main_":
    main()