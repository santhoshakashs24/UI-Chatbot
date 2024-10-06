# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import *
import sys
import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

path = os.path.abspath(".")
sys.path.insert(0, os.path.join(path, "libs"))

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None

icon_path = 'C:\\Users\\Akash\\Desktop\\lseg\\lseg_Chatbot\\resources\\images\\logo.ico'

a = Analysis(
    ['C:\\Users\\Akash\\Desktop\\lseg\\lseg_Chatbot\\lseg_Chatbot.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\Akash\\Desktop\\lseg\\lseg_Chatbot\\Chats.kv', '.'),
        ('C:\\Users\\Akash\\Desktop\\lseg\\lseg_Chatbot\\resources\\', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LsegChatbot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Change this to False for a windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Make sure this line is present
)

coll = COLLECT(
    exe,
    Tree('C:\\Users\\Akash\\Desktop\\lseg\\lseg_Chatbot\\'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LsegChatbot',
)