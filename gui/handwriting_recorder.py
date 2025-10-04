import time
import tkinter as tk

class HandwritingRecorder:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.strokes_data = []  # 儲存所有筆畫數據 (stroke_num, timestamp, x, y, pressure)
        self.current_stroke_points = []  # 儲存當前筆畫的點
        self.stroke_number = 0  # 筆畫編號
        self.is_drawing = False # 繪圖狀態
        self.prev_x, self.prev_y = 0, 0 # 上一個點的座標

        # 儲存所有繪製的 Canvas 線條物件 ID，按筆畫分組
        self.all_canvas_lines = []
        # 儲存當前筆畫的 Canvas 線條物件 ID
        self.current_canvas_line_ids = []

    def start_stroke(self, event):
        self.is_drawing = True
        self.stroke_number += 1
        self.current_stroke_points = [] # 為新的筆畫清空點列表
        self.current_canvas_line_ids = [] # 為新的筆畫清空線條 ID 列表
        self._record_point(event.x, event.y)
        self.prev_x, self.prev_y = event.x, event.y

    def draw_stroke(self, event):
        if self.is_drawing:
            line_id = self.canvas.create_line(
                self.prev_x, self.prev_y, event.x, event.y,
                fill="red", width=3, capstyle=tk.ROUND, smooth=tk.TRUE, tags="drawing_stroke"
            )
            self.current_canvas_line_ids.append(line_id) # 儲存當前筆畫的線條 ID
            self._record_point(event.x, event.y)
            self.prev_x, self.prev_y = event.x, event.y

    def end_stroke(self, event):
        if self.is_drawing: # 只有在確實有繪製時才儲存
            self.is_drawing = False
            # 將當前筆畫的點添加到總資料中
            self.strokes_data.extend(self.current_stroke_points)
            # 筆畫結束時，將當前筆畫的所有線條 ID 添加到總列表中
            self.all_canvas_lines.append(self.current_canvas_line_ids)
            self.current_canvas_line_ids = [] # 清空以準備下一個筆畫

    def _record_point(self, x, y, pressure=0.1):
        """內部方法，記錄單個點的資料"""
        timestamp = time.time()
        self.current_stroke_points.append((self.stroke_number, timestamp, x, y, pressure))

    def get_recorded_data(self):
        return self.strokes_data

    def get_all_canvas_lines(self):
        return self.all_canvas_lines

    def clear_recorder_data(self):
        """清除錄製器內部的所有資料和筆畫記錄"""
        self.strokes_data = []
        self.current_stroke_points = []
        self.stroke_number = 0
        self.all_canvas_lines = []
        self.current_canvas_line_ids = []
        print("錄製器資料已重置。")