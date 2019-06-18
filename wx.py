#coding=utf-8
from wxpy import *
from executeAgent.script._360connect import Start

#扫二维码登陆
#登录缓存
bot = Bot(cache_path=True)

def send_news():
    try:
        my_friend = bot.friends().search(u"华蓝L")[0]#指定接收消息的对象
        my_friend.send("请发送360动态密码")
    except:
        my_friend = bot.friends.search(u"童话")[0]
        my_friend.send("消息发送失败")
#消息监听，监听指定对象发来的消息
found = bot.friends().search('华蓝L')
#@bot.register()，这个就是把下面的函数绑定，然后如果微信好友发消息的话，就会调用该函数
@bot.register(found)
def print_news(msg):
    r = str(msg)
    msgs = r.split(":")[1].split(" (")[0].strip()
    print(msgs)
    Start(msgs)

if __name__ == "__main__":
    send_news()
    #保证程序运行
    embed()