from flask import request, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import requests
from models.response import ResponseModel
from numpy.random import choice

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('4poqR3ysAMBpgMOLOx49z4n0j1WC2KnC5HveklFjEEEXgeVi1QC+QcWQZx57hAC0WD4KJrpTRgQM5SxWyaAhJdVNzICVmC2zFlg3IlRxUsoVGLQBL/skhXCz2kCtMmizFO4O2vUC+hRKdkvrlOgi5QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('55367dbf03220fd02e41d0ac87e76c7c')

class LineChat(Resource):

    def post(self):

        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        print(f'signature: {signature}')
        # get request body as text
        body = request.get_data(as_text=True)
        print(f'body: {body}')
        # app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
        
        return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 1. get intent
    resp = requests.get(url="http://35.223.169.18:5000/intent_classifier",json={'value':event.message.text})
    intent_id = resp.json()['intent_id']

    # 2. get intent response
    reply_text = choice(ResponseModel.query.filter_by(intent_id=intent_id).all()).json()['value']
    print(f'USE resource called: reply_text: {reply_text}')
    print(f'reply token: {event.reply_token}')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))