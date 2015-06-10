class GameException(Exception):
    def __init__(self, msg = None):
        if msg:
            self._msg = msg
        else:
            self._msg = None

class InvalidCommandError(GameException):
    def __init__(self, msg = None):
        super(InvalidCommandError, self).__init__(msg)
    
    def __str__(self):
        if self._msg:
            return repr(self._msg)
        else:
            return repr("Command not found!")

class ObjectNotFoundError(GameException):
    def __init__(self, msg = None):
        super(ObjectNotFoundError, self).__init__(msg)
    
    def __str_(self):
        if self._msg:
            return repr(self._msg)
        else:
            return repr("Object not found!")

class ObjectAlreadyInSceneError(RPGDemoException):
	def __init__(self, msg=None):
		super(ObjectAlreadyInSceneError, self).__init__(msg)
		
	def __str__(self):
		if self._msg:
			return repr(self._msg)
		else:
			return repr("Object already part of the scene!")

class InstanceNotFoundError(RPGDemoException):
	def __init__(self, msg=None):
		super(InstanceNotFoundError, self).__init__(msg)
		
	def __str__(self):
		if self._msg:
			return repr(self._msg)
		else:
			return repr("Instance not found on layer!")