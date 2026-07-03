import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# 1. Khởi tạo Client Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Không tìm thấy GEMINI_API_KEY trong file .env!")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    # 2. Lấy trực tiếp danh sách tất cả các file ông đã upload lên Gemini Cloud trước đó
    print("🔄 Đang đồng bộ danh sách tri thức từ Gemini Cloud...")
    cloud_files = list(client.files.list())
    
    if not cloud_files:
        print("❌ Không tìm thấy file nào trên Cloud! Hãy chạy main.py để upload dữ liệu lên trước.")
        exit(1)
        
    print(f"✅ Đã kết nối thành công với {len(cloud_files)} file tri thức trên Cloud để làm RAG.")

    # 3. Định nghĩa câu hỏi bắt buộc theo đề bài
    query = "How do I add a YouTube video?"

    # 4. Gọi Model kèm theo danh sách file làm ngữ cảnh (Context)
    # Truyền đống file từ cloud_files vào tham số contents cùng với câu hỏi
    print("🤖 OptiBot đang xử lý câu hỏi...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[*cloud_files, query],
        config=types.GenerateContentConfig(
            system_instruction="""You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.""",
            temperature=0.2
        )
    )

    print("\n================ KẾT QUẢ TRẢ LỜI CỦA OPTIBOT ================")
    print(response.text)
    print("=============================================================")

except Exception as e:
    print(f"❌ Có lỗi xảy ra khi kết nối API: {e}")