import tkinter as tk
import time
from utility import config

class RecordPlayer:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.playback_speed = config.PLAYBACK_SPEED

    def play_strokes(self, all_canvas_lines: list):
        """
        播放所有筆畫。
        all_canvas_lines 是一個列表，其中每個元素又是一個列表，包含單一筆畫的所有線條 ID。
        """
        if not all_canvas_lines:
            print("沒有筆畫可以播放。")
            return

        # 1. 隱藏所有筆畫
        for stroke_lines in all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="") # 將顏色設為透明或背景色
        self.canvas.update()
        time.sleep(0.5) # 稍微停頓一下，讓隱藏的動作可見

        # 2. 依序顯示每個筆畫
        print("開始播放筆順...")
        for stroke_lines in all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="red") # 顯示線條
                self.canvas.update() # 強制更新畫布
                time.sleep(self.playback_speed) # 暫停一段時間
        print("筆順播放完畢。")

    def redraw_loaded_data(self, loaded_data: list):
        """
        根據載入的資料重新繪製筆畫，但不播放動畫。
        用於從檔案載入資料後，直接顯示在畫布上。
        回傳所有繪製的 canvas 線條 ID，按筆畫分組。
        """
        self.canvas.delete("drawing_stroke") # 清除所有現有筆畫
        if not loaded_data:
            print("沒有載入的資料可以重新繪製。")
            return []

        all_lines_on_canvas = []
        current_stroke_lines = []
        prev_stroke_num = None
        prev_x, prev_y = None, None

        for i, (stroke_num, _, x, y, _) in enumerate(loaded_data):
            if prev_stroke_num is None: # 第一個點
                prev_x, prev_y = x, y
                prev_stroke_num = stroke_num
                current_stroke_lines = []
                continue

            if stroke_num != prev_stroke_num: # 新的筆畫開始
                all_lines_on_canvas.append(current_stroke_lines)
                current_stroke_lines = []
                prev_x, prev_y = x, y
                prev_stroke_num = stroke_num
                continue

            # 同一筆畫
            line_id = self.canvas.create_line(
                prev_x, prev_y, x, y,
                fill="red", width=3, capstyle=tk.ROUND, smooth=tk.TRUE, tags="drawing_stroke"
            )
            current_stroke_lines.append(line_id)
            prev_x, prev_y = x, y

        # 添加最後一個筆畫的線條
        if current_stroke_lines:
            all_lines_on_canvas.append(current_stroke_lines)

        print(f"已從載入資料重新繪製 {len(all_lines_on_canvas)} 個筆畫。")
        return all_lines_on_canvas