import os
import sys
import subprocess
import hashlib
from typing import Optional

class ManimMotionGenerator:
    """Module chuyên biệt tạo Motion Graphics chuẩn After Effects bằng Manim:
    - Trim Paths (Vòng tròn & đường vector tự vẽ phát sáng)
    - Shape Morphing (Biến đổi hình học mượt mà)
    - Spring Physics & Overshoot Bounce
    - Mạng nơ-ron kết nối & Xung năng lượng Data Pulses
    """

    def __init__(self, temp_dir: str = "./temp/manim_build"):
        self.temp_dir = temp_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        self.python_exe = sys.executable

    def generate_and_render(
        self,
        headline_text: str,
        duration_sec: float,
        output_path: str,
        tag_label: str = "ĐỘT PHÁ CÔNG NGHỆ"
    ) -> str:
        clean_text = headline_text.strip().replace('"', '\\"')
        clean_tag = tag_label.strip().replace('"', '\\"')
        h = hashlib.md5(headline_text.encode()).hexdigest()[:8]
        output_media_dir = os.path.abspath(os.path.join(self.temp_dir, f"media_{h}")).replace("\\", "/")
        
        # Tạo mã nguồn Manim Scene động
        script_content = f'''import os
import sys

bin_dir = os.path.abspath("./bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_quad, ease_out_back

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#080C16"
config.media_dir = "{output_media_dir}"

class GeneratedMotionScene(Scene):
    def construct(self):
        # 1. TRIM PATHS: HUD TECH RETICLE
        circle_outer = Arc(radius=2.5, start_angle=0, angle=TAU * 0.75, color="#06B6D4", stroke_width=4)
        circle_inner = DashedVMobject(Circle(radius=2.1, color="#38BDF8", stroke_width=2), num_dashes=28)
        core_dot = Dot(point=ORIGIN, radius=0.2, color="#FFE600")

        self.play(
            Create(circle_outer, run_time=0.9, rate_func=ease_in_out_cubic),
            Create(circle_inner, run_time=0.8, rate_func=ease_out_quad),
            GrowFromCenter(core_dot, run_time=0.5, rate_func=ease_out_back)
        )

        # 2. KINETIC TEXT POPPING (Chữ tiêu đề nảy lò xo)
        title = Text("{clean_text[:28]}", font="Arial", weight="BOLD", font_size=42, color="#FFFFFF")
        title.to_edge(UP, buff=0.8)

        tag_box = RoundedRectangle(corner_radius=0.15, height=0.55, width=3.2, color="#DC2626", fill_opacity=0.35, stroke_width=2)
        tag_txt = Text("● {clean_tag[:20]}", font="Arial", font_size=20, color="#FFFFFF")
        tag_group = VGroup(tag_box, tag_txt).next_to(title, UP, buff=0.25)

        self.play(
            FadeIn(tag_group, shift=DOWN * 0.3, rate_func=ease_out_back, run_time=0.5),
            Write(title, run_time=0.7, rate_func=ease_out_quad)
        )

        # 3. SHAPE MORPHING: BIẾN ĐỔI SANG MẠNG NƠ-RON (CONNECTED NODES)
        node_coords = [
            UP * 1.3 + LEFT * 2.4,
            UP * 1.3 + RIGHT * 2.4,
            DOWN * 1.3 + LEFT * 2.4,
            DOWN * 1.3 + RIGHT * 2.4,
            ORIGIN
        ]
        nodes = VGroup(*[
            VGroup(
                Dot(pos, radius=0.24, color="#06B6D4"),
                Circle(radius=0.4, color="#38BDF8", stroke_width=2).move_to(pos)
            ) for pos in node_coords
        ])

        cables = VGroup(*[
            Line(ORIGIN, pos, color="#64748B", stroke_width=3)
            for pos in node_coords[:-1]
        ])

        self.play(
            ReplacementTransform(circle_outer, cables, run_time=0.8, rate_func=ease_in_out_cubic),
            ReplacementTransform(circle_inner, nodes, run_time=0.8, rate_func=ease_in_out_cubic)
        )

        # 4. DATA PULSES (Xung năng lượng chạy dọc đường cáp)
        pulses = [Dot(ORIGIN, radius=0.12, color="#FFE600") for _ in range(4)]
        pulse_anims = [
            pulses[i].animate(rate_func=ease_in_out_cubic, run_time=0.6).move_to(node_coords[i])
            for i in range(4)
        ]
        self.play(*pulse_anims)

        # 5. CALLOUT SUBTITLE NỔI KHỐI OVERSHOOT
        sub_box = RoundedRectangle(corner_radius=0.2, height=1.0, width=9.2, color="#FFE600", fill_color="#0F172A", fill_opacity=0.92, stroke_width=2)
        sub_box.to_edge(DOWN, buff=0.8)
        sub_txt = Text("{clean_text}", font="Arial", weight="BOLD", font_size=32, color="#FFE600")
        sub_txt.move_to(sub_box.get_center())
        sub_group = VGroup(sub_box, sub_txt)

        self.play(
            FadeIn(sub_group, shift=UP * 0.4, rate_func=ease_out_back, run_time=0.6),
            Wiggle(nodes, scale_value=1.12, rotation_angle=0.02 * TAU, run_time=0.8)
        )
        self.wait(0.5)

if __name__ == "__main__":
    scene = GeneratedMotionScene()
    scene.render()
'''
        script_file = os.path.join(self.temp_dir, f"manim_scene_{h}.py")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_content)

        # Chạy render bằng python
        cmd = [self.python_exe, script_file]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Tìm file mp4 thành phẩm
        expected_dir = os.path.join(output_media_dir, "videos", "1080p30")
        mp4_files = [os.path.join(expected_dir, f) for f in os.listdir(expected_dir) if f.endswith(".mp4") and not f.startswith("partial")] if os.path.exists(expected_dir) else []
        
        if not mp4_files:
            raise RuntimeError(f"Không tìm thấy file Manim render trong {expected_dir}")

        raw_mp4 = mp4_files[0]
        # Cắt hoặc điều chỉnh đúng duration_sec và xuất ra output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cmd_trim = [
            "ffmpeg", "-y",
            "-i", raw_mp4,
            "-t", str(duration_sec),
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return output_path
