import sys, os, re, math, random, shutil

from fife import fife

from scripts.objects.baseObject import BaseGameObject, GameObjectTypes

class BaseItem(BaseGameObject):
    def __int__(self, gameplay, layer, typeName, baseObjectName, itemType, itemName):
        super(BaseItem, self).__init__(gameplay, layer, typeName, baseObjectName, itemType, itemName, True)
    
    def _getItemType(self):
        return self._name
    
    def _getItemName(self):
        return self._id
    
    itemType = property(_getItemType)
    itemName = property(_getItemName)

class PickableItem(BaseItem):
    def __init__(self, gameplay, layer, typeName, baseObjectName, itemType, itemName):
        super(PickableItem, self).__init__(gameplay, layer, typeName, baseObjectName, itemType, itemName)
        self._type = GameObjectTypes['ITEM']
    
    def onPickUp(self):
        self._gameplay.scene.removeObjectFromScene(self)
    
    def onDrop(self, dropX, dropY):
        self._createFifeInstance(self, self._gameplay.scene.itemLayer)
        self.setMapPosition(dropX, dropY)
        
        self._gameplay.scene.addObjectToScene(self)

class GoldStack(PickableItem):
    def __init__(self, gameplay, layer, typeName, baseObjectName, itemType, itemName):
        super(GoldStack, self).__init__(gameplay, layer, typeName, baseObjectName, itemType, itemName)
        
        self._value = 0
    
    def serialize(self):
        lvars = super(GoldStack, self).serialize()
        lvars['value'] = self._value
        
        return lvars
    
    def deserialize(self, valueDict):
        super(GoldStack, self).deserialize(valueDict)
        
        if valueDict.has_key('value'):
            self._value = int(valueDict['value'])
        else:
            self._value = 0
    
    def _getValue(self):
        return self._value
    
    def _setValue(self, newValue):
        self._value = int(newValue)
    
    value = property(_getValue, _setValue)

class Portal(BaseItem):
    def __init__(self, gameplay, layer, typeName, baseObjectName, itemType, itemName):
        super(Portal, self).__init__(gameplay, layer, typeName, baseObjectName, itemType, itemName)
        self._type = GameObjectTypes['PORTAL']
        
        self._destination = None
    
    def serialize(self):
        lvars = super(Portal, self).serialize()
        lvars['destination'] = self._destination
        
        return lvars
    
    def deserialize(self, valueDict):
        super(Portal, self).deserialize(valueDict)
        
        if valueDict.has_key('destination'):
            self._destination = valueDict['destination']
        else:
            self._destination = "town"
    
    def _getDestination(self):
        return self._destination
    
    def _setDestination(self, newDestination):
        self._destination = destination
    
    destination = property(_getDestination, _setDestination)