# -*- coding=utf-8 -*-
import Tkinter
import getpass
import json
import urllib
import requests
import time
import sys,os
from lxml.html import fromstring
import pyperclip
from threading import Thread
import tkMessageBox

headers = {'referer': "https://www.youtubeinmp3.com/tr/"}
url = 'https://www.youtubeinmp3.com/tr/download/?video='
mp3_name = []
preview_mp3_name = ''
count = 0
char = ['/', '\\', ':', '?', '<', '>', '"', '|']

def notify(n2):
    if 'posix' in os.name:
        os.system("""osascript -e 'display notification "{}" with title "{}" '""".format('YouTube Mp3 Downloader', '{} Indirme tamamlandı.'.format(mp3_name[n2])))
    else:
        from bildirim import balloon_tip
        balloon_tip('YouTube Mp3 Downloader', '{} Indirme tamamlandı.'.format(mp3_name[n2]).decode('utf-8'))

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r" + "[ %d%% ], %d MB, %d KB/s, %d saniyede tamamlandi" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def download(copy, n2):
    try:
        mp3_name.append(json.loads(requests.post('https://www.youtubeinmp3.com/r.php',
                                                 data={'q': copy}, headers=headers).text)[0]['title'])

        res = requests.get(url + copy).text
        down_url = fromstring(res).xpath('//*[@id="download"]/@href')[0]
        for ch in char:
            saving_name = mp3_name[n2].replace(ch, '')
        urllib.urlretrieve('https://www.youtubeinmp3.com' + down_url, "C:\\Users\\"+getpass.getuser()+"\\Desktop\\" +
                           saving_name + '.mp3', reporthook=reporthook)

        notify(n2)

    except Exception:
        print Exception.message

top = Tkinter.Tk().withdraw()

while True:
    if pyperclip.paste().startswith('https://www.youtube.com/watch?v=') and preview_mp3_name != pyperclip.paste():
        print 1
        ans = tkMessageBox.askyesno("YouTube Mp3 Downloader", "Indirmek istiyor musunuz?", icon='question')
        if ans == 'yes':
            Thread(target=download, args=(pyperclip.paste(), count)).start()
        preview_mp3_name = pyperclip.paste()
    else:
        time.sleep(1)
