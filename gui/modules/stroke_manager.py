import tkinter

class StrokeManager:
    def __init__(self, canvas: tkinter.Canvas):
        self.canvas = canvas
        self.current_color = "red"
        self.current_width = 5
        self.replay_tasks = []

    def draw_segment(self, x1, y1, x2, y2):
        """畫出一條線，並回傳該線段的 ID"""
        line_id = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=self.current_color,
            width=self.current_width,
            capstyle=tkinter.ROUND, smooth=tkinter.TRUE,
            tags="user_drawn_stroke",
        )
        return line_id


    def set_stroke_visibility(self, stroke_ids, visible=True):
        state = 'normal' if visible else 'hidden'
        for item_id in stroke_ids:
            self.canvas.itemconfigure(item_id, state=state)


    def delete_stroke(self, stroke_ids):
        for item_id in stroke_ids:
            self.canvas.delete(item_id)


    def clear_all_strokes(self):
        self.canvas.delete("user_drawn_stroke")



    # --- 設定相關 ---
    def set_color(self, color):
        self.current_color = color


    def set_width(self, width):
        self.current_width = width
        
        
    def replay_raw_data(self, raw_data_list):
        self.stop_replay()
        self.clear_all_strokes()
        
        if not raw_data_list or len(raw_data_list) < 2:
                    return
                
        parsed_points = []
        try:
            for row in raw_data_list:
                s_id = int(row[0])
                t = float(row[1])
                x = float(row[2])
                y = float(row[3])
                parsed_points.append((s_id, t, x, y))
        except ValueError as e:
            print(f"資料格式解析錯誤: {e}")
            return

        start_time = parsed_points[0][1]

        for i in range(len(parsed_points) - 1):
            p1 = parsed_points[i]
            p2 = parsed_points[i+1]

            if p1[0] == p2[0]: # 同一筆畫
                
                delay = int((p2[1] - start_time) * 1000)
                
                task_id = self.canvas.after(
                    delay, 
                    lambda x1=p1[2], y1=p1[3], x2=p2[2], y2=p2[3]: 
                        self.draw_segment(x1, y1, x2, y2)
                )
                self.replay_tasks.append(task_id)


    def stop_replay(self):
        """停止所有排程"""
        for task_id in self.replay_tasks:
            self.canvas.after_cancel(task_id)
        self.replay_tasks.clear()