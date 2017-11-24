class Experience(object):

    def __init__(self, title, description, id=None, picture=None):
        self._id = id
        self._title = title
        self._description = description
        self._picture = picture

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def picture(self):
        return self._picture

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
