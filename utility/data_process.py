import csv
import os
from utility import config

class DataProcessor:
    def __init__(self):
        output_dir = os.path.dirname(config.OUTPUT_CSV_PATH)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save_data(self, strokes_data: list):
        if not strokes_data:
            print("沒有筆畫資料可以儲存。")
            return False

        with open(config.OUTPUT_CSV_PATH, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["stroke_num", "timestamp", "x", "y", "pressure"])
            writer.writerows(strokes_data)

        print(f"資料已儲存到 {config.OUTPUT_CSV_PATH}")
        print("儲存的資料範例 (前5筆):")
        for i, data in enumerate(strokes_data[:5]):
            print(data)
        if len(strokes_data) > 5:
            print("...")
        return True

    def load_data(self) -> list:
        if not os.path.exists(config.OUTPUT_CSV_PATH):
            print("沒有找到筆畫資料檔案。")
            return []

        loaded_data = []
        with open(config.OUTPUT_CSV_PATH, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                try:
                    stroke_num = int(row[0])
                    timestamp = float(row[1])
                    x = int(row[2])
                    y = int(row[3])
                    pressure = float(row[4])
                    loaded_data.append((stroke_num, timestamp, x, y, pressure))
                except (ValueError, IndexError) as e:
                    print(f"讀取資料時發生錯誤：{e}，跳過此行：{row}")
                    continue
        print(f"資料已從 {config.OUTPUT_CSV_PATH} 載入。")
        return loaded_data