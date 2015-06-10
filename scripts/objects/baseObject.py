import sys, os, re, math, random, shutil

from fife import fife
from fife.extensions.loaders import loadMapFile

from scripts.misc.exceptions import *
from scripts.misc.serializer import Serializer

GameObjectTypes = {
    "DEFAULT": 0,
    "ITEM": 1,
    "QUESTGIVER": 2,
    "PLAYER": 3,
    "NPC": 4,
    "ENEMY": 5,
    "GOLD": 6,
    "PORTAL": 7,
}

class ObjectActionListener(fife.InstanceActionListener):
    def __init__(self, gameplay, obj):
        fife.InstanceActionListener.__init__(self)
        self._gameplay = gameplay
        self._object = obj
        
        self._attached = False
    
    def detachActionListener(self):
        if self._attached:
            self._object.instance.removeActionListener(self)
            self._attached = False
    
    def attachActionListener(self):
        if not self._attached:
            self._object.instance.addActionListener(self)
            self._attached = True
    
    def onInstanceActionFinished(self, instance, action):
        pass
    
    def onInstanceActionCancelled(self, instance, action):
        pass
    
    def onInstanceActionFrame(self, instance, action, frame):
        pass

class BaseGameObject(Serializer):
    def __init(self, gameplay, layer, typeName, baseObjectName, instanceName, instanceId = None, createInstance = False):
        self._gameplay = gameplay
        self._fifeObject = None
        
        self._typeName = typeName
        self._type = GameObjectTypes[typeName]
        self._baseObjectName = baseObjectName
        
        self._name = instanceName
        if instanceId:
            self._id = instanceId
        else:
            self._id = self._name
            
        self._instance = None
        self._position = fife.DoublePoint(0.0, 0.0)
        
        self._actionListener = None
        
        self._layer = layer
        
        if createInstance:
            self._createFifeInstance(self._layer)
        else:
            self._findFifeInstance(self._layer)
            
        self._activated = True
        
    def hide(self):
        if self._instance:
            self._instance.get2dGfxVisual().setVisible(False)
    
    def show(self):
        if self._instance:
            self._instance.get2dGfxVisual().setVisible(True)
    
    def destroy(self):
        if self._actionListener:
            self._actionListener.detachActionListener(self)
            
        if self._instance:
            self._layer.deleteInstance(self._instance)
            self._instance = None
        
        self._activated = False
    
    def spawn(self, x, y):
        if self._instance:
            self._setMapPosition(x, y)
            self.show()
        else:
            self._position.x = x
            self._position.y = y
            self._createFifeInstance(self, self._layer)
        
        if self._actionListener and self._instance:
            self._actionListener.attachActionListener()
            
        self._activated = True

    def setMapPosition(self, x, y):
        currentLoc = self.location
        
        self._position = self.location.getExactLayerCoordinates()
        self._position.x = x
        self._position.y = y
        
        currentLoc.setExactLayerCoordinates(self._position)
        self.location = currentLoc
        
    def serialize(self):
        lvars = {}
        (x,y) = self.position
        lvars['posx'] = x
        lvars['posy'] = y
        lvars['type'] = self._typeName
        lvars['objectName'] = self._baseObjectName
        
        return lvars
    
    def deserialize(self, valueDict = None):
        if not valueDict:
            return
        
        if valueDict.has_key('posx'):
            x = float(valueDict['posx'])
        else:
            x = 0
            
        if valueDict.has_key('posy'):
            y = float(valueDict['posy'])
        else:
            y = 0
            
        self.setMapPosition(x, y)
    
    def _createFifeInstance(self, layer):
        mapModel = self._gameplay.engine.getModel()
        self._fifeObject = mapModel.getObject(self._name, self._gameplay.settings.get("RPG", "ObjectNamespace", "http://www.fifengine.net/xml/rpg"))
        
        self._instance = layer.createInstance(self._fifeObject, fife.ExactModelCoordinate(self._position.x, self._position.y), self._id)
        fife.InstanceVisual.create(self._instance)
        
        self._instance.thisown = 0
    
    def _findFifeInstance(self, layer):
        self._instance = self._layer.getInstance(self._id)
        if self._instance:
            self._instance.thisown = 0
        else:
            raise InstanceNotFoundError(self._id + " not found on layer")
        
    def _getLocation(self):
        return self._instance.getLocation()
    
    def _setLocation(self, location):
        self._instance.setLocation(location)
    
    def _getInstance(self):
        return self._instance
    
    def _getType(self):
        return self._type
    
    def _getId(self):
        return self._id
    
    def _getModelName(self):
        return self._name
    
    def _getPosition(self):
        if self._instance:
            self._position = self.location.getExactLayerCoordinates()
        
        return (self._position.x, self._position.y)
    
    def _setPosition(self, tuplexy):
        self.setMapPosition(tuplexy[0], tuplexy[1])
        
    def _getActivated(self):
        return self._activated
    
    def _setActivated(self, activate):
        self._activated = activate

    location = property(_getLocation, _setLocation)
    instance = property(_getInstance)
    type = property(_getType)
    id = property(_getId)
    modelName = property(_getModelName)
    position = property(_getPosition, _setPosition)
    active = property(_getActivated, _setActivated)