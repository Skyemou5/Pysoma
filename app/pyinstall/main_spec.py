# -*- PyInstaller input file -*-
# -*- mode: python           -*-

added_files = [
    ['app/doc/info.md'],
    ['app/data/Project_Dirs.json'],
]

block_sipher = None

a = Analysis(
    ['app/main.py'],
    pathex=['/Developer/PItests/minimal'],
    binaries=None,
    datas=added_files,
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
    excludes=None,
    cipher=block_cipher,
)

