import lesson_16.tanks as tanks
import lesson_16.shells as shells
from lesson_16.constants import *


class GameRound:
    def __init__(self, canvas, difficulty=1):
        assert difficulty < 10
        self._canvas = canvas
