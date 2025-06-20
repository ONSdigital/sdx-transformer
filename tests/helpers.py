from app.config.root import PROJECT_ROOT


def get_saucy_path(filepath: str) -> str:
    """
    Means we dont have to change working directory when running tests.
    """

    if filepath.startswith("/"):
        return f"{PROJECT_ROOT}{filepath}"
    return f"{PROJECT_ROOT}/{filepath}"
