class Scene(object):

    def __init__(self, id=None, title=None, description=None, picture=None,
                 latitude=None, longitude=None, experience_id=None):
        self._id = id
        self._title = title
        self._description = description
        self._picture = picture
        self._latitude = latitude
        self._longitude = longitude
        self._experience_id = experience_id

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

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def experience_id(self):
        return self._experience_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
