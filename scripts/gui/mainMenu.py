import os

from fife import fife
from fife.extensions import pychan
from fife.extensions.pychan import widgets

from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

class MainMenu(object):
    def __init__(self, gameplay, setting):
        self._gameplay = gameplay
        self._setting = setting
        
        self._widget = pychan.loadXML("gui/mainMenu.xml")
        
        self._continue = self._widget.findChild(name="continue")
        self._newgame = self._widget.findChild(name="new_game")
        self._settings = self._widget.findChild(name="settings")
        self._credits = self._widget.findChild(name="credits")
        self._quit = self._widget.findChild(name="quit")
        
        self._widget.position = (0,0)
        
        eventMap = {
            'settings': self._setting.onOptionsPress,
            'credits': self._gameplay.showCredits,
            'quit': self._gameplay.quit,
        }
        
        self._widget.mapEvents(eventMap)
        
        self._continueMinWidth = self._continue.min_width
        self._continueMinHeight = self._continue.min_height
        self._continueMaxWidth = self._continue.max_width
        self._continueMaxHeight = self._continue.max_height
        
    def show(self, cont=False):
        if cont:
            self._continue.min_width = self._continueMinWidth
            self._continue.min_height = self._continueMinHeight
            self._continue.max_width = self._continueMaxWidth
            self._continue.max_height = self._continueMaxHeight
        else:
            self._continue.min_width = 0
            self._continue.min_height = 0
            self._continue.max_width = 0
            self._continue.max_height = 0
            
        self._continue.adaptLayout()
        self._widget.show()
        
    def hide(self):
        self._widget.hide()
    
    def isVisible(self):
        self._widget.isVisible()
        
class CreditsDisplay(object):
    def __init__(self, gameplay):
        self._gameplay = gameplay
        self._widget = pychan.loadXML('gui/credits.xml')
        
        eventMap = {
            'close': self.hide,
        }
        
        self._widget.mapEvents(eventMap)
        
    def show(self):
        self._widget.show()
        
    def hide(self):
        self._widget.hide()