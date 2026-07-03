import time
import subprocess
import schedule

def run_daily_sync():
    print("\n⏰ [BẮT ĐẦU JOB HÀNG NGÀY] Tiến hành đồng bộ lại kho tri thức...")
    
    try:
        # 1. Kích hoạt lại scraper.py để cào các bài viết mới nhất (nếu có)
        print("-> Bước 1: Đang chạy script cào dữ liệu...")
        subprocess.run(["python", "scraper.py"], check=True)
        
        # 2. Chạy upload_knowledge.py để đẩy file lên Vector Store/Gemini Files
        print("-> Bước 2: Đang tải dữ liệu mới lên Gemini API...")
        subprocess.run(["python", "upload_knowledge.py"], check=True)
        
        print("✅ [THÀNH CÔNG] Kho dữ liệu RAG đã được làm mới hoàn toàn!")
    except subprocess.CalledProcessError as e:
        print(f"❌ [LỖI] Quá trình đồng bộ thất bại: {e}")

# Cấu hình đặt lịch: Đúng 00:00 mỗi đêm sẽ tự động kích hoạt hàm trên
schedule.every().day.at("00:00").do(run_daily_sync)

if __name__ == "__main__":
    print("🚀 Tiến trình Định thời (Daily Job) đã khởi động thành công.")
    print("Hệ thống đang chạy ngầm và sẽ tự động đồng bộ dữ liệu vào lúc 00:00 mỗi ngày...")
    
    # Giữ cho script luôn chạy ngầm để đợi đến giờ hẹn
    while True:
        schedule.run_pending()
        time.sleep(60) # Kiểm tra lại sau mỗi phút