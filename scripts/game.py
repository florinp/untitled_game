import os, sys

# import FIFE main module
from fife import fife

# import the ApplicationBase
from fife.extensions.basicapplication import ApplicationBase

# import FIFE pychan module
from fife.extensions import pychan

# import scripts
from scripts import gameplay
from scripts.common import eventListenerBase

class GameListener(eventListenerBase.EventListenerBase):
    def __init__(self, engine, gameplay):
        super(GameListener, self).__init__(engine, regKeys=True, regCmd=True, regMouse=False, regConsole=True, regWidget=True)
        self._engine = engine
        self._gameplay = gameplay
        self._quit = False
        
    def keyPressed(self, event):
        keyval = event.getKey().getValue()
        keystr = event.getKey().getAsString().lower()
        consumed = False
        if keyval == fife.Key.ESCAPE:
            self._gameplay.showMainMenu()
            event.consume()
            
    def onCommand(self, command):
        self._quit = (command.getCommandType() == fife.CMD_QUIT_GAME)
        if self._quit:
            command.consume()

class Game(ApplicationBase):
    """
    The main application. Inherit the fife.extensions.ApplicationBase    
    """
    def __init__(self, settings):
        super(Game, self).__init__(settings)
        
        self._gameplay = gameplay.Gameplay(self, self.engine, self._setting)
        self._listener = GameListener(self.engine, self._gameplay)
    
    def requestQuit(self):
        cmd = fife.Command()
        cmd.setSource(None)
        cmd.setCommandType(fife.CMD_QUIT_GAME)
        self.engine.getEventManager().dispatchCommand(cmd)
    
    def createListener(self):
        pass # already created in construct
           
    def _pump(self):
        if self._listener._quit:
            self.breakRequested = True   
        else:
            self._gameplay.pump()
   