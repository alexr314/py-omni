from dataclasses import dataclass, field, fields
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
    children: List["Task"] = field(default_factory=list)

    def __repr__(self):
        """Compact representation with non-None fields."""
        attrs = [f"id={self.id!r}", f"name={self.name!r}"]
        for f in fields(self):
            if f.name in {"id", "name"}:
                continue
            value = getattr(self, f.name)
            if value not in (None, [], False):  # omit falsy except True
                attrs.append(f"{f.name}={value!r}")
        return f"Task({', '.join(attrs)})"

    def __str__(self):
        """Friendly multiline summary for printing."""
        parts = [f"Task: {self.name} ({self.id})"]
        for f in fields(self):
            if f.name in {"id", "name"}:
                continue
            value = getattr(self, f.name)
            if value not in (None, [], False):
                parts.append(f"  {f.name}: {value}")
        return "\n".join(parts)