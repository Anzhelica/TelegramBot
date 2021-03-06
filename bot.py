from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram
import requests
get_response = requests.get(url='https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
data = get_response.json() 
text= ''

for val in data:
      text+='• <b>' + val['cc']+'</b> - '+ val['txt'] + '\n'
    
def get(bot, update):
  print(update.message.from_user.first_name);
  print(update.message.text);
  title = (update.message.text).split(" ") 
  update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
  for val in data:
    if val['cc'] == title[1]:
      update.message.reply_text('по курсу НБУ {0} - {1}грн'.format(title[1],val['rate']))

def getAll(bot, update):
    bot.sendMessage(parse_mode='HTML', chat_id=update.message.chat.id, text=' ВВЕДИТЕ КОД ВАЛЮТЫ  \n 💰<b>Доступные валюты:</b>💰 \n  '+text)


def text_callback(bot, update):
  custom_keyboard = [['список доступных валют', 'курс'],
                       ['конвертация в валюту'],]
  reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
  bot.send_message(chat_id=update.message.chat_id, text = "Выберите действие..\n 💶 список доступных валют\n 💶 курс \n 💶 конвертация в валюту ",reply_markup = reply_markup)
    
def get_rate(bot, update):
  bot.sendMessage(parse_mode='HTML', chat_id=update.message.chat.id, text=' <b>ВВЕДИТЕ КОД ВАЛЮТЫ</b> 💰 \n  <i>например:</i> RUB ',reply_markup=telegram.ReplyKeyboardRemove())
  
def get_rate_2(bot, update):
  for val in data:
    if val['cc'] == update.message.text:
      fl = 1
      update.message.reply_text('🙀 по курсу НБУ {0} = {1}грн'.format(update.message.text,val['rate']))

def convert(bot, update):
  bot.sendMessage(parse_mode='HTML', chat_id=update.message.chat.id, text=' <b>ВВЕДИТЕ КОЛИЧЕСТВО ГРИВЕН И ВАЛЮТУ</b> 💰 \n  <i>например: </i> 3.5 RUB ',reply_markup=telegram.ReplyKeyboardRemove())
  
def convert2(bot, update):
  my_list = update.message.text.split(" ")
  print(my_list[1])
  for val in data:
    if val['cc'] == my_list[1]:
      total = float(my_list[0])*float(val['rate'])
      print(total)
      update.message.reply_text('🙀 по курсу НБУ {0} грн = {1} {2}'.format(my_list[0], total,  my_list[1]))
  
  
updater = Updater('851425956:AAE4cvbT2hit0L0CBjXWpnD41qdUqEzNm0A')

updater.dispatcher.add_handler(CommandHandler('get', get))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('список доступных валют'), getAll))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('курс'), get_rate))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^[a-zA-Z]{3}$'), get_rate_2))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('конвертация в валюту'), convert))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^[0-9,.]{1,}[ ]{1,}[a-zA-Z]{3}$'), convert2))
updater.dispatcher.add_handler(MessageHandler([Filters.text], text_callback))

updater.start_polling()
updater.idle()