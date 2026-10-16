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
    print(f"🚀 [ENVATO MOTION DESIGN TEST] CHU TRÌNH TỐI ƯU HÓA HOÀN CHỈNH...")
    print(f"============================================================")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    audio_manifest = AudioManifest.model_validate(data["audio_manifest"])
    # Chỉ lấy 2 cảnh đầu để tối ưu tốc độ test hook (tổng ~17.5s)
    audio_manifest.scene_audios = audio_manifest.scene_audios[:2]

    # THỰC THI QUY TẮC 2.5 GIÂY (THE 2.5-SECOND RULE):
    # Chia 2 cảnh dài thành 7 visual shots liên tiếp (trung bình 2.5s/shot)
    # Xen kẽ đa dạng: Stock Video -> 3D Parallax -> Ken Burns Bézier
    shots_data = [
        # Scene 1: 7920ms (Chia làm 3 shots)
        VisualShot(
            shot_id="shot_01_a",
            scene_id="scene_01",
            source_type="STOCK_VIDEO",
            asset_filepath="",
            duration_ms=2640,
            camera_effect="zoom_in",
            on_screen_text="AI ĐANG THAY ĐỔI TOÀN BỘ THẾ GIỚI",
            motion_style="stock_broll_motion",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="shot_01_b",
            scene_id="scene_01",
            source_type="AI_IMAGE_KEN_BURNS",
            asset_filepath="",
            duration_ms=2640,
            camera_effect="zoom_in",
            on_screen_text="BỘ NÃO NHÂN TẠO ĐỘT PHÁ",
            motion_style="parallax_3d",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="shot_01_c",
            scene_id="scene_01",
            source_type="AI_IMAGE_KEN_BURNS",
            asset_filepath="",
            duration_ms=2640,
            camera_effect="pan_left",
            on_screen_text="TỐC ĐỘ XỬ LÝ KHỦNG KHIẾP",
            motion_style="ken_burns_eased",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        # Scene 2: 9650ms (Chia làm 4 shots)
        VisualShot(
            shot_id="shot_02_a",
            scene_id="scene_02",
            source_type="STOCK_VIDEO",
            asset_filepath="",
            duration_ms=2410,
            camera_effect="zoom_in",
            on_screen_text="MẠNG LƯỚI TOÀN CẦU",
            motion_style="stock_broll_motion",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="shot_02_b",
            scene_id="scene_02",
            source_type="AI_IMAGE_KEN_BURNS",
            asset_filepath="",
            duration_ms=2410,
            camera_effect="zoom_in",
            on_screen_text="KỶ NGUYÊN TỰ ĐỘNG HÓA",
            motion_style="parallax_3d",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="shot_02_c",
            scene_id="scene_02",
            source_type="AI_IMAGE_KEN_BURNS",
            asset_filepath="",
            duration_ms=2410,
            camera_effect="zoom_out",
            on_screen_text="THỜI KHẮC LỊCH SỬ BẮT ĐẦU",
            motion_style="ken_burns_eased",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        ),
        VisualShot(
            shot_id="shot_02_d",
            scene_id="scene_02",
            source_type="STOCK_VIDEO",
            asset_filepath="",
            duration_ms=2420,
            camera_effect="zoom_in",
            on_screen_text="BẠN ĐÃ SẴN SÀNG CHƯA",
            motion_style="stock_broll_motion",
            hud_accents=["brackets", "progress_bar", "tag", "vignette"]
        )
    ]

    visual_manifest = VisualManifest(
        visual_style_prompt_prefix="futuristic artificial intelligence technology cyber",
        shots=shots_data
    )

    print(f"\n🎬 Kế hoạch phân cảnh Motion Graphics & The 2.5s Rule:")
    for i, s in enumerate(visual_manifest.shots):
        print(f"   Shot #{i+1}: Style={s.motion_style:18} | Cam={s.camera_effect:8} | Dur={s.duration_ms/1000:.2f}s | Text='{s.on_screen_text}'")

    tung = TungVideoEditor()
    final_video = tung.assemble_final_video(
        project_id="motion_design_v2",
        audio_manifest=audio_manifest,
        visual_manifest=visual_manifest,
        output_filename="envato_motion_25s_rule.mp4"
    )

    print(f"\n============================================================")
    print(f"🔍 [HOÀNG QA LEAD] TIẾN HÀNH THẨM ĐỊNH ĐỊNH LƯỢNG VIDEO...")
    print(f"============================================================")
    eval_res = evaluate_rendered_video(final_video, visual_manifest, audio_manifest)
    print(json.dumps(eval_res, indent=2, ensure_ascii=False))

    print(f"\n✅ ĐÃ HOÀN TẤT VÒNG LẶP RENDER & QA THÀNH CÔNG!")
    print(f"File video thành phẩm: {final_video}")

if __name__ == "__main__":
    main()
