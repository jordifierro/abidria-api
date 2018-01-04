class Picture:

    def __init__(self, small_url, medium_url, large_url):
        self._small_url = small_url
        self._medium_url = medium_url
        self._large_url = large_url

    @property
    def small_url(self):
        return self._small_url

    @property
    def medium_url(self):
        return self._medium_url

    @property
    def large_url(self):
        return self._large_url
