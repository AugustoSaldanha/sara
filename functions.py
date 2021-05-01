import os
import subprocess

def getVideo(chat_id, command, bot):
    bot.sendMessage(chat_id, str("Procurando video"))
    getLink = command.split(", ")[1]
    url = subprocess.getoutput("youtube-dl -g -f best " + getLink) #need of youtube-dl
    print(url)
    os.system("omxplayer -o hdmi " + "'" + url + "'")#need of omx player

def getTorrent(chat_id, command, bot):
    bot.sendMessage(chat_id, str("Verificando link"))
    os.system("peerflix " + "'" + command + "' " + "--r --fullscrean --omx")#need of peerflix
    bot.sendMessage(chat_id, str("O Filme terminou"))

def openKodi(chat_id, command, bot):
    bot.sendMessage(chat_id, str("Abrindo o Kodi"))#need of kodi
    os.system(command)
    bot.sendMessage(chat_id, str("Kodi fechado"))

def searchTorrent(chat_id, command, bot):
    magnet = ""
    media = command.split(", ")
    mediaType, mediaName = media[0], media[1]

    if (mediaType == "Serie" or mediaType == "Anime"):
        getInfo = subprocess.getoutput("node torrentIndexer.js " + "'" + mediaName + "' " + mediaType + " " + media[2] + " " + media[3])# get name and send to torrentIndexer
    else :
        getInfo = subprocess.getoutput("node torrentIndexer.js " + "'" + mediaName + "'")

    for n in getInfo.split("'"):
        if("magnet" in n):
            magnet = n
    bot.sendMessage(chat_id, str(getInfo))
    os.system("peerflix " + "'" + magnet + "' " + "--fullscrean -f /share/")
  #  os.system("peerflix " + "'" + magnet + "' " + "--omx")
