"""
このテストでは、subprocess.run をモック（擬似化）することで、外部のシェルコマンドを実際に実行せずに関数の動作を検証します。
"""
import pytest
import subprocess  # subprocessをインポート
from unittest import mock
from app.utils.run_shell_command import run_shell_command
from app.utils.logger import writedebuglog, writeerrorlog


# 正常にシェルコマンドが実行されるテスト
@mock.patch("app.utils.run_shell_command.subprocess.run")
@mock.patch("app.utils.run_shell_command.writedebuglog")
def test_run_shell_command_success(mock_writedebuglog, mock_subprocess_run):
    # モックの戻り値を設定
    mock_subprocess_run.return_value = mock.Mock(stdout="Command executed successfully")

    # シェルコマンドを実行
    result = run_shell_command("echo 'Hello World'")

    assert result is True

    # subprocess.runが正しく呼び出されたか確認
    mock_subprocess_run.assert_called_once_with("echo 'Hello World'", shell=True, check=True, capture_output=True, text=True)
    
    # writedebuglogが正しく呼び出されたか確認
    mock_writedebuglog.assert_called_once_with("Command executed successfully")


# コマンドがエラーを返した場合のテスト
@mock.patch("app.utils.run_shell_command.subprocess.run", side_effect=subprocess.CalledProcessError(1, "echo 'Hello World'", stderr="Error occurred"))
@mock.patch("app.utils.run_shell_command.writeerrorlog")
def test_run_shell_command_error(mock_writeerrorlog, mock_subprocess_run):
    with mock.patch("builtins.print") as mock_print:
        # シェルコマンドを実行し、エラーを発生させる
        result = run_shell_command("echo 'Hello World'")

        assert result is False

        # subprocess.runがエラーで呼び出されたか確認
        mock_subprocess_run.assert_called_once_with("echo 'Hello World'", shell=True, check=True, capture_output=True, text=True)
        
        # 実際のprint内容を確認
        mock_print.assert_any_call("An error occurred while running the command: Command 'echo 'Hello World'' returned non-zero exit status 1.")
        mock_print.assert_any_call("Standard Error: Error occurred")
        
        # writeerrorlogが呼び出されたか確認
        mock_writeerrorlog.assert_any_call("An error occurred while running the command: Command 'echo 'Hello World'' returned non-zero exit status 1.")
        mock_writeerrorlog.assert_any_call("Standard Error: Error occurred")
