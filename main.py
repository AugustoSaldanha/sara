#!/usr/bin/python

import telepot
import threading
from telepot.loop import MessageLoop
from sara import *


#needs the bot id
bot = telepot.Bot('bot id')
tdSara = sara(bot)
print(bot.getMe())
MessageLoop(tdSara.bot, tdSara.handle).run_as_thread()
print('Listening')

while True:
    pass
