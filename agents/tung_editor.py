import os
import subprocess
import hashlib
import math
from typing import Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from schemas.contracts import AudioManifest, VisualManifest, VisualShot
from agents.media_downloader import MediaDownloader
from agents.manim_generator import ManimMotionGenerator

# ==========================================
# 12 PRINCIPLES OF MOTION DESIGN: EASING FUNCTIONS
# ==========================================
def ease_in_out_cubic(p: float) -> float:
    """Đường cong Bézier mượt mà (Slow In & Slow Out) - Triệt tiêu chuyển động tuyến tính thô cứng."""
    p = max(0.0, min(1.0, p))
    return 3 * (p ** 2) - 2 * (p ** 3)

def ease_out_back(p: float, s: float = 1.70158) -> float:
    """Hiệu ứng đàn hồi nảy quá đà (Overshoot Bounce) từ After Effects - Dành cho Pop-in text & graphics."""
    p = max(0.0, min(1.0, p))
    return (p - 1) * (p - 1) * ((s + 1) * (p - 1) + s) + 1

def ease_out_quad(p: float) -> float:
    """Giảm tốc êm ái về điểm dừng."""
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) * (1 - p)


class TungVideoEditor:
    """Agent Tùng - Technical Video Editor (Motion Graphics & Viral Retention Edition):
    - Triệt để thực thi 12 nguyên lý Animation & Motion Graphics (Envato Tuts+).
    - Không dùng chuyển động tuyến tính: Áp dụng Easing Bézier Curves & Overshoot Bounce.
    - Công nghệ 3D Multi-Plane Parallax Camera mô phỏng After Effects (Tách lớp Background mờ & Midground sắc nét).
    - Kinetic Typography: Word-by-Word Highlight với nền kính mờ bo tròn (Frosted Glass Badge).
    - HUD Tech Elements: Corner Reticle Brackets `[  ]`, Top Progress Line, Category Badge with Pulse Indicator.
    - Layered Sound Design: Hòa âm đa tầng (Voiceover -6dB, BGM Ducking 14%, Transition SFX Whooshes).
    """

    def __init__(self, temp_dir: str = "./temp", output_dir: str = "./output"):
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.downloader = MediaDownloader()
        self.manim_gen = ManimMotionGenerator(temp_dir=os.path.join(self.temp_dir, "manim_build"))
        
        # Thư mục B-Roll cục bộ dự trữ
        self.local_broll_dir = os.path.abspath("./assets/broll_library")
        os.makedirs(self.local_broll_dir, exist_ok=True)
        
        # Thư mục SFX
        self.sfx_dir = os.path.abspath("./assets/sfx")
        
        # Đường dẫn font chữ tiếng Việt chuẩn trên Windows
        self.font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
        ]
        self.primary_font = None
        for fp in self.font_paths:
            if os.path.exists(fp):
                self.primary_font = fp
                break

    def _get_font(self, size: int):
        if self.primary_font:
            try:
                return ImageFont.truetype(self.primary_font, size)
            except Exception:
                pass
        return ImageFont.load_default()

    def create_motion_graphic_frame(
        self,
        base_image: Image.Image,
        headline_text: str,
        output_image_path: str,
        tag_label: str = "TIÊU ĐIỂM",
        progress: float = 0.0,
        highlight_idx: int = 0,
        hud_accents: Optional[List[str]] = None
    ) -> str:
        """Tạo khung hình 1920x1080 với bố cục Motion Graphics chuẩn Envato:
        - Corner Brackets [  ] phong cách Cyberpunk / Modern Documentary
        - Top Scene Progress Bar
        - Tag Badge với Pulse Dot
        - Word-by-Word Highlight Subtitle Box với Frosted Glass effect
        """
        target_w, target_h = 1920, 1080
        if hud_accents is None:
            hud_accents = ["brackets", "progress_bar", "tag", "vignette"]

        # Đảm bảo base_image đúng tỷ lệ 1920x1080
        img_ratio = base_image.width / base_image.height
        target_ratio = target_w / target_h
        if img_ratio > target_ratio:
            new_h = target_h
            new_w = int(target_h * img_ratio)
        else:
            new_w = target_w
            new_h = int(target_w / img_ratio)
        resized_bg = base_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        cropped_bg = resized_bg.crop((left, top, left + target_w, top + target_h))

        # Khởi tạo overlay trong suốt
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # 1. Gradient Vignette & Darkening phía dưới và trên
        if "vignette" in hud_accents:
            gradient_h = 420
            for i in range(gradient_h):
                alpha = int(220 * (i / gradient_h))
                y = target_h - gradient_h + i
                draw_ov.line([(0, y), (target_w, y)], fill=(8, 12, 22, alpha))
            
            top_grad_h = 130
            for i in range(top_grad_h):
                alpha = int(140 * (1 - i / top_grad_h))
                draw_ov.line([(0, i), (target_w, i)], fill=(8, 12, 22, alpha))

        # 2. Tech Corner Brackets [  ] (Bố cục dẫn hướng mắt - Staging Principle)
        if "brackets" in hud_accents:
            b_pad_x, b_pad_y = 60, 50
            b_len, b_thick = 32, 3
            bracket_color = (6, 182, 212, 175) # Cyber Cyan

            # Top-Left Bracket
            draw_ov.line([(b_pad_x, b_pad_y), (b_pad_x + b_len, b_pad_y)], fill=bracket_color, width=b_thick)
            draw_ov.line([(b_pad_x, b_pad_y), (b_pad_x, b_pad_y + b_len)], fill=bracket_color, width=b_thick)
            # Top-Right Bracket
            draw_ov.line([(target_w - b_pad_x, b_pad_y), (target_w - b_pad_x - b_len, b_pad_y)], fill=bracket_color, width=b_thick)
            draw_ov.line([(target_w - b_pad_x, b_pad_y), (target_w - b_pad_x, b_pad_y + b_len)], fill=bracket_color, width=b_thick)
            # Bottom-Left Bracket
            draw_ov.line([(b_pad_x, target_h - b_pad_y), (b_pad_x + b_len, target_h - b_pad_y)], fill=bracket_color, width=b_thick)
            draw_ov.line([(b_pad_x, target_h - b_pad_y), (b_pad_x, target_h - b_pad_y - b_len)], fill=bracket_color, width=b_thick)
            # Bottom-Right Bracket
            draw_ov.line([(target_w - b_pad_x, target_h - b_pad_y), (target_w - b_pad_x - b_len, target_h - b_pad_y)], fill=bracket_color, width=b_thick)
            draw_ov.line([(target_w - b_pad_x, target_h - b_pad_y), (target_w - b_pad_x, target_h - b_pad_y - b_len)], fill=bracket_color, width=b_thick)

        # 3. Top Progress Line (Secondary Action & Viewer Pacing)
        if "progress_bar" in hud_accents:
            prog_w = int(target_w * max(0.01, min(1.0, progress)))
            draw_ov.line([(0, 2), (target_w, 2)], fill=(255, 255, 255, 30), width=4)
            draw_ov.line([(0, 2), (prog_w, 2)], fill=(6, 182, 212, 240), width=4)

        base_rgba = cropped_bg.convert("RGBA")
        combined = Image.alpha_composite(base_rgba, overlay)
        draw = ImageDraw.Draw(combined)

        # 4. Category Tag Badge góc trên bên trái
        if "tag" in hud_accents and tag_label:
            tag_font = self._get_font(26)
            tag_text = f"● {tag_label.upper()}"
            tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
            tag_w = tag_bbox[2] - tag_bbox[0]
            tag_h = tag_bbox[3] - tag_bbox[1]
            
            tag_x, tag_y = 110, 60
            pad_x, pad_y = 18, 8
            # Nền kính mờ sẫm màu với viền đỏ nổi bật
            draw.rounded_rectangle(
                [tag_x, tag_y, tag_x + tag_w + 2 * pad_x, tag_y + tag_h + 2 * pad_y],
                radius=10,
                fill=(15, 23, 42, 230),
                outline=(220, 38, 38, 220),
                width=2
            )
            draw.text((tag_x + pad_x, tag_y + pad_y), tag_text, font=tag_font, fill=(255, 255, 255, 255))

        # 5. Kinetic Typography & Word Highlighting Subtitle Box
        clean_text = headline_text.strip()
        if clean_text:
            sub_font = self._get_font(52)
            words = clean_text.split()[:8]
            
            word_boxes = []
            for w in words:
                bbox = draw.textbbox((0, 0), w + " ", font=sub_font)
                word_boxes.append(bbox[2] - bbox[0])
            
            total_w = sum(word_boxes)
            start_x = (target_w - total_w) // 2
            start_y = target_h - 150
            
            # Khung kính mờ tối màu bao quanh cụm từ
            pad_box_x, pad_box_y = 36, 18
            draw.rounded_rectangle(
                [start_x - pad_box_x, start_y - pad_box_y, start_x + total_w + pad_box_x, start_y + 65 + pad_box_y],
                radius=20,
                fill=(8, 12, 22, 225),
                outline=(255, 255, 255, 55),
                width=2
            )
            
            # Vẽ từng từ: highlight từ đang nói bằng màu vàng neon rực rỡ
            cur_x = start_x
            active_pos = highlight_idx % max(1, len(words))
            for i, w in enumerate(words):
                if i == active_pos:
                    # Nền pill sáng nhẹ phía sau từ được highlight
                    w_w = word_boxes[i]
                    draw.rounded_rectangle(
                        [cur_x - 6, start_y - 4, cur_x + w_w - 4, start_y + 60],
                        radius=8,
                        fill=(255, 230, 0, 40)
                    )
                    draw.text((cur_x, start_y), w, font=sub_font, fill=(255, 230, 0, 255))
                else:
                    draw.text((cur_x, start_y), w, font=sub_font, fill=(245, 245, 245, 215))
                cur_x += word_boxes[i]

        final_rgb = combined.convert("RGB")
        final_rgb.save(output_image_path, quality=95)
        return output_image_path

    def render_motion_stock_video_clip(
        self,
        stock_video_path: str,
        headline_text: str,
        duration_sec: float,
        output_clip_path: str,
        tag_label: str = "TIÊU ĐIỂM",
        fps: int = 25
    ) -> str:
        """Render 1 clip từ Video B-roll chuyển động thực tế kết hợp HUD Motion Graphics."""
        frames_dir = os.path.join(self.temp_dir, "vid_extract_tmp")
        styled_dir = os.path.join(self.temp_dir, "vid_styled_tmp")
        for d in [frames_dir, styled_dir]:
            if os.path.exists(d):
                for f in os.listdir(d):
                    try: os.remove(os.path.join(d, f))
                    except Exception: pass
            os.makedirs(d, exist_ok=True)

        # 1. Trích xuất frame từ video B-roll
        cmd_extract = [
            "ffmpeg", "-y",
            "-ss", "0", "-t", str(duration_sec),
            "-i", stock_video_path,
            "-r", str(fps),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
            os.path.join(frames_dir, "frame_%04d.jpg")
        ]
        subprocess.run(cmd_extract, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
        if not frame_files:
            raise RuntimeError("Không trích xuất được frame nào từ video stock!")

        words = headline_text.split()[:8]
        num_words = max(1, len(words))

        for idx, f in enumerate(frame_files):
            prog = idx / max(1, len(frame_files) - 1)
            active_idx = int(prog * num_words)
            raw_frame_path = os.path.join(frames_dir, f)
            styled_frame_path = os.path.join(styled_dir, f)
            
            with Image.open(raw_frame_path) as base_img:
                self.create_motion_graphic_frame(
                    base_image=base_img,
                    headline_text=headline_text,
                    output_image_path=styled_frame_path,
                    tag_label=tag_label,
                    progress=prog,
                    highlight_idx=active_idx
                )

        # 2. Đóng gói lại thành MP4
        cmd_pack = [
            "ffmpeg", "-y",
            "-r", str(fps),
            "-i", os.path.join(styled_dir, "frame_%04d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_clip_path
        ]
        subprocess.run(cmd_pack, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_clip_path

    def render_parallax_3d_clip(
        self,
        base_image_path: str,
        headline_text: str,
        duration_sec: float,
        output_clip_path: str,
        tag_label: str = "3D FOCUS",
        fps: int = 25
    ) -> str:
        """Kỹ thuật 3D Camera Parallax (After Effects 3D Layer Separation):
        - Layer 1 (Background): Zoom chậm 1.08x -> 1.16x, làm mờ nhẹ (GaussianBlur) tạo độ sâu.
        - Layer 2 (Midground Card): Card sắc nét với viền Cyber Cyan nổi khối, zoom từ 0.94x -> 1.03x ngược pha.
        - Layer 3 (Foreground): HUD Corner Brackets & Kinetic Typography đứng vững trên đỉnh.
        """
        frames_dir = os.path.join(self.temp_dir, "parallax_tmp_frames")
        if os.path.exists(frames_dir):
            for f in os.listdir(frames_dir):
                try: os.remove(os.path.join(frames_dir, f))
                except Exception: pass
        os.makedirs(frames_dir, exist_ok=True)

        target_w, target_h = 1920, 1080
        total_frames = max(10, int(duration_sec * fps))

        try:
            raw_img = Image.open(base_image_path).convert("RGB")
        except Exception:
            raw_img = Image.new("RGB", (target_w, target_h), (15, 23, 42))

        # Chuẩn hóa ảnh gốc 1920x1080
        img_ratio = raw_img.width / raw_img.height
        target_ratio = target_w / target_h
        if img_ratio > target_ratio:
            new_h = target_h
            new_w = int(target_h * img_ratio)
        else:
            new_w = target_w
            new_h = int(target_w / img_ratio)
        raw_img = raw_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        source_img = raw_img.crop((left, top, left + target_w, top + target_h))

        # Tạo background mờ (Depth Blur)
        blurred_bg = source_img.filter(ImageFilter.GaussianBlur(radius=5))

        words = headline_text.split()[:8]
        num_words = max(1, len(words))

        for f in range(total_frames):
            prog = f / max(1, total_frames - 1)
            # Easing Curve Bézier mượt mà
            eased_p = ease_in_out_cubic(prog)
            
            # Layer 1: Background Zoom chậm (1.05x -> 1.15x)
            bg_scale = 1.05 + 0.10 * eased_p
            bg_cw = int(target_w / bg_scale)
            bg_ch = int(target_h / bg_scale)
            bg_left = (target_w - bg_cw) // 2
            bg_top = (target_h - bg_ch) // 2
            frame_bg = blurred_bg.crop((bg_left, bg_top, bg_left + bg_cw, bg_top + bg_ch)).resize((target_w, target_h), Image.Resampling.BILINEAR)

            # Layer 2: Midground Card sắc nét nổi khối ở trung tâm (0.93x -> 1.02x)
            card_scale = 0.93 + 0.09 * eased_p
            card_w = int(1440 * card_scale)
            card_h = int(810 * card_scale)
            
            card_crop_w = int(target_w * 0.85)
            card_crop_h = int(target_h * 0.85)
            c_left = (target_w - card_crop_w) // 2
            c_top = (target_h - card_crop_h) // 2
            card_content = source_img.crop((c_left, c_top, c_left + card_crop_w, c_top + card_crop_h))
            card_resized = card_content.resize((card_w, card_h), Image.Resampling.LANCZOS)

            # Đặt card vào giữa frame_bg với viền sáng Cyberpunk
            paste_x = (target_w - card_w) // 2
            paste_y = (target_h - card_h) // 2 - 30 # Đẩy nhẹ lên trên để chừa chỗ cho subtitle
            
            # Vẽ bóng đổ và viền card
            card_frame = Image.new("RGBA", (card_w + 16, card_h + 16), (0, 0, 0, 0))
            draw_card = ImageDraw.Draw(card_frame)
            draw_card.rounded_rectangle([0, 0, card_w + 15, card_h + 15], radius=24, outline=(6, 182, 212, 190), width=3)
            
            frame_bg.paste(card_resized, (paste_x, paste_y))
            frame_bg.paste(card_frame, (paste_x - 8, paste_y - 8), card_frame)

            # Layer 3: HUD Elements & Kinetic Subtitles
            active_idx = int(prog * num_words)
            frame_path = os.path.join(frames_dir, f"frame_{f:04d}.jpg")
            self.create_motion_graphic_frame(
                base_image=frame_bg,
                headline_text=headline_text,
                output_image_path=frame_path,
                tag_label=tag_label,
                progress=prog,
                highlight_idx=active_idx
            )

        cmd = [
            "ffmpeg", "-y",
            "-r", str(fps),
            "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_clip_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_clip_path

    def render_ken_burns_clip(
        self,
        base_image_path: str,
        headline_text: str,
        duration_sec: float,
        output_clip_path: str,
        camera_effect: str = "zoom_in",
        tag_label: str = "TIÊU ĐIỂM",
        fps: int = 25
    ) -> str:
        """Render clip Ken Burns với đường cong Bézier Easing mượt mà."""
        frames_dir = os.path.join(self.temp_dir, "kb_tmp_frames")
        if os.path.exists(frames_dir):
            for f in os.listdir(frames_dir):
                try: os.remove(os.path.join(frames_dir, f))
                except Exception: pass
        os.makedirs(frames_dir, exist_ok=True)
        
        target_w, target_h = 1920, 1080
        total_frames = max(10, int(duration_sec * fps))
        
        if os.path.exists(base_image_path):
            try:
                raw_img = Image.open(base_image_path).convert("RGB")
            except Exception:
                raw_img = Image.new("RGB", (target_w, target_h), (15, 23, 42))
        else:
            raw_img = Image.new("RGB", (target_w, target_h), (15, 23, 42))

        img_ratio = raw_img.width / raw_img.height
        target_ratio = target_w / target_h
        if img_ratio > target_ratio:
            new_h = target_h
            new_w = int(target_h * img_ratio)
        else:
            new_w = target_w
            new_h = int(target_w / img_ratio)
        raw_img = raw_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        raw_img = raw_img.crop((left, top, left + target_w, top + target_h))

        words = headline_text.split()[:8]
        num_words = max(1, len(words))

        for f in range(total_frames):
            prog = f / max(1, total_frames - 1)
            # Áp dụng Ease In Out Bézier
            eased_p = ease_in_out_cubic(prog)
            
            if camera_effect == "zoom_out":
                scale = 1.15 - 0.15 * eased_p
            else:
                scale = 1.0 + 0.15 * eased_p
            
            crop_w = int(target_w / scale)
            crop_h = int(target_h / scale)
            
            if camera_effect == "pan_left":
                pan_offset = int((target_w - crop_w) * eased_p)
                c_left = pan_offset
                c_top = (target_h - crop_h) // 2
            elif camera_effect == "pan_right":
                pan_offset = int((target_w - crop_w) * (1 - eased_p))
                c_left = pan_offset
                c_top = (target_h - crop_h) // 2
            else:
                c_left = (target_w - crop_w) // 2
                c_top = (target_h - crop_h) // 2

            zoomed_bg = raw_img.crop((c_left, c_top, c_left + crop_w, c_top + crop_h)).resize((target_w, target_h), Image.Resampling.BILINEAR)
            
            active_idx = int(prog * num_words)
            frame_path = os.path.join(frames_dir, f"frame_{f:04d}.jpg")
            self.create_motion_graphic_frame(
                base_image=zoomed_bg,
                headline_text=headline_text,
                output_image_path=frame_path,
                tag_label=tag_label,
                progress=prog,
                highlight_idx=active_idx
            )

        cmd = [
            "ffmpeg", "-y",
            "-r", str(fps),
            "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_clip_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_clip_path

    def render_shot_clip(
        self,
        shot_id: str,
        duration_sec: float,
        headline_text: str,
        output_clip_path: str,
        search_query: Optional[str] = None,
        camera_effect: str = "zoom_in",
        motion_style: str = "ken_burns_eased",
        tag_label: str = "TIÊU ĐIỂM"
    ) -> str:
        """Thông minh lựa chọn phương án dựng:
        1. Ưu tiên 1: Video B-roll thực tế (Motion Stock Video)
        2. Ưu tiên 2: 3D Camera Parallax (nếu motion_style == 'parallax_3d')
        3. Ưu tiên 3: Ken Burns Eased Bézier Zoom
        """
        clip_temp_dir = os.path.join(self.temp_dir, "shots")
        os.makedirs(clip_temp_dir, exist_ok=True)

        q_lower = (search_query or "").lower()
        real_video_path = None
        
        # Kiểm tra kho B-roll cục bộ trước
        if any(k in q_lower for k in ["robot", "vật lý", "physical"]):
            local_candidate = os.path.join(self.local_broll_dir, "broll_robot.mp4")
            if os.path.exists(local_candidate): real_video_path = local_candidate
        elif any(k in q_lower for k in ["code", "lập trình", "dòng lệnh", "màn hình"]):
            local_candidate = os.path.join(self.local_broll_dir, "broll_code.mp4")
            if os.path.exists(local_candidate): real_video_path = local_candidate
        elif any(k in q_lower for k in ["ai", "trợ lý", "mạng lưới", "trí tuệ"]):
            local_candidate = os.path.join(self.local_broll_dir, "broll_ai.mp4")
            if os.path.exists(local_candidate): real_video_path = local_candidate

        # Nếu chưa có video cục bộ, thử tải từ Pexels Video
        if not real_video_path and search_query:
            target_vid = os.path.join(clip_temp_dir, f"vid_{shot_id}.mp4")
            try:
                en_query = "futuristic technology artificial intelligence"
                if "robot" in q_lower: en_query = "humanoid robot technology"
                elif "code" in q_lower: en_query = "computer coding screen"
                v_res = self.downloader.search_and_download_pexels_video(en_query, target_vid, min_duration=int(duration_sec))
                if v_res and os.path.exists(target_vid):
                    real_video_path = target_vid
            except Exception as e:
                print(f"[Tùng - Editor] Pexels Video Download: {e}")

        # TRƯỜNG HỢP 0: NẾU ĐƯỢC CHỈ ĐỊNH VECTOR MOTION GRAPHICS BẰNG MANIM
        if motion_style == "manim_vector" or "manim" in motion_style or "vector" in motion_style:
            print(f"   📐 [Tùng] Áp dụng VECTOR MOTION GRAPHICS (MANIM - After Effects Style)...")
            try:
                return self.manim_gen.generate_and_render(
                    headline_text=headline_text,
                    duration_sec=duration_sec,
                    output_path=output_clip_path,
                    tag_label=tag_label
                )
            except Exception as e:
                print(f"[Tùng - Editor] Lỗi render Manim: {e}. Fallback sang 3D Parallax.")

        # TRƯỜNG HỢP 1: NẾU ĐƯỢC CHỈ ĐỊNH RENDER 3D PARALLAX (AFX Style)
        if motion_style == "parallax_3d" or "parallax" in motion_style:
            print(f"   🎥 [Tùng] Áp dụng kỹ thuật 3D CAMERA PARALLAX...")
            raw_bg_path = os.path.join(clip_temp_dir, f"raw_{shot_id}.jpg")
            has_real_image = False
            try:
                en_img_q = "futuristic technology artificial intelligence"
                if "robot" in q_lower: en_img_q = "futuristic humanoid robot"
                elif "code" in q_lower: en_img_q = "cyberpunk computer screen"
                found_img = self.downloader.search_and_download_pexels_image(en_img_q, raw_bg_path)
                if found_img and os.path.exists(raw_bg_path):
                    has_real_image = True
            except Exception:
                pass

            if not has_real_image:
                stock_dir = os.path.abspath("./assets/stock_images")
                slides = [os.path.join(stock_dir, f) for f in os.listdir(stock_dir) if f.endswith(".png")] if os.path.exists(stock_dir) else []
                if slides:
                    h = int(hashlib.md5(shot_id.encode()).hexdigest(), 16)
                    raw_bg_path = slides[h % len(slides)]
                else:
                    raw_bg_path = os.path.abspath("./assets/default_bg.png")

            return self.render_parallax_3d_clip(
                base_image_path=raw_bg_path,
                headline_text=headline_text,
                duration_sec=duration_sec,
                output_clip_path=output_clip_path,
                tag_label="3D DEPTH"
            )

        # TRƯỜNG HỢP 2: CÓ VIDEO FOOTAGE THỰC TẾ
        if real_video_path and os.path.exists(real_video_path):
            try:
                print(f"   🎬 [Tùng] Sử dụng VIDEO FOOTAGE THỰC TẾ: {os.path.basename(real_video_path)}")
                return self.render_motion_stock_video_clip(
                    stock_video_path=real_video_path,
                    headline_text=headline_text,
                    duration_sec=duration_sec,
                    output_clip_path=output_clip_path,
                    tag_label=tag_label
                )
            except Exception as err:
                print(f"[Tùng - Editor] Lỗi render motion stock: {err}. Chuyển sang Parallax/Ken Burns.")

        # TÌM ẢNH CHẤT LƯỢNG CAO CHO KEN BURNS EASING
        raw_bg_path = os.path.join(clip_temp_dir, f"raw_{shot_id}.jpg")
        has_real_image = False
        try:
            en_img_q = "technology artificial intelligence"
            if "robot" in q_lower: en_img_q = "futuristic humanoid robot"
            elif "code" in q_lower: en_img_q = "cyberpunk computer screen"
            found_img = self.downloader.search_and_download_pexels_image(en_img_q, raw_bg_path)
            if found_img and os.path.exists(raw_bg_path):
                has_real_image = True
        except Exception:
            pass

        if not has_real_image:
            stock_dir = os.path.abspath("./assets/stock_images")
            slides = [os.path.join(stock_dir, f) for f in os.listdir(stock_dir) if f.endswith(".png")] if os.path.exists(stock_dir) else []
            if slides:
                h = int(hashlib.md5(shot_id.encode()).hexdigest(), 16)
                raw_bg_path = slides[h % len(slides)]
            else:
                raw_bg_path = os.path.abspath("./assets/default_bg.png")

        # TRƯỜNG HỢP 3: KEN BURNS VỚI ĐƯỜNG CONG BÉZIER EASING
        return self.render_ken_burns_clip(
            base_image_path=raw_bg_path,
            headline_text=headline_text,
            duration_sec=duration_sec,
            output_clip_path=output_clip_path,
            camera_effect=camera_effect,
            tag_label=tag_label
        )

    def assemble_final_video(
        self,
        project_id: str,
        audio_manifest: AudioManifest,
        visual_manifest: VisualManifest,
        output_filename: str = "viral_master_edition.mp4"
    ) -> str:
        """Lắp ráp hoàn chỉnh video triệu view với đầy đủ hình ảnh động, kinetic text và âm thanh đa tầng."""
        proj_temp = os.path.join(self.temp_dir, project_id)
        os.makedirs(proj_temp, exist_ok=True)
        final_output = os.path.join(self.output_dir, f"{project_id}_{output_filename}")

        print(f"\n🎬 [Tùng - Editor] Đang biên tập {len(visual_manifest.shots)} phân cảnh video theo tiêu chuẩn VIRAL MOTION GRAPHICS...")
        shot_clips = []
        for idx, shot in enumerate(visual_manifest.shots):
            dur_sec = max(1.0, shot.duration_ms / 1000.0)
            shot_file = os.path.join(proj_temp, f"shot_{idx:03d}.mp4")
            
            caption = shot.on_screen_text or ""
            query = caption if caption else visual_manifest.visual_style_prompt_prefix

            # Xác định tag nhãn chuyên nghiệp
            tag = "HOOK CAO TRÀO" if idx == 0 else ("ĐỘT PHÁ" if idx % 2 == 1 else "TIÊU ĐIỂM")
            style = getattr(shot, "motion_style", "ken_burns_eased") or "ken_burns_eased"
            cam = getattr(shot, "camera_effect", "zoom_in") or "zoom_in"

            print(f"   -> Rendering shot {idx+1}/{len(visual_manifest.shots)}: [{tag}] '{caption[:30]}...' ({dur_sec:.1f}s, Style: {style})")
            self.render_shot_clip(
                shot_id=f"{project_id}_{shot.shot_id}_{idx}",
                duration_sec=dur_sec,
                headline_text=caption,
                output_clip_path=shot_file,
                search_query=query,
                camera_effect=cam,
                motion_style=style,
                tag_label=tag
            )
            shot_clips.append(shot_file)

        # 1. Ghép nối các video clip
        video_list_txt = os.path.join(proj_temp, "video_list.txt")
        with open(video_list_txt, "w", encoding="utf-8") as f:
            for c in shot_clips:
                f.write(f"file '{os.path.abspath(c)}'\n")

        merged_video = os.path.join(proj_temp, "merged_video.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", video_list_txt, "-c", "copy", merged_video],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )

        # 2. Ghép nối giọng đọc voiceover
        audio_list_txt = os.path.join(proj_temp, "audio_list.txt")
        with open(audio_list_txt, "w", encoding="utf-8") as f:
            for a in audio_manifest.scene_audios:
                f.write(f"file '{os.path.abspath(a.audio_filepath)}'\n")

        merged_voice = os.path.join(proj_temp, "merged_voice.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audio_list_txt, "-c", "copy", merged_voice],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )

        # 3. Tạo SFX Track chuyển cảnh (Whoosh) tự động
        sfx_whoosh_path = os.path.join(self.sfx_dir, "whoosh.wav")
        has_sfx = os.path.exists(sfx_whoosh_path)
        sfx_track_path = os.path.join(proj_temp, "sfx_transitions.wav")

        total_dur_sec = sum(max(1.0, s.duration_ms / 1000.0) for s in visual_manifest.shots)
        if has_sfx and len(visual_manifest.shots) > 1:
            try:
                cuts_sec = []
                accum_time = 0.0
                for s in visual_manifest.shots[:-1]:
                    accum_time += max(1.0, s.duration_ms / 1000.0)
                    cuts_sec.append(accum_time)

                sfx_inputs = []
                sfx_filters = []
                for idx_c, cut_t in enumerate(cuts_sec):
                    delay_ms = int(cut_t * 1000)
                    sfx_inputs.extend(["-i", sfx_whoosh_path])
                    sfx_filters.append(f"[{idx_c}:a]adelay={delay_ms}|{delay_ms}[sfx_{idx_c}]")

                mix_in = "".join(f"[sfx_{idx_c}]" for idx_c in range(len(cuts_sec)))
                filter_sfx = f"{';'.join(sfx_filters)};{mix_in}amix=inputs={len(cuts_sec)}:dropout_transition=0[sfx_out]"
                cmd_sfx = ["ffmpeg", "-y"] + sfx_inputs + [
                    "-filter_complex", filter_sfx,
                    "-map", "[sfx_out]",
                    "-t", str(total_dur_sec),
                    sfx_track_path
                ]
                subprocess.run(cmd_sfx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except Exception as e:
                print(f"[Tùng - Editor] Lỗi tạo SFX transitions: {e}")
                has_sfx = False
        else:
            has_sfx = False

        # 4. Phối trộn Âm thanh Đa tầng (Voiceover + BGM Ducking 14% + Transition SFX 30%)
        bgm_path = audio_manifest.background_music_filepath
        has_bgm = os.path.exists(bgm_path) if bgm_path else False

        if has_bgm and has_sfx and os.path.exists(sfx_track_path):
            print("   -> 🎵 Đang hòa âm đa tầng (Voiceover + BGM 14% + Transition SFX Whoosh)...")
            final_cmd = [
                "ffmpeg", "-y",
                "-i", merged_video,
                "-i", merged_voice,
                "-i", bgm_path,
                "-i", sfx_track_path,
                "-filter_complex", "[2:a]volume=0.14[bgm];[3:a]volume=0.30[sfx];[1:a][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                final_output
            ]
        elif has_bgm:
            print("   -> 🎵 Đang mix nhạc nền BGM cinematic với giọng đọc (Volume BGM: 15%)...")
            final_cmd = [
                "ffmpeg", "-y",
                "-i", merged_video,
                "-i", merged_voice,
                "-i", bgm_path,
                "-filter_complex", "[2:a]volume=0.15[bgm];[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                final_output
            ]
        else:
            final_cmd = [
                "ffmpeg", "-y",
                "-i", merged_video,
                "-i", merged_voice,
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                final_output
            ]

        subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"   ✅ [Tùng - Editor] Render video thành công: {final_output}")
        return final_output
