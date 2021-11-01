import re
import aiohttp
from .tars import tarscore
import json

class SenderInfo(tarscore.struct):
    def __init__(self):
        self.lUid = 0
        self.lImid = 0
        self.sNickName = ""
        self.iGender = 0

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        var = SenderInfo()
        var.lUid = t.read(tarscore.int64, 0, False, var.lUid)
        var.lImid = t.read(tarscore.int64, 1, False, var.lImid)
        var.sNickName = t.read(tarscore.string, 2, False, var.sNickName)
        var.iGender = t.read(tarscore.int32, 3, False, var.iGender)
        return var

class MessageNotice:
    def __init__(self):
        self.tUserInfo = None,
        self.lTid = 0,
        self.lSid = 0,
        self.sContent = "",
        self.iShowMode = 0,
        self.tFormat = None
        self.tBulletFormat = None
        self.iTermType = 0,
        self.vDecorationPrefix = None
        self.vDecorationSuffix = None
        self.vAtSomeone = None
        self.lPid = 0

    def readFrom(self, t: tarscore.TarsInputStream):
        self.tUserInfo = t.read(SenderInfo, 0, False, self.tUserInfo)
        self.lTid = t.read(tarscore.int64, 1, False, self.lTid)
        self.lSid = t.read(tarscore.int64, 2, False, self.lSid)
        self.sContent = t.read(tarscore.string, 3, False, self.sContent)
        self.iShowMode = t.read(tarscore.int32, 4, False, self.iShowMode)
        # self.tFormat = t.read(tarscore.struct, 5, False, self.tFormat)
        # self.tBulletFormat = t.read(tarscore.struct, 6, False, self.tBulletFormat)
        self.iTermType = t.read(tarscore.int32, 7, False, self.iTermType)
        # self.vDecorationPrefix = t.read(tarscore.vctclass, 8, False, self.vDecorationPrefix)
        # self.vDecorationSuffix = t.read(tarscore.vctclass, 9, False, self.vDecorationSuffix)
        # self.vAtSomeone = t.read(tarscore.vctclass, 10, False, self.vAtSomeone)
        self.lPid = t.read(tarscore.int64, 11, False, self.lPid)

class GiftNotice:
    def __init__(self):
        #self.tUserInfo = None,
        self.sGiftsender = "",
        self.roomid = "",
        self.gifttype="",
        self.price=None,
        self.giftnum=None,
        
    def readFrom(self, t: tarscore.TarsInputStream):
        #self.tUserInfo = t.read(SenderInfo, 0, False, self.tUserInfo)
        #self.lSid = t.read(tarscore.int64, 2, False, self.lSid)
        self.giftnum=t.read(tarscore.int64, 2, False, self.giftnum)
        self.roomid=t.read(tarscore.string, 5, False, self.roomid)
        self.sGiftsender= t.read(tarscore.string, 6, False, self.sGiftsender)
        self.gifttype= t.read(tarscore.string, 20, False, self.gifttype)
        self.price=t.read(tarscore.int64, 41, False, self.price)
        # self.tFormat = t.read(tarscore.struct, 5, False, self.tFormat)
        # self.tBulletFormat = t.read(tarscore.struct, 6, False, self.tBulletFormat)
        #self.iTermType = t.read(tarscore.int32, 7, False, self.iTermType)
        # self.vDecorationPrefix = t.read(tarscore.vctclass, 8, False, self.vDecorationPrefix)
        # self.vDecorationSuffix = t.read(tarscore.vctclass, 9, False, self.vDecorationSuffix)
        # self.vAtSomeone = t.read(tarscore.vctclass, 10, False, self.vAtSomeone)
        #self.lPid = t.read(tarscore.int64, 11, False, self.lPid)



class Huya:
    wss_url = 'wss://cdnws.api.huya.com/'
    heartbeat = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75' \
                b'\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00' \
                b'\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f' \
                b'\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60' \
                b'\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c '
    heartbeatInterval = 60

    @staticmethod
    async def get_ws_info_details(url):
        reg_datas = []
        url = 'https://m.huya.com/' + url.split('/')[-1]
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}

        async with aiohttp.ClientSession() as session:        
            async with session.get(url, headers=headers) as resp:
                room_page = await resp.text()
                info=json.loads(re.findall(r"<script> window.HNF_GLOBAL_INIT = (.*)</script>", room_page)[0])
                nickname=info["roomInfo"]["tProfileInfo"]["sNick"]
                sex=info["roomInfo"]["tProfileInfo"]["iSex"]
                level=info["roomInfo"]["tProfileInfo"]["iLevel"]
                livestatus=info["roomInfo"]["eLiveStatus"]
                ActCount=""
                GameFullName=""
                UserCount=""
                TotalCount=""
                Intro=""
                data_collected=[]

                if info["roomInfo"]["eLiveStatus"] == 1:
                    ActCount=info["roomInfo"]["tRecentLive"]["lActivityCount"]
                    GameFullName=info["roomInfo"]["tRecentLive"]["sGameFullName"]
                    UserCount=info["roomInfo"]["tRecentLive"]["lUserCount"]
                    TotalCount=info["roomInfo"]["tRecentLive"]["lTotalCount"]
                    Intro=info["roomInfo"]["tRecentLive"]["sIntroduction"]

            # live
                elif info["roomInfo"]["eLiveStatus"] == 2:
                    ActCount=info["roomInfo"]["tLiveInfo"]["lActivityCount"]
                    GameFullName=info["roomInfo"]["tLiveInfo"]["sGameFullName"]
                    UserCount=info["roomInfo"]["tLiveInfo"]["lUserCount"]
                    TotalCount=info["roomInfo"]["tLiveInfo"]["lTotalCount"]
                    Intro=info["roomInfo"]["tLiveInfo"]["sIntroduction"]
                    
                elif info["roomInfo"]["eLiveStatus"] == 3:
                    ActCount=info["roomInfo"]["tReplayInfo"]["lActivityCount"]
                    GameFullName=info["roomInfo"]["tReplayInfo"]["sGameFullName"]
                    UserCount=info["roomInfo"]["tReplayInfo"]["lUserCount"]
                    TotalCount=info["roomInfo"]["tReplayInfo"]["lTotalCount"]
                    Intro=info["roomInfo"]["tReplayInfo"]["sIntroduction"]

                data_collected= {'nickname': nickname, 'sex': sex,'level':level,'actcount': ActCount, 'gamefullname':GameFullName,'usercount':UserCount,'totalcount':TotalCount,'intro':Intro,'livestatus':livestatus}

        return data_collected

    @staticmethod
    async def get_ws_info(url):
        reg_datas = []
        url = 'https://m.huya.com/' + url.split('/')[-1]
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                room_page = await resp.text()
                #info=json.loads(re.findall(r"<script> window.HNF_GLOBAL_INIT = (.*)</script>", room_page)[0])
                #if info["roomInfo"]["eLiveStatus"] == 1:
                    #ayyuid=info["roomInfo"]["tRecentLive"]["lYyid"]
                    #tid=info["roomInfo"]["tRecentLive"]["lChannel"]
                    #sid=info["roomInfo"]["tRecentLive"]["lLiveChannel"]

            # live
                #elif info["roomInfo"]["eLiveStatus"] == 2:
                    #ayyuid=info["roomInfo"]["tLiveInfo"]["lYyid"]
                    #tid=info["roomInfo"]["tLiveInfo"]["lChannel"]
                    #sid=info["roomInfo"]["tLiveInfo"]["lLiveChannel"]

                #elif info["roomInfo"]["eLiveStatus"] == 3:
                    #ayyuid=info["roomInfo"]["tReplayInfo"]["lYyid"]
                    #tid=info["roomInfo"]["tReplayInfo"]["lChannel"]
                    #sid=info["roomInfo"]["tReplayInfo"]["lLiveChannel"]
                m = re.search(r"lYyid\":([0-9]+)", room_page, re.MULTILINE)
                ayyuid = m.group(1)
                m = re.search(r"lChannelId\":([0-9]+)", room_page, re.MULTILINE)
                tid = m.group(1)
                m = re.search(r"lSubChannelId\":([0-9]+)", room_page, re.MULTILINE)
                sid = m.group(1)

        oos = tarscore.TarsOutputStream()
        oos.write(tarscore.int64, 0, int(ayyuid))
        oos.write(tarscore.boolean, 1, True)  # Anonymous
        oos.write(tarscore.string, 2, "")  # sGuid
        oos.write(tarscore.string, 3, "")
        oos.write(tarscore.int64, 4, int(tid))
        oos.write(tarscore.int64, 5, int(sid))
        oos.write(tarscore.int64, 6, 0)
        oos.write(tarscore.int64, 7, 0)

        wscmd = tarscore.TarsOutputStream()
        wscmd.write(tarscore.int32, 0, 1)
        wscmd.write(tarscore.bytes, 1, oos.getBuffer())

        reg_datas.append(wscmd.getBuffer())
        return Huya.wss_url, reg_datas

    @staticmethod
    def decode_msg(data):
        class user(tarscore.struct):
            def readFrom(ios):
                return ios.read(tarscore.string, 2, False).decode('utf8')

        name = ''
        content = ''
        gifttype=''
        price=''
        msgtype=''
        giftnumber=''
        msgs = []
        
        ios = tarscore.TarsInputStream(data)
        if ios.read(tarscore.int32, 0, False) == 7:
            ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 1, False))
            iuri=ios.read(tarscore.int64, 1, False)
            if iuri == 1400:
                ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 2, False))
                msgdecode = MessageNotice()
                msgdecode.readFrom(ios)
                #print(f' [{msgdecode.tUserInfo.sNickName.decode("utf-8")}]')
                name=msgdecode.tUserInfo.sNickName.decode("utf-8")
                content=msgdecode.sContent.decode("utf-8")
                msgtype='danmaku'
            elif iuri==6501:
                ios = tarscore.TarsInputStream(ios.read(tarscore.bytes, 2, False))
                msgdecode = GiftNotice()
                msgdecode.readFrom(ios)
                name=msgdecode.sGiftsender.decode("utf-8")
                gifttype=msgdecode.gifttype.decode("utf-8")
                price=msgdecode.price
                giftnum=msgdecode.giftnum
                msgtype='gift'
                #print(f' [{msgdecode.sGiftsender.decode("utf-8")}]:{msgdecode.gifttype.decode("utf-8")},{msgdecode.price} ,{msgdecode.giftnum} gift ')
        if msgtype=='danmaku':
            msg = {'name': name, 'content': content,'price':'','msg_type': msgtype}
        elif msgtype=='gift':
            msg = {'name': name, 'content': gifttype, 'price':price,'giftnum':giftnum, 'msg_type': msgtype}
        else:
            msg={'name': '', 'content': '','price':'', 'msg_type': 'other'}
        msgs.append(msg)
        return msgs