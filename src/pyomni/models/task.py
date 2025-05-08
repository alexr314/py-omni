from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Task:
    id: str
    name: str
    note: Optional[str] = None
    flagged: bool = False
    completed: bool = False
    blocked: bool = False
    dropped: bool = False
    defer_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    dropped_date: Optional[datetime] = None
    in_inbox: bool = False
    estimated_minutes: Optional[int] = None
    tags: Optional[List[str]] = None
    container: Optional[str] = None  # Project name or 'Inbox'
