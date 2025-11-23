import hashlib


class Article:

    def __init__(self, title, link, published_time):

        # main article info
        self.title = title
        self.link = link
        self.published_time = published_time

        # generate unique id
        self.id = int(hashlib.sha256((str(self.link) + str(self.published_time)).encode('utf-8')).hexdigest(), 16)

    def __str__(self):
        s = '\nid:' + str(self.id)
        s += '\ntitle:' + str(self.title)
        s += '\nlink:' + str(self.link)
        s += '\npublished_time:' + str(self.published_time)
        return s
