import time
import tkinter

# 讓 HandwritingRecorder 繼承 tkinter.Frame
class HandwritingRecorder(tkinter.Frame): # <--- 這裡修改
    def __init__(self, master: tkinter.Widget, canvas: tkinter.Canvas): # <--- 接收 master 和 canvas
        super().__init__(master) # <--- 呼叫父類別 Frame 的初始化
        # self.pack() # 如果這個 Frame 需要在 MainGUI 佈局中顯示，可以在 MainGUI 中 pack 或 grid
        self.canvas = canvas
        self.strokes_data = []
        self.current_stroke_points = []
        self.stroke_number = 0
        self.is_drawing = False
        self.prev_x, self.prev_y = 0, 0

        self.all_canvas_lines = []
        self.current_canvas_line_ids = []

        # (可選) 如果 recorder 需要自己的 UI 元素，可以在這裡添加，例如一個狀態標籤
        # self.status_label = tkinter.Label(self, text="準備錄製")
        # self.status_label.pack()

    # ... 其他方法保持不變 ...
    # start_stroke, draw_stroke, end_stroke, _record_point, get_recorded_data, get_all_canvas_lines, clear_recorder_data
    # 這些方法的核心邏輯不變，因為它們仍然操作傳入的 self.canvas
    def start_stroke(self, event):
        self.is_drawing = True
        self.stroke_number += 1
        self.current_stroke_points = []
        self.current_canvas_line_ids = []
        self._record_point(event.x, event.y)
        self.prev_x, self.prev_y = event.x, event.y
        # if hasattr(self, 'status_label'):
        #     self.status_label.config(text=f"錄製中... 筆畫 {self.stroke_number}")

    def draw_stroke(self, event):
        if self.is_drawing:
            line_id = self.canvas.create_line(
                self.prev_x, self.prev_y, event.x, event.y,
                fill="red", width=3, capstyle=tkinter.ROUND, smooth=tkinter.TRUE, tags="drawing_stroke"
            )
            self.current_canvas_line_ids.append(line_id)
            self._record_point(event.x, event.y)
            self.prev_x, self.prev_y = event.x, event.y

    def end_stroke(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.strokes_data.extend(self.current_stroke_points)
            self.all_canvas_lines.append(self.current_canvas_line_ids)
            self.current_canvas_line_ids = []
            # if hasattr(self, 'status_label'):
            #     self.status_label.config(text=f"筆畫 {self.stroke_number} 完成")

    def _record_point(self, x, y, pressure=0.1):
        timestamp = time.time()
        self.current_stroke_points.append((self.stroke_number, timestamp, x, y, pressure))

    def get_recorded_data(self):
        return self.strokes_data

    def get_all_canvas_lines(self):
        return self.all_canvas_lines

    def clear_recorder_data(self):
        self.strokes_data = []
        self.current_stroke_points = []
        self.stroke_number = 0
        self.all_canvas_lines = []
        self.current_canvas_line_ids = []
        # if hasattr(self, 'status_label'):
        #     self.status_label.config(text="準備錄製")
        print("錄製器資料已重置。")