from abc import ABC, abstractmethod
from typing import ContextManager, Dict, Any, Optional, List
from sqlalchemy.orm import Session

class BaseDatabase(ABC):
    """
    Base Class for Database Admin Operations
    """

    @abstractmethod
    def startup(self) -> None:
        """Initialize the Database Connection"""
    
    @abstractmethod
    def teardown(self) -> None:
        """Close the Database Connection"""
    
    @abstractmethod
    def get_session(self) -> ContextManager[Session]:
        """Get a Database Session"""

class BaseRepository(ABC):
    """
    Base Class defining Repository Pattern for Data Access
    """
    def __init__(self, session:Session):
        self.session = session
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        """ Create a New Record """
    
    @abstractmethod
    def delete(self, record_id: Any) -> bool:
        """ Delete an record by ID: record_id"""

    @abstractmethod
    def update(self, record_id:Any, data: Dict[str,Any])-> Optional[Any]:
        """ Update a record by ID: record_id and Data: data"""
    
    @abstractmethod
    def list(self, limit: int =100, offset: int = 0) -> List[Any]:
        """List Records with Pagination"""
    
    @abstractmethod
    def get_by_id(self, record_id: Any) -> Optional[Any]:
        """Get a record by ID."""
        
