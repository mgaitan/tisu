class Issue(object):

    def __init__(self, title, body, number=None, *kwargs):
        self.title = title
        self.body = body
        self.number = number

    def dump(self):
        if self.number:
            return "# {0.title} [#{0.number}]\n\n{0.body}\n\n".format(self)
        return "# {0.title}\n\n{0.body}\n\n".format(self)
