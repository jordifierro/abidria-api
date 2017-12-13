class Experience(object):

    def __init__(self, title, description, author_id, author_username=None, id=None, picture=None):
        self._id = id
        self._title = title
        self._description = description
        self._picture = picture
        self._author_id = author_id
        self._author_username = author_username

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
    def author_id(self):
        return self._author_id

    @property
    def author_username(self):
        return self._author_username

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
