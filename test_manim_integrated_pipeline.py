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

from schemas.contracts import AudioManifest, VisualManifest, VisualShot
from agents.tung_editor import TungVideoEditor
from agents.hoang_manager_qa import evaluate_rendered_video

def main():
    json_path = os.path.abspath("./storage/project_b188f98c.json")
    print(f"============================================================")
    print(f"🚀 [MANIM + REMOTION + STOCK HYBRID] KHỞI CHẠY STUDIO...")
    print(f"============================================================")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    audio_manifest = AudioManifest.model_validate(data["audio_manifest"])
    audio_manifest.scene_audios = audio_manifest.scene_audios[:2]

    # Cấu hình chuỗi phân cảnh kết hợp đỉnh cao:
    # Shot 1: MANIM VECTOR MOTION GRAPHICS (Trim Paths & Neural Network Morphing)
    # Shot 2: STOCK B-ROLL VIDEO (Footage thực tế AI)
    # Shot 3: 3D CAMERA PARALLAX (Tách lớp đa tầng)
    # Shot 4: MANIM VECTOR MOTION GRAPHICS (Kinetic Callout)
    shots_data = [
        VisualShot(
            shot_id="manim_shot_01",
            scene_id="scene_01",
            source_type="MANIM_MOTION_GRAPHIC",
            asset_filepath="",
            duration_ms=4000,
            camera_effect="zoom_in",
            on_screen_text="AI THAY ĐỔI TOÀN BỘ THẾ GIỚI",
            motion_style="manim_vector",
            hud_accents=["brackets", "progress_bar", "tag"]
        ),
        VisualShot(
            shot_id="stock_shot_02",
            scene_id="scene_01",
            source_type="STOCK_VIDEO",
            asset_filepath="",
            duration_ms=3920,
            camera_effect="zoom_in",
            on_screen_text="BỘ NÃO NHÂN TẠO ĐỘT PHÁ",
            motion_style="stock_broll_motion",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="parallax_shot_03",
            scene_id="scene_02",
            source_type="AI_IMAGE_KEN_BURNS",
            asset_filepath="",
            duration_ms=4820,
            camera_effect="zoom_in",
            on_screen_text="KỶ NGUYÊN TỰ ĐỘNG HÓA",
            motion_style="parallax_3d",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="manim_shot_04",
            scene_id="scene_02",
            source_type="MANIM_MOTION_GRAPHIC",
            asset_filepath="",
            duration_ms=4830,
            camera_effect="zoom_in",
            on_screen_text="BẠN ĐÃ SẴN SÀNG CHƯA",
            motion_style="manim_vector",
            hud_accents=["brackets", "progress_bar", "tag"]
        )
    ]

    visual_manifest = VisualManifest(
        visual_style_prompt_prefix="futuristic artificial intelligence technology cyber",
        shots=shots_data
    )

    print(f"\n🎬 Danh sách phân cảnh cấu hình Hybrid:")
    for i, s in enumerate(visual_manifest.shots):
        print(f"   Shot #{i+1}: Source={s.source_type:20} | Style={s.motion_style:16} | Dur={s.duration_ms/1000:.2f}s | Text='{s.on_screen_text}'")

    tung = TungVideoEditor()
    final_video = tung.assemble_final_video(
        project_id="manim_hybrid_v1",
        audio_manifest=audio_manifest,
        visual_manifest=visual_manifest,
        output_filename="manim_motion_master.mp4"
    )

    print(f"\n============================================================")
    print(f"🔍 [HOÀNG QA LEAD] THẨM ĐỊNH ĐỊNH LƯỢNG VIDEO...")
    print(f"============================================================")
    eval_res = evaluate_rendered_video(final_video, visual_manifest, audio_manifest)
    print(json.dumps(eval_res, indent=2, ensure_ascii=False))

    print(f"\n✅ ĐÃ HOÀN TẤT RENDER & QA THÀNH CÔNG!")
    print(f"File video thành phẩm: {final_video}")

if __name__ == "__main__":
    main()
