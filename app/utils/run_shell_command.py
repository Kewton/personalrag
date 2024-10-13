import subprocess
from app.utils.logger import declogger, writeinfolog, writedebuglog, writeerrorlog


# シェルコマンドを実行する関数
@declogger
def run_shell_command(command):
    try:
        # コマンドを実行し、出力をキャプチャ
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        writedebuglog(result.stdout)
        print(result.stdout)  # コマンドの標準出力を表示
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
        print(f"Standard Error: {e.stderr}")
        writeerrorlog(f"An error occurred while running the command: {e}")
        writeerrorlog(f"Standard Error: {e.stderr}")
        return False
