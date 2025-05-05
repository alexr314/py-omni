def resolve_project_applescript(project_path: str) -> tuple[str, str]:
    parts = [p.strip() for p in project_path.split(">")]
    folder_parts = parts[:-1]
    project_name = parts[-1]

    script_lines = ["set currentFolder to default document"]
    for folder in folder_parts:
        script_lines.append(
            f'set currentFolder to first folder of currentFolder whose name is "{folder}"'
        )
    script_lines.append(
        f'set currentProject to first project of currentFolder whose name is "{project_name}"'
    )
    return "\n".join(script_lines), "currentProject"


def resolve_folder_applescript(folder_path: str) -> tuple[str, str]:
    components = [f'"{part.strip()}"' for part in folder_path.split(">")]
    script_lines = ["set currentFolder to default document"]
    for name in components:
        script_lines.append(
            f'set currentFolder to first folder of currentFolder whose name is {name}'
        )
    return "\n".join(script_lines), "currentFolder"
