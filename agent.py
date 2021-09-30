from utils.turn_manager import TurnManager


def agent(observation, configuration):
    turn_manager = TurnManager(observation, configuration)
    return turn_manager.play_turn()
