import os
import sys

# 將 src 目錄添加到 Python 路徑
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

print("Python Path:")
for path in sys.path:
    print(f"  - {path}")

print("\nCurrent Directory:", os.getcwd())
print("Script Location:", os.path.abspath(__file__))
print("Source Path:", src_path)

# 導入並運行主程式
if __name__ == "__main__":
    from main import main
    sys.exit(main())