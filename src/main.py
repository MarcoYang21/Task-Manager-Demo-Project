import sys
import os
from PySide6.QtWidgets import QApplication

# 將專案根目錄添加到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)  # 添加 src 目錄到路徑

from controllers.task import TaskController


def main():
    app = QApplication(sys.argv)

    # 載入樣式表
    style_path = os.path.join(current_dir, "resources/styles/main.qss")
    try:
        with open(style_path, "r", encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: Could not find style file at {style_path}")

    # 創建控制器
    controller = TaskController()
    controller.view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
