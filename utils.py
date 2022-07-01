from telegram import ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([['Random frog', 'Save my frog'], ['Subscribe', 'Unsubscribe']], True, True)
