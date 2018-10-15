import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of the algo'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.game_strategy(game_state)

        game_state.submit_turn()
        
    def game_strategy(self, game_state):
        start_postitions = [[ 0, 13],[ 2, 13],[ 4, 13],[ 6, 13],[ 8, 13],[ 10, 13],[ 12, 13],[ 14, 13],
                            [ 16, 13],[ 18, 13],[ 20, 13],[ 22, 13],[ 24, 13],[ 26, 13]]

        for pos in start_postitions:
            if game_state.can_spawn(FILTER,pos):
                game_state.attempt_spawn(FILTER,pos)  

        edge_positions = [[ 0, 13],[ 27, 13],[ 1, 12],[ 26, 12],[ 2, 11],[ 25, 11],
                          [ 3, 10],[ 24, 10],[ 4, 9],[ 23, 9],[ 5, 8],[ 22, 8],[ 6, 7],
                          [ 21, 7],[ 7, 6],[ 20, 6],[ 8, 5],[ 19, 5],[ 9, 4],[ 18, 4],
                          [ 10, 3],[ 17, 3],[ 11, 2],[ 16, 2],[ 12, 1],[ 15, 1],[ 13, 0],[ 14, 0]]
        while(game_state.number_affordable(PING)>0):
            pos = random.choice(edge_positions)
            if game_state.can_spawn(PING,pos):
                game_state.attempt_spawn(PING,pos)

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
