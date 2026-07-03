import os
import requests
import json
import hashlib
from markdownify import markdownify as md

STATE_FILE = "sync_state.json"

def calculate_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def fetch_optisigns_articles():
    print("🔄 [Scraper] Đang tiến hành cào TOÀN BỘ dữ liệu tri thức từ OptiSigns...")
    
    # Anh em mình đổi locale sang endpoint chung hoặc giữ en-us nhưng chạy phân trang
    base_url = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"
    page = 1
    per_page = 100  # Tăng lên tối đa 100 bài/trang cho đỡ tốn lượt gọi API
    
    os.makedirs("articles_md", exist_ok=True)
    current_state = load_state()
    new_state = {}
    
    delta_files = []
    metrics = {"added": 0, "updated": 0, "skipped": 0}
    
    while True:
        url = f"{base_url}?per_page={per_page}&page={page}"
        print(f"📖 Đang quét trang {page}...")
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                print(f"❌ Lỗi gọi API ở trang {page}: {response.status_code}")
                break
                
            data = response.json()
            articles = data.get("articles", [])
            
            # Nếu trang này không còn bài viết nào nữa -> Đã cào hết sạch, thoát vòng lặp!
            if not articles:
                print("🏁 Đã quét hết tất cả các trang bài viết thành công!")
                break
                
            for article in articles:
                # Bỏ qua các bài viết bị ẩn hoặc nháp
                if article.get("draft") is True:
                    continue
                    
                title = article.get("title")
                html_url = article.get("html_url")
                slug = html_url.split("/")[-1]
                body_html = article.get("body")
                
                if body_html:
                    markdown_content = md(body_html, heading_style="ATX")
                    full_content = f"# {title}\n\n{markdown_content}\n\nArticle URL: {html_url}"
                    
                    current_hash = calculate_hash(full_content)
                    file_name = f"{slug}.md"
                    file_path = f"articles_md/{file_name}"
                    
                    if file_name not in current_state:
                        metrics["added"] += 1
                        delta_files.append(file_path)
                        print(f"➕ Bài mới: {file_name}")
                    elif current_state[file_name] != current_hash:
                        metrics["updated"] += 1
                        delta_files.append(file_path)
                        print(f"📝 Bài cập nhật: {file_name}")
                    else:
                        metrics["skipped"] += 1
                    
                    new_state[file_name] = current_hash
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(full_content)
                        
            # Chuyển sang trang tiếp theo
            page += 1
            
        except Exception as e:
            print(f"❌ Gặp sự cố khi cào dữ liệu ở trang {page}: {e}")
            break
                
    save_state(new_state)
    
    print(f"\n📊 [Tổng kết Toàn bộ hệ thống] Added: {metrics['added']} | Updated: {metrics['updated']} | Skipped: {metrics['skipped']}")
    return delta_files, metrics

if __name__ == "__main__":
    fetch_optisigns_articles()