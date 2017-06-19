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
