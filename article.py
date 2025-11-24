import hashlib


class Article:

    def __init__(self, title, link, published_time):

        # main article info
        self.title = title
        self.link = link
        self.published_time = published_time

        # generate unique id
        self.id = int(hashlib.sha256((str(self.link) + str(self.published_time)).encode('utf-8')).hexdigest(), 16)

        # info loading in progress
        self.origin_text = None
        self.vector = None
        self.rewrite_text = None

    def set_origin_text(self, origin_text):
        self.origin_text = origin_text

    def set_vector(self, vector):
        self.vector = vector

    def set_rewrite_text(self, rewrite_text):
        self.rewrite_text = rewrite_text

    def __str__(self):
        s = '\nid:' + str(self.id)
        s += '\ntitle:' + str(self.title)
        s += '\nlink:' + str(self.link)
        s += '\npublished_time:' + str(self.published_time)
        s += '\norigin_text:' + str(self.origin_text)
        s += '\nvector:' + str(self.vector[:5])
        s += '\nrewrite_text:' + str(self.rewrite_text)
        return s
