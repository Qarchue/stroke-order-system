import tkinter
from PIL import Image, ImageTk

from utility import config
from utility import DataProcess

from .modules.buttons import ClearBtn, ReplayBtn
from .modules.custom_canva import CustomCanva

class MainGUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._load_background_image()
        self._create_canvas()
        self._create_buttons()
        
    def _setup_window(self):
        self.title("筆順學習系統")
        self.resizable(False, False)

    def _load_background_image(self):
        self.original_image = Image.open('gui/tianzige.png')
        self.bg_image = ImageTk.PhotoImage(
            self.original_image.resize(
                (config.CANVAS_WIDTH, config.CANVAS_HEIGHT), 
                Image.LANCZOS,
            )
        )
        
        
    def _create_canvas(self):
        self.canva = CustomCanva(self)

        self.canva.pack()
        self.canva.create_image(
            0, 0, 
            image=self.bg_image, 
            anchor=tkinter.NW, 
            tags="background_image"
        )


    def _create_buttons(self):
            """新增：建立按鈕區域"""
            # 1. 建立一個容器 Frame，放在畫布下方
            btn_frame = tkinter.Frame(self)
            btn_frame.pack(side="bottom", pady=20)

            # 2. 實例化清除按鈕 (傳入 btn_frame 作為父容器，self.canva 作為控制對象)
            self.btn_clear = ClearBtn(btn_frame, self.canva)
            self.btn_clear.pack(side="left", padx=20)

            # 3. 實例化回放按鈕
            self.btn_replay = ReplayBtn(btn_frame, self.canva)
            self.btn_replay.pack(side="left", padx=20)