import random


class Die:
    """
    This represent a dice and gives a value when it is rolled.
    Attributes ---> value : int {value of the dice when it is rolled}
    Methods ---> get_value(): returns the value of the dice.
                 roll(): rolls the dice
    """

    def __init__(self, val=1):
        """
        Finalizes all the necessary attributes for the die object
        """
        self.roll()

    def get_value(self):
        """ Returns the value"""
        return self._value

    def roll(self):
        """ Gives a random number to value """
        self._value = random.randint(1, 6)


class DiceCup:
    """
    This class represent a list of dice objects and consists of
    all methods required after rolling is performed
    for dice objects .
    Attributes ---> dice : list {A list of die objects}
    Methods --->  roll(): rolls the die objects only that are not banked.
                  value(): returns the value of the rolled dice object at particular index
                  bank(): banks the value at given index
                  is_banked(): returns boolean value whether it is banked or not
                  release(): releases the banked value at given index by making booldice as false
                  release_all(): releases all the banked values
    """

    def __init__(self, no_of_faces: int):
        """
        constructs the faces attribute with the list of die objects
        Parameters -----> no_of_faces
                          no.of faces  can be used to play is given by no_of_faces 
        """
        self._dice = []
        for _ in range(no_of_faces):
            self._dice.append([Die(), False])

    def roll(self):
        """
        Rolling of all the die objects is performed here
        Parameters ------>None
        Returns   ------->None
        """
        for dice in self._dice:
            if dice[1] == False:
                dice[0].roll()

    def value(self, ref: int) -> int:
        """
        Returns the value at the given ref of the die object
        Parameters------>ref
                         ref of the list of die objects 
        Returns : int
        value of the die object
        """
        return self._dice[ref][0].get_value()

    def bank(self, ref: int):
        """
        Banks the value at the given ref by making booldice 
        list af given ref to true
        Parameters------>ref 
                         ref of the list which has to be true
         Returns ------->None
        """
        self._dice[ref][1] = True

    def is_banked(self, ref):
        """
        Returns True or False ref that the die object is 
        banked or not
        Parameters -------->ref
                          ref of the list which has to be true (or) false
        Returns ----->True (or) False
        """
        return self._dice[ref][1]

    def release(self, ref: int) -> bool:
        """
        Releases the value at the given index by making false 
        at booldice list of given ref
        Parameters -------> ref
            ref of the list which has to be true
        Returns --------> None
        """
        self._dice[ref][1] = False

    def release_all(self):
        """
        Releases all the values of the list by making false 
        at every position of booldice
        Parameters ------> None
        Returns -------> None
        """
        for dice in self._dice:
            dice[1] = False


class ShipOfFools:
    """
    Main logic will be done in this class using Die class 
    and Dicecup class
    Attributes ---------> cup : Dicecup object 
       A Dicecup object is instantiated in this attribute
    Methods------>round():
       This is part where all the conditions are given 
       after the dice are rolled
    """

    def __init__(self):
        """
        constructs the cup attribute with the dicecup object
        Parameters ------->None 
        """
        self._dicecup = DiceCup(5)
        self._final_score = 21

    def rounds(self) -> int:
        player_start_score = 0
        """
        Dice is rolled 3 times the ship, captain and 
        crew has to be banked.
        Returns the score if all are banked 
        Parameters ----->None 
        Returns -------> Score after 3 rounds
        """
        has_ship, has_captain, has_crew = False, False, False
        self._dicecup.release_all()
        for round_ in range(3):
            self._dicecup.roll()
            value = [self._dicecup._dice[i][0].get_value() for i in range(5)]
            print("rolled values:", value)
            if not has_ship and value.count(6):
                self._dicecup.bank(value.index(6))
                has_ship = True

            if not has_captain and has_ship and value.count(5):
                self._dicecup.bank(value.index(5))
                has_captain = True

            if not has_crew and has_captain and value.count(4):
                self._dicecup.bank(value.index(4))
                has_crew = True

            if has_ship and has_captain and has_crew:
                if round_ == 2:
                    for i in range(5):
                        if self._dicecup.is_banked(i):
                            pass
                        else:
                            self._dicecup.bank(i)
                if round_ < 2:
                    for i in range(5):
                        if self._dicecup._dice[i][0].get_value() > 3 and not self._dicecup.is_banked(i):
                            self._dicecup.bank(i)

            if round_ == 2:
                print("After 3 rolls:", value, "\n")

        if has_ship and has_captain and has_crew:
            for i in range(5):
                player_start_score = player_start_score + self._dicecup._dice[i][0].get_value()
            player_start_score = player_start_score - 15
        return player_start_score


class Player:
    """
    Player class is responsible for adding the players and 
    managing the individual scores
    ...
    Attributes -------->name : string 
       Name of the player
       score : int
       Score of the player(individual score)   
    Methods ------>set_name():
        Method to give the name of the player
        play_round():
        player plays a round(3 rolls) of game and takes score
        current_score():
        Adds the score with the previous score     
        reset_score():
        Resets the score of a playerto 0    
    """

    def __init__(self, player_name: str):
        """
        constructs the name and score attribute with the name 
        of the player and 0
        Parameters --------> Namestring: creates a new string from the
        given object
        """
        self._score = 0
        self.set_name(player_name)

    def set_name(self, player_name):
        """ sets the name with given name """

        self._name = player_name

    def play_round(self, games: object):
        """ A round of a player is done in this method and adds
         the returned score """
        self._score = self._score + games.rounds()

    def current_score(self):
        """ Adds the new score with the previous score after
         round method is performed """
        return self._score

    def updated_score(self):
        """ Updates the score to zero"""
        self._score = 0


class PlayerRoom:
    """
    PlayRoom is responsible for all players objects from the
     player class and prints all the scores and Winner
    ...
    Attributes ------> game : object
                 object of the class ShipOfFoolsGame
                  players : list objects
                  A list of all player objects added in the game  
    Methods  -------> set_game():
            Starts the game only when it is called
            add_player(): Adds the player object in the players list
            reset_scores(): Resets scores of all players to zero      
            play_round(): All players plays a round(3 rolls) of game
            game_finished(): Checks whether atleast one player has reached winning score and ends the game if it happens  
            print_scores(): Prints the scores of all players   
            print_winner(): Prints the name of winner
            if winner is one print the nme
            else draw   
    """

    def __init__(self):
        self._players = []
        """
        constructs the game and players attribute with the object
        of the class ShipOfFoolsGame and empty list
        Parameters -------> None
        """

    def set_game(self, games):

        """ construct game as the object of 
        ShipOfFoolsGame class """
        self._games = games

    def add_player(self, players: Player):
        """Appends the player object to list of players when 
        it is created at main code"""

        self._players.append(players)

    def reset_scores(self):
        """ Resets the score of all the players to 0 zero """
        i = 0
        while i < len(self._players):
            self._players[i].updated_score()
            i += 1

    def play_round(self):

        """ Play a round of game for all the player objects"""
        i = 0
        while i < len(self._players):
            self._players[i].play_round(self._games)
            i += 1

    def game_finished(self) -> bool:

        """ Checks whether atleast one player reached 
        the winning score and returns true if happens
        Returns : Boolean
           True (or) False
        """

        req = False
        i = 0
        while i < len(self._players):
            if self._players[i].current_score() >= self._games._final_score:
                req = True
            i += 1
        return req

    def print_scores(self):

        """Prints the scores of all the players 
        after the round method  is performed """

        i = 0
        while i < len(self._players):
            print(f"{self._players[i]._name}'s score is {self._players[i].current_score()}")
            i += 1

    def final_winner(self):

        """Print the final winner name who has scored more points
            if there are more than one players it returns
            the game is draw"""
        end_score = 21
        draw_players = []
        count = 0
        while count < len(self._players):
            if self._players[count].current_score() >= end_score:
                draw_players.append(self._players[count]._name)
            count += 1
        if len(draw_players) == 1:
            print(f"The winner is {draw_players[0]}")
        else:
            print("Game is draw", draw_players)


if __name__ == "__main__":
    room = PlayerRoom()
    room.set_game(ShipOfFools())
    room.add_player(Player("loki1"))
    room.add_player(Player("loki2"))
    room.add_player(Player("loki3"))
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()

    room.final_winner()
