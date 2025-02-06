def send_message_with_emoji(update, context, message):
    """Send a message with emojis."""
    context.bot.send_message(chat_id=update.message.chat_id, text=message)