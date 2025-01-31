import PyInstaller.__main__
import os
import sys

# 添加 src 目錄到 Python 路徑
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# 確保資源檔案已編譯
os.system("pyside6-rcc src/resources/resources.qrc -o src/resources/resources_rc.py")

PyInstaller.__main__.run([
    'start.py',
    '--name=TaskManager',
    '--windowed',
    '--add-data=src/resources/styles/main.qss;src/resources/styles',
    '--hidden-import=PySide6.QtSvg',
    '--hidden-import=PySide6.QtXml',
    '--noconsole',
    '--clean',
    '--onefile',
    '--paths=src'
])