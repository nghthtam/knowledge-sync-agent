import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

def sync_delta_to_gemini(delta_files):
    if not delta_files:
        print("⚡ [Uploader] Không có file nào thay đổi (Delta trống). Không cần upload gì thêm!")
        return
        
    client = genai.Client()
    print(f"\n☁️ [Uploader] Đang đồng bộ {len(delta_files)} file thay đổi lên Gemini Cloud...")
    
    try:
        existing_files = list(client.files.list())
    except Exception:
        existing_files = []

    for file_path in delta_files:
        file_name = os.path.basename(file_path)
        
        # Nếu là bài update, tìm và xóa bản cũ trên Cloud trước để tránh trùng dữ liệu
        for remote_file in existing_files:
            if remote_file.display_name == file_name:
                print(f"🧹 Xóa bản cũ của file trên Cloud: {file_name}")
                try:
                    client.files.delete(name=remote_file.name)
                    time.sleep(0.2)
                except Exception:
                    pass

        # Tiến hành nạp bản mới lên
        print(f"🚀 Đang tải lên bản mới: {file_name}...")
        try:
            file_gemini = client.files.upload(file=file_path, mime_type="text/plain")
            time.sleep(0.5) # Chống Rate Limit
        except Exception as e:
            print(f"❌ Lỗi nạp file {file_name}: {e}")

    # Cập nhật lại toàn bộ danh sách URIs mới nhất vào file .env để Bot đọc ngầm
    try:
        all_current_files = client.files.list()
        uris = [f.uri for f in all_current_files if f.name.endswith(".md") or "articles_md" in f.uri]
        uris_string = ",".join(uris)
        
        with open(".env", "r") as f:
            lines = f.readlines()
        lines = [line for line in lines if "GEMINI_FILES_URIS" not in line]
        with open(".env", "w") as f:
            f.writelines(lines)
            f.write(f"\nGEMINI_FILES_URIS={uris_string}")
        print("💾 Đã làm mới danh sách liên kết tài liệu GEMINI_FILES_URIS trong file .env")
    except Exception as e:
        print(f"⚠️ Không thể cập nhật danh sách URI vào .env: {e}")