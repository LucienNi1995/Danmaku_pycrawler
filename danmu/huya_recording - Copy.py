# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿，尝试将返回地址 tx.hls.huya.com 中的 tx 改为 bd、migu-bd。

import requests
import re
import base64
import urllib.parse
import hashlib
import time
import datetime
import random
import os
import threading
import json


class HuYa:

    def __init__(self, rid):
        self.rid = rid

    def get_recording(self):
        try:
            room_url = 'https://m.huya.com/' + str(self.rid)
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36 '
            }
            response = requests.get(url=room_url, headers=header).text
            info = json.loads(re.findall(r"<script> window.HNF_GLOBAL_INIT = (.*)</script>", response)[0])
            if info == {'exceptionType': 0}:
                raise Exception('房间不存在')
            roomInfo = info["roomInfo"]
            real_url = {}

            # not live
            if roomInfo["eLiveStatus"] == 1:
                raise Exception('未开播')

            # live
            elif roomInfo["eLiveStatus"] == 2:
                streamInfos = roomInfo["tLiveInfo"]["tLiveStreamInfo"]["vStreamInfo"]["value"]
                for streamInfo in streamInfos:
                    real_url[streamInfo["sCdnType"].lower() + "_flv"] = streamInfo["sFlvUrl"] + "/" + streamInfo["sStreamName"] + "." + \
                                                                  streamInfo["sFlvUrlSuffix"] + "?" + streamInfo["sFlvAntiCode"]
                    real_url[streamInfo["sCdnType"].lower() + "_hls"] = streamInfo["sHlsUrl"] + "/" + streamInfo["sStreamName"] + "." + \
                                                                  streamInfo["sHlsUrlSuffix"] + "?" + streamInfo["sHlsAntiCode"]
            # replay
            elif roomInfo["eLiveStatus"] == 3:
                real_url["replay"] = roomInfo["tReplayInfo"]["tReplayVideoInfo"]["sUrl"]
            else:
                raise Exception('未知错误')
        except Exception as e:
            raise Exception(e)   
        timenow=datetime.datetime.today()
        timenewform=timenow.strftime('%Y-%m-%d%H%M%S')
        filename=timenewform+self.rid+'.flv'
        print(filename)
        file_path='liverecords_'+timenewform+'_'+self.rid
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        if roomInfo["eLiveStatus"]==2:
            print(real_url)
            #os.system('{}/ffmpeg.exe -i {} -c copy -movflags +faststart {}'.format(os.getcwd(),real_url['al_hls'].split('?')[0],os.path.join(file_path,filename)))
            #add_address='http://121.12.115.26/'
            #http,adrs=real_url['tx_hls'].split('?')[0].split('//')
            #url_update=add_address+adrs
            #print(url_update)
            # os.system('{}/ffmpeg.exe -i {} -c copy -movflags +faststart {}'.format(os.getcwd(),url_update,os.path.join(file_path,filename)))     
        elif roomInfo["eLiveStatus"] == 3:
            # print(real_url)
            os.system('{}/ffmpeg.exe -i {} -c copy -movflags +faststart {}'.format(os.getcwd(),real_url['replay'].split('?')[0],os.path.join(file_path,filename))) 
            
    def recording(self):
        global flag,anchor_status
        while True:
            print("-------recording-------")
            print(len(anchor_status)==0)
            print(flag)
            time.sleep(5)
            if len(anchor_status)==0 and flag:
                print("---get into self prepare")
                self .get_recording()
                flag=False
            elif len(anchor_status)!=0:
                flag=True

anchor_status = ["1"]
flag = True


if __name__ == '__main__':
    rid = 'chuhe'
    #rid2 = 'buqiuren'
    site=HuYa(rid)
    #site2=HuYa(rid2)
    ffm=threading.Thread(target=site.get_recording)
    #ffm2=threading.Thread(target=site2.get_recording)
    ffm.start()
    #ffm2.start()