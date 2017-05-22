import vk
import time
import urllib.request
from bs4 import BeautifulSoup

lastVideos = []
nowUser = 0

def get_html(url):
    resp = urllib.request.urlopen(url)
    return resp.read()

def vkonta(info):
    TOKEN = '' #НЕОБХОДИМО АВТОРИЗОВАТЬСЯ ПРИ ПОМОЩИ ТОКЕНА
    session = vk.Session(access_token=TOKEN)
    vk_api = vk.API(session)

    print(info)
    vk_api.messages.send(message=info, user_id=' КОМУ ОТПРАВЛЯЕМ НОВОСТЬ (ИД) ')
    time.sleep(3)

def parse(html):
    soup = BeautifulSoup(html,'html.parser')
    video = soup.find_all('div',class_='yt-lockup-content')[:1] # берем только одно первое видео. ЗАЧЕМ БОЛЬШЕ?

    #print(video[0].a['title'] + ' link is : ' + video[0].a['href']) #какое видео является последним

    if lastVideos[nowUser]!= video[0].a['href']:
        if lastVideos[nowUser] != '':
            lastVideos.insert(nowUser, video[0].a['href'])
            info = 'Новое видео '+video[0].a['title']+' .Доступно по ссылке: '+'https://www.youtube.com'+video[0].a['href']
            vkonta(info)
        else:
            lastVideos.insert(nowUser, video[0].a['href'])
            info = 'Новое видео '+video[0].a['title']+' .Доступно по ссылке: '+'https://www.youtube.com'+video[0].a['href'] + ' .ЭТО ТЕСТ.'
            vkonta(info)

file = open('C:\chanals.txt') # расположение файла с каналами где файл имеет тип : user/PewDiePie;Название канала
for i in file:
    lastVideos.append('') # получаем количество каналов
file.close()

while True:
    nowUser = 0
    file = open('C:\chanals.txt')
    for line in file:
        chanal = line.split(';')#разделяем сплитом на 2 части : канал и его название.
        print('Сейчас канал: '+chanal[1].rstrip()+'('+str(nowUser+1)+')')
        parse(get_html('https://www.youtube.com/'+chanal[0]+'/videos'))
        nowUser+=1
    file.close()
