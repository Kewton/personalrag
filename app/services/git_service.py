import os
from app.utils.run_shelll_command import run_shell_command
from app.utils.url_operation import extract_path
from app.core.config import DOC_DOWNLOAD_DIR


def git_clone(githuburl: str) -> bool:
    try:
        _path = os.getenv(DOC_DOWNLOAD_DIR, extract_path(githuburl))
        run_shell_command(f"git clone {githuburl} {_path}")
        return True
    except Exception as e:
        print(e)
        return False


def git_pull(githuburl: str) -> bool:
    try:
        _path = os.getenv(DOC_DOWNLOAD_DIR, extract_path(githuburl))
        run_shell_command(f"(cd {_path} && git pull {githuburl})")
        return True
    except Exception as e:
        print(e)
        return False