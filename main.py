'''
Heroku：https://qiita.com/1-row/items/80f89c8ada2e61f04446
git add .
git commit -am "update"
git push heroku master
heroku run python test.py
heroku open
heroku logs --tail
'''

import os
import sys
import mk_message as mm
import word2vec as wv
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Sitlature header value
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

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    word = str(event.message.text)
    rep_message2,rep_message3 = '',''

    try:
        food,place = word.split()
        food_list,similar_list,error = wv.relevance(food)

        #コーパスに存在する場合
        if error == 0:
            rep_message1 = mm.Tabelog_recommend(food_list,similar_list) #おすすめの食べ物３つ
            rep_message2,rep_message3 = mm.Tabelog_shopInfo(food_list[1],place) #おすすめの食べ物の店の情報
        #コーパスに存在しない場合
        elif error == 1:
            rep_message1 = 'コーパスに存在しません'
            rep_message2 = mm.Tabelog_shopInfo(food,place)
        #モデルが見つからない場合
        elif error == 2:
            rep_message1 = 'モデルが見つかりません'
    
    except ValueError:
        rep_message1 = '『食べたいもの　場所』で入力してください！' 

    if (not rep_message2) and (not rep_message3):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=rep_message1)
        )
    elif not (rep_message3):
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=rep_message1),TextSendMessage(text=rep_message2)]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=rep_message1),TextSendMessage(text=rep_message2),TextSendMessage(text=rep_message3)]
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)