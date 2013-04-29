"""
Translate pygame events that we care about 
to our own abstracted schtuff.
"""
from pygame.locals import *

BRK_KEYDOWN = 1
BRK_KEYUP = 2
BRK_MOUSEMOVE = 3

PYGAME_EVENT_TO_BRK = {
        KEYDOWN: BRK_KEYDOWN,
        KEYUP: BRK_KEYUP,
        MOUSEMOTION: BRK_MOUSEMOVE
}

def pygame_get_event_params(event_type, event):
    if event_type in [BRK_KEYDOWN, BRK_KEYUP]:
        return {
            'key': event.key,
            'mod': event.mod
        }
    elif event_type == BRK_MOUSEMOVE:
        return {
            'rel': event.rel
        }
