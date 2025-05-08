def resolve_project_applescript(project_path: str) -> tuple[str, str]:
    parts = [p.strip() for p in project_path.split(">")]
    folder_parts = parts[:-1]
    project_name = parts[-1]

    script_lines = []
    for folder in folder_parts:
        if not script_lines:
            script_lines.append(
                f'set currentFolder to first folder of default document whose name is "{folder}"'
            )
        else:
            script_lines.append(
                f'set currentFolder to first folder of currentFolder whose name is "{folder}"'
            )

    script_lines.append(
        f'set currentProject to first project of currentFolder whose name is "{project_name}"'
    )
    return "\n".join(script_lines), "currentProject"


def resolve_folder_applescript(folder_path: str) -> tuple[str, str]:
    components = [part.strip() for part in folder_path.split(">")]
    script_lines = []
    for i, name in enumerate(components):
        if i == 0:
            script_lines.append(
                f'set currentFolder to first folder of default document whose name is "{name}"'
            )
        else:
            script_lines.append(
                f'set currentFolder to first folder of currentFolder whose name is "{name}"'
            )
    return "\n".join(script_lines), "currentFolder"


def safe_resolve_project_applescript(project_path: str) -> tuple[str, str]:
    parts = [p.strip() for p in project_path.split(">")]
    if len(parts) == 1:
        # Top-level project, no folder navigation
        project_name = parts[0]
        script = f'set currentProject to first project of default document whose name is "{project_name}"'
        return script, "currentProject"
    else:
        return resolve_project_applescript(project_path)
