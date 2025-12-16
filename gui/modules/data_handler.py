import time
import csv
import os

class DataHandler:

    def create_point(index, x, y, pressure=0.1):
        """
        負責產生格式正確的資料點 (Tuple)
        格式: (第幾筆, 時間戳, x, y, pressure)
        """
        timestamp = time.time()
        return (index, timestamp, x, y, pressure)


    def save_to_csv(all_strokes_history, filename="character_data.csv"):
        """
        接收 CustomCanva 傳來的完整歷史紀錄並存檔
        all_strokes_history 結構預期: [ {'points': [...], ...}, ... ]
        """
        if not all_strokes_history:
            print("沒有資料可以儲存")
            return

        try:
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['stroke_id', 'timestamp', 'x', 'y', 'pressure'])
                
                for stroke in all_strokes_history:
                    for point in stroke['points']:
                        writer.writerow(point)
            
            print(f"資料已成功儲存至 {filename}")
        except Exception as e:
            print(f"儲存 CSV 失敗: {e}")