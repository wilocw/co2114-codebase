"""ENGINE.PY
This contains the code for the base engine
"""

import pygame
import time
from datetime import datetime
from collections.abc import *

if __name__ == "__main__":
    from agent import colors
    COLOR_BLACK, COLOR_WHITE = colors.COLOR_BLACK, colors.COLOR_WHITE
else:
    from .colors import COLOR_BLACK, COLOR_WHITE

## GLOBALS
DEFAULT_FPS:int = 30  # Render frames per second
DEFAULT_LPS:int = 2   # Environment steps per second

class BaseEngine:
    size = width, height = 600, 400
    def __init__(self):
        print(f"Creating instance of {self.name}")
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(f"{self.name} (co2114)")
        self._font = pygame.font.SysFont(None, 28)  # Default system font
        self._running:bool = True
    @property
    def name(self) -> str:
        return self.__class__.__name__
    @property
    def isrunning(self) -> bool:
        return self._running
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def cleanup(self):
        print(f"Quiting {self.name}")
        pygame.quit()
    def run(self, *render_sequence):
        while (self.isrunning):
            for event in pygame.event.get():
                self.on_event(event)
            for fcn in render_sequence:
                fcn()
        self.cleanup()

class Engine(BaseEngine):
    """Engine"""
    def __init__(self, fps:int=DEFAULT_FPS, lps:int=DEFAULT_LPS, dims=None):
        if dims and isinstance(dims, Iterable) and len(dims)==2:
            self.size = self.width, self.height = dims
        super().__init__()
        self._framerate:int = fps if isinstance(fps, int) else DEFAULT_FPS
        self._looprate:int = lps if isinstance(lps, int) else DEFAULT_LPS
        self._t0, self._l0 = time.time(), time.time()  # timing count
    def _update(self):
        """ Processing loop internals """
        # frame limiter
        if self._framerate is None or not isinstance(self._framerate, int):
            self._framerate = DEFAULT_FPS  # corrective measures
        mspf = (1000/self._framerate)  # ms per frame
        if (time.time() - self._t0) < mspf:  # if faster than framerate
            time.sleep((mspf - (time.time()-self._t0))/1000)  # sleep
        self._t0 = time.time()  # update timer
        # main render loop
        if self._looprate is None or not isinstance(self._looprate, int):
            self._looprate = DEFAULT_LPS  # corrective measures
        spf = 1/self._looprate  # s per frame
        if(time.time() - self._l0) > spf:  # if enough time passed
            self._l0 = time.time()  # update timer
            self.update()  # run main process update
    def _render(self):
        """ Render loop internals """
        self.screen.fill(COLOR_BLACK)  # write black to buffer
        self.render()  # run main render loop
        pygame.display.flip()  # flip buffer
    def update(self):
        NotImplemented
    def render(self):
        NotImplemented
    def run(self):
        super().run(self._update, self._render)


class App(Engine):
    @classmethod
    def run_default(App):
        app = App()
        app.run()


class EmptyApp(App):
    pass

#######################
class ClockApp(App):
    """ Example PyGame App """
    
    # size = width, height = 600, 400  # uncomment to override

    def __init__(self):
        super().__init__(fps=60, lps=60)
        self._font = pygame.font.SysFont(None, 128)  # override font
        self.t = datetime.now()

    def update(self):
        """ Main process loop
                Gets current system time
        """
        self.t = datetime.now()
    
    def render(self):
        """ Main render loop 
                Writes time to screen
        """
        renderTime = self._font.render(
            self.t.strftime("%H:%M:%S.%f")[:-5],
            True,
            COLOR_WHITE)
        rect = renderTime.get_rect()
        self.screen.blit(
            renderTime, 
            (self.width//2 - rect.width//2, 
             self.height//2 - rect.height//2))


####################################
if __name__ == "__main__":
    print("Running engine.py as script.")
    ClockApp.run_default()