from domain.project import Project

_project: Project | None = None


def set_current_project(project: Project):
    global _project
    assert _project is None, _project
    _project = project


def get_current_project() -> Project:
    return _project
