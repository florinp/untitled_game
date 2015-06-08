# import FIFE main module
from fife import fife

import copy
import math, random

# import FIFE extensions
from fife.extensions import pychan
from fife.extensions.pychan import widgets
from fife.extensions.soundmanager import SoundManager

# import Common modules
from scripts.common.eventListenerBase import EventListenerBase

# import GUI modules
from scripts.gui.mainMenu import *

class Gameplay(EventListenerBase):
    def __init__(self, app, engine, setting):
        super(Gameplay, self).__init__(engine, regKeys=True)
        
        self._application = app
        self._engine = engine
        self._setting = setting
        self._timeManager = engine.getTimeManager()
        self._eventManager = engine.getEventManager()
        self._model = engine.getModel()
        
        self._fileName = ''
        self._keyState = {} # todo: add default key state
        
        self._pump_ctr = 0
        self._map = None
        self._scene = None
        self._paused = True
        self._pausedTime = 0
        self._startTime = 0
        
        self._soundManager = SoundManager(self._engine)
        
        self._mainMenu = MainMenu(self, self._setting)
        self.showMainMenu()
        
        self._creditsDisplay = CreditsDisplay(self)
        self._creditsDisplay.hide()
    
    def showMainMenu(self):
        if self._scene:
            self._paused = True
            cont = True
        else:
            cont = False
            
        self._mainMenu.show(cont)
    
    def showCredits(self):
        self._creditsDisplay.show()
    
    def pump(self):
        
        if not self._scene:
            return
        
    def quit(self):
        self._application.requestQuit()
    