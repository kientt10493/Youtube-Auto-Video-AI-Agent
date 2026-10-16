import os
import json
import uuid
from typing import Optional, Dict, Any
from agents.linh_researcher import create_linh_researcher
from agents.khoa_scriptwriter import create_khoa_scriptwriter
from agents.hoang_manager_qa import create_hoang_manager
from agents.dat_audio import DatAudioEngineer
from agents.van_visual import create_van_visual
from agents.tung_editor import TungVideoEditor
from agents.ha_growth_seo import create_ha_growth
from schemas.contracts import (
    ResearchPack, MasterScript, ScriptQAResult,
    AudioManifest, VisualManifest, PublishPackage
)

class MinhOrchestrator:
    def __init__(self, max_qa_retries: int = 3):
        self.max_qa_retries = max_qa_retries
        self.linh = create_linh_researcher()
        self.khoa = create_khoa_scriptwriter()
        self.hoang = create_hoang_manager()
        self.dat = DatAudioEngineer()
        self.van = create_van_visual()
        self.tung = TungVideoEditor()
        self.ha = create_ha_growth()

    def run_full_pipeline(self, niche_topic: str) -> Dict[str, Any]:
        project_id = str(uuid.uuid4())[:8]
        print(f"\n==========================================")
        print(f"🎬 [MINH] KHỞI ĐỘNG DỰ ÁN YOUTUBE MỚI: {project_id}")
        print(f"📌 Chủ đề: {niche_topic}")
        print(f"==========================================")

        # GIAI ĐOẠN 1: LINH NGHIÊN CỨU
        print("\n🔍 [BƯỚC 1] Linh (Trend Researcher) đang nghiên cứu thị trường...")
        research_prompt = (
            f"Nghiên cứu thị trường và tìm ra góc tiếp cận đột phá cho chủ đề YouTube sau:\n{niche_topic}\n"
            "Hãy phân tích đối thủ, tìm Content Gap và liệt kê danh sách verified_facts chính xác."
        )
        research_pack: ResearchPack = self.linh.run(research_prompt)
        print(f"   -> Đã chọn góc tiếp cận: {research_pack.chosen_angle}")
        print(f"   -> Từ khóa chính: {', '.join(research_pack.target_keywords[:3])}")

        # GIAI ĐOẠN 2: KHOA VIẾT KỊCH BẢN + HOÀNG KIỂM DUYỆT (QA LOOP)
        master_script: Optional[MasterScript] = None
        qa_result: Optional[ScriptQAResult] = None
        attempt = 0

        while attempt < self.max_qa_retries:
            attempt += 1
            print(f"\n✍️ [BƯỚC 2 - Vòng {attempt}/{self.max_qa_retries}] Khoa (Scriptwriter) đang viết kịch bản...")
            if qa_result is None:
                script_prompt = (
                    f"Dựa trên dữ liệu nghiên cứu sau của Linh, hãy viết kịch bản YouTube Retention hoàn chỉnh:\n"
                    f"{research_pack.model_dump_json(indent=2)}"
                )
            else:
                script_prompt = (
                    f"Kịch bản trước bị HOÀNG REJECT với điểm {qa_result.overall_score}/10.\n"
                    f"Lỗi cụ thể: {qa_result.specific_issues}\n"
                    f"Yêu cầu sửa đổi: {qa_result.actionable_feedback}\n"
                    f"Bản kịch bản cũ:\n{master_script.model_dump_json(indent=2)}\n"
                    f"Hãy sửa lại các scene_id lỗi và xuất lại toàn bộ MasterScript mới."
                )

            master_script = self.khoa.run(script_prompt)
            print(f"   -> Đã tạo kịch bản: '{master_script.working_title}' ({len(master_script.scenes)} cảnh)")

            print("⚖️ [BƯỚC 2.1] Hoàng (Manager & QA) đang thẩm định chất lượng kịch bản...")
            qa_prompt = (
                f"Hãy chấm điểm kịch bản của Khoa so với ResearchPack của Linh:\n"
                f"--- DỮ LIỆU GỐC ---\n{research_pack.model_dump_json(indent=2)}\n"
                f"--- KỊCH BẢN ĐỀ XUẤT ---\n{master_script.model_dump_json(indent=2)}"
            )
            qa_result = self.hoang.run(qa_prompt)
            print(f"   -> Kết quả: {qa_result.status} | Điểm: {qa_result.overall_score}/10 (Hook: {qa_result.hook_score}, Fact-check: {qa_result.fact_check_score})")

            if qa_result.status == "PASS" and qa_result.overall_score >= 8.5:
                print("   ✅ HOÀNG ĐÃ PHÊ DUYỆT KỊCH BẢN!")
                break
            else:
                print(f"   ❌ HOÀNG YÊU CẦU SỬA: {qa_result.actionable_feedback[:100]}...")

        # GIAI ĐOẠN 3: ĐẠT LÀM VOICE & ĐO THỜI LƯỢNG
        print("\n🎙️ [BƯỚC 3] Đạt (Audio Engineer) đang render voiceover & tính actual_duration_ms...")
        audio_manifest = self.dat.process_script(master_script, project_id)
        print(f"   -> Tổng thời lượng âm thanh: {audio_manifest.total_audio_duration_ms / 1000:.1f} giây ({len(audio_manifest.scene_audios)} file thoại)")

        # GIAI ĐOẠN 4: VÂN LÀM STORYBOARD & HÀ LÀM SEO THUMBNAIL (SONG SONG)
        print("\n🎨 [BƯỚC 4] Vân (Art Director) đang dựng Storyboard khớp thời lượng âm thanh...")
        visual_prompt = (
            f"Dựa trên MasterScript và AudioManifest sau, hãy thiết kế các VisualShot khớp chính xác thời lượng:\n"
            f"--- MASTER SCRIPT ---\n{master_script.model_dump_json(indent=2)}\n"
            f"--- AUDIO MANIFEST (THỜI LƯỢNG THỰC TẾ) ---\n{audio_manifest.model_dump_json(indent=2)}"
        )
        visual_manifest: VisualManifest = self.van.run(visual_prompt)
        print(f"   -> Đã tạo {len(visual_manifest.shots)} VisualShot hình ảnh/B-Roll")

        print("\n📈 [BƯỚC 5] Hà (SEO & Growth) đang tạo 3 phương án A/B Thumbnail & Description...")
        seo_prompt = (
            f"Thiết kế 3 Thumbnail A/B Testing và bộ SEO YouTube tối ưu CTR cho video sau:\n"
            f"Tiêu đề dự kiến: {master_script.working_title}\n"
            f"Từ khóa: {', '.join(research_pack.target_keywords)}\n"
            f"Kịch bản tóm tắt: {master_script.scenes[0].spoken_text}"
        )
        publish_package: PublishPackage = self.ha.run(seo_prompt)
        print(f"   -> Đã tạo 3 bộ A/B Titles: {publish_package.ab_test_titles}")

        # GIAI ĐOẠN 5: TÙNG ASSEMBLE VIDEO
        print("\n🎞️ [BƯỚC 6] Tùng (Technical Editor) đang dựng và render video thành phẩm bằng FFmpeg...")
        final_video_file = self.tung.assemble_final_video(project_id, audio_manifest, visual_manifest)
        print(f"   -> 🎬 VIDEO HOÀN TẤT TẠI: {final_video_file}")

        # LƯU TOÀN BỘ PROJECT PACKAGE
        project_data = {
            "project_id": project_id,
            "niche_topic": niche_topic,
            "research_pack": research_pack.model_dump(),
            "master_script": master_script.model_dump(),
            "qa_result": qa_result.model_dump() if qa_result else None,
            "audio_manifest": audio_manifest.model_dump(),
            "visual_manifest": visual_manifest.model_dump(),
            "publish_package": publish_package.model_dump(),
            "final_video_path": final_video_file,
        }

        save_path = f"./storage/project_{project_id}.json"
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)

        print(f"\n✨ TOÀN BỘ DỰ ÁN ĐÃ ĐƯỢC ĐÓNG GÓI VÀO: {save_path}")
        return project_data
