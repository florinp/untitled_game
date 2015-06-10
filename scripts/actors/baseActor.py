import sys, os, re, math, random, shutil

from fife import fife
from fife.extensions.loaders import loadMapFile

from scripts.objects.baseObject import ObjectActionListener, BaseGameObject, GameObjectTypes
from scripts.objects.items import GoldStack
from scripts.misc.serializer import Serializer

Actions = {
    "NONE": 0,
    "PICKUP": 1,
    "TALK": 2,
    "ATTACK": 3,
    "OPEN": 4,
    "ENTER": 5
}

class BaseAction(object):
    def __init__(self):
        self._actionType = Actions["NONE"]
    
    def execute(self):
        pass

class PickUpItemAction(BaseAction):
    def __init__(self, actor, item):
        self._actionType = Actions["PICKUP"]
        self._actor = actor
        self._item = item
    
    def execute(self):
        self._actor.pickUpItem(self._item)

class TalkAction(BaseAction):
    def __init__(self, sourceObject, destinationObject):
        self._actionType = Actions['TALK']
        self._source = sourceObject
        self._destination = destinationObject
    
    def execute(self):
        if self._destination.type == GameObjectTypes['QUESTGIVER']:
            if self._destination.haveQuest():
                if not self._destination.activeQuest:
                    self._destination.offerNextQuest()
                else:
                    self._destination.completeQuest()
            else:
                self._destination.showNoQuestDialog()
        else:
            self._destination.say("Hello World!")

class AttackAction(BaseAction):
    def __init__(self, attacker, defender):
        self._actionType = Actions['ATTACK']
        self._attacker = attacker
        self._defender = defender
    
    def execute(self):
        if self._defender.type == GameObjectTypes["ENEMY"]:
            self._defender.say("Ouch")

class EnterLocationAction(BaseAction):
    def __init__(self, actor, location):
        self._actionType = Actions['ENTER']
        self._actor = actor
        self._location = location
    
    def execute(self):
        self._actor.enterLocation(self._location)

ActorStates = {
    "STAND": 0,
    "WALK": 1,
    "ATTACK": 2
}

class ActorActionListener(ObjectActionListener):
    def __init__(self, gameplay, obj):
        super(ActorActionListener, self).__init__(gameplay, obj)
    
    def onInstanceActionFinished(self, instance, action):
        if action.getId() == "walk":
            self._object.stand()
            self._object.performNextAction()
    
    def onInstanceActionCancelled(self, instance, action):
        pass

class ActorAttributes(Serializer):
    def __init__(self, strength = 0, dexterity = 0, intelligence = 0, health = 0, walkSpeed = 0):
        self._str = strength
        self._dex = dexterity
        self._int = intelligence
        self._hp = health
        self._walkSpeed = walkSpeed
    
    def serialize(self):
        lvars = {}
        
        lvars["str"] = self._str
        lvars["dex"] = self._dex
        lvars["int"] = self._int
        lvars["hp"] = self._hp
        lvars["walkSpeed"] = self._walkSpeed
        
        return lvars
    
    def deserialize(self, valueDict):
        if valueDict.has_key("str"):
            self._str = valueDict["str"]
        if valueDict.has_key("dex"):
            self._dex = valueDict["dex"]
        if valueDict.has_key("int"):
            self._int = valueDict["int"]
        if valueDict.has_key("hp"):
            self._hp = valueDict["hp"]
        if valueDict.has_key("walkSpeed"):
            self._walkSpeed = valueDict["walkSpeed"]
    
    def _getStrength(self):
        return self._str

    def _setStrength(self, strength):
        self._str = strength

    def _getDexterity(self):
        return self._dexterity

    def _setDexterity(self, dexterity):
        self._dexterity = dexterity

    def _getIntelligence(self):
        return self._int

    def _setIntelligence(self, intelligence):
        self._int = intelligence

    def _getHealth(self):
        return self._hp

    def _setHealth(self, health):
        self._hp = health

    def _getWalkSpeed(self):
        return self._walkSpeed

    def _setWalkSpeed(self, walkSpeed):
        self._walkSpeed = walkSpeed

    strength = property(_getStrength, _setStrength)
    dexterity = property(_getDexterity, _setDexterity)
    intelligence = property(_getIntelligence, _setIntelligence)
    health = property(_getHealth, _setHealth)
    walkSpeed = property(_getWalkSpeed, _setWalkSpeed)

class Actor(BaseGameObject):
    def __init__(self, gameplay, layer, typeName, baseObjectName, instanceName, instanceId = None, createInstance = False):
        super(Actor, self).__init__(gameplay, layer, typeName, baseObjectName, instanceName, instanceId, createInstance)
        
        self._nextAction = None
        self._inventory = []
        self._maxInventoryItems = 20
        
        self._gold = 0
        self._attributes = ActorAttributes()
        
        self._attributes.walkSpeed = 4.0
        
        self.stand()
    
    def stand(self):
        self._state = ActorStates["STAND"]
        self._instance.actOnce('stand', self._instance.getFacingLocation())
    
    def walk(self, location):
        self._state = ActorStates["WALK"]
        self._instance.move("walk", location, self._attributes.walkSpeed)
    
    def say(self, text):
        self._instance.say(text, 2500)
    
    def performNextAction(self):
        if self._nextAction:
            self._nextAction.execute()
            self._nextAction = None
    
    def pickUpItem(self, item):
        if self.addItemToInventory(item):
            item.onPickUp()
        else:
            # @TODO: make something like throw item on the ground or execute another action
            pass
    
    def enterLocation(self, location):
        if self._id == "player":
            self._gameplay.switchMap(location.destination)
        else:
            self._gameplay.scene.removeObjectFromScene(self._id)
    
    def addItemToInventory(self, item):
        if len(self._inventory) >= self._maxInventoryItems:
            return False
        else:
            if type(item) == GoldStack:
                self._gold += item.value
            else:
                self._inventory.append(item)
        
        return True
    
    def removeItemFromInventory(self, itemId):
        itemToRemove = None
        for item in self._inventory:
            if item.id == itemId:
                itemToRemove = item
        
        if itemToRemove:
            self._inventory.remove(itemToRemove)
    
    def serialize(self):
        lvars = super(Actor, self).serialize()
        
        lvars["gold"] = self._gold
        
        attVars = self._attributes.serialize()
        for key,value in attVars.items():
            lvars[key] = value
        
        return lvars
    
    def deserialize(self, valueDict):
        super(Actor, self).deserialize(valueDict)
        
        if valueDict.has_key("gold"):
            self._gold = valueDict["gold"]
        else:
            self._gold = 0
        
        self._attributes.deserialize(valueDict)
    
    def _getState(self):
        return self._state
    
    def _setState(self, newState):
        self._state = newState
    
    def _getNextAction(self):
        return self._nextAction
    
    def _setNextAction(self, newAction):
        self._nextAction = newAction
    
    def _getGold(self):
        return self._gold
    
    def _setGold(self, newValue):
        self._gold = newValue
    
    def _getInventory(self):
        return self._inventory
    
    def _setInventory(self, newInventory):
        self._inventory = newInventory
    
    def _getAttributes(self):
        return self._attributes
    
    state = property(_getState, _setState)
    nextAction = property(_getNextAction, _setNextAction)
    gold = property(_getGold, _setGold)
    inventory = property(_getInventory, _setInventory)
    attributes = property(_getAttributes)