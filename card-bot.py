import telebot
from telebot import types
from Durak import Durak

bot = telebot.TeleBot('1684865185:AAHaAj-z7cQ8ohIZUjmgsN_IJc5JhYMHCpA')

active_game = {}
try:
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
            game = active_game[call.from_user.id]
            if call.from_user.id != game.who_turn:
                bot.send_message(call.from_user.id, 'Не ваш ход')
            else:
                what_return_check = game.check_turn(call.data, call.from_user.id)
                if  what_return_check == True:
                    if game.winner != None:
                        bot.edit_message_text(chat_id= game.host_id, message_id = game.host_message_id, text= f"Игра завершена, победитель - {game.winner} \n"+ message_for_host(game))
                        bot.edit_message_text(chat_id= game.guest_id, message_id = game.guest_message_id, text= f"Игра завершена, победитель - {game.winner} \n" + message_for_guest(game))
                        del active_game[game.host_id]
                        del active_game[game.guest_id]
                    else: 
                        update_message(game)

                elif what_return_check == 'Перевод козырем':
                    if game.winner != None:
                        bot.edit_message_text(chat_id= game.host_id, message_id = game.host_message_id, text= f"Игра завершена, победитель - {game.winner} \n" + message_for_host(game))
                        bot.edit_message_text(chat_id= game.guest_id, message_id = game.guest_message_id, text= f"Игра завершена, победитель - {game.winner} \n" + message_for_guest(game))
                        del active_game[game.host_id]
                        del active_game[game.guest_id]
                    else: 
                        to_clarify(call.from_user.id)
                else:    
                    bot.send_message(call.from_user.id, 'Неверный ход')
        
        elif call.data == 'Бито':
            game = active_game[call.from_user.id]
            if call.from_user.id != game.who_turn:
                bot.send_message(call.from_user.id, 'Не ваш ход')
            elif call.from_user.id != game.who_attacking:
                bot.send_message(call.from_user.id, 'Вы должны отбивать карты')
            elif game.card_on_desk ==[]:
                bot.send_message(call.from_user.id, 'Стол пуст, положите карту')
            else:  
                game.attack_pass()
                update_message(game)

        elif call.data =='Взять':
            game = active_game[call.from_user.id]
            if call.from_user.id != game.who_turn:
                bot.send_message(call.from_user.id, 'Не ваш ход')
            elif call.from_user.id == game.who_attacking:
                bot.send_message(call.from_user.id, 'Вы атакуете, положите карту')
            elif game.card_on_desk == []:
                bot.send_message(call.from_user.id, 'Стол пуст')

            else:  
                game.give_up(call.from_user.id)
                update_message(game)

        elif call.data == 'Закончить игру':
            game  = active_game[call.from_user.id]
            bot.edit_message_text(chat_id= game.host_id, message_id = game.host_message_id, text= f"Игра завершена")
            bot.edit_message_text(chat_id= game.guest_id, message_id = game.guest_message_id, text= f"Игра завершена")
            del active_game[game.host_id]
            del active_game[game.guest_id]

        elif call.data == 'Перевожу':
            game = active_game[call.from_user.id]
            game.trump_was_switch()
            bot.delete_message(call.from_user.id, call.message.message_id)
            update_message(game, switch = True)

        elif call.data == 'Бью':
            game = active_game[call.from_user.id]
            game.trump_was_defence()
            bot.delete_message(call.from_user.id, call.message.message_id)
            update_message(game, switch = False)

        

        else: #код исполняется только вначале игры
            host_id_and_name = call.data.split()
            host_id = int(host_id_and_name[0]) #id принимающего
            host_name = host_id_and_name[1] #имя принимающего
            guest_id = call.from_user.id #id гостя
            guest_name=call.from_user.first_name #имя гостя

            if host_id in active_game.keys() or guest_id in active_game.keys():
                if host_id in active_game.keys():
                    bot.send_message(host_id, 'У вас есть незаконченная игра')
                elif guest_id in active_game.keys():
                    bot.send_message(guest_id, 'У вас есть незаконченная игра')
                return False
            else:

                host_game = bot.send_message(host_id, 'Игра началась')
                guest_game = bot.send_message(guest_id, 'Игра началась')

                game  = Durak(host_id, guest_id, host_name, guest_name, host_game.message_id, guest_game.message_id)
                
                #записал два раза в словарь для отслеживания текущей игры. Ключом является id игроков
                active_game[host_id]=game
                active_game[guest_id]=game

                #Изменил сообщение-приглашение 
                bot.edit_message_text(inline_message_id=call.inline_message_id,
                    text=f'Игра между {game.host_name} и {game.guest_name} началась. Перейдите в диалог с ботом. Удачи')
                #начало игры
                game.start_game()

                update_message(game) 

    def update_message(game, switch =None):
        #записываю в кнопки какие карты на руках
        kb_host = types.InlineKeyboardMarkup()
        for card in game.hand_host:
            kb_host.add(types.InlineKeyboardButton(text=f'{card}', callback_data = f'{card}'))
        kb_host.add(types.InlineKeyboardButton(text='Бито', callback_data = 'Бито'))
        kb_host.add(types.InlineKeyboardButton(text='Взять', callback_data = 'Взять'))
        kb_host.add(types.InlineKeyboardButton(text='Закончить игру', callback_data = 'Закончить игру'))

        host_text = message_for_host(game)


        kb_guest = types.InlineKeyboardMarkup()
        #kb_guest.row_width = 3
        for card in game.hand_guest:
            kb_guest.add(types.InlineKeyboardButton(text=f'{card}', callback_data = f'{card}'))
        kb_guest.add(types.InlineKeyboardButton(text='Бито', callback_data = 'Бито'))
        kb_guest.add(types.InlineKeyboardButton(text='Взять', callback_data = 'Взять'))
        kb_guest.add(types.InlineKeyboardButton(text='Закончить игру', callback_data = 'Закончить игру'))

        guest_text = message_for_guest(game)

        if switch == True :
            host_text += 'Козырем перевели'
            guest_text += 'Козырем перевели'
        elif switch == False:
            host_text += 'Козырем побили карту'
            guest_text += 'Козырем побили карту'


        bot.edit_message_text(chat_id= game.host_id, message_id = game.host_message_id, text= host_text, reply_markup =kb_host )
        bot.edit_message_text(chat_id= game.guest_id, message_id = game.guest_message_id, text= guest_text, reply_markup = kb_guest)


    def message_for_host(game):
        
        on_deck = ''
        for card in game.card_on_desk:
            on_deck += card

        text = f''' В колоде {len(game.deck_of_card)} карт
        Козырь {game.trump}
        Карты соперника: {"🃏"*len(game.hand_guest)}
        На столе:
        {on_deck}
        Ходит: {game.get_name_who_turn()}
        '''
        return(text)

    def message_for_guest(game):
        
        on_deck = ''
        for card in game.card_on_desk:
            on_deck += card

        text = f''' В колоде {len(game.deck_of_card)} карт
        Козырь {game.trump}
        Карты соперника: {"🃏"*len(game.hand_host)}
        На столе:
        {on_deck}
        Ходит: {game.get_name_who_turn()}
        '''
        return(text)

    def to_clarify(id):
        kb = types.InlineKeyboardMarkup()
        kb.row_width = 2
        kb.add(types.InlineKeyboardButton(text='Перевожу', callback_data = 'Перевожу'))
        kb.add(types.InlineKeyboardButton(text='Бью', callback_data = 'Бью'))
        
        bot.send_message(id, 'Вы переводите козырем или бьете  карту?', reply_markup=kb)
    


except KeyError as ke:
    print(ke)
    bot.send_message(ke, 'Ошибка, попробуйте позже сыграть')


bot.polling(none_stop=True)