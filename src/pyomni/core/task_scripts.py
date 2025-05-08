def build_task_query_applescript(selector: str) -> str:
    return f'''
tell application "OmniFocus"
    tell default document
        set taskList to {selector}
        set taskBlocks to ""
        repeat with t in taskList
            set blockText to ""
            try
                set blockText to blockText & "id:" & (id of t as text) & return
            end try
            try
                set blockText to blockText & "name:" & (name of t as text) & return
            end try
            try
                set blockText to blockText & "note:" & (note of t as text) & return
            end try
            try
                set blockText to blockText & "flagged:" & (flagged of t as text) & return
            end try
            try
                set blockText to blockText & "completed:" & (completed of t as text) & return
            end try
            try
                set blockText to blockText & "blocked:" & (blocked of t as text) & return
            end try
            try
                set blockText to blockText & "dropped:" & (dropped of t as text) & return
            end try
            try
                set blockText to blockText & "in_inbox:" & (in inbox of t as text) & return
            end try
            try
                set blockText to blockText & "defer_date:" & (defer date of t as text) & return
            end try
            try
                set blockText to blockText & "due_date:" & (due date of t as text) & return
            end try
            try
                set blockText to blockText & "creation_date:" & (creation date of t as text) & return
            end try
            try
                set blockText to blockText & "modification_date:" & (modification date of t as text) & return
            end try
            try
                set blockText to blockText & "completion_date:" & (completion date of t as text) & return
            end try
            try
                set blockText to blockText & "dropped_date:" & (dropped date of t as text) & return
            end try
            try
                set blockText to blockText & "estimated_minutes:" & (estimated minutes of t as text) & return
            end try
            try
                set tagNames to name of every tag of t
                set blockText to blockText & "tags:" & (tagNames as string) & return
            end try
            try
                repeat with c in every task of t
                    try
                        set blockText to blockText & "CHILD:id:" & (id of c as text) & return
                        set blockText to blockText & "CHILD:name:" & (name of c as text) & return
                    end try
                end repeat
            end try
            set taskBlocks to taskBlocks & blockText & return
        end repeat
        return taskBlocks
    end tell
end tell
'''
