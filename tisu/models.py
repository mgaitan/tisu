
class Metadata(dict):

    def __str__(self):
        metadata = []
        for k, v in self.items():
            if isinstance(v, list):
                v = ', '.join(v)
            metadata.append(":{}: {}".format(k, v))
        return '\n'.join(metadata)


class Issue(object):
    def __init__(self, title, body, number=None, metadata=None, *kwargs):
        self.title = title
        self.body = body
        self.number = number
        self.metadata = metadata if metadata else Metadata()

    def __repr__(self):
        if self.number:
            return "<{0.__class__.__name__}: [#{0.number}] {0.title}>".format(self)
        return "<{0.__class__.__name__}: {0.title}>".format(self)

    def __str__(self):

        s = '\n\n'.join((v.strip() for v in (self.title,
                                             str(self.metadata),
                                             self.body) if v and v.strip()))
        if self.number:
            return "# [#{}] {}\n\n".format(self.number, s)
        return "# {}\n\n".format(s)

    @property
    def labels(self):
        return self.metadata.get('labels') or []

    @property
    def milestone(self):
        return self.metadata.get('milestone')

    @property
    def assignee(self):
        return self.metadata.get('assignee')

    @property
    def state(self):
        return self.metadata.get('state')
