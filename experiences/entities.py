class Experience(object):

    def __init__(self, id=None, title=None, description=None, picture=None):
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


class Picture(object):

    def __init__(self, small=None, medium=None, large=None):
        self._small = small
        self._medium = medium
        self._large = large

    @property
    def small(self):
        return self._small

    @property
    def medium(self):
        return self._medium

    @property
    def large(self):
        return self._large
