import os
import sys

# Đảm bảo ffmpeg trong PATH
bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from manim import *
from manim.utils.rate_functions import ease_in_out_cubic, ease_out_quad, ease_out_back

# Cấu hình render Full HD 1080p, 30fps
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#0B0F19" # Dark Cyber Slate
config.media_dir = "./output/manim_media"

class AIMotionGraphicsShowcase(Scene):
    """Minh họa các kỹ thuật Motion Graphics kinh điển của After Effects bằng Manim:
    1. Trim Paths (Vòng tròn công nghệ & HUD Reticle tự vẽ phát sáng)
    2. Shape Morphing (Biến đổi khối hình thành Mạng Nơ-ron AI)
    3. Kinetic Typography (Chữ nảy lò xo & Highlight vàng neon)
    4. Pulse Signal (Xung năng lượng truyền dọc theo các đường kết nối)
    """
    def construct(self):
        # 1. TECH HUD RETICLE & CORNER BRACKETS (After Effects Trim Paths)
        circle_outer = Arc(radius=2.6, start_angle=0, angle=TAU * 0.75, color="#06B6D4", stroke_width=4)
        circle_inner = DashedVMobject(Circle(radius=2.2, color="#38BDF8", stroke_width=2), num_dashes=30)
        center_core = Dot(point=ORIGIN, radius=0.18, color="#FFE600")

        hud_group = VGroup(circle_outer, circle_inner, center_core)

        # Hiệu ứng Trim Paths tự vẽ vòng tròn
        self.play(
            Create(circle_outer, run_time=1.2, rate_func=ease_in_out_cubic),
            Create(circle_inner, run_time=1.0, rate_func=ease_out_quad),
            GrowFromCenter(center_core, run_time=0.6, rate_func=ease_out_back),
        )

        # 2. KINETIC TEXT POPPING (Chữ tiêu đề nảy lò xo)
        title_text = Text("AI REVOLUTION", font="Arial", weight="BOLD", font_size=48, color="#FFFFFF")
        title_text.next_to(hud_group, UP, buff=0.6)
        
        tag_box = RoundedRectangle(corner_radius=0.15, height=0.6, width=3.4, color="#DC2626", fill_opacity=0.3, stroke_width=2)
        tag_label = Text("● ĐỘT PHÁ CÔNG NGHỆ", font="Arial", font_size=20, color="#FFFFFF")
        tag_badge = VGroup(tag_box, tag_label).next_to(title_text, UP, buff=0.3)

        self.play(
            FadeIn(tag_badge, shift=DOWN * 0.3, rate_func=ease_out_back),
            Write(title_text, run_time=0.8, rate_func=ease_out_quad),
        )
        self.wait(0.3)

        # 3. SHAPE MORPHING (Biến đổi từ vòng tròn HUD sang Mạng Nơ-ron / Connected Nodes)
        node_positions = [
            UP * 1.5 + LEFT * 2.2,
            UP * 1.5 + RIGHT * 2.2,
            DOWN * 1.5 + LEFT * 2.2,
            DOWN * 1.5 + RIGHT * 2.2,
            ORIGIN,
        ]
        nodes = VGroup(*[
            VGroup(
                Dot(pos, radius=0.22, color="#06B6D4"),
                Circle(radius=0.38, color="#38BDF8", stroke_width=2).move_to(pos)
            ) for pos in node_positions
        ])

        # Các đường cáp kết nối các node về trung tâm (Connecting lines / Trim paths)
        connections = VGroup(*[
            Line(ORIGIN, pos, color="#64748B", stroke_width=3)
            for pos in node_positions[:-1]
        ])

        # Chuyển đổi trạng thái (Shape Morphing After Effects)
        self.play(
            ReplacementTransform(circle_outer, connections, run_time=1.0, rate_func=ease_in_out_cubic),
            ReplacementTransform(circle_inner, nodes, run_time=1.0, rate_func=ease_in_out_cubic),
        )

        # 4. DATA PULSES (Xung năng lượng chạy dọc theo đường kết nối)
        pulses = [
            Dot(ORIGIN, radius=0.12, color="#FFE600")
            for _ in range(4)
        ]
        pulse_anims = [
            pulses[i].animate(rate_func=ease_in_out_cubic, run_time=0.8).move_to(node_positions[i])
            for i in range(4)
        ]
        self.play(*pulse_anims)

        # 5. SUBTITLE CALLOUT WITH OVERSHOOT BOUNCE
        callout_box = RoundedRectangle(corner_radius=0.2, height=1.0, width=9.0, color="#FFE600", fill_color="#0F172A", fill_opacity=0.9, stroke_width=2)
        callout_box.to_edge(DOWN, buff=0.8)
        callout_text = Text("SIÊU TRÍ TUỆ NHÂN TẠO KHỞI CHẠY", font="Arial", weight="BOLD", font_size=32, color="#FFE600")
        callout_text.move_to(callout_box.get_center())
        callout_group = VGroup(callout_box, callout_text)

        self.play(
            FadeIn(callout_group, shift=UP * 0.5, rate_func=ease_out_back, run_time=0.8),
            Wiggle(nodes, scale_value=1.15, rotation_angle=0.03 * TAU, run_time=1.0)
        )
        self.wait(1.0)

if __name__ == "__main__":
    scene = AIMotionGraphicsShowcase()
    scene.render()
