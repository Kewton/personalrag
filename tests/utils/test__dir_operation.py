import os
import shutil
import pytest
from unittest import mock
from app.utils.dir_operation import remove_directory_if_exists
from app.utils.logger import writeinfolog, writeerrorlog

# ディレクトリが存在し、正常に削除された場合のテスト
@mock.patch("app.utils.dir_operation.os.path.exists")
@mock.patch("app.utils.dir_operation.os.path.isdir")
@mock.patch("app.utils.dir_operation.shutil.rmtree")
@mock.patch("app.utils.dir_operation.writeinfolog")
def test_remove_directory_if_exists_success(mock_writeinfolog, mock_rmtree, mock_isdir, mock_exists):
    mock_exists.return_value = True  # ディレクトリが存在する
    mock_isdir.return_value = True  # 存在するのがディレクトリである

    result = remove_directory_if_exists("/path/to/dir")

    # ディレクトリが削除されているか
    mock_rmtree.assert_called_once_with("/path/to/dir")
    # 情報ログが正しく記録されているか
    mock_writeinfolog.assert_called_once_with("ディレクトリを削除しました: /path/to/dir")
    assert result is True  # 正しく削除されたことを確認

# 存在しないディレクトリの場合のテスト
@mock.patch("app.utils.dir_operation.os.path.exists")
@mock.patch("app.utils.dir_operation.writeinfolog")
def test_remove_directory_if_exists_not_exist(mock_writeinfolog, mock_exists):
    mock_exists.return_value = False  # ディレクトリは存在しない

    result = remove_directory_if_exists("/path/to/dir")

    # 情報ログが正しく記録されているか
    mock_writeinfolog.assert_called_once_with("ディレクトリは存在しません: /path/to/dir")
    assert result is False  # 削除されない

# 指定されたパスがディレクトリではない場合のテスト
@mock.patch("app.utils.dir_operation.os.path.exists")
@mock.patch("app.utils.dir_operation.os.path.isdir")
@mock.patch("app.utils.dir_operation.writeinfolog")
def test_remove_directory_if_exists_not_a_directory(mock_writeinfolog, mock_isdir, mock_exists):
    mock_exists.return_value = True  # パスは存在する
    mock_isdir.return_value = False  # しかしディレクトリではない

    result = remove_directory_if_exists("/path/to/file")

    # 情報ログが正しく記録されているか
    mock_writeinfolog.assert_called_once_with("指定されたパスはディレクトリではありません: /path/to/file")
    assert result is False  # 削除されない

# ディレクトリ削除中に例外が発生した場合のテスト
@mock.patch("app.utils.dir_operation.os.path.exists")
@mock.patch("app.utils.dir_operation.os.path.isdir")
@mock.patch("app.utils.dir_operation.shutil.rmtree", side_effect=Exception("削除エラー"))
@mock.patch("app.utils.dir_operation.writeerrorlog")
def test_remove_directory_if_exists_error(mock_writeerrorlog, mock_rmtree, mock_isdir, mock_exists):
    mock_exists.return_value = True  # ディレクトリが存在する
    mock_isdir.return_value = True  # 存在するのがディレクトリである

    result = remove_directory_if_exists("/path/to/dir")

    # 削除が失敗したことを確認
    mock_rmtree.assert_called_once_with("/path/to/dir")
    # エラーログが正しく記録されているか
    mock_writeerrorlog.assert_called_once_with("ディレクトリの削除に失敗しました: 削除エラー")
    assert result is False  # 削除は失敗したことを確認
