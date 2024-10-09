from collections import defaultdict
import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.balls = []
    
    def add_balls(self, balls_list, num):
        for i in range (num):
            self.balls.append(balls_list.pop())
        
class Bank:
    def __init__(self):
        self.ball_array = open("ball_values.txt").read().split(", ")
        
    def select_balls(self, num):
        balls = []
        for i in range(num):
            balls.append(self.ball_array.pop())
        return balls
    
    def randomize(self):
        random.shuffle(self.ball_array)

class GoldenBalls:
    def __init__(self, socketio, clients):
        self.player_array = [Player("James"), Player("Luke"), Player("Emily"), Player("Jack")]
        self.bank = Bank()
        self.bank.randomize()
        self.balls_in_play = ['KILLER', 'KILLER', 'KILLER', 'KILLER'] + (self.bank.select_balls(12))
        random.shuffle(self.balls_in_play)
        self.total = 0
        self.remove_choices = defaultdict(int)
        self.vote_counter = 0

        self.socketio = socketio
        self.clients = clients
        
    def concat(self, list):
        message = ""
        for w in list:
            message += (str(w) + " ")
        return message
    
    def send_message_to_clients(self, command, sid, message):
        if sid in self.clients:
            self.socketio.emit(command, message, to=sid)  # Send message to specific client
        else:
            print(f"Client with sid {sid} not connected.")

    def play(self):

        for i, player in enumerate(self.player_array):
            player.add_balls(self.balls_in_play, 4)
            balls = self.concat(player.balls)
            print(f"{i} | {balls}")
            
        self.show_balls_to_players()

        for i in range (4):
            client_sid = list(self.clients.keys())[i]  # Get the sid from clients by index
            self.send_message_to_clients("vote_1", client_sid, "")

    def round_two(self):
        
        self.repopulate()
        self.balls_in_play.append("KILLER")
        self.balls_in_play += self.bank.select_balls(2)
        random.shuffle(self.balls_in_play)
        print("")
        
        for i, player in enumerate(self.player_array):
            player.add_balls(self.balls_in_play, 5)
            balls = self.concat(player.balls)
            print(f"{i} | {balls}")
           
        self.show_balls_to_players()
        
    def bin_or_win(self):
        
        random.shuffle(self.balls_in_play)
        print("")
        
        for i in range(0,10):
            if i % 2 == 0:
                while True:
                    try:
                        b = int(input("Choose a ball to win: "))
                        if 1 <= b <= len(self.balls_in_play) and self.balls_in_play[b-1] is not None:
                            break
                        
                        print("Invalid input\n")
                            
                    except ValueError:
                        print("Invalid input\n")
                
                select = self.balls_in_play[b-1]
                
                if select == "KILLER":
                    print(f"You have selected the KILLER, total is divided by 10")
                    self.total /= 10
                else:
                    print(f"You add ${select} to your total")
                    self.total += int(select)
                
                self.balls_in_play[b-1] = None
                print(f"Total: {self.total}")
                    
            if i % 2 == 1:
                while True:
                    try:
                        b = int(input("Choose a ball to bin: "))
                        if 1 <= b <= len(self.balls_in_play) and self.balls_in_play[b-1] is not None:
                            break
                        
                        print("Invalid input\n")
                            
                    except ValueError:
                        print("Invalid input\n")
                        
                select = self.balls_in_play[b-1]

                print(f"You binned the {select}")
                self.balls_in_play[b-1] = None
                
            print("")
    
    def remove_player(self, round):
        global clients
                
        print("Removing a player...")

        most_voted_player = max(self.remove_choices, key=self.remove_choices.get)
        print("Most voted player is player: " , most_voted_player, "/ " + self.player_array[most_voted_player].name)
        self.player_array.remove(self.player_array[most_voted_player])
        del clients[most_voted_player]

        self.remove_choices = defaultdict(int)
        self.vote_counter = 0

        if round == 1:
            self.round_two()
        if round == 2:
            self.bin_or_win()
                
    
    def repopulate(self):
        for player in self.player_array:
            for ball in player.balls:
                self.balls_in_play.append(ball)
                player.balls = []
                
                
    def show_balls_to_players(self):
        for i, a_player in enumerate(self.player_array):
            for j, b_player in enumerate(self.player_array):
                if i == j:
                    message = f"Your balls:\t{self.concat(a_player.balls)}\n"
                else:
                    message = f"{b_player.name}'s balls:\t{b_player.balls[0]} {b_player.balls[1]}\n"
                client_sid = list(self.clients.keys())[i]  # Get the sid from clients by index
                self.send_message_to_clients("ball_values", client_sid, message)