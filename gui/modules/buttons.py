import tkinter

class BaseActionBtn(tkinter.Button):
    """基礎按鈕：定義統一的大小、字體、樣式"""
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.config(
            font=("Arial", 12, "bold"),
            width=10,
            height=1,
            bg="#f0f0f0",
            relief="raised"
        )

class ClearBtn(BaseActionBtn):
    """清除按鈕"""
    def __init__(self, master, canvas_instance):
        # 接收 canvas 實例，以便控制它
        self.canvas = canvas_instance
        super().__init__(master, text="清除全部", command=self.click_action)

    def click_action(self):
        # 呼叫 Canvas 的清除方法
        self.canvas.clear_canvas()

class ReplayBtn(BaseActionBtn):
    """回放按鈕"""
    def __init__(self, master, canvas_instance):
        self.canvas = canvas_instance
        super().__init__(master, text="畫筆回放", command=self.click_action)

    def click_action(self):
        # 呼叫 Canvas 的回放方法
        self.canvas.start_replay()