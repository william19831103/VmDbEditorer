# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('config.json', '.'), ('spell_fields.py', '.'), ('logger.py', '.'), ('config.py', '.')]
binaries = [('DBCGenerator.dll', '.'), ('mpqpatcher.dll', '.'), ('StormLib.dll', '.'), ('libmySQL.dll', '.'), ('C:\\Python312-32\\Lib\\site-packages\\PyQt5\\Qt5\\plugins\\platforms\\qwindows.dll', 'platforms'), ('C:\\Python312-32\\Lib\\site-packages\\PyQt5\\Qt5\\plugins\\styles\\qwindowsvistastyle.dll', 'styles'), ('C:\\Python312-32\\Lib\\site-packages\\PyQt5\\Qt5\\plugins\\imageformats\\*.*', 'imageformats')]
hiddenimports = ['mysql.connector.plugins', 'mysql.connector.plugins.mysql_native_password', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.sip', 'win32com.client', 'wmi', 'cryptography']
tmp_ret = collect_all('mysql.connector')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt5')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['VmDbEditorer.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_bootlocale'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SpellEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='..\\version.txt',
)
