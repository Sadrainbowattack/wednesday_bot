

def greet_user(update,context):
    print('Вызван /start')
    update.message.reply_text(
        f"Здарова, бандиты!")