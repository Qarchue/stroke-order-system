import tkinter as tk
from PIL import Image, ImageTk

from utility import config
from utility import DataProcessor

from .handwriting_recorder import HandwritingRecorder
from .record_player import RecordPlayer

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._load_background_image()
        self._create_canvas()
        self._initialize_functional_modules()
        self._create_buttons()
        self._bind_events() # 新增：綁定事件

    def _setup_window(self):
        """設定主視窗的基本屬性"""
        self.title("筆順學習系統")
        self.resizable(False, False)

    def _load_background_image(self):
        """載入並準備背景圖片"""
        self.original_image = Image.open(config.BG_IMAGE_PATH)
        self.bg_image = ImageTk.PhotoImage(
            self.original_image.resize((config.CANVAS_WIDTH, config.CANVAS_HEIGHT), Image.LANCZOS)
        )

    def _create_canvas(self):
        """創建並配置繪圖畫布"""
        self.canvas = tk.Canvas(
            self, 
            width=config.CANVAS_WIDTH, 
            height=config.CANVAS_HEIGHT, 
            bg="white"
        )
        
        self.canvas.pack()
        self.canvas.create_image(
            0, 0, 
            image=self.bg_image, 
            anchor=tk.NW, 
            tags="background_image"
        )

    def _initialize_functional_modules(self):
        """實例化錄製器、播放器和資料處理器"""
        self.recorder = HandwritingRecorder(self.canvas)
        self.player = RecordPlayer(self.canvas)
        self.data_processor = DataProcessor()

    def _bind_events(self):
        """綁定滑鼠事件到錄製器的方法"""
        self.canvas.bind("<Button-1>", self.recorder.start_stroke)
        self.canvas.bind("<B1-Motion>", self.recorder.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.recorder.end_stroke)

    def _create_buttons(self):
        """創建並佈局按鈕"""
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.clear_button = tk.Button(button_frame, text="清除筆畫", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="儲存資料", command=self.save_current_data)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(button_frame, text="載入資料", command=self.load_and_redraw_data)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.play_button = tk.Button(button_frame, text="播放筆順", command=self.play_recorded_strokes)
        self.play_button.pack(side=tk.LEFT, padx=5)

    def clear_all(self):
        """清除畫布上的所有筆畫並重置錄製器資料"""
        self.canvas.delete("drawing_stroke")
        self.recorder.clear_recorder_data()
        print("畫布已清除，錄製器資料已重置。")

    def save_current_data(self):
        """儲存錄製器中當前的筆畫資料"""
        recorded_data = self.recorder.get_recorded_data()
        self.data_processor.save_data(recorded_data)

    def load_and_redraw_data(self):
        """從檔案載入資料並重新繪製到畫布上"""
        loaded_data = self.data_processor.load_data()
        if loaded_data:
            self.recorder.all_canvas_lines = self.player.redraw_loaded_data(loaded_data)
            # 重置 recorder 的數據和筆畫編號，以便在載入後可以從正確的狀態繼續錄製
            self.recorder.strokes_data = loaded_data
            # 找到載入數據中最大的筆畫編號，並在此基礎上加1作為下一個筆畫的編號
            self.recorder.stroke_number = max([s[0] for s in loaded_data]) if loaded_data else 0
            print("載入資料後，如果需要繼續錄製，將從載入資料的末尾繼續。")
        else:
            print("沒有載入任何資料。")

    def play_recorded_strokes(self):
        """播放錄製器中已記錄的筆畫"""
        all_lines = self.recorder.get_all_canvas_lines()
        self.player.play_strokes(all_lines)