class ClsCreater(object):
    def __init__(self, name = ''):
        self._members = []
        self._relevants = []
        self._mode = []
        self._name = name
        self._action = None     

    @property
    def name(self):
        return self._name

    @property
    def action(self):
        return self._action
    @action.setter
    def action(self, value):
        self._action = value

    @property
    def members(self):
        return self._members

    def bMember(self, val):
        return str(val) in self._members
    
    def pushMember(self, val):
        if str(val) not in self._members:
            self._members.append(str(val))

    @property
    def relevants(self):
        return self._relevants

    def pushRelevant(self, val):
        if str(val) not in self._relevants:
            self._relevants.append(str(val))

    @property
    def mode(self):
        return self._mode

    def setMode(self, valArr):
        self._mode = valArr         