import asyncio
import websockets
from requests import get,post
from random import randrange
from youtubesearchpython import VideosSearch
from re import search

prefix = "PREFIX_BOT_MUSIC"
id = "YOUR_CHANNEL_ID_HERE"
token = "YOUR_TOKEN_DISCORD_HERE"
gate_way_discord_vc = "http://127.0.0.1:3001/"

def send_msg(id,msg):
    print(f"[send msg] {msg}")
    post(f"https://discordapp.com/api/v9/channels/{id}/messages",json={"content":msg,"nonce":randrange(1111111111111111, 99999999999999999),"tts":False},headers={"authorization": token,"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36"})

def check_null(data):
    if data == "" or data == None:
        return True
    return False

async def hello(ws, path):
    print("[ws] someone connected")
    await ws.send("Hi")
    while True :
        msg = await ws.recv()
        print(f"[ws] msg : {msg}")
        if check_null(msg):
            pass
        elif msg.startswith("เปิดเพลง"):
            msg = msg.replace("เปิดเพลง", "")
            if not check_null(msg):
                send_msg(id, f"{prefix}p {msg}")
        elif msg.startswith("หาเพลง") or msg.startswith("ห้าเพลง"):
            msg = msg.replace("หาเพลง", "")
            msg = msg.replace("ห้าเพลง", "")
            if not check_null(msg):
                vs = VideosSearch(msg, limit=5).result()["result"]
                if len(vs) == 0:
                    send_msg(id, f"หาเพลง {msg} ไม่เจอ")
                else :
                    msg = "0 | พูด\"เปิดเพลงที่\" ตามด้วยลำดับเพลง เพื่อเลือกเพลง หรือ พูด\"ยกเลิก\" เพื่อยกเลิก \n"
                    i = 1
                    for a in vs:
                        msg += f"{i} | `{a['title']}`\n"
                        i += 1
                    send_msg(id, msg)
                    while True:
                        msg_ = await ws.recv()
                        print(msg_)
                        if msg_ == "ยกเลิก":
                            send_msg(id, f"ok ยกเลิก")
                            break
                        if "เปิดเพลงที่" in msg_:
                            #msg_ = msg_.replace("เปิดเพลงที่", "")
                            msg_ = search('เปิดเพลงที่(.*)', msg_).group(1)
                            print(msg_)
                            c = True
                            if check_null(msg):
                                pass
                            elif msg_ == "หนึ่ง" or msg_ == "1":
                                send_msg(id, f"{prefix}p https://www.youtube.com/watch?v={vs[0]['id']}")
                            elif msg_ == "สอง" or msg_ == "2":
                                send_msg(id, f"{prefix}p https://www.youtube.com/watch?v={vs[1]['id']}")
                            elif msg_ == "สาม" or msg_ == "3":
                                send_msg(id, f"{prefix}p https://www.youtube.com/watch?v={vs[2]['id']}")
                            elif msg_ == "สี่" or msg_ == "4":
                                send_msg(id, f"{prefix}p https://www.youtube.com/watch?v={vs[3]['id']}")
                            elif msg_ == "ห้า" or msg_ == "5":
                                send_msg(id, f"{prefix}p https://www.youtube.com/watch?v={vs[4]['id']}")
                            else :
                                c = False
                            if c:
                                break
        elif msg.startswith("ข้ามเพลง"):
            if not check_null(msg):
                send_msg(id, f"{prefix}s")
        elif msg.startswith("ปิดเพลง"):
            send_msg(id, f"{prefix}leave")
        elif msg.startswith("คิว"):
            send_msg(id, f"{prefix}q")
        elif msg.startswith("ปิดไหม") or msg.startswith("ผิดไหม"):
            get(f"{gate_way_discord_vc}?do=mute&method=true")
        elif msg.startswith("เปิดไหม"):
            get(f"{gate_way_discord_vc}?do=mute&method=false")
        elif msg.startswith("ปิดหูฟัง"):
            get(f"{gate_way_discord_vc}?do=deafen&method=true")
        elif msg.startswith("เปิดหูฟัง"):
            get(f"{gate_way_discord_vc}?do=deafen&method=false")
        elif msg.startswith("เปิดกล้อง"):
            get(f"{gate_way_discord_vc}?do=video&method=false")
        elif msg.startswith("ปิดกล้อง"):
            get(f"{gate_way_discord_vc}?do=video&method=true")
        elif msg.startswith("เปิดจอ") or msg.startswith("ภจ"):
            get(f"{gate_way_discord_vc}?do=screen&method=true")
        elif msg.startswith("ปิดจอ"):
            get(f"{gate_way_discord_vc}?do=screen&method=false")
        elif msg.startswith("ออก"):
            get(f"{gate_way_discord_vc}?do=disconnect")
        elif msg.startswith("ทดสอบ"):
            send_msg(id, "test")

start_server = websockets.serve(hello, '127.0.0.1', 3000)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()