from fife import fife

from fife.extensions.serializers.simplexml import SimpleXMLSerializer
from scripts.quests.baseQuest import Quest, ReturnItemQuest, QuestTypes
from scripts.misc.serializer import Serializer

class QuestManager(Serializer):
    def __init__(self, gameplay):
        self._gameplay = gameplay
        
        self._questSettings = None
        
        self._quests = []
        self._activeQuests = []
        self._completedQuests = []
    
    def serialize(self):
        pass
    
    def deserialize(self, valueDict):
        questFile = "maps/quests.xml"
        
        self._questSettings = SimpleXMLSerializer(questFile)
        
        for identifier in self._questSettings.get("QuestGivers", "list", []):
            for quest in self._questSettings.get(identifier, "questList", []):
                questDict = self._questSettings.get(identifier, quest, [])
                if questDict["type"] == 'RETURN_ITEM':
                    questObj = ReturnItemQuest(identifier, quest, questDict["name"], questDict["desc"])
                    for ritem in self._questSettings.get(quest + "_items", "itemlist", []):
                        itemDict = self._questSettings.get(quest + "_items", ritem, [])
                        if itemDict["name"] == "GOLD_COINS":
                            questObj.addRequiredGold(itemDict["value"])
                        else:
                            questObj.addRequiredItem(ritem)
                else:
                    questObj = Quest(identifier, quest, questDict["name"], questDict["desc"])
                
                if questDict.has_key("quest_incomplete_dialog"):
                    questObj._incompleteDialog = questDict["quest_incomplete_dialog"]
                
                if questDict.has_key("quest_complete_dialog"):
                    questObj._completeDialog = questDict["quest_complete_dialog"]
                
                self._gameplay.questManager.addQuest(questObj)
    
    def reset(self):
        self._quests = []
        self._activeQuests = []
        self._completedQuests = []
    
    def addQuest(self, quest):
        if self._quests.has_key(quest.ownerId):
            if not quest in self._quests[quest.ownerId]:
                self._quests[quest.ownerId].append(quest)
        else:
            self._quests[quest.ownerId] = [quest]
    
    def getQuest(self, questId):
        for owner in self._quests:
            for quest in self._quests[owner]:
                if quest.id == questId:
                    return quest
        return None
    
    def getNextQuest(self, ownerId):
        if self._quests.has_key(ownerId):
            for quest in self._quests[ownerId]:
                if not quest in self._activeQuests and not quest in self._completedQuests:
                    return quest
        return None

    def activateQuest(self, quest):
        if not quest in self._activeQuests:
            self._activeQuests.append(quest)
    
    def completeQuest(self, quest):
        if not quest in self._completedQuests:
            self._completedQuests.append(quest)
        
        if quest in self._activeQuests:
            self._activeQuests.remove(quest)
    
    def activateQuestById(self, questId):
        quest = self.getQuest(questId)
        if quest:
            self.activateQuest(quest)
    
    def completeQuestById(self, questId):
        quest = self.getQuest(questId)
        if quest:
            self.completeQuest(quest)
    
    def _getActiveQuests(self):
        return self._activeQuests
    
    def _getCompletedQuests(self):
        return self._completedQuests
    
    def _getAllQuests(self):
        return self._quests
    
    activeQuests = property(_getActiveQuests)
    completedQuests = property(_getCompletedQuests)
    quests = property(_getAllQuests)