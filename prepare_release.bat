@echo off
echo 准备发布文件...

REM 创建必要的目录
mkdir release\platforms 2>nul

REM 复制主程序和配置文件
copy qtversion\dist\SpellEditor.exe release\
copy qtversion\config.json release\

REM 复制Qt平台插件
copy "%PYTHON_HOME%\Lib\site-packages\PyQt5\Qt5\plugins\platforms\qwindows.dll" release\platforms\

REM 复制其他必要的DLL
copy qtversion\DBCGenerator.dll release\
copy qtversion\mpqpatcher.dll release\
copy qtversion\StormLib.dll release\
copy qtversion\libmySQL.dll release\

echo 发布文件准备完成！
echo 发布目录: %CD%\release
pause 