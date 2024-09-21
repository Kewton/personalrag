import os
import shutil


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
                print(f"ディレクトリを削除しました: {directory_path}")
            except Exception as e:
                print(f"ディレクトリの削除に失敗しました: {e}")
        else:
            print(f"指定されたパスはディレクトリではありません: {directory_path}")
    else:
        print(f"ディレクトリは存在しません: {directory_path}")