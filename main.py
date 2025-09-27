import tkinter as tk
import time
from PIL import Image, ImageTk
import csv # 導入 csv 模組，用於處理 CSV 文件

class HandwritingRecorder:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("筆順記錄器")

        # 設定 Canvas 寬高，並固定窗口大小
        canvas_width = 500
        canvas_height = 500
        master.resizable(False, False)

        # 載入背景圖片
        self.bg_image_path = "筆順/tianzige.png"
        self.original_image = Image.open(self.bg_image_path)
        self.bg_image = ImageTk.PhotoImage(
            self.original_image.resize((canvas_width, canvas_height), Image.LANCZOS)
        )

        # 創建 Canvas 並放置背景圖片
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW, tags="background_image")

        # 綁定滑鼠事件
        self.canvas.bind("<Button-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

        self.strokes_data = [] # 儲存所有筆畫數據
        self.current_stroke = [] # 儲存當前筆畫的點
        self.stroke_number = 0   # 筆畫編號
        self.is_drawing = False  # 繪圖狀態

        # 創建並放置清除按鈕
        self.clear_button = tk.Button(master, text="清除", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        # 創建並放置儲存資料按鈕
        self.save_button = tk.Button(master, text="儲存資料", command=self.save_data)
        self.save_button.pack(side=tk.LEFT)


    def start_stroke(self, event):
        """處理滑鼠左鍵按下事件，開始新筆畫"""
        self.is_drawing = True
        self.stroke_number += 1
        self.current_stroke = []
        self.record_point(event.x, event.y)
        self.prev_x, self.prev_y = event.x, event.y


    def draw_stroke(self, event):
        """處理滑鼠拖動事件，繪製線條"""
        if self.is_drawing:
            self.canvas.create_line(
                self.prev_x, self.prev_y, event.x, event.y,
                fill="red", width=3, capstyle=tk.ROUND, smooth=tk.TRUE, tags="drawing_stroke"
            )
            self.record_point(event.x, event.y)
            self.prev_x, self.prev_y = event.x, event.y


    def end_stroke(self, event):
        """處理滑鼠釋放事件，結束筆畫"""
        self.is_drawing = False
        self.strokes_data.extend(self.current_stroke)


    def record_point(self, x, y):
        """記錄點的資訊 (筆畫編號, 時間戳, x, y, 力道)"""
        timestamp = time.time()
        self.current_stroke.append((self.stroke_number, timestamp, x, y, 0.1))


    def clear_canvas(self):
        """清除畫布上的筆畫並重置數據"""
        self.canvas.delete("drawing_stroke") # 刪除所有帶有 "drawing_stroke" 標籤的物件
        self.strokes_data = []
        self.current_stroke = []
        self.stroke_number = 0
        print("畫布上的筆畫已清除，資料已重置。")


    def save_data(self):
        """將記錄到的筆畫數據儲存到 CSV 文件"""
        if not self.strokes_data:
            print("沒有筆畫資料可以儲存。")
            return

        # 以寫入模式打開 CSV 文件
        # newline='' 參數對於 CSV 寫入很重要，防止空行
        with open("筆順/handwriting_data.csv", "w", newline='') as f:
            writer = csv.writer(f) # 創建一個 csv writer 物件
            # 寫入 CSV 標題行
            writer.writerow(["stroke_num", "timestamp", "x", "y", "pressure"])
            # 寫入所有筆畫數據
            writer.writerows(self.strokes_data)

        print("資料已儲存到 handwriting_data.csv")
        print("儲存的資料範例 (前5筆):")
        # 印出前五筆資料作為範例
        for i, data in enumerate(self.strokes_data[:5]):
            print(data)
        if len(self.strokes_data) > 5:
            print("...")


root = tk.Tk()
recorder = HandwritingRecorder(root)
root.mainloop()