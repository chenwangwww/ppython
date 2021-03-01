class NeureCtr:
    def __init__(self, content_label):
        self._uuid = content_label
        self._relevants = {}

    @property
    def uuid(self):
        return self._uuid

    @property
    def relevants(self):
        return self._relevants
    @relevants.setter
    def relevants(self, value):
        if value[0] not in self._relevants:
            self._relevants[value[0]] = [value[1]]
        else:
            info = self._relevants[value[0]]
            info.append(value[1])