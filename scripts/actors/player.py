import sys, os, re, math, random, shutil

from fife import fife
from scripts.actors.baseActor import Actor, ActorStates, ActorActionListener
from scripts.objects.baseObject import GameObjectTypes, BaseGameObject

class PlayerActionListener(ActorActionListener):
    def __init__(self, gameplay, obj):
        super(PlayerActionListener, self).__init__(gameplay, obj)
    
    def onInstanceActionFinished(self, instance, action):
        super(PlayerActionListener, self).onInstanceActionFinished(instance, action)
        if action.getId() == 'walk':
            pass
    
    def onInstanceActionCancelled(self, instance, action):
        pass
    
class Player(Action):
    def __init__(self, gameplay, layer, playerModelName):
        super(Player, self).__init__(gameplay, layer, "PLAYER", "player", playerModelName, "player", True)
        
        self._actionListener = PlayerActionListener(self._gameplay, self)
        self._actionListener.attachActionListener()
        
        self._quests = []
    
    def serialize(self):
        lvars = super(Player, self).serialize()
        
        activeQuests = ""
        
        for quest in self._gameplay.questManager.activeQuests:
            if activeQuests == "":
                activeQuests = quest.id
            else:
                activeQuests = activeQuests + "," + quest.id
        
        lvars["activeQuests"] = activeQuests
        
        completedQuests = ""
        
        for quest in self._gameplay.questManager.completedQuests:
            if completedQuests == "":
                completedQuests = quest.id
            else:
                completedQuests = completedQuests + "," + quest.id
        
        lvars["completedQuests"] = completedQuests
        
        return lvars
    
    def deserialize(self, valueDict):
        super(Player, self).deserialize(valueDict)
        
        activeQuests = valueDict["activeQuests"].split(",")
        for questId in activeQuests:
            self._gameplay.questManager.activateQuestById(questId)
        
        completedQuests = valueDict["completedQuests"].split(",")
        for questId in completedQuests:
            self._gameplay._questManager.completeQuestById(questId)