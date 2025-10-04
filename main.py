import tkinter as tk
from gui import MainGUI

def run_gui_part():
    app_gui = MainGUI() # <--- 直接呼叫 MainGUI()，無需傳遞任何參數
    app_gui.mainloop() # <--- 呼叫 MainGUI 實例自己的 mainloop()

if __name__ == "__main__":
    print("啟動應用程式的其他部分...")
    # ... 其他的程式邏輯 ...

    run_gui_part()
    print("應用程式結束。")