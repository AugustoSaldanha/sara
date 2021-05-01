import os
import telepot
import subprocess
import threading
import json

from functions import *

#create sara class
class sara():
    def __init__(self, bot):
        self.bot = bot
    #get message and chat id
    def handle(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        #debug
        print ('Received:')
        print(chat_id)
        print(command)
        #compare chat id, only registered chats can control the bot!
        if  chat_id == 'integer with the chat id!!':
            #now compare message to do something *Commands in portuguese, but you can change this!
            if command == '/oi':
                self.bot.sendMessage(chat_id, str("Ola! Parabens, tudo funcionando"))
            elif command == '/horas':
                self.bot.sendMessage(chat_id, str("Horas: ") + str(now.hour) + str(":") + str(now.minute))
            elif command == 'Desligue a luz do quarto':
                self.bot.sendMessage(chat_id, str("Desligando..."))#sends the massage to bot.
                os.system("mosquitto_pub -t esp32/light -m 0")# send the message to ESP32 through MQTT
            elif command == 'Ligue a luz do quarto':
                self.bot.sendMessage(chat_id, str("Ligando..."))
                os.system("mosquitto_pub -t esp32/light -m 1")
            elif command == 'Desligue a tv':
                self.bot.sendMessage(chat_id, str("Desligando..."))
                os.system("echo 'standby 0' | cec-client -s -d 1")# send command to HDMI through the CEC protocol
            elif command == 'Ligue a tv':
                self.bot.sendMessage(chat_id, str("Ligando..."))
                os.system("echo 'on 0' | cec-client -s -d 1")
            elif command == 'Aumente o volume':
                self.bot.sendMessage(chat_id, str("Volume +1"))
                os.system("echo 'volup 0' | cec-client -s -d 1")
            elif command == 'Diminua o volume':
                self.bot.sendMessage(chat_id, str("Volume -1"))
                os.system("echo 'voldown 0' | cec-client -s -d 1")
            elif command == 'Ligue o ps4':
                self.bot.sendMessage(chat_id, str("Ligando"))
                os.system("echo 'on 4' | cec-client -s -d 1")
            elif command == 'Modo de espera ps4':
                self.bot.sendMessage(chat_id, str("Ligando"))
                os.system("echo 'standby 4' | cec-client -s -d 1")
            elif command == 'Temperatura':
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
            elif command == '/help':
                data = open('help.json', 'r')
                hp = json.load(data)#load help data and sends to bot
                for n in hp:
                    self.bot.sendMessage(chat_id, n)
                dados.close()
                del hp
            elif 'Youtube,' in command:
                t = threading.Thread(target=getVideo, args=(chat_id, command, self.bot))#call function with another thread
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
            elif 'Serie,' or 'Filme,' or 'Anime,' or 'Musica,' in command:
                try:
                    t = threading.Thread(target=searchTorrent, args=(chat_id, command, self.bot))
                    t.start()
                except:
                    self.bot.sendMessage(chat_id, str("Houve um erro :( "))
        else:
            self.bot.sendMessage(chat_id, str("Celular nao cadastrado"))

