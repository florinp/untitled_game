import sys, os, re, math, random, shutil
from datetime import datetime

from fife import fife

QuestTypes = {
    'DEFAULT': 0,
    'RETURN_ITEM': 1
}

class Quest(object):
    def __init__(self, ownerId, questId, questTitle, questText):
        self._ownerId = ownerId
        self._questId = questId
        self._title = questTitle
        self._text = questText
        
        self._completeDialog = "Complete"
        self._incompleteDialog = "Incomplete"
    
    def __eq__(self, other):
        return self._questId == other.id
    
    def checkQuestCompleted(self, actor):
        pass
    
    def _getOwnerId(self):
        return self._ownerId
    
    def _getTitle(self):
        return self._title
    
    def _setTitle(self, title):
        self._title = title
    
    def _getText(self):
        return self._text
    
    def _setText(self, text):
        self._text = text
    
    def _getId(self):
        return self._questId
    
    ownerId = property(_getOwnerId)
    title = property(_getTitle, _setTitle)
    text = property(_getText, _setText)
    id = property(_getId)

class ReturnItemQuest(Quest):
    def __init__(self, ownerId, questId, questTitle, questText):
        super(ReturnItemQuest, self).__init__(ownerId, questId, questTitle, questText)
        
        self._requiredItems = []
        self._requiredGold = 0
    
    def addRequiredItem(self, itemId):
        self._requiredItems.append(itemId)
    
    def addRequiredGold(self, goldCount):
        self._requiredGold += goldCount
    
    def checkQuestCompleted(self, actor):
        completed = False
        
        if self._requiredGold > 0:
            if actor.gold >= self._requiredGold:
                completed = True
        
        for itemId in self._requiredItems:
            if item in actor.inventory:
                completed = True
        
        return completed
    
    def _getRequiredGold(self):
        return self._requiredGold
    
    def _getRequiredItems(self):
        return self._requiredItems
    
    requiredGold = property(_getRequiredGold)
    requiredItems = property(_getRequiredItems)