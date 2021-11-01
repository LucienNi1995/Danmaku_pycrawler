# 部分弹幕功能代码来自项目：https://github.com/IsoaSFlus/danmaku，感谢大佬
# 快手弹幕代码来源及思路：https://github.com/py-wuhao/ks_barrage，感谢大佬
# 仅抓取用户弹幕，不包括入场提醒、礼物赠送等。

import asyncio
import danmaku
import nest_asyncio
import time
import datetime
import threading
import csv
import os
nest_asyncio.apply()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()



async def printer(q,roomid,path,namei):
    while True:
        m = await q.get()
        
        if m['msg_type'] == 'danmaku':
            timenow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(path+'/'+'_'+path+'_'+namei+'_'+roomid+'_danmu'+'.csv','a',newline='',encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([roomid,m["nickname"],m["sex"],m["level"],m["gamefullname"],m["actcount"],m["usercount"],m["totalcount"],m['intro'],m["livestatus"],m["name"],m["content"],timenow])
                f.close()
                print(roomid,f'{m["name"]}：{m["content"]}',timenow)
        elif m['msg_type'] == 'gift':
            timenow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(path+'/'+'_'+path+'_'+namei+'_'+roomid+'_gift'+'.csv','a',newline='',encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow([roomid,m["nickname"],m["sex"],m["level"],m["gamefullname"],m["actcount"],m["usercount"],m["totalcount"],m['intro'],m["livestatus"],m["name"],m["content"],m["price"],m["giftnum"],timenow])
                f.close()
                print(roomid,f'{m["name"]}：{m["content"]},{m["price"]},{m["giftnum"]}',timenow)

            

async def main(url,roomid,path,namei):
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q,roomid,path,namei))
    await dmc.start()

def task(a,number_a,path,nameall):
    new_loop=asyncio.new_event_loop()
    t=threading.Thread(target=start_loop,args=(new_loop,))
    t.start()
    
    for i in range(number_a):
        cr=main('https://www.huya.com/'+a[i],a[i],path,nameall[i])
        asyncio.run_coroutine_threadsafe(cr,new_loop)
    #cr2=main('https://www.huya.com/'+a[1],a[1])
    #cr3=main('https://www.huya.com/'+a[2],a[2])
    #cr4=main('https://www.huya.com/'+a[3],a[3])
    #cr5=main('https://www.huya.com/'+a[4],a[4])
    #cr6=main('https://www.huya.com/'+a[5],a[5])
    #cr7=main('https://www.huya.com/'+a[6],a[6])
    #cr8=main('https://www.huya.com/'+a[7],a[7])
    #cr9=main('https://www.huya.com/'+a[8],a[8])
    #cr10=main('https://www.huya.com/'+a[9],a[9])

    #asyncio.run_coroutine_threadsafe(cr1,new_loop)
    #asyncio.run_coroutine_threadsafe(cr2,new_loop)
    #asyncio.run_coroutine_threadsafe(cr3,new_loop)
    #asyncio.run_coroutine_threadsafe(cr4,new_loop)
    #asyncio.run_coroutine_threadsafe(cr5,new_loop)
    #asyncio.run_coroutine_threadsafe(cr6,new_loop)
    #asyncio.run_coroutine_threadsafe(cr7,new_loop)
    #asyncio.run_coroutine_threadsafe(cr8,new_loop)
    #asyncio.run_coroutine_threadsafe(cr9,new_loop)
    #asyncio.run_coroutine_threadsafe(cr10,new_loop)
if __name__ == "__main__": 
    number_a=15
    timenow=datetime.datetime.today()
    newpath=timenow.strftime('%Y-%m-%d%H%M%S')
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    a=['333003','521999','572329','688','243547','891487','761174','28917','buqiuren','pp1204','523980','1380','458911','luban','116']
    nameall=['Zz1tai姿态','盛世-叫我久哥哥【GLZ】','雨初歇-北枫','张大仙','久爱-预见【吕德华】','LING-张老三','DK-阿顺','久帝-金榜','DK-不求人','华星-皮皮宝宝【925】','子龙-【黑龙军团】','集梦阿布【感恩】','向阳哥哥【海鲜战队】','小鲁班007','集梦会长【116超跑】']
    for i in range(number_a):
        with open(newpath+'/'+'_'+newpath+'_'+nameall[i]+'_'+a[i]+'_danmu'+'.csv','a',newline='',encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['roomnumber','nickname','sex','level','gamefullname','actcount','usercount','totalcount','introduction','livestatus','username','msg','time'])
            f.close()
            
        with open(newpath+'/'+'_'+newpath+'_'+nameall[i]+'_'+a[i]+'_gift'+'.csv','a',newline='',encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['roomnumber','nickname','sex','level','gamefullname','actcount','usercount','totalcount','introduction','livestatus','username','gift','price','num','time'])
            f.close()
    task(a,number_a,newpath,nameall)






# 虎牙直播：https://www.huya.com/11352915
# 斗鱼直播：https://www.douyu.com/85894
# B站直播：https://live.bilibili.com/70155
# 快手直播：https://live.kuaishou.com/u/jjworld126
# 火猫直播：
# 企鹅电竞：https://egame.qq.com/383204988
# 花椒直播：https://www.huajiao.com/l/303344861?qd=hu
# 映客直播：https://www.inke.cn/liveroom/index.html?uid=87493223&id=1593906372018299
# CC直播：https://cc.163.com/363936598/
# 酷狗直播：https://fanxing.kugou.com/1676290
# 战旗直播：
# 龙珠直播：http://star.longzhu.com/wsde135864219
# PPS奇秀直播：https://x.pps.tv/room/208337
# 搜狐千帆直播：https://qf.56.com/520208a
# 来疯直播：https://v.laifeng.com/656428
# LOOK直播：https://look.163.com/live?id=196257915
# AcFun直播：https://live.acfun.cn/live/23682490
# 艺气山直播：http://www.173.com/96
