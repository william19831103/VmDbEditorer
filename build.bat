@echo off
echo 开始构建程序...

REM 切换到脚本所在目录
cd /d "%~dp0"
cd qtversion

REM 安装依赖
echo 正在检查依赖...
pip install -r ..\requirements.txt

REM 清理旧的构建文件
echo 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /f /q *.spec

REM 获取PyQt5路径
for /f "tokens=*" %%i in ('python -c "import PyQt5; import os; print(os.path.dirname(PyQt5.__file__))"') do set PYQT5_PATH=%%i

echo 使用的PyQt5路径: %PYQT5_PATH%

REM 使用PyInstaller打包
echo 开始打包程序...
pyinstaller --noconsole --onefile ^
    --add-binary "DBCGenerator.dll;." ^
    --add-binary "mpqpatcher.dll;." ^
    --add-binary "StormLib.dll;." ^
    --add-binary "libmySQL.dll;." ^
    --add-binary "%PYQT5_PATH%\Qt5\plugins\platforms\qwindows.dll;platforms" ^
    --add-binary "%PYQT5_PATH%\Qt5\plugins\styles\qwindowsvistastyle.dll;styles" ^
    --add-binary "%PYQT5_PATH%\Qt5\plugins\imageformats\*.*;imageformats" ^
    --add-data "config.json;." ^
    --add-data "spell_fields.py;." ^
    --add-data "logger.py;." ^
    --add-data "config.py;." ^
    --hidden-import mysql.connector.plugins ^
    --hidden-import mysql.connector.plugins.mysql_native_password ^
    --hidden-import PyQt5 ^
    --hidden-import PyQt5.QtCore ^
    --hidden-import PyQt5.QtGui ^
    --hidden-import PyQt5.QtWidgets ^
    --hidden-import PyQt5.sip ^
    --hidden-import win32com.client ^
    --hidden-import wmi ^
    --hidden-import cryptography ^
    --collect-all mysql.connector ^
    --collect-all PyQt5 ^
    --exclude-module _bootlocale ^
    --disable-windowed-traceback ^
    --version-file ..\version.txt ^
    --name "SpellEditor" ^
    VmDbEditorer.py

REM 检查是否打包成功
if exist "dist\SpellEditor.exe" (
    echo 程序打包成功！
    
    REM 创建发布目录结构
    mkdir "..\release" 2>nul
    mkdir "..\release\platforms" 2>nul
    mkdir "..\release\styles" 2>nul
    mkdir "..\release\imageformats" 2>nul
    
    REM 复制文件到发布目录
    echo 正在准备发布文件...
    copy "dist\SpellEditor.exe" "..\release\"
    copy "config.json" "..\release\"
    
    REM 复制Qt插件
    copy "%PYQT5_PATH%\Qt5\plugins\platforms\qwindows.dll" "..\release\platforms\"
    copy "%PYQT5_PATH%\Qt5\plugins\styles\qwindowsvistastyle.dll" "..\release\styles\"
    copy "%PYQT5_PATH%\Qt5\plugins\imageformats\*.dll" "..\release\imageformats\"
    
    REM 复制其他DLL
    copy "DBCGenerator.dll" "..\release\"
    copy "mpqpatcher.dll" "..\release\"
    copy "StormLib.dll" "..\release\"
    copy "libmySQL.dll" "..\release\"
    
    REM 创建qt.conf
    echo [Paths] > "..\release\qt.conf"
    echo Prefix = . >> "..\release\qt.conf"
    echo Plugins = . >> "..\release\qt.conf"
    echo Binaries = . >> "..\release\qt.conf"
    
    echo.
    echo 发布文件已准备完成！
    echo 发布目录: %CD%\..\release
) else (
    echo 打包失败！请检查错误信息。
)

echo.
echo 按任意键退出...
pause >nul