import os
import telepot
import subprocess
import threading
import json

from functions import *
from pyYify import yify


class sara():
    def __init__(self, bot):
        self.bot = bot
    def handle(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        
        print ('Received:')
        print(chat_id)
        print(command)

        if  chat_id == 1193864225:
            if command == '/oi':
                self.bot.sendMessage(chat_id, str("Ola! Parabens, tudo funcionando"))
            elif command.lower() == '/horas':
                self.bot.sendMessage(chat_id, str("Horas: ") + str(now.hour) + str(":") + str(now.minute))
            elif command.lower() == 'desligue a luz do quarto':
                self.bot.sendMessage(chat_id, str("Desligando..."))
                os.system("mosquitto_pub -t Test -m 0")
            elif command.lower() == 'ligue a luz do quarto':
                self.bot.sendMessage(chat_id, str("Ligando..."))
                os.system("mosquitto_pub -t Test -m 1")
            elif command.lower() == 'desligue a tv':
                self.bot.sendMessage(chat_id, str("Desligando..."))
                os.system("echo 'standby 0' | cec-client -s -d 1")
            elif command.lower() == 'ligue a tv':
                self.bot.sendMessage(chat_id, str("Ligando..."))
                os.system("echo 'on 0' | cec-client -s -d 1")
            elif command.lower() == 'aumente o volume':
                self.bot.sendMessage(chat_id, str("Volume +1"))
                os.system("echo 'volup 0' | cec-client -s -d 1")
            elif command.lower() == 'diminua o volume':
                self.bot.sendMessage(chat_id, str("Volume -1"))
                os.system("echo 'voldown 0' | cec-client -s -d 1")
            elif command.lower() == 'ligue o ps4':
                self.bot.sendMessage(chat_id, str("Ligando"))
                os.system("echo 'on 4' | cec-client -s -d 1")
            elif command.lower() == 'modo de espera ps4':
                self.bot.sendMessage(chat_id, str("Ligando"))
                os.system("echo 'standby 4' | cec-client -s -d 1")
            elif command.lower() == 'temperatura':
                self.bot.sendMessage(chat_id, str("Medindo"))
                temp = subprocess.getoutput("mosquitto_sub -t esp32/temperature -R -C 1 -W 10")
                if temp == "":
                    self.bot.sendMessage(chat_id, str("Impossivel ler a temperatura"))
                    return
                else:
                    self.bot.sendMessage(chat_id, temp + "Graus")
                    self.bot.sendMessage(chat_id, str("Humidade: "))
                    humi = subprocess.getoutput("mosquitto_sub -t esp32/humidity -R -C 1")
                    self.bot.sendMessage(chat_id, str(humi + "%"))
            elif command.lower() == '/help':
                dados = open('help.json', 'r')
                hp = json.load(dados)
                for n in hp:
                    self.bot.sendMessage(chat_id, n)
                dados.close()
                del hp
            elif 'Youtube,' in command:
                t = threading.Thread(target=getVideo, args=(chat_id, command, self.bot))
                t.start()
            elif 'Kodi' in command:
                t = threading.Thread(target=openKodi, args=(chat_id, "kodi", self.bot))
                t.start()
            elif 'magnet:' in command:
                try:
                    t = threading.Thread(target=getTorrent, args=(chat_id, command, self.bot))
                    t.start()
                    self.bot.sendMessage(chat_id, str("Bom filme :)"))
                except:
                    self.bot.sendMessage(chat_id, str("Nao foi possivel executar"))
            elif 'serie,' in command.lower() or 'filme,' in command.lower() or 'anime,' in command.lower() or 'musica,' in command.lower():
                try:
                    t = threading.Thread(target=searchTorrent, args=(chat_id, command, self.bot))
                    t.start()
                except:
                    self.bot.sendMessage(chat_id, str("Houve um erro :( "))
            else:

                self.bot.sendMessage(chat_id, str('Comando nao reconhecido'))
        else:
            self.bot.sendMessage(chat_id, str("Celular nao cadastrado"))

