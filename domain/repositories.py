from abc import ABC, abstractmethod
from domain.issue import Issue

class AbstractIssueRepository(ABC):
    """
    Bu bir sözleşmedir (Interface).
    Veritabanımız MySQL de olsa, MongoDB de olsa bu kurallara uymak zorundadır.
    """
    
    @abstractmethod
    def save(self, issue: Issue) -> Issue:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        pass

    @abstractmethod
    def get_by_id(self, issue_id: str) -> Issue | None:
        pass

    @abstractmethod
    def update(self, issue_id: str, update_data: dict) -> Issue | None:
        pass

    @abstractmethod
    def delete(self, issue_id: str) -> bool:
        pass

    @abstractmethod
    def get_issues_by_assignee(self, user_id: str, skip: int = 0, limit: int = 100, status: str | None = None, search_query: str | None = None, sort_by: str = "created_at", sort_order: str = "desc") -> list[Issue]:
        pass