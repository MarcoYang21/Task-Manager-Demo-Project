# Task Manager 任務管理系統

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![PySide Version](https://img.shields.io/badge/PySide6-6.5.0+-green.svg)
![License](https://img.shields.io/badge/license-GPL--2.0-blue.svg)

這是一個基於 PySide6 開發的任務管理系統，採用 MVC 架構設計，用於展示 Python GUI 應用程式的最佳實踐。

## 功能特色

- 📝 任務管理：新增、編輯、刪除和查看任務
- 🎯 任務狀態追蹤：待辦、進行中、已完成
- 💾 資料持久化：使用 SQLite 資料庫儲存
- 🎨 現代化界面：支援自訂主題和圖示
- 🔧 模組化設計：基於 MVC 架構，易於擴展

## 系統需求

- Python 3.10 或更高版本
- pipenv
- SQLite 3

## 快速開始

### 1. 克隆專案

```bash
git clone https://github.com/MarcoYang21/Task-Manager-Demo-Project.git
cd Task-Manager-Demo-Project
```

### 2. 安裝 pipenv

```bash
# Windows/macOS/Linux
pip install pipenv
```

### 3. 設置開發環境

```bash
# 建立虛擬環境並安裝依賴
pipenv install --dev

# 啟動虛擬環境
pipenv shell
```

### 4. 編譯資源檔

```bash
pipenv run pyside6-rcc src/resources/resources.qrc -o src/resources/resources_rc.py
```

### 5. 執行應用程式

```bash
pipenv run python src/main.py
```

## 專案結構

```
task_manager/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 程式進入點
│   ├── config.py               # 配置檔案
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py            # 基礎資料模型
│   │   ├── task.py            # 任務模型
│   │   └── database.py        # 資料庫連接
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py     # 主視窗
│   │   ├── task_dialog.py     # 任務編輯對話框
│   │   └── widgets/
│   │       ├── __init__.py
│   │       └── task_list.py   # 任務列表元件
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── task.py            # 任務控制器
│   └── resources/
│       ├── icons/
│       │   ├── app.ico
│       │   └── actions/
│       │       ├── add.png
│       │       ├── edit.png
│       │       └── delete.png
│       ├── styles/
│       │   └── main.qss
│       └── resources.qrc
├── tests/                     # 測試程式碼
│   └── ...
├── README.md
└── requirements.txt
├── Pipfile                    # pipenv 依賴配置
├── Pipfile.lock               # pipenv 依賴版本鎖定
└── README.md                  # 說明文件
```

## 開發指南

### 環境設置

1. 安裝開發依賴
```bash
pipenv install --dev
```

2. 設置 pre-commit hooks
```bash
pipenv run pre-commit install
```

### 程式碼風格

本專案遵循 PEP 8 規範，使用 black 進行程式碼格式化：

```bash
# 格式化程式碼
pipenv run black src/

# 執行風格檢查
pipenv run flake8 src/
```

### 執行測試

```bash
# 執行所有測試
pipenv run pytest

# 執行特定測試
pipenv run pytest tests/test_task_model.py

# 產生測試覆蓋率報告
pipenv run pytest --cov=src tests/
```

### 依賴管理

```bash
# 新增依賴
pipenv install package_name

# 新增開發依賴
pipenv install --dev package_name

# 更新依賴
pipenv update

# 查看依賴關係圖
pipenv graph
```

## 使用說明

### 基本操作

1. **新增任務**
   - 點擊工具列的「新增」按鈕
   - 填寫任務資訊
   - 點擊「確定」儲存

2. **編輯任務**
   - 選擇要編輯的任務
   - 點擊「編輯」按鈕
   - 修改任務資訊
   - 點擊「確定」儲存

3. **刪除任務**
   - 選擇要刪除的任務
   - 點擊「刪除」按鈕
   - 確認刪除操作

### 快速鍵

- `Ctrl+N`: 新增任務
- `Ctrl+E`: 編輯任務
- `Delete`: 刪除任務
- `Ctrl+F`: 搜尋任務

## 自訂化

### 修改樣式

1. 編輯 `src/resources/styles/main.qss`
2. 重新編譯資源檔
3. 重啟應用程式

### 新增功能

1. 在相應的 MVC 層級新增程式碼
2. 更新單元測試
3. 更新文件

## 故障排除

### 常見問題

1. **虛擬環境問題**
   - 確認 pipenv 已正確安裝
   - 使用 `pipenv --venv` 檢查虛擬環境位置
   - 使用 `pipenv graph` 檢查依賴關係

2. **無法啟動應用程式**
   - 確認是否在虛擬環境中 (`pipenv shell`)
   - 檢查依賴套件是否正確安裝
   - 確認資源檔是否已編譯

3. **資料庫錯誤**
   - 確認 SQLite 檔案權限
   - 檢查資料庫結構是否正確

4. **介面顯示異常**
   - 確認 QSS 檔案語法
   - 檢查資源檔是否正確載入

## 貢獻指南

1. Fork 專案
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 版本歷史

- 1.0.0 (2025-01-31)
    - 初始版本發布
    - 基本任務管理功能
    - MVC 架構實現

## 授權條款

本專案採用 GPL2 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 作者

[Marco Yang] - [marco_yang@msn.com]

## 致謝

- PySide6 團隊提供優秀的 GUI 框架
- 所有貢獻者的寶貴意見和建議

## 相關資源

- [Pipenv 文件](https://pipenv.pypa.io/en/latest/)
- [PySide6 文件](https://doc.qt.io/qtforpython-6/)
- [SQLite 文件](https://www.sqlite.org/docs.html)
- [Python 文件](https://docs.python.org/3/)
- [Flake8 文件](https://flake8.pycqa.org/en/latest/)
