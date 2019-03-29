import json
import requests,re,urllib
from ftplib import FTP
from bs4 import BeautifulSoup
from flask import Flask,request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,ImageSendMessage,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

def binus_login():
    print("part of binus login")

app = Flask(__name__)
 
bot = LineBotApi('')
handler = WebhookHandler('')
 
@app.route("/") 
def index():
    return " bisa"
 
@app.route("/callback",methods=['POST']) 
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'
 
@handler.add(MessageEvent,message=TextMessage)
def handle_text_message(event):
    msg = event.message.text

    if msg.startswith("Add_") or msg.startswith("add_"):
        msg1 = msg.split("_")
        msg2 = msg1[1].split("|")
        url = ''
        msg3 = msg2[2].split("/")
        msg4 = ""
        msg4 += "%s/%s/%s"%(msg3[1],msg3[0],msg3[2])
        date = ""
        date += msg4
        date += msg2[3]
        payload={"name":msg2[0],"course":msg2[1],"time":date}
        resp = requests.post(url=url,data=payload)
        bot.reply_message(event.reply_token,TextSendMessage(text="Add "+msg2[0]+" success"))

    elif msg.lower() == "see more":
        msg1 = ""
        msg1 += "How to Add Assignment:\nAdd Judul Course Date(DD/MM/YY) TIME(HH:MM)\n\n"
        msg1 += "How to Remove Assignment\nRemove Judul\n"
        msg1 += "\nMore Information\n "
        bot.reply_message(event.reply_token,TextSendMessage(text=msg1))

    elif msg.lower() == "resetdata":
        ftp = FTP('','','')
        f = open("datajson.txt","w")
        f.write("")
        f.close()
        file = open("datajson.txt","rb")
        ftp.storbinary("STOR datajson.txt",file)
        file.close()
        ftp.quit()
        bot.reply_message(event.reply_token,TextSendMessage(text="Reset Data Success!"))

    elif msg.lower() == "getdata":
        msg1 = ""
        msg1 += str(binus_login())
        len1 = len(msg1)
        ftp = FTP('','','')
        f = open("datajson.txt","w")
        f.write("{}".format(msg1))
        f.close()
        file = open("datajson.txt","rb")
        ftp.storbinary("STOR datajson.txt",file)
        file.close()
        ftp.quit()
        bot.reply_message(event.reply_token,TextSendMessage(text="Success Retreive Data!"))
        
    elif msg.lower() == "view": 
        url = ''
        resp = requests.get(url=url) 
        x = resp.text.split("|")
        if x[0] != "":
            msg1 = "ADA TUGAS NIH, KERJAIN YAA!\n\nTitle : "
            msg1 += str(x[0])
            msg1 += "\nCourse : "
            msg1 += str(x[1])
            msg1 += "\nDate  : "
            y = x[2].split(" ")
            msg1 += str(y[0])
            msg1 += "\nTime : "
            msg1 += str(y[1])
            msg1 += "\n\nMore Information\n "
            bot.reply_message(event.reply_token,TextSendMessage(text=msg1))
        else:
            bot.reply_message(event.reply_token,TextSendMessage(text="Ga ada tugas boi"))
    elif msg.lower() == "modify":
        bot.reply_message(event.reply_token,TextSendMessage(text=""))
    elif msg.lower() == "print":
        bot.reply_message(event.reply_token,ImageSendMessage(original_content_url='',preview_image_url=''))
    elif msg.lower() == "list": 
        url = ''
        s = requests.get(url=url)
        text = s.text.split("<br>")
        if len(text) > 1:
            msg1 = "BANYAK TUGAS NIH, KERJAIN YAA!\n\n"
            for x in range(0,len(text)-1):
                if text[x][0] != '=':
                    x = text[x].split("|")
                    msg1 += "Title : "
                    msg1 += str(x[0])
                    msg1 += "\nCourse : "
                    msg1 += str(x[1])
                    msg1 += "\nDate  : "
                    y = x[2].split(" ")
                    msg1 += str(y[0])
                    msg1 += "\nTime : "
                    msg1 += str(y[1])
                    msg1 += "\n\n"
            msg1 += "More Information\n "
            bot.reply_message(event.reply_token,TextSendMessage(text=msg1))
        else: 
            bot.reply_message(event.reply_token,TextSendMessage(text="Ga ada tugas boi"))

    elif msg.startswith("remove_") or msg.startswith("Remove_"):
        msg1 = msg.split("_")
        if len(msg1)==2:
            urlcheck = ""
            payload={"name":msg1[1]}
            resp = requests.post(url=urlcheck,data=payload)
            if "-1" in resp.text:
                bot.reply_message(event.reply_token,TextSendMessage(text=msg1[1]+" not in the database"))
            else:
                url = ""
                payload={"as":"delete","item":resp.text}
                resp2 = requests.get(url = url , params = payload)
                bot.reply_message(event.reply_token,TextSendMessage(text="Remove "+msg1[1]+" success"))

    elif msg.lower() == "hi bot" or msg.lower().startswith("help"):
        carousel = TemplateSendMessage(alt_text="Hello, Can I Help You?",template=CarouselTemplate(columns=[
            CarouselColumn(thumbnail_image_url="https://fast.customer.io/s/cio-mascot-hello-wave.gif",title="Hello, Can I Help You?",text=" ",actions=[MessageTemplateAction(label="Closest Assigment ",text="View"),
        MessageTemplateAction(label="All Assignment",text="List"),MessageTemplateAction(label="See More",text="see more")]),CarouselColumn(thumbnail_image_url="https://media.giphy.com/media/tn8zWeNYA73G0/giphy.gif",title="This is Your Schedule",text="Don't be late guys ...",actions=[MessageTemplateAction(label="Today's Class",text="todays"),
        MessageTemplateAction(label="Tomorrow's Class",text="tomorrows"),MessageTemplateAction(label="Credits",text="credits")])]))
        bot.reply_message(event.reply_token,carousel)
    elif msg.lower() == "todays":
        msgspl = msg.split()
        if len(msgspl) == 1:
            url = ''
            resp = requests.get(url=url)
            if resp.text != "[]":
                data = json.loads(resp.text)
                msg1 = "TODAY'S CLASS! LA07 \n%s [%d Session]\n\n"%(data[0]['date'],len(data))
                for x in range(0,len(data)):
                    msg1 += str(data[x]['course'])
                    msg1 += "\n"
                    msg1 += "Start : "
                    msg1 += str(data[x]['start'])
                    msg1 += "\n"
                    msg1 += "End   : "
                    msg1 += str(data[x]['end'])
                    msg1 += "\n"
                    msg1 += "Class : "
                    msg1 += str(data[x]['class'])
                    msg1 += "\n\n"
            else:
                msg1 = "Libur Boi"
        bot.reply_message(event.reply_token,TextSendMessage(text=msg1))
    elif msg.lower() == "tomorrows":
        msgspl = msg.split()
        if len(msgspl) == 1:
            url = ''
            resp = requests.get(url=url)
            if resp.text != "[]":
                data = json.loads(resp.text)
                msg1 = "TOMORROW'S CLASS! LA07 \n%s [%d Session]\n\n"%(data[0]['date'],len(data))
                for x in range(0,len(data)):
                    msg1 += str(data[x]['course'])
                    msg1 += "\n"
                    msg1 += "Start : "
                    msg1 += str(data[x]['start'])
                    msg1 += "\n"
                    msg1 += "End   : "
                    msg1 += str(data[x]['end'])
                    msg1 += "\n"
                    msg1 += "Class : "
                    msg1 += str(data[x]['class'])
                    if x != len(data)-1: msg1 += "\n\n"
            else:
                msg1 = "Libur Boi"
        bot.reply_message(event.reply_token,TextSendMessage(text=msg1))

    elif msg.lower() == "credits":
        bot.reply_message(event.reply_token,TextSendMessage(text="This bot is made by\nJason Theopilus & Christoval Leaved"))


@handler.add(PostbackEvent)
def postback(event):
    if event.postback.data == "databutton":
        bot.reply_message(event.reply_token,TextMessage("Postback masuk"))
 
if __name__ == "__main__": #int main()
    app.run()