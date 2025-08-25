import telebot 
import sqlite3 as sql

con = sql.connect('data.db')
cursor = con.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS calculator(monitor TEXT, chat_id INT)')

bot = telebot.TeleBot('7812295957:AAGsAM2wfyKoylYKBRsGby3SwSlIIQBllnk')
import re

def sanitize_expression(expr):
    
    expr = re.sub(r'\b0+(\d+)', r'\1', expr)
    return expr

buttonsh = telebot.types.InlineKeyboardButton
markup = telebot.types.InlineKeyboardMarkup(row_width= 4)
buttons = [
    buttonsh('1', callback_data='1'),
    buttonsh('2', callback_data='2'),
    buttonsh('3', callback_data='3'),
    buttonsh('➕', callback_data='plus'),
    buttonsh('4', callback_data='4'),
    buttonsh('5', callback_data='5'),
    buttonsh('6', callback_data='6'),
    buttonsh('➖', callback_data='negative'),
    buttonsh('7', callback_data='7'),
    buttonsh('8', callback_data='8'),
    buttonsh('9', callback_data='9'),
    buttonsh('✖️', callback_data='cross'),
    buttonsh('0', callback_data='0'),
    buttonsh('.', callback_data='point'),
    buttonsh('^', callback_data='power'),
    buttonsh('➗', callback_data='devide'),
    buttonsh('🟰', callback_data='equal')

    ]
for i in range(0, len(buttons), 4):
    markup.add(*buttons[i:i+4])


start_markup = telebot.types.InlineKeyboardMarkup()
channel_button = telebot.types.InlineKeyboardButton('Our channel !', 'https://t.me/techsa_ir')
start_markup.add(channel_button)
@bot.message_handler(commands=['start'])
def send(message):
    bot.send_message(message.chat.id, 'Hey👋 Welcome to Calcura!\nSend /calculator to open the calculator✅\nor you can add me to your group👥\n🟠Subscribe us if you can', reply_markup=start_markup)

@bot.message_handler(commands=['calculator'])
def send(message):
    
    con = sql.connect('data.db')
    cursor = con.cursor()
    cursor.execute(f'SELECT chat_id FROM calculator WHERE 1')
    IsExists = (message.chat.id, ) in cursor.fetchall()
    if IsExists:
        cursor.execute(f'SELECT monitor FROM calculator WHERE chat_id = {message.chat.id}')
        monitor = cursor.fetchall()[0][0]
        bot.send_message(message.chat.id, f'This is monitor:\n{monitor}\n_________________________', reply_markup=markup)
    else:
        cursor.execute(f'INSERT INTO calculator VALUES("", {message.chat.id})')
        con.commit()
        cursor.execute(f'SELECT monitor FROM calculator WHERE chat_id = {message.chat.id}')
        monitor = cursor.fetchall()[0][0]
        bot.send_message(message.chat.id, f'This is monitor:\n{monitor}\n_________________________', reply_markup=markup)
@bot.message_handler(commands=['reset'])
def rset(message):
    con = sql.connect('data.db')
    cursor = con.cursor()
    cursor.execute(f'UPDATE calculator SET monitor = "" WHERE chat_id = {message.chat.id}')
    con.commit()
    bot.send_message(message.chat.id, 'The monitor cleared!')
@bot.callback_query_handler()
def handle(call):
    con = sql.connect('data.db')
    cursor = con.cursor()
    cursor.execute(f'SELECT monitor FROM calculator WHERE chat_id = {call.message.chat.id}')
    monitor = cursor.fetchall()[0][0]
    if call.data in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        bot.edit_message_text(f'This is monitor:\n{monitor + call.data}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
        cursor.execute(f'UPDATE calculator SET monitor = "{monitor+call.data}" WHERE chat_id = {call.message.chat.id}')
        con.commit()
    elif not monitor[len(monitor)-1] in ['+', '-', '÷', '\u00D7', '.', '^']:
        if call.data == 'plus':
            bot.edit_message_text(f'This is monitor:\n{monitor +'+'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'+'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'negative':
            bot.edit_message_text(f'This is monitor:\n{monitor +'-'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'-'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'cross':
            bot.edit_message_text(f'This is monitor:\n{monitor +'\u00D7'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'\u00D7'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'devide':
            bot.edit_message_text(f'This is monitor:\n{monitor +'÷'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'÷'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'point':
            bot.edit_message_text(f'This is monitor:\n{monitor +'.'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'.'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'power':
            bot.edit_message_text(f'This is monitor:\n{monitor +'^'}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
            cursor.execute(f'UPDATE calculator SET monitor = "{monitor+'^'}" WHERE chat_id = {call.message.chat.id};')
            con.commit()
        elif call.data == 'equal':
            index = ''
            for i in call.message.text:
                if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '+', '-']:
                    index += i 
                elif i == '\u00D7':
                    index += '*'
                elif i == '÷':
                    index += '/'
                elif i == '^':
                    index += '**'
            try:
                result = eval(sanitize_expression(index))
                bot.edit_message_text(f'This is monitor:\n{result}\n_________________________', call.message.chat.id, call.message.message_id, reply_markup=markup)
                cursor.execute(f'UPDATE calculator SET monitor = "{result}" WHERE chat_id = {call.message.chat.id};')
                con.commit()
            except:
                bot.answer_callback_query(call.id, "Could not do that", True)
                
    else:
        bot.answer_callback_query(call.id, "You can't make result or use operator after operator", True)
bot.infinity_polling()


