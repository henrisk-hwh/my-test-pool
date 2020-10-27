# -*- coding:utf-8 -*-
import os, math
import sys
import time

# if len(sys.argv) < 2:
#     print("usage: dui_tts_generator.py *.txt")
#     exit()

DIR = "./"
idx = 1
wav_file = DIR + "tts.txt"
wav_header = "curl -H 'Content-Type:application/json;' -d \'"
wav_json_1 = '{"context":{"productId":"278572295"},"request":{"requestId":"tryRequestId","audio":{"audioType":"mp3","sampleRate":16000,"channel":1,"sampleBytes":2},"tts":{"text":"'
wav_json_2 = '","textType":"text","voiceId":"gqlanf","volume":100,"speed":0.83}}}'
https_url = "https://tts.dui.ai/runtime/v1/synthesize?productId=278572295&apikey=80e65d9c2ecb4b90a577701e05670109"

with open(wav_file, 'r') as fr:
    for line in fr.readlines():
        words = line.strip().split(' ')
        file_name = wav_header + wav_json_1 + words[1] + wav_json_2 + "\' \"" + https_url + "\" --output " + words[0]
        print file_name
        os.system(file_name)
        item = bytes(idx)
        file_size = os.path.getsize(words[0])
        if (file_size == 0):
            os.system(file_name)
        idx = idx + 1
        time.sleep(0.1)
        os.system("adb push {} /mnt/app/tts".format(words[0]))