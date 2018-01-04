class Experience:

    def __init__(self, title, description, author_id,
                 author_username=None, id=None, picture=None, is_mine=False, is_saved=False):
        self._id = id
        self._title = title
        self._description = description
        self._picture = picture
        self._author_id = author_id
        self._author_username = author_username
        self._is_mine = is_mine
        self._is_saved = is_saved

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

    @property
    def is_mine(self):
        return self._is_mine

    @property
    def is_saved(self):
        return self._is_saved

    def builder(self):
        return Experience.Builder(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    class Builder:

        def __init__(self, experience):
            self._id = experience.id
            self._title = experience.title
            self._description = experience.description
            self._picture = experience.picture
            self._author_id = experience.author_id
            self._author_username = experience.author_username
            self._is_mine = experience.is_mine
            self._is_saved = experience.is_saved

        def id(self, id):
            self._id = id
            return self

        def title(self, title):
            self._title = title
            return self

        def description(self, description):
            self._description = description
            return self

        def picture(self, picture):
            self._picture = picture
            return self

        def author_id(self, author_id):
            self._author_id = author_id
            return self

        def author_username(self, author_username):
            self._author_username = author_username
            return self

        def is_mine(self, is_mine):
            self._is_mine = is_mine
            return self

        def is_saved(self, is_saved):
            self._is_saved = is_saved
            return self

        def build(self):
            return Experience(id=self._id, title=self._title, description=self._description,
                              picture=self._picture, author_id=self._author_id,
                              author_username=self._author_username, is_mine=self._is_mine,
                              is_saved=self._is_saved)
