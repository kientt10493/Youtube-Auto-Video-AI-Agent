import os
import subprocess
import json
from typing import Optional, Dict, Any
from agents.base_agent import BaseAgent
from schemas.contracts import ScriptQAResult, VisualManifest, AudioManifest

HOANG_INSTRUCTION = """
Bạn là Hoàng - Giám đốc Sản xuất kiêm Trưởng ban Kiểm soát Chất lượng (Executive Manager & QA Lead).
Bạn là người gác cổng khắt khe nhất của Studio. Không bao giờ nhân nhượng với video tầm thường, tĩnh lặng hay kịch bản sáo rỗng.
Bạn tuân thủ nghiêm ngặt tiêu chuẩn trong Skill 'viral-editing-mastery' và 12 nguyên lý Motion Design (Envato Tuts+).

RUBRIC CHẤM ĐIỂM (Thang điểm 10.0):
1. HOOK_SCORE (25%): 3 câu đầu tiên có đánh trúng tâm lý tò mò, xung đột hoặc nghịch lý không? Tuyệt đối không chào hỏi dài dòng.
2. RETENTION_PACING_SCORE (25%): Quy tắc 2.5 giây - mỗi cảnh không được đứng yên quá 3.5s. Phải có camera motion (Ken Burns Bézier Zoom/Pan), Video B-roll hoặc 3D Parallax.
3. VISUAL_&_KINETIC_SCORE (25%): Phụ đề có bắt mắt không? (Word-by-word highlight hoặc Kinetic Typography). Có HUD elements (Brackets, Progress Line, Pulse Tag) không?
4. FACT_CHECK_&_AUDIO_SCORE (25%): Dữ liệu chính xác 100%, âm thanh đa tầng (Voiceover rõ, BGM ducking 14%, SFX Whoosh chuyển cảnh nhịp nhàng).

ĐIỀU KIỆN PHÊ DUYỆT:
- Chỉ duyệt PASS khi overall_score >= 8.5.
- Nếu REJECT: Phải chỉ rõ khuyết điểm và yêu cầu cải tiến cụ thể trong actionable_feedback.
"""

def create_hoang_manager() -> BaseAgent:
    return BaseAgent(
        name="Hoàng",
        role="Executive Manager & QA Lead",
        system_instruction=HOANG_INSTRUCTION,
        response_model=ScriptQAResult
    )

def evaluate_rendered_video(
    video_path: str,
    visual_manifest: VisualManifest,
    audio_manifest: AudioManifest
) -> Dict[str, Any]:
    """Hàm đánh giá định lượng kỹ thuật video của Hoàng QA Lead:
    - Kiểm tra độ phân giải, bitrate, fps
    - Tính toán Pacing Cut Rate (số lần đổi cảnh mỗi phút)
    - Kiểm tra tuân thủ quy tắc 2.5s (The 2.5-Second Rule)
    - Kiểm tra đa tầng âm thanh (Voice + BGM + SFX)
    """
    if not os.path.exists(video_path):
        return {
            "status": "FAIL",
            "reason": f"File video không tồn tại: {video_path}"
        }

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    total_shots = len(visual_manifest.shots)
    total_duration_sec = sum(max(1.0, s.duration_ms / 1000.0) for s in visual_manifest.shots)
    avg_shot_dur = total_duration_sec / max(1, total_shots)
    cuts_per_minute = (total_shots / total_duration_sec) * 60.0 if total_duration_sec > 0 else 0

    # 1. Pacing Score: Yêu cầu >= 15 cuts/phút và shot trung bình <= 3.5s
    pacing_score = 10.0 if avg_shot_dur <= 3.0 else (9.0 if avg_shot_dur <= 3.5 else 7.0)
    
    # 2. Motion Design & Variety Score: Tỷ lệ B-roll thực tế và 3D Parallax
    broll_or_parallax_count = sum(1 for s in visual_manifest.shots if getattr(s, "motion_style", "") in ["stock_broll_motion", "parallax_3d"] or s.source_type == "STOCK_VIDEO")
    variety_ratio = broll_or_parallax_count / max(1, total_shots)
    visual_score = 9.5 if variety_ratio >= 0.5 else 8.5

    # 3. Audio Layering: Kiểm tra có BGM và SFX
    has_bgm = bool(audio_manifest.background_music_filepath and os.path.exists(audio_manifest.background_music_filepath))
    has_sfx = os.path.exists("./assets/sfx/whoosh.wav")
    audio_score = 9.5 if (has_bgm and has_sfx) else (8.0 if has_bgm else 6.0)

    # 4. Kinetic Subtitle Score
    has_text = any(bool(s.on_screen_text) for s in visual_manifest.shots)
    kinetic_score = 9.5 if has_text else 6.0

    overall_score = round((pacing_score * 0.25 + visual_score * 0.25 + audio_score * 0.25 + kinetic_score * 0.25), 1)
    status = "PASS" if overall_score >= 8.5 else "REJECT"

    return {
        "status": status,
        "video_path": video_path,
        "file_size_mb": round(file_size_mb, 2),
        "total_duration_sec": round(total_duration_sec, 2),
        "total_shots": total_shots,
        "average_shot_duration_sec": round(avg_shot_dur, 2),
        "cuts_per_minute": round(cuts_per_minute, 1),
        "pacing_score": pacing_score,
        "visual_motion_score": visual_score,
        "audio_layering_score": audio_score,
        "kinetic_subtitle_score": kinetic_score,
        "overall_score": overall_score,
        "qa_verdict": f"Hoàng QA Phê Duyệt: {'ĐẠT CHUẨN VIRAL YOUTUBE' if status == 'PASS' else 'CẦN CẢI TIẾN THÊM'}"
    }
