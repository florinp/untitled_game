import sys, os, re, math, random, shutil

from fife import fife
from scripts.objects.baseObject import BaseGameObject, GameObjectTypes
from scripts.actors.baseActor import Actor

class QuestGiver(Actor):
    def __init__(self, gameplay, layer, typeName, baseObjectName, instanceName, instanceId = None, createInstance = False):
        super(QuestGiver, self).__init__(gameplay, layer, typeName, baseObjectName, instanceName, instanceId, createInstance)
        self._type = GameObjectTypes["QUESTGIVER"]
        
        self._noQuestDialog = "Nothing"
        
    def offerNextQuest(self):
        if self._gameplay.questManager.getNextQuest(self.id):
            self._gameplay.guiController.showQuestDialog(self)
    
    def getNextQuest(self):
        return self._gameplay.questManager.getNextQuest(self.id)
    
    def activateQuest(self, quest):
        return self._gameplay.questManager.activateQuest(quest)
    
    def completeQuest(self, quest):
        for activeQuest in self._gameplay.questManager.activeQuests:
            if activeQuest.ownerId == self.id:
                if activeQuest.checkQuestCompleted(self._gameplay.scene.player):
                    self.say(activeQuest._completeDialog)
                    
                    self._gameplay.scene.player.gold = self._gameplay.scene.player.gold - activeQuest.requiredGold
                    
                    for itemId in activeQuest.requiredItems:
                        self._gameplay.scene.player.removeItemFromInventory(itemId)
                    
                    self._gameplay.questManager.completeQuest(activeQuest)
                else:
                    self.say(activeQuest._incompleteDialog)
    
    def haveQuest(self):
        return bool(self._gameplay.questManager.getNextQuest(self.id)) or bool(self._getActiveQuest())
    
    def serialize(self):
        lvars = super(QuestGiver, self).serialize()
        
        lvars["noQuestDialog"] = self._noQuestDialog
        
        return lvars
    
    def deserialize(self, valueDict):
        super(QuestGiver, self).deserialize(valueDict)
        self._noQuestDialog = valueDict["noQuestDialog"]
    
    def _getActiveQuest(self):
        for quest in self._gameplay.questManager.activeQuests:
            if quest.ownerId == self.id:
                return quest
    
    activeQuest = property(_getActiveQuest)