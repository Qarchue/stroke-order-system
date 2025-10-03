import tkinter as tk
import time
from PIL import Image, ImageTk
import csv

class HandwritingRecorder:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("筆順記錄器")

        canvas_width = 500
        canvas_height = 500
        master.resizable(False, False)

        self.bg_image_path = "images/tianzige.png"
        self.original_image = Image.open(self.bg_image_path)
        self.bg_image = ImageTk.PhotoImage(
            self.original_image.resize((canvas_width, canvas_height), Image.LANCZOS)
        )

        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW, tags="background_image")

        self.canvas.bind("<Button-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

        self.strokes_data = [] # 儲存所有筆畫數據
        self.current_stroke = [] # 儲存當前筆畫的點
        self.stroke_number = 0   # 筆畫編號
        self.is_drawing = False  # 繪圖狀態

        # 新增：儲存所有繪製的 Canvas 線條物件 ID
        self.all_canvas_lines = []
        # 新增：儲存當前筆畫的 Canvas 線條物件 ID
        self.current_canvas_lines = []

        self.clear_button = tk.Button(master, text="清除", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(master, text="儲存資料", command=self.save_data)
        self.save_button.pack(side=tk.LEFT)

        # 新增：倒放按鈕
        self.rewind_button = tk.Button(master, text="倒放", command=self.rewind_strokes)
        self.rewind_button.pack(side=tk.LEFT)

        self.playback_speed = 0.05 # 倒放或播放的間隔時間

    def start_stroke(self, event):
        self.is_drawing = True
        self.stroke_number += 1
        self.current_stroke = []
        self.current_canvas_lines = [] # 為新的筆畫清空線條 ID 列表
        self.record_point(event.x, event.y)
        self.prev_x, self.prev_y = event.x, event.y

    def draw_stroke(self, event):
        if self.is_drawing:
            line_id = self.canvas.create_line(
                self.prev_x, self.prev_y, event.x, event.y,
                fill="red", width=3, capstyle=tk.ROUND, smooth=tk.TRUE, tags="drawing_stroke"
            )
            self.current_canvas_lines.append(line_id) # 儲存當前筆畫的線條 ID
            self.record_point(event.x, event.y)
            self.prev_x, self.prev_y = event.x, event.y

    def end_stroke(self, event):
        self.is_drawing = False
        self.strokes_data.extend(self.current_stroke)
        # 筆畫結束時，將當前筆畫的所有線條 ID 添加到總列表中
        self.all_canvas_lines.append(self.current_canvas_lines)
        self.current_canvas_lines = [] # 清空以準備下一個筆畫

    def record_point(self, x, y):
        timestamp = time.time()
        self.current_stroke.append((self.stroke_number, timestamp, x, y, 0.1))

    def clear_canvas(self):
        self.canvas.delete("drawing_stroke")
        self.strokes_data = []
        self.current_stroke = []
        self.stroke_number = 0
        self.all_canvas_lines = [] # 清除所有儲存的線條 ID
        self.current_canvas_lines = []
        print("畫布上的筆畫已清除，資料已重置。")

    def save_data(self):
        if not self.strokes_data:
            print("沒有筆畫資料可以儲存。")
            return

        with open("筆順/handwriting_data.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["stroke_num", "timestamp", "x", "y", "pressure"])
            writer.writerows(self.strokes_data)

        print("資料已儲存到 handwriting_data.csv")
        print("儲存的資料範例 (前5筆):")
        for i, data in enumerate(self.strokes_data[:5]):
            print(data)
        if len(self.strokes_data) > 5:
            print("...")

    def rewind_strokes(self):
        """倒放所有筆畫，先全部隱藏再依序顯示"""
        if not self.all_canvas_lines:
            print("沒有筆畫可以倒放。")
            return

        # 1. 隱藏所有筆畫
        for stroke_lines in self.all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="") # 將顏色設為透明或背景色
        self.master.update()
        time.sleep(0.5) # 稍微停頓一下，讓隱藏的動作可見

        # 2. 依序顯示每個筆畫
        # 這裡的 "倒放" 指的是 "按照書寫順序重新顯示"
        # 如果你真的想要像錄影帶倒帶一樣，從最後一筆畫的最後一點開始倒著「抹去」，那會更複雜
        # 我先實現「從頭開始重現書寫過程」
        print("開始播放筆順...")
        for stroke_lines in self.all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="red") # 顯示線條
                self.master.update() # 強制更新畫布
                time.sleep(self.playback_speed) # 暫停一段時間

        print("筆順播放完畢。")

root = tk.Tk()
recorder = HandwritingRecorder(root)
root.mainloop()