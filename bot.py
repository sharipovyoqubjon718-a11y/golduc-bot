import os
import threading
import urllib.parse
from flask import Flask
import telebot
from telebot import types

TOKEN = '8810181137:AAE7YDMH500atp10a957EyZE6kX_gtweazM'
bot = telebot.TeleBot(TOKEN)

WHATSAPP_NUMBER = '992102806343'
INSTAGRAM_REVIEW_LINK = (
    'https://www.instagram.com/golduc.tj?igsh=bHQxcmJpcHJiajZ4&utm_source=qr'
)

LANGUAGES = {
    'tj': {
        'welcome': 'Салом! Лутфан забонро интихоб кунед:',
        'select_service': 'Лутфан хизматрасониро интихоб кунед:',
        'btn_gold': '🪙 GOLD',
        'btn_uc': '💎 PUBG UC',
        'btn_lang': '🌐 Забон / Language',
        'btn_back': '⬅️ Ба менюи асосӣ',
        'btn_whatsapp': '🛒 Харид (WhatsApp)',
        'btn_reviews': '💬 Наш канал с отзывами',
        'uc_price_list': (
            '🔥 *PUBG MOBILE UC*\n\n'
            '💰 *Прайс-лист:*\n'
            '• 30 UC — 8 сомонӣ\n'
            '• 60 UC — 12 сомонӣ\n'
            '• 325 UC — 48 сомонӣ\n'
            '• 660 UC — 99 сомонӣ\n'
            '• 720 UC — 110 сомонӣ\n'
            '• 985 UC — 148 сомонӣ\n'
            '• 1380 UC — 210 сомонӣ\n\n'
            '✅ Шарҳҳои воқеии муштариён\n'
            '✉️ Ба паёмҳои шахсӣ нависед, зуд ҷавоб медиҳам!'
        ),
        'gold_price_list': (
            '🪙 *MORTAL LEGENDS GOLD*\n\n'
            '💰 *Прайс-лист:*\n'
            '• 300 Gold — 30 сомонӣ\n'
            '• 500 Gold — 50 сомонӣ\n'
            '• 1000 Gold — 100 сомонӣ\n'
            '• 1400 Gold — 140 сомонӣ\n'
            '• 2000 Gold — 200 сомонӣ\n'
            '• 3000 Gold — 300 сомонӣ\n'
            '• 4000 Gold — 400 сомонӣ\n'
            '• 5000 Gold — 500 сомонӣ\n'
            '• 6000 Gold — 600 сомонӣ\n'
            '• 7000 Gold — 700 сомонӣ\n'
            '• 8000 Gold — 800 сомонӣ\n'
            '• 9000 Gold — 900 сомонӣ\n'
            '• 10000 Gold — 1000 сомонӣ\n\n'
            '✉️ Ба паёмҳои шахсӣ нависед, зуд ҷавоб медиҳам!'
        ),
    },
    'ru': {
        'welcome': 'Привет! Пожалуйста, выберите язык:',
        'select_service': 'Пожалуйста, выберите услугу:',
        'btn_gold': '🪙 GOLD',
        'btn_uc': '💎 PUBG UC',
        'btn_lang': '🌐 Язык / Language',
        'btn_back': '⬅️ В главное меню',
        'btn_whatsapp': '🛒 Купить (WhatsApp)',
        'btn_reviews': '💬 Наш канал с отзывами',
        'uc_price_list': (
            '🔥 *PUBG MOBILE UC*\n\n'
            '💰 *Прайс-лист:*\n'
            '• 30 UC — 8 сомони\n'
            '• 60 UC — 12 сомони\n'
            '• 325 UC — 48 сомони\n'
            '• 660 UC — 99 сомони\n'
            '• 720 UC — 110 сомони\n'
            '• 985 UC — 148 сомони\n'
            '• 1380 UC — 210 сомони\n\n'
            '✅ Реальные отзывы клиентов\n'
            '✉️ Пиши в личные сообщения, отвечаю быстро!'
        ),
        'gold_price_list': (
            '🪙 *MORTAL LEGENDS GOLD*\n\n'
            '💰 *Прайс-лист:*\n'
            '• 300 Gold — 30 сомони\n'
            '• 500 Gold — 50 сомони\n'
            '• 1000 Gold — 100 сомони\n'
            '• 1400 Gold — 140 сомони\n'
            '• 2000 Gold — 200 сомони\n'
            '• 3000 Gold — 300 сомони\n'
            '• 4000 Gold — 400 сомони\n'
            '• 5000 Gold — 500 сомони\n'
            '• 6000 Gold — 600 сомони\n'
            '• 7000 Gold — 700 сомони\n'
            '• 8000 Gold — 800 сомони\n'
            '• 9000 Gold — 900 сомони\n'
            '• 10000 Gold — 1000 сомони\n\n'
            '✉️ Пиши в личные сообщения, отвечаю быстро!'
        ),
    },
}

user_lang = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_lang[message.chat.id] = 'tj'
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
      types.InlineKeyboardButton('🇹🇯 Тоҷикӣ', callback_data='lang_tj'),
      types.InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_ru'),
  )
  bot.send_message(
      message.chat.id,
      'Салом! Пожалуйста, выберите язык / Лутфан забонро интихоб кунед:',
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  chat_id = call.message.chat.id
  if chat_id not in user_lang:
    user_lang[chat_id] = 'tj'

  lang = user_lang[chat_id]

  if call.data == 'lang_tj':
    user_lang[chat_id] = 'tj'
    show_main_menu(chat_id, call.message.message_id, 'tj')
  elif call.data == 'lang_ru':
    user_lang[chat_id] = 'ru'
    show_main_menu(chat_id, call.message.message_id, 'ru')
  elif call.data == 'menu_uc':
    show_price_list(chat_id, call.message.message_id, 'uc')
  elif call.data == 'menu_gold':
    show_price_list(chat_id, call.message.message_id, 'gold')
  elif call.data == 'change_lang':
    send_language_menu(chat_id, call.message.message_id)
  elif call.data == 'back_to_main':
    show_main_menu(chat_id, call.message.message_id, lang)


def show_main_menu(chat_id, message_id, lang):
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_uc'], callback_data='menu_uc'
      ),
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_gold'], callback_data='menu_gold'
      ),
  )
  markup.add(
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_lang'], callback_data='change_lang'
      )
  )

  bot.edit_message_text(
      chat_id=chat_id,
      message_id=message_id,
      text=LANGUAGES[lang]['select_service'],
      reply_markup=markup,
  )


def send_language_menu(chat_id, message_id):
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
      types.InlineKeyboardButton('🇹🇯 Тоҷикӣ', callback_data='lang_tj'),
      types.InlineKeyboardButton('🇷🇺 Русский', callback_data='lang_ru'),
  )
  bot.edit_message_text(
      chat_id=chat_id,
      message_id=message_id,
      text='Лутфан забонро интихоб кунед / Пожалуйста, выберите язык:',
      reply_markup=markup,
  )


def show_price_list(chat_id, message_id, item_type):
  lang = user_lang.get(chat_id, 'tj')

  if item_type == 'uc':
    text = LANGUAGES[lang]['uc_price_list']
    wa_text = (
        'Салом! Ба ман PUBG UC даркор аст.'
        if lang == 'tj'
        else 'Здравствуйте! Мне нужен PUBG UC.'
    )
  else:
    text = LANGUAGES[lang]['gold_price_list']
    wa_text = (
        'Салом! Ба ман Gold даркор аст.'
        if lang == 'tj'
        else 'Здравствуйте! Мне нужен Gold.'
    )

  markup = types.InlineKeyboardMarkup(row_width=1)
  whatsapp_url = (
      f'https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(wa_text)}'
  )

  markup.add(
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_whatsapp'], url=whatsapp_url
      )
  )
  markup.add(
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_reviews'], url=INSTAGRAM_REVIEW_LINK
      )
  )
  markup.add(
      types.InlineKeyboardButton(
          LANGUAGES[lang]['btn_back'], callback_data='back_to_main'
      )
  )

  bot.edit_message_text(
      chat_id=chat_id,
      message_id=message_id,
      text=text,
      parse_mode='Markdown',
      reply_markup=markup,
  )


# --- СЕРВЕРИ ФЛАСК БАРОИ РЕНДЕР ---
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot is running!'


def run_flask():
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
  # Сервери Фласкро дар поток (thread) алоҳида ба кор меандозем, то ба бот халал нарасонад
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.start()

  print('Бот бомуваффақият оғоз шуд...')
  bot.infinity_polling()
