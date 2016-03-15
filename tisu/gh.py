from .models import Issue
from github import Github, GithubException


class GithubManager(object):

    def __init__(self, repo, login_or_token=None, password=None):
        self.g = Github(login_or_token, password)
        self.repo = self.g.get_repo(repo)

    def fetcher(self, state):
        issues = []
        for issue in self.repo.get_issues(state=state):
            issues.append(Issue(issue.title, issue.body, issue.number))
        return issues

    def sender(self, issues):
        for issue in issues:
            if issue.number:
                try:
                    self.repo.get_issue(issue.number).edit(title=issue.title, body=issue.body)
                    print('Updated #{}: {}'.format(issue.number, issue.title))
                except GithubException:
                    print('Not found #{}: {} (ignored)'.format(issue.number, issue.title))
            else:
                gh_issue = self.repo.create_issue(title=issue.title, body=issue.body)
                print('Created #{}: {}'.format(gh_issue.number, gh_issue.title))



