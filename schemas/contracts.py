from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# 1. OUTPUT CỦA LINH (TREND & MARKET RESEARCHER)
class CompetitorGap(BaseModel):
    video_title: str = Field(description="Tiêu đề video đối thủ có lượt xem cao")
    views_count: int = Field(default=0, description="Số lượt xem ước tính")
    weakness_or_gap: str = Field(description="Điểm yếu hoặc thông tin đối thủ bỏ sót mà ta có thể khai thác")

class ResearchPack(BaseModel):
    chosen_angle: str = Field(description="Góc tiếp cận độc đáo nhất cho video")
    target_keywords: List[str] = Field(description="Bộ từ khóa SEO chính và phụ")
    competitor_analysis: List[CompetitorGap] = Field(description="Phân tích 3-5 đối thủ hàng đầu")
    verified_facts: List[str] = Field(description="Danh sách các số liệu, sự thật đã kiểm chứng để đưa vào kịch bản")

# 2. OUTPUT CỦA KHOA (RETENTION SCRIPTWRITER)
class ScriptScene(BaseModel):
    scene_id: str = Field(description="Mã định danh cảnh, ví dụ: scene_01, scene_02")
    section_type: Literal["HOOK", "INTRO", "BODY", "MINI_HOOK", "PAYOFF", "OUTRO"]
    spoken_text: str = Field(description="Lời thoại chính xác để đọc Voice TTS (không chứa ghi chú kỹ thuật)")
    emotion_tone: Literal["excited", "serious", "curious", "urgent", "calm"] = Field(description="Cảm xúc giọng đọc")
    visual_cue: str = Field(description="Mô tả chi tiết hình ảnh/B-Roll cần hiển thị khớp với lời thoại")
    estimated_duration_sec: int = Field(description="Thời lượng ước tính (giây), lý tưởng từ 3-7 giây mỗi cảnh")

class MasterScript(BaseModel):
    working_title: str = Field(description="Tiêu đề dự kiến của video")
    total_estimated_duration_sec: int = Field(description="Tổng thời lượng dự kiến của toàn bộ video")
    scenes: List[ScriptScene] = Field(description="Danh sách các phân cảnh nối tiếp nhau")

# 3. OUTPUT CỦA HOÀNG (EXECUTIVE MANAGER & QA)
class ScriptQAResult(BaseModel):
    status: Literal["PASS", "REJECT"] = Field(description="Quyết định duyệt hoặc yêu cầu làm lại")
    hook_score: float = Field(description="Điểm 5 giây đầu (thang 10)")
    retention_pacing_score: float = Field(description="Điểm nhịp điệu và giữ chân người xem (thang 10)")
    fact_check_score: float = Field(description="Điểm độ chính xác so với ResearchPack (thang 10)")
    overall_score: float = Field(description="Điểm trung bình tổng hợp (Pass khi >= 8.5)")
    specific_issues: List[str] = Field(default_factory=list, description="Danh sách các scene_id bị lỗi và lý do cụ thể")
    actionable_feedback: str = Field(description="Chỉ dẫn chi tiết để Khoa sửa lại kịch bản ở lần lặp tiếp theo")

# 4. OUTPUT CỦA ĐẠT (AUDIO & VOICE ENGINEER)
class WordTimestamp(BaseModel):
    word: str
    start_ms: int
    end_ms: int

class SceneAudioAsset(BaseModel):
    scene_id: str
    audio_filepath: str = Field(description="Đường dẫn file .wav/.mp3 của cảnh")
    actual_duration_ms: int = Field(description="Thời lượng thực tế đo từ file audio (mili-giây)")
    word_timestamps: List[WordTimestamp] = Field(default_factory=list, description="Tọa độ từng chữ để làm phụ đề động")
    sfx_cue: Optional[str] = Field(default=None, description="Hiệu ứng âm thanh đi kèm: whoosh, pop, riser, glitch")

class AudioManifest(BaseModel):
    background_music_filepath: str
    bgm_mood: str
    total_audio_duration_ms: int
    scene_audios: List[SceneAudioAsset]

# 5. OUTPUT CỦA VÂN (VISUAL & ART DIRECTOR)
class VisualShot(BaseModel):
    shot_id: str
    scene_id: str
    source_type: Literal["STOCK_VIDEO", "AI_IMAGE_KEN_BURNS", "AI_VIDEO", "MANIM_MOTION_GRAPHIC"]
    asset_filepath: str = Field(description="Đường dẫn file .mp4 hoặc .png đã tải/render")
    duration_ms: int = Field(description="Bắt buộc khớp tổng thời lượng với actual_duration_ms của Đạt")
    camera_effect: Literal["zoom_in", "zoom_out", "pan_left", "pan_right", "static"]
    on_screen_text: Optional[str] = Field(default=None, description="Chữ nổi bật hiển thị giữa màn hình")
    motion_style: Optional[str] = Field(default="ken_burns_eased", description="Phong cách motion: stock_broll_motion, ken_burns_eased, parallax_3d, kinetic_collage")
    easing_curve: Optional[str] = Field(default="ease_in_out", description="Đường cong chuyển động: ease_in_out, overshoot_bounce, linear")
    hud_accents: Optional[List[str]] = Field(default_factory=lambda: ["brackets", "progress_bar", "category_tag"])

class VisualManifest(BaseModel):
    visual_style_prompt_prefix: str = Field(description="Cụm từ khóa định hình phong cách chung")
    shots: List[VisualShot]

# 6. OUTPUT CỦA HÀ (GROWTH, THUMBNAIL & SEO)
class ThumbnailVariant(BaseModel):
    variant_name: Literal["A_Curiosity", "B_Fear_Negativity", "C_Direct_Benefit"]
    image_prompt: str = Field(description="Prompt tạo ảnh Flux.1 chi tiết, bố cục rõ ràng")
    thumbnail_text_overlay: str = Field(description="Tối đa 3-4 từ in đậm đánh vào thị giác")
    generated_filepath: Optional[str] = None

class PublishPackage(BaseModel):
    ab_test_titles: List[str] = Field(description="3 tiêu đề khác nhau để chạy YouTube A/B Testing")
    thumbnails: List[ThumbnailVariant]
    seo_description: str = Field(description="Mô tả chứa từ khóa ở 2 dòng đầu + Timestamps tự động")
    tags: List[str]
    category_id: str = Field(default="27", description="ID danh mục YouTube")
