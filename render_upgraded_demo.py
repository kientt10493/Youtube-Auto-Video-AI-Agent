import sys
import os
import json

# Khởi tạo mã hóa UTF-8 cho toàn bộ output trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Đảm bảo PATH có ffmpeg
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from schemas.contracts import AudioManifest, VisualManifest
from agents.tung_editor import TungVideoEditor

def main():
    json_path = os.path.abspath("./storage/project_b188f98c.json")
    print(f"Loading cached project data from: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    audio_manifest = AudioManifest.model_validate(data["audio_manifest"])
    visual_manifest = VisualManifest.model_validate(data["visual_manifest"])

    # Bổ sung phụ đề động chữ lớn nổi bật cho từng shot
    scenes_map = {s["scene_id"]: s["spoken_text"] for s in data["master_script"]["scenes"]}
    for idx, shot in enumerate(visual_manifest.shots):
        text = scenes_map.get(shot.scene_id, "")
        words = text.split()
        if len(words) > 6:
            # Chọn cụm từ điểm nhấn cho shot
            chunk = " ".join(words[:7])
            shot.on_screen_text = chunk.upper()
        else:
            shot.on_screen_text = text.upper()

    print(f"Bắt đầu render video nâng cấp với {len(visual_manifest.shots)} phân cảnh...")
    tung = TungVideoEditor()
    final_video = tung.assemble_final_video(
        project_id="b188f98c_v2",
        audio_manifest=audio_manifest,
        visual_manifest=visual_manifest,
        output_filename="engaging_pro_video.mp4"
    )
    print("\n================== HOÀN TẤT RENDER VIDEO ==================")
    print(f"Video thành phẩm: {final_video}")
    print(f"Dung lượng file: {os.path.getsize(final_video) / (1024*1024):.2f} MB")
    print("============================================================")

if __name__ == "__main__":
    main()
