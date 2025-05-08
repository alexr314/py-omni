# task_scripts.py
def build_task_query_applescript(task_selector: str) -> str:
    return f'''
    set taskList to {task_selector}
    set taskStrings to {{}}
    repeat with t in taskList
        set tagNames to name of every tag of t
        set tagString to tagNames as string
        set taskString to "{{" & ¬
            "id:\\"" & id of t & "\\", " & ¬
            "name:\\"" & name of t & "\\", " & ¬
            "note:\\"" & note of t & "\\", " & ¬
            "flagged:" & flagged of t & ", " & ¬
            "completed:" & completed of t & ", " & ¬
            "blocked:" & blocked of t & ", " & ¬
            "dropped:" & dropped of t & ", " & ¬
            "in_inbox:" & in inbox of t & ", " & ¬
            "defer_date:\\"" & defer date of t & "\\", " & ¬
            "due_date:\\"" & due date of t & "\\", " & ¬
            "creation_date:\\"" & creation date of t & "\\", " & ¬
            "modification_date:\\"" & modification date of t & "\\", " & ¬
            "completion_date:\\"" & completion date of t & "\\", " & ¬
            "dropped_date:\\"" & dropped date of t & "\\", " & ¬
            "estimated_minutes:" & estimated minutes of t & ", " & ¬
            "tags:\\"" & tagString & "\\"}}"
        set end of taskStrings to taskString
    end repeat
    return taskStrings
    '''
