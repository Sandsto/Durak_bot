import telebot
from telebot import types
import Durak

bot = telebot.TeleBot('1684865185:AAHaAj-z7cQ8ohIZUjmgsN_IJc5JhYMHCpA')

active_game = {}

@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_text(query):
    #записал id и имя того кто начал игру, чтобы затем передать это вместе с callback, т.к id и имя самого callback будут того, кто нажал кнопку
    who_start_game = str(query.from_user.id) + ' ' + query.from_user.first_name

    kb = types.InlineKeyboardMarkup()

    kb.add(types.InlineKeyboardButton(text='Я', callback_data = f'{who_start_game}'))

    results = []

    durak_game = types.InlineQueryResultArticle(
        id="1", title="Сыграть в дурачка",
        input_message_content=types.InputTextMessageContent(message_text=f"Кто сыграет в дурака с {query.from_user.first_name}?"),
        description = 'Хоть ты любишь в очко',
        thumb_url = 'https://sun9-74.userapi.com/c851520/v851520704/c474a/izjMTwMVmto.jpg',
        thumb_width = 16,
        thumb_height = 16,
        reply_markup=kb
    )
    results.append(durak_game)

    start_talk = types.InlineQueryResultArticle(
        id="2", title="Нажми чтобы открыть ЛС с ботом",
        input_message_content=types.InputTextMessageContent(message_text="Перейди в ЛС бота @shdausdvbot и нажми start для начала диалога. \nЗатем возвращайся сюда и можешь бросить вызов игроку, написав @shdausdvbot и выбрав Сыграть в дурачка"),
        description = 'Нужно чтобы игра запустилась',
        thumb_width = 16,
        thumb_height = 16
    )

    results.append(start_talk)

    bot.answer_inline_query(query.id, results, cache_time=1, is_personal = True)   


#ответ на нажатие кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data[-2]  in '♠️♥️♣️♦️':
        if call.from_user.first_name != active_game[call.from_user.id].who_turn:
            bot.send_message(call.from_user.id, 'Не ваш ход')
        else:
            if active_game[call.from_user.id].put_on_desk(call.data) == 'Перевод козырем':
                update_message(call.from_user.id, call.from_user.first_name)

            elif active_game[call.from_user.id].put_on_desk(call.data) !=  False :
                update_message(call.from_user.id)
            else: 
              bot.send_message(call.from_user.id, 'Неверный ход')
    elif call.data =='Бито':
        if call.from_user.first_name != active_game[call.from_user.id].who_turn:
            bot.send_message(call.from_user.id, 'Не ваш ход')
        else:
            if active_game[call.from_user.id].bito(call.from_user.first_name) != False:
                update_message(call.from_user.id)
    elif call.data == 'Взять':
        if call.from_user.first_name != active_game[call.from_user.id].who_turn:
            bot.send_message(call.from_user.id, 'Не ваш ход')
        else:
            if active_game[call.from_user.id].vzat(call.from_user.first_name) != False:
                update_message(call.from_user.id)
    elif call.data == 'Бью':
        
        active_game[call.from_user.id].change_turn()
        update_message(call.from_user.id, pobili=True)
    elif call.data == 'Перевожу':
        active_game[call.from_user.id].change_attacking()
        update_message(call.from_user.id, pereveli=True)


    else: #код исполняется только вначале игры
        host_id_and_name = call.data.split()
        host_id = int(host_id_and_name[0]) #id принимающего
        host_name = host_id_and_name[1] #имя принимающего
        guest_id = call.from_user.id #id гостя
        guest_name=call.from_user.first_name #имя гостя

        host_game = bot.send_message(host_id, 'Игра началась')
        guest_game = bot.send_message(guest_id, 'Игра началась')

        game  = Durak(host_id, guest_id, host_name, guest_name, host_game.message_id, guest_game.message_id)
        
        #записал два раза в словарь для отслеживания текущей игры. Ключом является id игроков
        active_game[host_id]=game
        active_game[guest_id]=game
        #начало игры
        game.start_game()

        update_message(call.from_user.id) 

def update_message(id, somebody_switch=None, pobili=None, pereveli = None):
    #записываю в кнопки какие карты на руках
    kb_host = types.InlineKeyboardMarkup()
    for card in active_game[id].hand_host:
        kb_host.add(types.InlineKeyboardButton(text=f'{card}', callback_data = f'{card}'))
    kb_host.add(types.InlineKeyboardButton(text='Бито', callback_data = 'Бито'))
    kb_host.add(types.InlineKeyboardButton(text='Взять', callback_data = 'Взять'))


        
    kb_guest = types.InlineKeyboardMarkup()
    for card in active_game[id].hand_guest:
        kb_guest.add(types.InlineKeyboardButton(text=f'{card}', callback_data = f'{card}'))
    kb_guest.add(types.InlineKeyboardButton(text='Бито', callback_data = 'Бито'))
    kb_guest.add(types.InlineKeyboardButton(text='Взять', callback_data = 'Взять'))

    return bot.edit_message_text(chat_id= active_game[id].id_host, message_id = active_game[id].id_host_message, text= message_for_host(active_game[id]), reply_markup =kb_host ), bot.edit_message_text(chat_id= active_game[id].id_guest, message_id = active_game[id].id_guest_message, text= message_for_guest(active_game[id]), reply_markup = kb_guest)