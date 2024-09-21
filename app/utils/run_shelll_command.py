import subprocess


# シェルコマンドを実行する関数
def run_shell_command(command):
    try:
        # コマンドを実行し、出力をキャプチャ
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)  # コマンドの標準出力を表示
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
        print(f"Standard Error: {e.stderr}")
