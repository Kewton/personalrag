import os
from app.utils.run_shell_command import run_shell_command
from app.utils.url_operation import extract_path
from app.core.config import DOC_DOWNLOAD_DIR
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog
import shutil


@declogger
def git_clone(githuburl: str) -> bool:
    try:
        _path = os.path.join(DOC_DOWNLOAD_DIR, extract_path(githuburl).lstrip("/"))

        # ディレクトリが存在するか確認
        if os.path.exists(_path):
            # ディレクトリかどうか確認
            if os.path.isdir(_path):
                # ディレクトリを削除
                shutil.rmtree(_path)
                writeinfolog(f'ディレクトリ {_path} を削除しました。')

        run_shell_command(f"git clone {githuburl} {_path}")
        return True
    except Exception as e:
        print(e)
        writeerrorlog(e)
        return False


@declogger
def git_pull(githuburl: str) -> bool:
    try:
        # os.path.join関数は、パスを結合する際に、引数にスラッシュ(/)で始まるパスが含まれている場合、その部分以降が優先されてしまいます。
        writedebuglog(f"DOC_DOWNLOAD_DIR={DOC_DOWNLOAD_DIR}")
        writedebuglog(f"extract_path(githuburl)={extract_path(githuburl).lstrip('/')}")
        _path = os.path.join(DOC_DOWNLOAD_DIR, extract_path(githuburl).lstrip("/"))
        run_shell_command(f"(cd {_path} && git pull {githuburl})")
        return True
    except Exception as e:
        print(e)
        writeerrorlog(e)
        return False
