import logging
import time
from collections import namedtuple
from typing import List

from selenium import webdriver

GAME_URL = 'http://flappybird.io/'
OPENING_OFFSET = 200

logger = logging.getLogger(__name__)

Opening = namedtuple('Opening', ['x', 'bot', 'top'])
Position = namedtuple('Positioning', ['x', 'y'])


class GameOver(BaseException):
    pass


class GameWrapper:
    def __init__(self):
        self._next_opening = None
        self._openings = []

        self.driver = webdriver.Chrome()
        self.driver.get(GAME_URL)
        # wait for the site to load
        time.sleep(3)

    @property
    def bird(self) -> Position:
        return self.get_bird_pos()

    @property
    def openings(self) -> List[Opening]:
        return self.get_openings()

    @property
    def next_opening(self) -> Opening:
        return self.get_next_opening()

    def jump(self) -> None:
        logger.info('Jumping')
        self.driver.execute_script('spacebar();')

    def get_bird_pos(self) -> Position:
        bird_loc = self.driver.execute_script('return [bird.x, bird.y]')
        return Position(bird_loc[0], bird_loc[1])

    def get_openings(self) -> List[Opening]:
        try:
            all_pipes = self.driver.execute_script('''
                x = []; 
                pipes.children.forEach(element => x.push([element.x, element.y])); 
                return x;
            ''')
        except Exception as e:
            pass
        else:
            pipe_positions = [Position(pipe[0], pipe[1]) for pipe in all_pipes]
            all_openings = []
            for i in range(0, len(pipe_positions), 2):
                all_openings.append(Opening(pipe_positions[i].x, pipe_positions[i].y, pipe_positions[i + 1].y))
            self._openings = all_openings
        finally:
            return self._openings

    def get_next_opening(self) -> Opening:
        bird = self.bird
        for opening in self.openings:
            # Delay moving to the next opening until we've truly cleared it
            if opening.x + OPENING_OFFSET > bird.x:
                return opening

    def raise_game_status(self) -> None:
        if self.is_game_over():
            raise GameOver()

    def is_game_over(self) -> bool:
        return self.driver.execute_script('return !started || dead')
