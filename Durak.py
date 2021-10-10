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
    guest_message_id):
        self.host_id = host_id
        self.guest_id = guest_id
        self. host_name = host_name
        self.guest_name = guest_name
        self.host_message_id = host_message_id
        self.guest_message_id = guest_message_id
        self.hand_host = []
        self.hand_guest = []
        self.deck_of_card = []
        self.card_on_desk = [] 
        self.who_turn = 0
        self.who_attacking = 0

    def start_game(self):
        self.deck_of_card= random.sample(all_cards36.keys(), len(all_cards36)) #вернет массив с обозначением карт
        self.full_hand()
        self.trump = self.deck_of_card[-1] #получаю значение козыря. '7♣️' например
        self.trump_suit = self.trump[-2] #получаю значение масти козыря отдельно. '♣️' например
        self.who_attacking = self.who_start_game()
        self.who_turn  = self.who_start_game()
       
     
    def full_hand(self, who_attacking_id = None):
        if (len(self.hand_guest) <6 or len(self.hand_guest) < 6) and self.deck_of_card !=[]:
            if who_attacking_id == self.host_id:
                if self.deck_of_card !=[]:
                    if len(self.hand_host)<6:
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
        print(trump_host_card)
        trump_guest_card = []
        #тоже самое для второго игрока
        for guest_card in  self.hand_guest:
            if self.trump_suit in guest_card:
                trump_guest_card.append(all_cards36[guest_card])
        print(trump_guest_card)
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
            print(min_trump)
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


A = Durak(111,222,'host', 'guest',333,444)

A.start_game()

print(A.trump, A.hand_host, A.hand_guest, A.who_turn)