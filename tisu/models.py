
class Metadata(dict):

    def dump(self):
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
        self.metadata = metadata

    def dump(self):
        if self.number:
            return "# {0.title} [#{0.number}]\n\n{0.body}\n\n".format(self)
        return "# {0.title}\n\n{0.body}\n\n".format(self)
