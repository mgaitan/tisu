from jira import JIRA

from ..models import Issue, Metadata
from . import TrackerManager


class JiraManager(TrackerManager):
    def __init__(self, project, server, login, token):
        super().__init__(project, login, token)
        self._jira = JIRA(server=server, basic_auth=(login, token))
        self.project = project

    def fetcher(self, state):
        jql = f'project = "{self.project}" AND status = "{state}"'
        for issue in self._jira.search_issues(jql):
            meta = Metadata()
            meta["parent"] = issue.fields.parent.key if hasattr(issue.fields, "parent") else None
            # labels & assignee & state …
            yield Issue(title=issue.fields.summary, body=issue.fields.description, number=issue.key, metadata=meta)

    def sender(self, issues):
        for issue in issues:
            if issue.number:
                jira_issue = self._jira.issue(issue.number)
                jira_issue.update(
                    summary=issue.title,
                    description=issue.body,
                    fields={
                        "labels": issue.labels,
                        "parent": {"key": issue.metadata.get("parent")},
                        "assignee": {"name": issue.assignee} if issue.assignee else None,
                        "issuetype": {"name": issue.metadata.get("issuetype", "Task")},
                    },
                )
            else:
                fields = {
                    "project": {"key": self.project},
                    "summary": issue.title,
                    "description": issue.body,
                    "issuetype": {"name": issue.metadata.get("issuetype", "Task")},
                }
                parent = issue.metadata.get("parent")
                if parent:
                    fields["parent"] = {"key": parent}
                new = self._jira.create_issue(fields=fields)
                print(f"Created {new.key}: {new.fields.summary}")
