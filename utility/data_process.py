import csv
import time
import os
class DataProcess:

    @staticmethod
    def save_stroke(all_strokes_history):
        if not all_strokes_history:
            return

        filename = f"data/stroke/{int(time.time())}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['stroke_index', 'timestamp', 'x', 'y', 'pressure'])
            
            for stroke in all_strokes_history:
                for point in stroke['points']:
                    writer.writerow(point)


    @staticmethod
    def load_from_csv(filename):
        
        loaded_data = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    row_list = [row['stroke_index'], row['timestamp'], row['x'], row['y'], row['pressure']]
                    loaded_data.append(row_list)
            return loaded_data
        except Exception as e:
            print(f"讀取錯誤: {e}")
            return []