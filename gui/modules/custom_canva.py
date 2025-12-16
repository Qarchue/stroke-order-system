import tkinter
from tkinter import Toplevel, Scale, Button, Label, HORIZONTAL, colorchooser, filedialog
from utility import config, DataProcess
from .stroke_manager import StrokeManager
from .data_handler import DataHandler
import os

class CustomCanva(tkinter.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            width=config.CANVAS_WIDTH, 
            height=config.CANVAS_HEIGHT,
            bg="white",
        )
        
        self.stroke = StrokeManager(self)

        self.history_stack = []
        """儲存所有已完成的筆畫"""

        self.redo_stack = []
        """儲存被 Undo 的筆畫"""
        
        # 當前正在畫的暫存
        self.current_stroke = {
            'stroke_ids': [],
            'points': []
        }
        
        self.replay_data = []
        
        self.stroke_index = 0
        """計算第幾筆"""
        
        self.prev_x, self.prev_y = 0, 0
        

        # --- 事件綁定 ---
        self.bind("<ButtonPress-1>", self.start_stroke)
        self.bind("<B1-Motion>", self.draw_stroke)
        self.bind("<ButtonRelease-1>", self.end_stroke)
        self.bind("<Button-2>", self.open_settings_window)
        
        
        self.bind("<Control-z>", self.on_undo)
        self.bind("<Control-Z>", self.on_redo)
        
        self.bind("<Control-Shift-z>", self.on_redo)
        self.bind("<Control-s>", self.save_data)

        self.bind("<r>", self.replay)
        
        self.focus_set() 


    def start_replay(self):
        default_dir = os.path.join(os.getcwd(), "data", "stroke")
        
        file_path = filedialog.askopenfilename(
            initialdir=default_dir,
            title="請選擇要回放的檔案",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            self.replay_data = DataProcess.load_from_csv(file_path)

            if self.replay_data:
                self.replay()
            else:
                pass


    def replay(self, event: tkinter.Event = None):

        self.stroke.replay_raw_data(self.replay_data)


    def start_stroke(self, event: tkinter.Event):
        self._clear_redo_stack_physically()
        """清除 Redo Stack"""
        self.stroke_index += 1
        
        self.current_stroke = {'stroke_ids': [], 'points': []}
        self.prev_x, self.prev_y = event.x, event.y
        
        first_point = DataHandler.create_point(self.stroke_index, event.x, event.y)
        self.current_stroke['points'].append(first_point)

    def draw_stroke(self, event: tkinter.Event):
        line_id = self.stroke.draw_segment(
            self.prev_x, self.prev_y, event.x, event.y
        )
        point = DataHandler.create_point(self.stroke_index, event.x, event.y)
        
        self.current_stroke['stroke_ids'].append(line_id)
        self.current_stroke['points'].append(point)

        self.prev_x, self.prev_y = event.x, event.y


    def end_stroke(self, event: tkinter.Event):
        if self.current_stroke['stroke_ids']:
            self.history_stack.append(self.current_stroke)
            self.replay_data = [u for poi in self.history_stack for u in poi['points']]
            
            
    def on_undo(self, event):
        if not self.history_stack:
            return
        stroke = self.history_stack.pop()
        self.stroke.set_stroke_visibility(stroke['stroke_ids'], visible=False)
        self.redo_stack.append(stroke)
        

    def on_redo(self, event):
        if not self.redo_stack:
            return
        stroke = self.redo_stack.pop()
        self.stroke.set_stroke_visibility(stroke['stroke_ids'], visible=True)
        self.history_stack.append(stroke)


    def _clear_redo_stack_physically(self):
        """刪除復原暫存"""
        if not self.redo_stack:
            return       
        for stroke in self.redo_stack:
            self.stroke.delete_stroke(stroke['stroke_ids']) 
        self.redo_stack.clear()


    def clear_canvas(self):
        self.stroke.clear_all_strokes()
        self.history_stack.clear()
        self.redo_stack.clear()
        self.current_stroke = {'stroke_ids': [], 'points': []}
        self.stroke_index = 0
        self.history_stack = []
        self.replay_data = []   

    def save_data(self, event=None):
        DataProcess.save_stroke(self.history_stack)





    def open_settings_window(self, event):
        window = Toplevel(self)
        window.title("筆畫設定")
        window.geometry(f"250x150+{event.x_root}+{event.y_root}")
        window.attributes('-topmost', True) 

        Label(window, text="筆畫粗細:").pack(pady=5)
        def update_width(val):
            self.stroke.set_width(float(val))
        scale = Scale(window, from_=1, to=20, orient=HORIZONTAL, command=update_width)
        scale.set(self.stroke.current_width)
        scale.pack(fill="x", padx=20)

        Label(window, text="顏色設定:").pack(pady=5)
        def choose_color():
            color = colorchooser.askcolor(color=self.stroke.current_color)[1]
            if color:
                self.stroke.set_color(color)
                color_btn.config(bg=color)
        color_btn = Button(window, text="選擇顏色", bg=self.stroke.current_color, command=choose_color)
        color_btn.pack(pady=5)
        
        
