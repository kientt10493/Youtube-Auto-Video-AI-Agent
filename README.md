# YOUTUBE AI AGENT STUDIO - MULTI-AGENT SYSTEM (V2)

Hệ thống Multi-Agent tự động hóa quy trình sản xuất video YouTube từ A-Z, áp dụng triệt để tư duy quản trị nhân sự số của đội ngũ xAI (Lauren Tan & Peng Zeng).

---

## 👥 DANH SÁCH 8 NHÂN SỰ SỐ (AGENT ROSTER)

1. **Hoàng (Executive Manager & QA Lead):** Giám đốc sản xuất, thẩm định kịch bản khắt khe theo rubric (Hook 30%, Pacing 30%, Fact-check 40%). Chỉ duyệt PASS khi điểm >= 8.5/10.
2. **Minh (Lead Producer & Orchestrator):** Điều phối luồng làm việc, quản lý state và chuyển giao dữ liệu tinh gọn giữa các Agent.
3. **Linh (Trend & Market Researcher):** Nghiên cứu từ khóa, cào dữ liệu đối thủ, phát hiện khoảng trống nội dung (Content Gap).
4. **Khoa (Retention Scriptwriter):** Biên kịch gia tăng tỷ lệ giữ chân (AVD > 65%), cấu trúc Hook 5s, Open Loops, Mini-hooks mỗi 60-90s, cấm văn mẫu AI.
5. **Đạt (Audio & Voice Engineer):** Xử lý giọng đọc TTS, đo đạc thời lượng chính xác từng cảnh (`actual_duration_ms`) bằng FFprobe và tạo Word-level timestamps.
6. **Vân (Visual & Art Director):** Lên kịch bản hình ảnh (Storyboard), tuân thủ quy tắc 4 giây (chuyển cảnh liên tục khớp chính xác mili-giây với giọng đọc).
7. **Tùng (Technical Video Editor):** Biên dịch mã lệnh FFmpeg, ráp video B-Roll, lồng nhạc nền, tự động hạ nhạc nền khi có tiếng nói (Audio Ducking) và xuất file MP4 hoàn chỉnh.
8. **Hà (Growth, Thumbnail & SEO Specialist):** Thiết kế 3 bộ A/B Thumbnail + Title, viết Description chuẩn SEO và gắn Tags.

---

## 📁 CẤU TRÚC DỰ ÁN TẠI `E:\AI\Youtube AI Agent Team`

```
E:\AI\Youtube AI Agent Team\
├── agents/
│   ├── base_agent.py          # Kết nối OpenAI-compatible API (Gemini Web Gateway / 9Router)
│   ├── hoang_manager_qa.py    # Agent Hoàng - QA Lead
│   ├── minh_orchestrator.py   # Agent Minh - Điều phối toàn bộ luồng
│   ├── linh_researcher.py     # Agent Linh - Nghiên cứu thị trường
│   ├── khoa_scriptwriter.py   # Agent Khoa - Viết kịch bản Retention
│   ├── dat_audio.py           # Agent Đạt - Xử lý Audio & Đo actual_duration_ms
│   ├── van_visual.py          # Agent Vân - Storyboard & B-Roll
│   ├── tung_editor.py         # Agent Tùng - FFmpeg Render Engine
│   └── ha_growth_seo.py       # Agent Hà - Thumbnail A/B & SEO
├── schemas/
│   ├── __init__.py
│   └── contracts.py           # Toàn bộ Pydantic Data Contracts (Input/Output ép kiểu chặt chẽ)
├── assets/
│   ├── bgm/                   # Nhạc nền miễn phí bản quyền
│   ├── sfx/                   # Hiệu ứng âm thanh (whoosh, pop, riser...)
│   └── fonts/                 # Phông chữ phụ đề & Thumbnail
├── storage/                   # Dữ liệu dự án đã chạy (.json)
├── output/                    # Video thành phẩm (.mp4)
├── temp/                      # File dựng tạm thời
├── main_api.py                # FastAPI Server (port 8090) kết nối Webhook / n8n
├── test_run.py                # Script chạy thử nghiệm trực tiếp qua Terminal
├── .env                       # Cấu hình Gateway API & Model
└── README.md
```

---

## 🚀 HƯỚNG DẪN CHẠY VÀ SỬ DỤNG

### 1. Kích hoạt môi trường và chạy thử nghiệm
Mở Terminal trong thư mục `E:\AI\Youtube AI Agent Team`:

```powershell
& "e:\AI\notebooklm-venv\Scripts\python.exe" test_run.py "Vì sao đồng hồ Rolex đắt đỏ nhưng ai cũng khao khát sở hữu?"
```

### 2. Khởi chạy FastAPI Server (kết nối n8n hoặc Webhook)
```powershell
& "e:\AI\notebooklm-venv\Scripts\python.exe" main_api.py
```
- Server chạy tại: `http://localhost:8090`
- API Docs: `http://localhost:8090/docs`
- Kích hoạt sản xuất video tự động bằng request POST:
  ```bash
  curl -X POST http://localhost:8090/produce \
    -H "Content-Type: application/json" \
    -d '{"topic": "Bí mật đằng sau sự thành công của chip AI Nvidia"}'
  ```
