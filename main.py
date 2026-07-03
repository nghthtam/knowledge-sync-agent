import sys
from scraper import fetch_optisigns_articles
from upload_knowledge import sync_delta_to_gemini

def main():
    print("==================================================")
    print("🚀 BẮT ĐẦU CHẠY TIẾN TRÌNH ĐỒNG BỘ TRI THỨC HÀNG NGÀY")
    print("==================================================")
    
    # Bước 1: Cào dữ liệu và tính toán sự chênh lệch (Delta) dựa trên MD5 Hash
    delta_files, metrics = fetch_optisigns_articles()
    
    # Bước 2: Chỉ upload những file nằm trong vùng Delta lên Gemini Cloud
    sync_delta_to_gemini(delta_files)
    
    # Bước 3: In log thống kê chuẩn chỉ đúng theo barem điểm chấm bài
    print("\n================ KẾT QUẢ JOB SỰ KIỆN ================")
    print(f"📌 Tổng số bài viết THÊM MỚI (Added) : {metrics['added']}")
    print(f"📌 Tổng số bài viết CẬP NHẬT (Updated) : {metrics['updated']}")
    print(f"📌 Tổng số bài viết BỎ QUA (Skipped)   : {metrics['skipped']}")
    print("======================================================")
    print("✅ Tiến trình kết thúc thành công. Exit Code: 0")
    
    # Thoát chương trình với mã trạng thái 0 (Success) theo đúng yêu cầu Docker
    sys.exit(0)

if __name__ == "__main__":
    main()