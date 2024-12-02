@echo off

rem 仮想環境のパスを指定
set VENV_PATH=your_directory\.venv

rem 仮想環境をアクティベート
call "%VENV_PATH%\Scripts\activate"

rem すべての引数を1つずつ処理し、ファイルパスを二重引用符で囲む
for %%F in (%*) do (
    python "your_directory\main.py" "%%~F"
)

rem 仮想環境のディアクティベート
deactivate
