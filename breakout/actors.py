from random import randint
from breakout.input_events import *
from pygame.locals import *

class ScreenActor(object):
    def __init__(self, x, y, width, height, state):
        self.width = width
        self.height = height
        self.state = state
        self.rect = state.pygame_obj.Rect(x, y, width, height)

class QuadActor(ScreenActor):
    """
    Square/Rectangle actor, nothing special
    """
    def __init__(self, x, y, width, height, state):
        if not getattr(self, 'color', None):
            self.color = state.pygame_obj.Color(255, 255, 255)
        super(QuadActor, self).__init__(x, y, width, height, state)

    def draw(self, canvas, pygame):
        """
        Draws a single rectangle as the actor
        """
        pygame.draw.rect(
                canvas, self.color, 
                (self.rect.x, self.rect.y, self.width, self.height)
            )


class Brick(QuadActor):
    WIDTH = 40.0
    HEIGHT = 20.0

    def __init__(self, x, y, state):
        self.color = state.pygame_obj.Color(
                randint(10, 255), randint(10, 255), randint(10, 255)
                )
        super(Brick, self).__init__(
                x, y, 
                Brick.WIDTH, Brick.HEIGHT,
                state
            )

    def tick(self, ticks):
        pass


class Ball(QuadActor):
    WIDTH = 10.0
    HEIGHT = 10.0
    INITIAL_SPEED = 3.5

    def __init__(self, x, y, state, coords_min, coords_max):
        self.dx = Ball.INITIAL_SPEED
        self.dy = -Ball.INITIAL_SPEED
        self.coords_min = coords_min
        self.coords_max = coords_max
        super(Ball, self).__init__(
                x, y,
                Ball.WIDTH, Ball.HEIGHT,
                state
            )

    def event(self, event_type, event_params):
        pass

    def _detect_collisions(self, dx, dy):
        'cheapo collision detection'
        if self.state.player.rect.colliderect(self.rect):
            if dx != 0:
                self.dx = -self.dx
                self.rect.x += self.dx
            elif dy != 0:
                self.dy = -self.dy
                self.rect.y += self.dy
        else:
            for brick in self.state.bricks:
                if brick.rect.colliderect(self.rect):
                    if dx != 0:
                        self.dx = -self.dx
                        self.rect.x += self.dx
                    elif dy != 0:
                        self.dy = -self.dy
                        self.rect.y += self.dy
                    self.state.bricks.remove(brick)
                    break

    def tick(self, ticks):
        self.rect.x += self.dx
        self._detect_collisions(self.dx, 0)
        if self.rect.x + Ball.WIDTH > self.coords_max[0]:
            self.rect.x = self.coords_max[0] - Ball.WIDTH
            self.dx = -self.dx
        if self.rect.x < self.coords_min[0]:
            self.rect.x = self.coords_min[0]
            self.dx = -self.dx

        self.rect.y += self.dy
        self._detect_collisions(0, self.dy)
        if self.rect.y + Ball.HEIGHT > self.coords_max[1]:
            print 'holy fuck you fail'
            self.state.endgame()
        if self.rect.y < self.coords_min[1]:
            self.rect.y = self.coords_min[1]
            self.dy = -self.dy


class Player(QuadActor):
    WIDTH = 60.0
    HEIGHT = 20.0
    SPEED = 8.0

    def __init__(self, x, y, state, x_min, x_max):
        self.input_events = {}
        self.x_min = x_min
        self.x_max = x_max
        super(Player, self).__init__(
                x, y,
                Player.WIDTH, Player.HEIGHT,
                state
            )

    def input(self, input_type, params):
        if input_type == BRK_KEYDOWN:
            if params['key'] == K_LEFT:
                self.input_events['moveleft'] = 1
            elif params['key'] == K_RIGHT:
                self.input_events['moveright'] = 1
        elif input_type == BRK_KEYUP:
            if params['key'] == K_LEFT:
                self.input_events['moveleft'] = 0
            elif params['key'] == K_RIGHT:
                self.input_events['moveright'] = 0

    def tick(self, ticks):
        for event_type,event_val in self.input_events.items():
            if event_type == 'moveleft' and event_val == 1:
                self.rect.x = min( max(self.x_min, self.rect.x-Player.SPEED), self.x_max-Player.WIDTH )
            if event_type == 'moveright' and event_val == 1:
                self.rect.x = min( max(self.x_min, self.rect.x+Player.SPEED), self.x_max-Player.WIDTH )
