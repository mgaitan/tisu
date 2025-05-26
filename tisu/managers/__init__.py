from abc import ABC, abstractmethod


class TrackerManager(ABC):
    def __init__(self, project_or_repo, auth, password):
        self.auth = auth
        self.password = password

    @abstractmethod
    def fetcher(self, state): ...

    @abstractmethod
    def sender(self, issues): ...
