import tkinter
import time
from utility import config

# 讓 RecordPlayer 繼承 tkinter.Frame
class RecordPlayer(tkinter.Frame): # <--- 這裡修改
    def __init__(self, master: tkinter.Widget, canvas: tkinter.Canvas): # <--- 接收 master 和 canvas
        super().__init__(master) # <--- 呼叫父類別 Frame 的初始化
        # self.pack() # 如果這個 Frame 需要在 MainGUI 佈局中顯示
        self.canvas = canvas
        self.playback_speed = config.PLAYBACK_SPEED

        # (可選) 如果 player 需要自己的 UI 元素，可以在這裡添加，例如播放控制按鈕
        # self.play_button = tkinter.Button(self, text="播放", command=self._internal_play)
        # self.play_button.pack(side=tkinter.LEFT)

    # ... 其他方法保持不變 ...
    # play_strokes, redraw_loaded_data
    # 這些方法的核心邏輯不變，因為它們仍然操作傳入的 self.canvas
    def play_strokes(self, all_canvas_lines: list):
        if not all_canvas_lines:
            print("沒有筆畫可以播放。")
            return

        for stroke_lines in all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="")
        self.canvas.update()
        time.sleep(0.5)

        print("開始播放筆順...")
        for stroke_lines in all_canvas_lines:
            for line_id in stroke_lines:
                self.canvas.itemconfig(line_id, fill="red")
                self.canvas.update()
                time.sleep(self.playback_speed)
        print("筆順播放完畢。")

    def redraw_loaded_data(self, loaded_data: list):
        self.canvas.delete("drawing_stroke")
        if not loaded_data:
            print("沒有載入的資料可以重新繪製。")
            return []

        all_lines_on_canvas = []
        current_stroke_lines = []
        prev_stroke_num = None
        prev_x, prev_y = None, None

        for i, (stroke_num, _, x, y, _) in enumerate(loaded_data):
            if prev_stroke_num is None:
                prev_x, prev_y = x, y
                prev_stroke_num = stroke_num
                current_stroke_lines = []
                continue

            if stroke_num != prev_stroke_num:
                all_lines_on_canvas.append(current_stroke_lines)
                current_stroke_lines = []
                prev_x, prev_y = x, y
                prev_stroke_num = stroke_num
                continue

            line_id = self.canvas.create_line(
                prev_x, prev_y, x, y,
                fill="red", width=3, capstyle=tkinter.ROUND, smooth=tkinter.TRUE, tags="drawing_stroke"
            )
            current_stroke_lines.append(line_id)
            prev_x, prev_y = x, y

        if current_stroke_lines:
            all_lines_on_canvas.append(current_stroke_lines)

        print(f"已從載入資料重新繪製 {len(all_lines_on_canvas)} 個筆畫。")
        return all_lines_on_canvas