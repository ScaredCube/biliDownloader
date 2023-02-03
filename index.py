import asyncio
from bilibili_api import video, Credential, bangumi, sync, login, user, HEADERS
import httpx
from aiohttp import ClientSession
import os

# credential
try:
    with open('./bilidown_acc.log','r')as f:
        acc=f.read().split(';')
        SESSDATA = acc[0]
        BILI_JCT = acc[1]
except:
    SESSDATA = ''
    BILI_JCT = ''
BUVID3 = ""
credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
# FFMPEG 路径，查看：http://ffmpeg.org/
try:
    with open('./bilidown_ffpath.log','r')as f:
        FFMPEG_PATH=f.read()
except:
    FFMPEG_PATH = "ffmpeg"
bv='BV1qd4y1h7na'


async def main():
    v = video.Video(bvid=bv, credential=credential)
    print('正在获取url...')
    url = await v.get_download_url(0)
    ti=await v.get_info()
    ti=ti['title']
    if '/' in ti:
        ti=ti.replace('/',',')
    # 视频轨链接
    video_url = url["dash"]["video"][0]['baseUrl']
    # 音频轨链接
    audio_url = url["dash"]["audio"][0]['baseUrl']
    async with ClientSession() as sess:
        # 下载视频流
        async with sess.get(video_url, headers=HEADERS) as resp:
            length = resp.headers.get('content-length')
            with open('video_temp.m4s', 'wb') as f:
                process = 0
                while True:
                    chunk = await resp.content.read(4096*4)
                    if not chunk:
                        break
                    process += len(chunk)
                    per=int(process)/int(length)
                    perc=format(per,'.2%')
                    print(f'下载视频流 {process} / {length} ({perc})')
                    f.write(chunk)

        # 下载音频流
        async with sess.get(audio_url, headers=HEADERS) as resp:
            length = resp.headers.get('content-length')
            with open('audio_temp.m4s', 'wb') as f:
                process = 0
                while True:
                    chunk = await resp.content.read(4096*4)
                    if not chunk:
                        break
                    process += len(chunk)
                    per=int(process)/int(length)
                    perc=format(per,'.2%')
                    print(f'下载音频流 {process} / {length} ({perc})')
                    f.write(chunk)
        # 混流
        print('混流中')
        os.system(f'{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy {ti}.mp4')
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")
        print(f'已下载为: {ti}.mp4')

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608
def enc(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)

def down():
    global bv
    inv=input("请输入AV|BV|EP号 (必须以大写AV|BV|EP开头): ")
    if inv[:2]=='AV':
        print(enc(int(inv[2:])))
        bv=enc(int(inv[2:]))
    elif inv[:2]=='EP':
        ep=bangumi.Episode(int(inv[2:]))
        print(ep.get_bvid())
        bv=ep.get_bvid()
    elif inv[:2]=='BV':
        bv=inv
    else:
        print('请正确输入')
        return
    asyncio.get_event_loop().run_until_complete(main())

def lo():
    global credential
    print("请登录：")
    credential = login.login_with_qrcode()
    try:
        credential.raise_for_no_bili_jct()
        credential.raise_for_no_sessdata()
    except:
        print("登录失败")
        return
    print("登录成功,", sync(user.get_self_info(credential))['name'],'(已保存于bilidown_acc.log)')
    with open('./bilidown_acc.log','w')as f:
        f.write(credential.sessdata+';'+credential.bili_jct)

def ffp():
    path=input("请输入ffmpeg路径: ")
    with open('./bilidown_ffpath.log','w')as f:
        f.write(path)
    print('已保存于bilidown_ffpath.log')

def down_ss():
    global bv
    inss=input("请输入SS号 (必须以大写SS开头): ")
    if inss[:2]=='SS':
        ss=int(inss[2:])
    else:
        return
    bang=bangumi.Bangumi(ssid=ss)
    l=sync(bang.get_episode_list())['main_section']['episodes']
    print(f'共获取到 {len(l)} 个视频')
    info=sync(bangumi.Episode(l[0]['id']).get_episode_info())
    for i in range(1,len(l)+1):
        print(f"[{i}]{info['mediaInfo']['episodes'][i-1]['long_title']}")
    print('开始下载')
    for i in l:
        bvid=bangumi.Episode(i['id']).get_bvid()
        bv=bvid
        asyncio.get_event_loop().run_until_complete(main())
    


print("1.下载视频\n2.番剧批量下载\n3.设置ffmpeg路径 (默认为环境变量)\n4.登录\n")
cho=input('请输入序号: ')
if cho=='1':
    down()
elif cho=='2':
    down_ss()
elif cho=='3':
    ffp()
elif cho=='4':
    lo()

input('按回车退出')

## EP341216
## BV1qd4y1h7na
## AV170001
## SS34412