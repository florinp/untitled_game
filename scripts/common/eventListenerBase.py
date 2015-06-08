from fife import fife
from fife.extensions import pychan
from fife.extensions.pychan.internal import get_manager

class EventListenerBase(fife.IKeyListener, fife.ICommandListener, fife.IMouseListener, fife.ConsoleExecuter):
    def __init__(self, engine, regKeys=False, regCmd=False, regMouse=False, regConsole=False, regWidget=False):
        self.eventmanager = engine.getEventManager()
        
        fife.IKeyListener.__init__(self)
        if regKeys:
            self.eventmanager.addKeyListener(self)
            
        fife.ICommandListener.__init__(self)
        if regCmd:
            self.eventmanager.addCommandListener(self)
            
        fife.IMouseListener.__init__(self)
        if regMouse:
            self.eventmanager.addMouseListener(self)
            
        fife.ConsoleExecuter.__init__(self)
        if regConsole:
            get_manager().getConsole().setConsoleExecuter(self)

    def mousePressed(self, event):
        pass
    def mouseReleased(self, event):
        pass
    def mouseEntered(self, event):
        pass
    def mouseExited(self, event):
        pass
    def mouseClicked(self, event):
        pass
    def mouseWheelUp(self, event):
        pass
    def mouseWheelDown(self, event):
        pass
    def mouseMoved(self, event):
        pass
    def mouseDragged(self, event):
        pass
    def keyPressed(self, event):
        pass
    def keyReleased(self, event):
        pass
    def onCommad(self, command):
        pass
    def onToolsClick(self, event):
        print "No tools set up yet!"
    def onConsoleCommand(self, command):
        pass
    def onWidgetAction(self, event):
        pass
