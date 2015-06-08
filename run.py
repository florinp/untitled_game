import os, sys

# import FIFE main module
from fife import fife

# import FIFE Setting extension
from fife.extensions.fife_settings import Setting

# import Game class
from scripts.game import Game

# import mainMenu class
from scripts.gui.mainMenu import MainMenu

import tmxlib

settings = Setting(app_name='untitled_game', settings_file='./settings.xml', settings_gui_xml="")    
 
def main():
    app = Game(settings)
        
    app.run()
    
    
if __name__ == '__main__':
    main()