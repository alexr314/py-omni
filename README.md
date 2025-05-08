# pyomni

**pyomni** is a Python library for programmatically controlling OmniFocus on macOS using AppleScript under the hood. It provides a high-level API for listing, creating, updating, completing, and deleting tasks and projects.

This tool is ideal for scripting workflows, integrating with AI agents, or building custom productivity tools that interact with your OmniFocus database.

---

## 🚀 Features

- List tasks from any project, including Inbox
- Access full metadata (due dates, defer dates, tags, notes, etc.)
- Support for hierarchical subtasks (`children`)
- Create tasks in Inbox or nested project folders
- Complete tasks (with special handling for inbox tasks)
- Set due dates
- Update task name, note, and flag status
- Delete tasks by ID

---

## 📦 Installation

This package is designed for **macOS** with OmniFocus installed.

1. Clone the repo:
```bash
git clone https://github.com/yourusername/pyomni.git
cd pyomni

2. Create a virtual environment:
python3 -m venv pyomni-env
source pyomni-env/bin/activate

3. Install dependencies:
pip install -r requirements.txt

## Basic Usage

```python
from pyomni.client import OmniFocusClient
from datetime import datetime

client = OmniFocusClient()

# List tasks in a nested project
tasks = client.list_tasks("Work > Projects > AI Research")
for task in tasks:
    print(task.name, task.due_date)

# Create a task
client.create_task("Draft proposal", project_path="Work > Projects > AI Research", flagged=True)

# Complete a task
client.complete_task(task_id)

# Set due date
client.set_due_date(task_id, datetime(2025, 5, 10, 17, 0))

# Update task
client.update_task(task_id, note="Final version sent", flagged=False)

# Delete task
client.delete_task(task_id)
```

## 📁 Folder and Project Paths

Project and folder paths are specified using > to indicate hierarchy. For example:
"Inbox" — targets the inbox
"Work > Projects > AI Research" — nested project in folders

## Testing

Run all tests with
`PYTHONPATH=src pytest`
All integration tests are live and interact with OmniFocus. Make sure OmniFocus is open and not in a syncing state.

## Known Limitations

Inbox task completion: AppleScript does not allow directly marking inbox tasks complete. As a workaround, pyomni moves them into a hidden project called CompletedInboxTasks and marks them complete.
No full support for defer dates yet (stub included).
OmniFocus must be installed and accessible from `osascript`.

## 🤖 Why?

This project was built to enable LLM agents and structured automation to control OmniFocus with reliable APIs and readable structure. It’s part of a broader system for intelligent task management.