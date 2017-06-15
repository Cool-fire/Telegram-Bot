import telepot
import urllib3
import urllib
import requests
import json
import os
from bs4 import BeautifulSoup as bs
downurl = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='
xmlurl ='http://www.youtubeinmp3.com/fetch/?format=XML&video='
token = '383625898:AAFum_jTIg-ynl9Ni-2h2BdptlDTTXXsmOc'
youquery = 'https://www.youtube.com/results?search_query='
yourl='http://www.youtube.com'

def handle(msg):
    chatid=msg['chat']['id']
    text=msg['text']
    print(chatid)
    if text == '/start':
        telebot.sendMessage(chatid,"hello")
        telebot.sendMessage(chatid,"Type your Song name")
    else:
        song(msg)

def song(msg):
    urls=[]
    chatid=msg['chat']['id']
    text=msg['text']
    telebot.sendMessage(chatid,"your song is "+text)
    query = urllib.request.quote(text)
    youturl = youquery+query
    print(youturl)
    try:
        sauce = urllib.request.urlopen(youturl).read()
        telebot.sendMessage(chatid,"your song is on your way....")
        soup = bs(sauce,'lxml')
        jsonurl=''
        divtags = soup.find_all('div', attrs={'class' : 'yt-lockup-content'})
        for div in divtags:
            url = div.find('a')['href']
            urls.append(yourl+url)
            extend = yourl+url
            jsonurl =downurl+extend
            break
       
        
        print(jsonurl)
        download(msg,jsonurl)
    except:
        telebot.sendMessage(chatid,"we cant find the requested song please try optimising the query")
def download(msg,jsonurl):
    r = requests.get(jsonurl)
    r.raise_for_status()
    data = json.loads(r.content.decode('utf-8'))
    downyourl = data['link']
    print(downyourl)
    title = msg['text']
    print(downyourl)
    upload_file = title.lower() + '.mp4'
    downloadsong(msg,downyourl,upload_file)
def downloadsong(msg,url,title):
    chatid=msg['chat']['id']
    r=requests.get(url)
    f=open(title,'wb')
    telebot.sendMessage(chatid,"Downloading your song .... :)")
    print("downloading.......")
    for chunk in r.iter_content(chunk_size=255):
        if chunk:
            f.write(chunk)
    print('done downloading')
    f.close()
    audio = open(title,'rb')
    try:
        telebot.sendAudio(chatid,audio)
        print("done sending......")
    except:
        telebot.sendMessage(chatid,"Sorry the song cannot be Sent")


    

telebot = telepot.Bot(token)
telebot.getMe()
telebot.getUpdates()
telebot.message_loop(handle)
