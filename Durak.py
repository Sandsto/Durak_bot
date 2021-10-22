import random 

suiti = ['♠️', '♥️','♣️','♦️']
znach36 = ['6', '7', '8', '9', '10', 'J', 'Q','K', 'A']
znach52 = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

all_cards36 = {
    '6♠️': 6, '7♠️': 7, '8♠️': 8, '9♠️': 9, '10♠️': 10, 'J♠️': 11, 'Q♠️': 12, 'K♠️': 13, 'A♠️': 14,
    '6♥️': 6, '7♥️': 7, '8♥️': 8, '9♥️': 9, '10♥️': 10, 'J♥️': 11, 'Q♥️': 12, 'K♥️': 13, 'A♥️': 14,
    '6♣️': 6, '7♣️': 7, '8♣️': 8, '9♣️': 9, '10♣️': 10, 'J♣️': 11, 'Q♣️': 12, 'K♣️': 13, 'A♣️': 14,
    '6♦️': 6, '7♦️': 7, '8♦️': 8, '9♦️': 9, '10♦️': 10, 'J♦️': 11, 'Q♦️': 12, 'K♦️': 13, 'A♦️': 14}

all_cards52 = {
    '2♠️': 2, '3♠️': 3, '4♠️': 4, '5♠️': 5, '6♠️': 6, '7♠️': 7, '8♠️': 8,
    '9♠️': 9, '10♠️': 10, 'J♠️': 11, 'Q♠️': 12, 'K♠️': 13, 'A♠️': 14,
    '2♥️': 2, '3♥️': 3, '4♥️': 4, '5♥️': 5, '6♥️': 6, '7♥️': 7, '8♥️': 8,
    '9♥️': 9, '10♥️': 10, 'J♥️': 11, 'Q♥️': 12, 'K♥️': 13, 'A♥️': 14,
    '2♣️': 2, '3♣️': 3, '4♣️': 4, '5♣️': 5, '6♣️': 6, '7♣️': 7, '8♣️': 8,
    '9♣️': 9, '10♣️': 10, 'J♣️': 11, 'Q♣️': 12, 'K♣️': 13, 'A♣️': 14,
    '2♦️': 2, '3♦️': 3, '4♦️': 4, '5♦️': 5, '6♦️': 6, '7♦️': 7, '8♦️': 8,
    '9♦️': 9, '10♦️': 10, 'J♦️': 11, 'Q♦️': 12, 'K♦️': 13, 'A♦️': 14}



class Durak():
    def __init__(self, host_id, guest_id, host_name, guest_name, host_message_id,
    guest_message_id, host_nickname, guest_nickname):
        self.host_id = host_id
        self.guest_id = guest_id
        self.host_name = host_name
        self.guest_name = guest_name
        self.host_message_id = host_message_id
        self.guest_message_id = guest_message_id
        self.host_nickname = host_nickname
        self.guest_nickname = guest_nickname
        self.hand_host = []
        self.hand_guest = []
        self.deck_of_card = []
        self.card_on_desk = [] 
        self.who_turn = 0
        self.who_attacking = 0
        self.attacking_cards = []
        self.winner = None

    def start_game(self):
        self.deck_of_card= random.sample(all_cards36.keys(), len(all_cards36)) #вернет массив с обозначением карт
        self.full_hand()
        self.trump = self.deck_of_card[0] #получаю значение козыря. '7♣️' например
        self.trump_suit = self.trump[-2] #получаю значение масти козыря отдельно. '♣️' например
        self.who_attacking = self.who_start_game()
        self.who_turn  = self.who_start_game()
       
     
    def full_hand(self, who_attacking_id = None):
        if (len(self.hand_host) <6 or len(self.hand_guest) < 6) and self.deck_of_card !=[]:
            if who_attacking_id == self.host_id:
                if self.deck_of_card !=[]:
                    if len(self.hand_host) < 6:
                        self.hand_host.append(self.deck_of_card.pop())
                if self.deck_of_card !=[]:
                    if len(self.hand_guest) < 6:
                        self.hand_guest.append(self.deck_of_card.pop())
            else:
                if self.deck_of_card !=[]:
                    if len(self.hand_guest) < 6:
                        self.hand_guest.append(self.deck_of_card.pop())
                if self.deck_of_card !=[]:
                    if len(self.hand_host)<6:
                        self.hand_host.append(self.deck_of_card.pop())

            self.full_hand(who_attacking_id)
      
    def who_start_game(self): #определим кто ходит первым, найдя меньший козырь
        trump_host_card = []
        #пройдемся по каждой карте игрока и если это козырь, запишем достоинство карты в trump_host_card
        for host_card in  self.hand_host:
            if self.trump_suit in host_card:
                trump_host_card.append(all_cards36[host_card])
        
        trump_guest_card = []
        #тоже самое для второго игрока
        for guest_card in  self.hand_guest:
            if self.trump_suit in guest_card:
                trump_guest_card.append(all_cards36[guest_card])
        
        #если ни у кого не нашлось козырей, то всё обнуляем и заново начинаем игру
        if trump_host_card ==[] and trump_guest_card ==[]:
            self.deck_of_card = []
            self.hand_host = []
            self.hand_guest = []
            self.trump =[]
            self.trump_suit = []
            self.start_game()
        else:
            min_trump = min(trump_host_card+trump_guest_card)
            
            #возвращаем id того у кого меньший козырь
            if min_trump in trump_host_card:
                return self.host_id 
            else:
                return self.guest_id

    def get_name_who_turn(self):
        if self.who_turn == self.host_id:
            return self.host_name
        else:
            return self.guest_name 

    
    def change_who_turn(self):
        if self.who_turn == self.host_id:
            self.who_turn = self.guest_id
        else:
            self.who_turn = self.host_id 

    def change_who_attacking(self):
        if self.who_attacking == self.host_id:
            self.who_attacking = self.guest_id
        else:
            self.who_attacking = self.host_id    

    def is_trump(self, card):
        if self.trump_suit == card[-2]:
            return True
        else: return False

    def check_turn(self, card, who):
        if who == self.who_attacking:
            if self.card_on_desk == []:
                self.put_on_desk(card, attack=True)
                self.change_who_turn()
                return True
            else: 
                value_on_desk = []
                for one_card in self.card_on_desk:
                    value_on_desk.append(all_cards36[one_card])
                if all_cards36[card] in value_on_desk:
                    self.put_on_desk(card, attack=True)
                    self.change_who_turn()
                    return True
                else: return False
        else:
            #проверяю если количество карт на столе и которые нужно отбить совпали
            #и совпало значение карты с одной из карт на столе значит это перевод карты
            
            if len(self.card_on_desk) == len(self.attacking_cards) and len(self.card_on_desk)!= 0 and all_cards36[card] == all_cards36[self.card_on_desk[0]]:
                if self.is_trump(card):
                    #по умолчанию считаю, что козырем переводят
                    self.put_on_desk(card, attack=True)
                    if self.hand_defender_is_empty():
                        self.attack_pass()
                        return True
                    else:
                        return 'Перевод козырем'
                else: 
                    self.put_on_desk(card,attack=True)
                    if self.hand_defender_is_empty():
                        self.attack_pass()
                        return True
                    else: 
                        self.change_who_turn()
                        self.change_who_attacking()
                        return True
            #если не перевод то игрок отбивается
            else:
                #если козырь
                if self.is_trump(card):
                    if self.is_trump(self.attacking_cards[0]):
                        if all_cards36[card] > all_cards36[self.attacking_cards[0]]:
                            self.put_on_desk(card, attack=False)
                            if self.hand_defender_is_empty():
                                self.attack_pass()
                                return True
                            else:
                                if self.attacking_cards ==[]: #если больше нечего отбивать
                                    self.change_who_turn()
                                return True
                        else: return False
                    else: 
                        self.put_on_desk(card, attack=False)
                        if self.hand_defender_is_empty():
                            self.attack_pass()
                            return True
                        else: 
                            if self.attacking_cards ==[]:
                                self.change_who_turn()
                            return True
                #если обычная карта
                else:
                    if card[-2] == self.attacking_cards[0][-2]:
                        if all_cards36[card] > all_cards36[self.attacking_cards[0]]:
                            self.put_on_desk(card, attack=False)
                            if self.hand_defender_is_empty():
                                self.attack_pass()
                                return True
                            else: 
                                if self.attacking_cards ==[]:
                                    self.change_who_turn()
                                return True
                        else: return False
                    else: return False

        

    def put_on_desk(self, card, attack=None):
        #положить карту на стол и убрать ее с руки игрока
        self.card_on_desk.append(card)
        if attack:
            self.attacking_cards.append(card)
        else: self.attacking_cards.pop(0)
        if card in self.hand_host:
            self.hand_host.remove(card)
        else: self.hand_guest.remove(card)
        #добавил условие победы, если карты в колоде и на руке кончились, после того как положили карту
        if self.deck_of_card == []:
            if self.hand_host == []:
                self.winner = self.host_name
            elif self.hand_guest == []:
                self.winner = self.guest_name

    def trump_was_defence(self):
        #если перевод козырем оказался побитием карты
        self.attacking_cards.pop() #удаляем козырь из карт которые нужно отбить
        self.attacking_cards.pop(0) #удаляем карту которую козырь побил-первую карту
        self.change_who_turn()
    
    def trump_was_switch(self):
        #если козырем всё таки перевели то оставляем все как есть
        # только меняем атакующего и чей ход
        self.change_who_attacking()
        self.change_who_turn()

    def attack_pass(self): #при нажатии бито
        self.full_hand(self.who_attacking)
        self.card_on_desk = []
        self.attacking_cards = []
        self.change_who_turn()
        self.change_who_attacking()

    def give_up(self, who): #при нажатии "взять"
        for card in self.card_on_desk:
            if who == self.host_id:
                self.hand_host.append(card)
            else: self.hand_guest.append(card) 
        self.full_hand(self.who_attacking)
        self.card_on_desk = []
        self.attacking_cards = []
        self.change_who_turn()
            
    def hand_defender_is_empty(self):
        if self.who_attacking != self.host_id:
            if self.hand_host == []:
                return True
            else: return False
        else: 
            if self.hand_guest ==[]:
                return True
            else: return False
