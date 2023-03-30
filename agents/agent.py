"""Agent interface for defining player behaviour"""


class Agent:
    def __init__(self):
        pass

    def play(self, game, actions):
        raise NotImplementedError()
