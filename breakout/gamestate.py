"""
GameState -- maintains game logic and ticks
"""
from breakout.actors import Ball, Brick, Player
from breakout.input_events import *
from pygame.locals import *

class GameState(object):
    """
    Populates stage actors and is responsible for game ticks
    """
    STAGE_WIDTH = 600 # actual playable part of the canvas
    STAGE_HEIGHT = 420

    EVENT_TYPE_COLLISION = 1

    def __init__(self, canvas, clock, pygame_obj):
        self.canvas = canvas
        self.bricks = set()
        self.ball = None
        self.player = None
        self.clock = clock
        self.pygame_obj = pygame_obj
        self.running = False
        self.gameover = False

    def _populate_actors(self):
        """
        Populates the game actors as follows:
        - 10 x 10 brick grid
        - Single ball starting just below brick grid
        - player at bottom
        """
        self.bricks = set()
        stage_margin_left = (640 - GameState.STAGE_WIDTH)/2
        stage_margin_top = (480 - GameState.STAGE_HEIGHT)/2
        xbase = stage_margin_left + 100
        ybase = stage_margin_top + 20
        bwidth = Brick.WIDTH
        bheight = Brick.HEIGHT
        for i in range(0, 10):
            for j in range(0, 10):
                self.bricks.add(
                    Brick(
                        x = xbase + i*bwidth,
                        y = ybase + j*bheight,
                        state = self
                        )
                    )

        self.ball = Ball(
                x = xbase,
                y = ybase+bheight*11,
                state = self,
                coords_min = (stage_margin_left, stage_margin_top),
                coords_max = (
                    stage_margin_left+GameState.STAGE_WIDTH,
                    stage_margin_top+GameState.STAGE_HEIGHT
                    )
                )

        self.player = Player(
                x = xbase,
                y = GameState.STAGE_HEIGHT - Player.HEIGHT*2,
                state = self,
                x_min = stage_margin_left,
                x_max = stage_margin_left+GameState.STAGE_WIDTH
                )

    def _drawall(self):
        # draw actual stage border
        white = self.pygame_obj.Color(255, 255, 255)
        self.canvas.fill( self.pygame_obj.Color(0, 0, 0) )
        stage_margin_left = (640 - GameState.STAGE_WIDTH)/2
        stage_margin_top = (480 - GameState.STAGE_HEIGHT)/2
        self.pygame_obj.draw.line(self.canvas, white,
            (stage_margin_left, stage_margin_top), 
            (stage_margin_left+GameState.STAGE_WIDTH, stage_margin_top), 
            1)
        self.pygame_obj.draw.line(self.canvas, white,
            (stage_margin_left, stage_margin_top), 
            (stage_margin_left, stage_margin_top+GameState.STAGE_HEIGHT), 
            1)
        self.pygame_obj.draw.line(self.canvas, white,
            (stage_margin_left, stage_margin_top+GameState.STAGE_HEIGHT), 
            (stage_margin_left+GameState.STAGE_WIDTH, stage_margin_top+GameState.STAGE_HEIGHT), 
            1)
        self.pygame_obj.draw.line(self.canvas, white,
            (stage_margin_left+GameState.STAGE_WIDTH, stage_margin_top), 
            (stage_margin_left+GameState.STAGE_WIDTH, stage_margin_top+GameState.STAGE_HEIGHT), 
            1)

        self.ball.draw(self.canvas, self.pygame_obj)
        for brick in self.bricks:
            brick.draw(self.canvas, self.pygame_obj)
        self.player.draw(self.canvas, self.pygame_obj)

    def _tick(self):
        self.ball.tick(1)
        self.player.tick(1)

        if len(self.bricks) == 0:
            print 'holy shit you won'
            self.endgame()

    def _broadcast_input_event(self, event_type, event_params):
        """
        Right now the player is the only one that gives a shit
        about input events
        """
        self.player.input(event_type, event_params)

    def _update_input(self):
        for event in self.pygame_obj.event.get():
            if event.type == QUIT:
                self.running = False
                break

            if event.type not in PYGAME_EVENT_TO_BRK:
                continue

            brk_event_type = PYGAME_EVENT_TO_BRK[event.type]
            brk_event_params = pygame_get_event_params(brk_event_type, event)

            self._broadcast_input_event(brk_event_type, brk_event_params)

    def _mainloop(self):
        """
        Updates the game based on the number of ticks
        ball first, player second
        """
        while self.running:
            if not self.gameover:
                self._update_input()
                self._tick()
                self._drawall()
            else:
                self.running = False #XXX

            self.pygame_obj.display.update()
            self.clock.tick(30)

    def startgame(self):
        """
        Starts a fresh new game
        """
        self._populate_actors()
        self.running = True
        self._mainloop()

    def endgame(self):
        """
        Interrupts the game, will print "GAME OVER" eventually
        """
        self.gameover = True
