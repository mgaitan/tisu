from .models import Issue, Metadata
from github import Github, GithubException, GithubObject


class GithubManager(object):

    def __init__(self, repo, login_or_token=None, password=None):
        self.g = Github(login_or_token, password)
        self.repo = self.g.get_repo(repo)

    def fetcher(self, state):
        issues = []
        for issue in self.repo.get_issues(state=state):
            meta = Metadata()
            if issue.state != 'open':
                # assume state open
                meta['state'] = issue.state
            if issue.milestone:
                meta['milestone'] = issue.milestone.title
            if issue.labels:
                meta['labels'] = [l.name for l in issue.labels]
            if issue.assignee:
                meta['assignee'] = issue.assignee.login
            issues.append(Issue(title=issue.title,
                                body=issue.body,
                                number=issue.number,
                                metadata=meta))
        return issues

    def get_milestone(self, title):
        """
        given the title as str, looks for an existing milestone or create a new one,
        and return the object
        """
        if not title:
            return GithubObject.NotSet
        if not hasattr(self, '_milestones'):
            self._milestones = {m.title: m for m in self.repo.get_milestones()}

        milestone = self._milestones.get(title)
        if not milestone:
            milestone = self.repo.create_milestone(title=title)
        return milestone

    def get_assignee(self, login):
        """
        given the user login, looks for a user in assignee list of the repo
        and return it if was found.
        """
        if not login:
            return GithubObject.NotSet
        if not hasattr(self, '_assignees'):
            self._assignees = {c.login: c for c in self.repo.get_assignees()}
        if login not in self._assignees:
            # warning
            print("{} doesn't belong to this repo. This issue won't be assigned.".format(login))
        return self._assignees.get(login)

    def get_state(self, state):
        if not state:
            return 'open'
        if state not in ('open', 'closed'):
            print("{} isn't a valid state (i.e: open or closed)".format(state))
            return 'open'
        return state

    def sender(self, issues):
        """
        push a list of issues to github
        """

        for issue in issues:
            state = self.get_state(issue.state)
            if issue.number:
                try:
                    gh_issue = self.repo.get_issue(issue.number)
                    original_state = gh_issue.state
                    if original_state == state:
                        action = 'Updated'
                    elif original_state == 'closed':
                        action = 'Reopened'
                    else:
                        action = 'Closed'

                    gh_issue.edit(title=issue.title,
                                  body=issue.body,
                                  labels=issue.labels,
                                  milestone=self.get_milestone(issue.milestone),
                                  assignee=self.get_assignee(issue.assignee),
                                  state=self.get_state(issue.state)
                                  )
                    print('{} #{}: {}'.format(action, gh_issue.number, gh_issue.title))
                except GithubException:
                    print('Not found #{}: {} (ignored)'.format(issue.number, issue.title))
                    continue
            else:
                gh_issue = self.repo.create_issue(title=issue.title,
                                                  body=issue.body,
                                                  labels=issue.labels,
                                                  milestone=self.get_milestone(issue.milestone),
                                                  assignee=self.get_assignee(issue.assignee))
                print('Created #{}: {}'.format(gh_issue.number, gh_issue.title))





