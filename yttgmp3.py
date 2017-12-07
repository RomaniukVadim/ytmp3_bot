#!/usr/env python3
import requests
import os
import glob
import telegram
from time import sleep
token = "token"
bot = telegram.Bot(token=token)
# Боту шлется ссылка на ютуб, он загоняет ее в bash комманду youtube-dl -x --audio-format mp3 <link>, шлет загруженный mp3 обратно клиенту


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_audio(self, chat_id, audio):
        params = {'chat_id': chat_id, 'audio': audio}
        method = 'sendAudio'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            try:
                last_update = get_result[len(get_result)]
            except IndexError:
                last_update  = 'null'

        return last_update

def mp3_download(url):
    cwd = os.getcwd() + "/"
    os.system('youtube-dl -x --audio-format mp3 ' + url)
    try:
        sleep(15)
        mp3_name = glob.glob(cwd + "*.mp3")[0]
        return mp3_name
    except:
        print("Aw, man")

def song_rm():
    cwd = os.getcwd() + "/"
    try:
        os.system('rm ' +  cwd + '*.mp3')
    except:
        print("Aw, man")
mp3_bot = BotHandler(token)  

def main():  
    new_offset = None
    while True:
        mp3_bot.get_updates(new_offset)

        last_update = mp3_bot.get_last_update()
        try:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
        except:
            last_update_id = 0
            last_chat_text = 'null'
            last_chat_id = 0
        print(last_chat_text)
        if 'https://www.youtube.com/' in last_chat_text.lower() or 'https://youtu.be/' in last_chat_text.lower():            
            bot.send_message(chat_id=last_chat_id, text="Downloading, please wait....")
            song_name = mp3_download(last_chat_text)
            bot.send_message(chat_id=last_chat_id, text="Uploading, please wait....")
            bot.send_audio(chat_id=last_chat_id, audio=open(song_name, 'rb'))
            song_rm()
        elif '/start' in last_chat_text.lower():
            bot.send_message(chat_id=last_chat_id, text="Please send me youtube link.")
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
