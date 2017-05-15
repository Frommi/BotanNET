from telegram.ext import Updater
import BotCommand
import util

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logging.getLogger().setLevel(logging.DEBUG)


def main():
    util.init_BD()
    print(util.cursor)

    fkey = open('key.txt', "r")
    skey = fkey.readline()
    fkey.close()

    updater = Updater(token=skey)
    dispatcher = updater.dispatcher

    for i in BotCommand.handlers:
        dispatcher.add_handler(i)
    updater.start_polling()

if __name__ == "__main__":
    main()


