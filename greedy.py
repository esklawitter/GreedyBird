import logging
from datetime import datetime

from game_wrapper import GameWrapper

logger = logging.getLogger(__name__)

NO_OPENING_MIN = 100
BIRD_HEIGHT = 40
BOTTOM_OPENING_OFFSET = 30

# Jumping doesn't compound so no need to debounce jumps
TICK_RATE_S = 0


class GreedyBird:
    """
    Simple algorithm to play Flappy Bird.  Jumps anytime the bird is below the bottom pipe + an offset.
    """
    def __init__(self, game_wrapper: GameWrapper):
        self.game = game_wrapper
        self.bird_start = self.game.bird
        self.last_tick = datetime.now()

    def tick(self):
        now = datetime.now()
        if (now - self.last_tick).total_seconds() > TICK_RATE_S:
            self.last_tick = now
            if self.should_jump():
                self.game.jump()

    def should_jump(self):
        bird = self.game.bird
        opening = self.game.next_opening

        logger.debug(f'Bird: {bird}')
        logger.debug(f'Opening: {opening}')

        # If there are no pipes on screen yet, hover
        if not opening:
            if bird.y - self.bird_start.y > NO_OPENING_MIN:
                return True

        else:
            # negative = bird below opening
            eff_opening_bottom = opening.bot - BOTTOM_OPENING_OFFSET
            eff_bird_bottom = bird.y + BIRD_HEIGHT
            dist_below_opening = eff_bird_bottom - eff_opening_bottom
            if dist_below_opening > 0:
                return True

        return False
