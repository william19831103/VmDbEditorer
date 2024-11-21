@echo off
chcp 65001 >nul
echo 开始构建程序...

REM 切换到脚本所在目录
cd /d "%~dp0"
cd qtversion

REM 安装依赖
echo 正在检查依赖...
pip install -r ..\requirements.txt
pip install nuitka

REM 清理旧的构建文件
echo 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist SpellEditor.build rmdir /s /q SpellEditor.build
if exist SpellEditor.dist rmdir /s /q SpellEditor.dist
if exist "..\release" rmdir /s /q "..\release"

REM 获取PyQt5路径
for /f "tokens=*" %%i in ('python -c "import PyQt5; import os; print(os.path.dirname(PyQt5.__file__))"') do set PYQT5_PATH=%%i

echo 使用的PyQt5路径: %PYQT5_PATH%

REM 设置环境变量指向MinGW
set PATH=C:\mingw32\bin;%PATH%

REM 使用Nuitka打包
echo 开始打包程序...
python -m nuitka ^
    --windows-company-name="Your Company" ^
    --windows-product-name="SpellEditor" ^
    --windows-product-version=1.0.0.0 ^
    --windows-file-version=1.0.0.0 ^
    --windows-disable-console ^
    --standalone ^
    --show-progress ^
    --show-memory ^
    --enable-plugin=pyqt5 ^
    --include-package=mysql.connector ^
    --include-package=PyQt5 ^
    --include-package=win32com ^
    --include-package=wmi ^
    --include-package=cryptography ^
    --include-data-files=config.json=config.json ^
    --include-data-files=spell_fields.py=spell_fields.py ^
    --include-data-files=logger.py=logger.py ^
    --include-data-files=config.py=config.py ^
    --include-data-files=DBCGenerator.dll=DBCGenerator.dll ^
    --include-data-files=mpqpatcher.dll=mpqpatcher.dll ^
    --include-data-files=StormLib.dll=StormLib.dll ^
    --include-data-files=libmySQL.dll=libmySQL.dll ^
    --output-dir=dist ^
    --follow-imports ^
    --prefer-source-code ^
    --low-memory ^
    --remove-output ^
    --nofollow-import-to=tkinter,unittest,pdb,distutils,setuptools ^
    --nofollow-imports ^
    --no-prefer-source-code ^
    VmDbEditorer.py

REM 检查是否打包成功
if exist "dist\VmDbEditorer.dist" (
    echo 程序打包成功！
    
    REM 创建发布目录结构
    mkdir "..\release" 2>nul
    
    REM 复制文件到发布目录
    echo 正在准备发布文件...
    xcopy /E /I /Y "dist\VmDbEditorer.dist\*" "..\release\"
    
    REM 重命名可执行文件
    if exist "..\release\VmDbEditorer.exe" (
        ren "..\release\VmDbEditorer.exe" "SpellEditor.exe"
    )
    
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