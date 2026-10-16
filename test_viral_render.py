import sys
import os
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from schemas.contracts import AudioManifest, VisualManifest
from agents.tung_editor import TungVideoEditor

def main():
    json_path = os.path.abspath("./storage/project_b188f98c.json")
    print(f"[TEST RUN] Nạp dữ liệu dự án từ: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    audio_manifest = AudioManifest.model_validate(data["audio_manifest"])
    visual_manifest = VisualManifest.model_validate(data["visual_manifest"])

    # Chọn 4 shots đầu tiên (Đoạn Hook cao trào) để test tốc độ và đánh giá kỹ thuật viral
    visual_manifest.shots = visual_manifest.shots[:4]
    audio_manifest.scene_audios = audio_manifest.scene_audios[:2]

    scenes_map = {s["scene_id"]: s["spoken_text"] for s in data["master_script"]["scenes"]}
    for idx, shot in enumerate(visual_manifest.shots):
        text = scenes_map.get(shot.scene_id, "")
        words = text.split()
        if len(words) > 6:
            shot.on_screen_text = " ".join(words[:6]).upper()
        else:
            shot.on_screen_text = text.upper()

    print(f"\n🚀 Khởi chạy Agent Tùng với kỹ thuật Ken Burns Zoom & Word Highlighting Subtitles...")
    tung = TungVideoEditor()
    final_video = tung.assemble_final_video(
        project_id="viral_test_v1",
        audio_manifest=audio_manifest,
        visual_manifest=visual_manifest,
        output_filename="viral_retention_video.mp4"
    )
    print("\n================== HOÀN TẤT RENDER VIDEO VIRAL ==================")
    print(f"Video thành phẩm: {final_video}")
    print(f"Dung lượng: {os.path.getsize(final_video) / (1024*1024):.2f} MB")
    print("==================================================================")

if __name__ == "__main__":
    main()
