import os
import shutil
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog


def remove_directory_if_exists(directory_path):
    """
    指定されたディレクトリが存在する場合に削除します。

    Parameters:
    directory_path (str): 削除するディレクトリのパス
    """
    if os.path.exists(directory_path):
        if os.path.isdir(directory_path):
            try:
                shutil.rmtree(directory_path)
                writeinfolog(f"ディレクトリを削除しました: {directory_path}")
                return True
            except Exception as e:
                writeerrorlog(f"ディレクトリの削除に失敗しました: {e}")
                return False
        else:
            writeinfolog(f"指定されたパスはディレクトリではありません: {directory_path}")
            return False
    else:
        writeinfolog(f"ディレクトリは存在しません: {directory_path}")
        return False


def ensure_directory_exists(directory: str):    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")