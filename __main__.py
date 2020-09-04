import logging
import sys

from game_wrapper import GameWrapper, GameOver
from greedy import GreedyBird

logger = logging.getLogger(__name__)


def main():
    game = GameWrapper()
    while True:
        try:
            play_round(game)
        except GameOver as e:
            another_game = input('Game over.  Try again? [Y/N]')
            if another_game.upper() == 'Y':
                game.jump()
                continue
            else:
                raise e


def play_round(game: GameWrapper):
    algo = GreedyBird(game)
    logger.critical('Starting Game')
    game.jump()
    while True:
        algo.tick()
        game.raise_game_status()


def set_up_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    exclude_loggers()
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)7s] [%(name)10s] %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    logging.debug('Logging Initialized')


def exclude_loggers() -> None:
    # todo migrate off the root logger
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('parse').setLevel(logging.WARNING)


if __name__ == '__main__':
    set_up_logging()
    main()
