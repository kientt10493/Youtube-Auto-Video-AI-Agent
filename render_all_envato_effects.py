import os
import sys

bin_dir = os.path.abspath("./bin")
if bin_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from manim import *
from manim.utils.rate_functions import (
    ease_in_out_cubic,
    ease_out_back,
    ease_out_quad,
    ease_in_quad,
    rush_into,
    rush_from,
    there_and_back
)

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#070B14" # Deep Dark Cyber Slate
config.media_dir = "./output/envato_full_masterclass"

class EnvatoMotionDesignMasterclass(Scene):
    """BẢN TRÌNH DIỄN ĐẦY ĐỦ TẤT CẢ CÁC NGUYÊN LÝ & KỸ THUẬT TỪ PLAYLIST ENVATO TUTS+:
    Chương 1: 12 Nguyên lý Animation (Squash & Stretch, Anticipation, Easing Bézier vs Linear)
    Chương 2: Trim Paths & Vector Blueprint (Vòng tròn & HUD Reticle tự vẽ phát sáng)
    Chương 3: Shape Morphing & Web Micro-interactions (Biến đổi khối hình mượt mà)
    Chương 4: Hierarchical Parenting & Puppet Joints (Cánh tay cơ khí xoay quanh khớp)
    Chương 5: Kinetic Typography (Letter Stagger, Tracking Expansion & Highlight)
    Chương 6: 3D Multi-Plane Parallax Camera (Chiều sâu không gian đa tầng)
    Chương 7: Connected Network & Saul Bass Geometric Metaphor
    """
    def construct(self):
        # =========================================================================
        # CHƯƠNG 0: INTRO - BÀI HỌC MOTION GRAPHICS BASICS
        # =========================================================================
        intro_badge = RoundedRectangle(corner_radius=0.15, height=0.6, width=4.5, color="#06B6D4", fill_opacity=0.3, stroke_width=2)
        intro_badge_txt = Text("ENVATO TUTS+ MASTERCLASS", font="Arial", weight="BOLD", font_size=22, color="#06B6D4")
        intro_badge_grp = VGroup(intro_badge, intro_badge_txt).to_edge(UP, buff=0.8)

        intro_title = Text("10 KỸ THUẬT MOTION GRAPHICS ĐỈNH CAO", font="Arial", weight="BOLD", font_size=46, color="#FFFFFF")
        intro_sub = Text("Đúc kết từ chuỗi bài giảng After Effects hàng đầu thế giới", font="Arial", font_size=24, color="#94A3B8")
        intro_sub.next_to(intro_title, DOWN, buff=0.3)

        self.play(
            FadeIn(intro_badge_grp, shift=DOWN * 0.4, rate_func=ease_out_back),
            Write(intro_title, run_time=1.0, rate_func=ease_out_quad),
            FadeIn(intro_sub, shift=UP * 0.2, run_time=0.8)
        )
        self.wait(1.0)
        self.play(FadeOut(intro_title), FadeOut(intro_sub), FadeOut(intro_badge_grp))

        # =========================================================================
        # CHƯƠNG 1: SQUASH & STRETCH (CO GIÃN ĐÀN HỒI THEO QUÁN TÍNH)
        # =========================================================================
        sec1_tag = Text("● NGUYÊN LÝ 1: SQUASH & STRETCH (CO GIÃN VẬT LÝ)", font="Arial", weight="BOLD", font_size=26, color="#FFE600").to_edge(UP, buff=0.7)
        sec1_desc = Text("Vật thể co dẹp khi chạm sàn và dãn dài khi rơi/bật lên để giữ nguyên thể tích", font="Arial", font_size=20, color="#94A3B8").next_to(sec1_tag, DOWN, buff=0.2)
        ground = Line(LEFT * 4, RIGHT * 4, color="#475569", stroke_width=4).shift(DOWN * 2.2)
        ball = Circle(radius=0.7, color="#FFE600", fill_opacity=0.9).shift(UP * 2.2)

        self.play(FadeIn(sec1_tag, shift=DOWN * 0.2), FadeIn(sec1_desc), Create(ground))
        
        # Rơi xuống (Stretch theo phương thẳng đứng)
        self.play(ball.animate(rate_func=rush_into, run_time=0.5).stretch_to_fit_height(1.7).stretch_to_fit_width(1.1).move_to(DOWN * 1.35))
        # Va chạm sàn: Nén dẹp (Squash)
        self.play(ball.animate(rate_func=rush_into, run_time=0.12).stretch_to_fit_height(0.65).stretch_to_fit_width(2.2).move_to(DOWN * 1.88))
        # Bật nảy lên (Stretch trở lại rồi phục hồi hình tròn)
        self.play(ball.animate(rate_func=rush_from, run_time=0.55).stretch_to_fit_height(1.4).stretch_to_fit_width(1.4).move_to(UP * 1.8))
        self.play(ball.animate(rate_func=ease_out_quad, run_time=0.3).stretch_to_fit_height(1.4).stretch_to_fit_width(1.4))
        self.wait(0.6)
        self.play(FadeOut(sec1_tag), FadeOut(sec1_desc), FadeOut(ground), FadeOut(ball))

        # =========================================================================
        # CHƯƠNG 2: ANTICIPATION & OVERSHOOT (LẤY ĐÀ & BẬT NẢY QUÁ ĐÀ)
        # =========================================================================
        sec2_tag = Text("● NGUYÊN LÝ 2: ANTICIPATION & OVERSHOOT BOUNCE", font="Arial", weight="BOLD", font_size=26, color="#06B6D4").to_edge(UP, buff=0.7)
        sec2_desc = Text("Thu nhỏ lùi lại để lấy đà, sau đó phóng vọt tới và nảy quá đích trước khi dừng", font="Arial", font_size=20, color="#94A3B8").next_to(sec2_tag, DOWN, buff=0.2)
        
        rocket_card = RoundedRectangle(corner_radius=0.2, height=1.6, width=2.8, color="#06B6D4", fill_color="#0F172A", fill_opacity=0.9, stroke_width=3)
        rocket_icon = Text("🚀 BOOST", font="Arial", weight="BOLD", font_size=26, color="#38BDF8").move_to(rocket_card.get_center())
        rocket_grp = VGroup(rocket_card, rocket_icon).shift(LEFT * 4)

        self.play(FadeIn(sec2_tag, shift=DOWN * 0.2), FadeIn(sec2_desc), FadeIn(rocket_grp))
        
        # 1. Anticipation: Thu nhỏ và lùi nhẹ về bên trái
        self.play(rocket_grp.animate(rate_func=ease_in_quad, run_time=0.4).scale(0.82).shift(LEFT * 0.8))
        # 2. Burst: Phóng cực nhanh vượt đích sang phải
        self.play(rocket_grp.animate(rate_func=rush_into, run_time=0.45).scale(1.0 / 0.82).shift(RIGHT * 8.5))
        # 3. Overshoot Bounce: Đàn hồi giật ngược nhẹ rồi cố định vị trí
        self.play(rocket_grp.animate(rate_func=ease_out_back, run_time=0.5).shift(LEFT * 0.7))
        self.wait(0.6)
        self.play(FadeOut(sec2_tag), FadeOut(sec2_desc), FadeOut(rocket_grp))

        # =========================================================================
        # CHƯƠNG 3: EASING BÉZIER VS LINEAR (SO SÁNH ĐƯỜNG CONG TỐC ĐỘ)
        # =========================================================================
        sec3_tag = Text("● NGUYÊN LÝ 3: EASING CURVES (SLOW IN & SLOW OUT)", font="Arial", weight="BOLD", font_size=26, color="#EF4444").to_edge(UP, buff=0.7)
        
        label_linear = Text("Linear (Cơ học, buồn ngủ):", font="Arial", font_size=20, color="#94A3B8").shift(UP * 1.0 + LEFT * 3.5)
        ball_linear = Dot(radius=0.25, color="#EF4444").shift(UP * 1.0 + LEFT * 0.5)
        track_linear = Line(LEFT * 0.5, RIGHT * 4.5, color="#334155").shift(UP * 1.0)

        label_eased = Text("Bézier Eased (Mượt mà, sinh động):", font="Arial", font_size=20, color="#10B981").shift(DOWN * 0.5 + LEFT * 3.5)
        ball_eased = Dot(radius=0.25, color="#10B981").shift(DOWN * 0.5 + LEFT * 0.5)
        track_eased = Line(LEFT * 0.5, RIGHT * 4.5, color="#334155").shift(DOWN * 0.5)

        self.play(
            FadeIn(sec3_tag),
            FadeIn(label_linear), Create(track_linear), FadeIn(ball_linear),
            FadeIn(label_eased), Create(track_eased), FadeIn(ball_eased)
        )
        
        # Chạy cùng 1 quãng đường trong 2 giây nhưng khác biệt rate_func
        self.play(
            ball_linear.animate(rate_func=linear, run_time=2.0).shift(RIGHT * 4.8),
            ball_eased.animate(rate_func=ease_in_out_cubic, run_time=2.0).shift(RIGHT * 4.8)
        )
        self.wait(0.6)
        self.play(
            FadeOut(sec3_tag),
            FadeOut(label_linear), FadeOut(track_linear), FadeOut(ball_linear),
            FadeOut(label_eased), FadeOut(track_eased), FadeOut(ball_eased)
        )

        # =========================================================================
        # CHƯƠNG 4: TRIM PATHS & VECTOR BLUEPRINT (AFTER EFFECTS STROKE ANIMATION)
        # =========================================================================
        sec4_tag = Text("● BÀI HỌC 4: TRIM PATHS & VECTOR BLUEPRINT", font="Arial", weight="BOLD", font_size=26, color="#06B6D4").to_edge(UP, buff=0.7)
        sec4_desc = Text("Vẽ nét viền vector tự động chạy quanh chu vi tạo phong cách công nghệ", font="Arial", font_size=20, color="#94A3B8").next_to(sec4_tag, DOWN, buff=0.2)
        
        hud_outer = Arc(radius=2.3, start_angle=0, angle=TAU * 0.85, color="#06B6D4", stroke_width=4)
        hud_dashed = DashedVMobject(Circle(radius=1.8, color="#38BDF8", stroke_width=2), num_dashes=32)
        hud_inner = Circle(radius=1.3, color="#FFE600", stroke_width=2)
        hud_cross_h = Line(LEFT * 2.6, RIGHT * 2.6, color="#475569", stroke_width=1.5)
        hud_cross_v = Line(DOWN * 2.6, UP * 2.6, color="#475569", stroke_width=1.5)

        self.play(FadeIn(sec4_tag), FadeIn(sec4_desc))
        self.play(
            Create(hud_outer, run_time=1.2, rate_func=ease_in_out_cubic),
            Create(hud_dashed, run_time=1.0, rate_func=ease_out_quad),
            Create(hud_inner, run_time=0.8, rate_func=ease_out_back),
            Create(hud_cross_h, run_time=0.6),
            Create(hud_cross_v, run_time=0.6),
        )
        self.play(Rotate(hud_dashed, angle=TAU * 0.5, run_time=1.5, rate_func=linear))
        self.wait(0.5)
        self.play(
            FadeOut(sec4_tag), FadeOut(sec4_desc),
            FadeOut(hud_outer), FadeOut(hud_dashed), FadeOut(hud_inner), FadeOut(hud_cross_h), FadeOut(hud_cross_v)
        )

        # =========================================================================
        # CHƯƠNG 5: SHAPE MORPHING & MICRO-INTERACTIONS
        # =========================================================================
        sec5_tag = Text("● BÀI HỌC 5: SHAPE MORPHING (BIẾN ĐỔI KHỐI HÌNH VECTOR)", font="Arial", weight="BOLD", font_size=26, color="#F59E0B").to_edge(UP, buff=0.7)
        sec5_desc = Text("Chuyển đổi mượt mà cấu trúc đỉnh vector: Tròn -> Lục giác -> Khiên bảo mật", font="Arial", font_size=20, color="#94A3B8").next_to(sec5_tag, DOWN, buff=0.2)
        
        shape1 = Circle(radius=1.6, color="#F59E0B", stroke_width=4, fill_color="#F59E0B", fill_opacity=0.2)
        shape2 = RegularPolygon(n=6, radius=1.8, color="#06B6D4", stroke_width=4, fill_color="#06B6D4", fill_opacity=0.2)
        shape3 = Square(side_length=2.8, color="#10B981", stroke_width=4, fill_color="#10B981", fill_opacity=0.2)

        self.play(FadeIn(sec5_tag), FadeIn(sec5_desc), Create(shape1))
        # Morphing 1: Tròn -> Lục giác
        self.play(ReplacementTransform(shape1, shape2, run_time=0.9, rate_func=ease_in_out_cubic))
        # Morphing 2: Lục giác -> Vuông
        self.play(ReplacementTransform(shape2, shape3, run_time=0.9, rate_func=ease_in_out_cubic))
        self.wait(0.5)
        self.play(FadeOut(sec5_tag), FadeOut(sec5_desc), FadeOut(shape3))

        # =========================================================================
        # CHƯƠNG 6: HIERARCHICAL PARENTING & ROBOT ARM (LIÊN KẾT KHỚP NỐI)
        # =========================================================================
        sec6_tag = Text("● BÀI HỌC 6: HIERARCHICAL PARENTING (KHỚP NỐI CHA - CON)", font="Arial", weight="BOLD", font_size=26, color="#8B5CF6").to_edge(UP, buff=0.7)
        sec6_desc = Text("Khớp con (khuỷu, kẹp) di chuyển theo quỹ đạo và góc quay của khớp cha (vai)", font="Arial", font_size=20, color="#94A3B8").next_to(sec6_tag, DOWN, buff=0.2)
        
        base_joint = Dot(DOWN * 1.5 + LEFT * 2, radius=0.2, color="#8B5CF6")
        arm_upper = Line(DOWN * 1.5 + LEFT * 2, UP * 0.5 + LEFT * 1.5, color="#A78BFA", stroke_width=8)
        elbow_joint = Dot(UP * 0.5 + LEFT * 1.5, radius=0.18, color="#C4B5FD")
        arm_fore = Line(UP * 0.5 + LEFT * 1.5, UP * 1.2 + RIGHT * 1.0, color="#DDD6FE", stroke_width=6)
        claw = Square(side_length=0.4, color="#FFE600", stroke_width=3).move_to(UP * 1.2 + RIGHT * 1.0)

        arm_full = VGroup(base_joint, arm_upper, elbow_joint, arm_fore, claw)

        self.play(FadeIn(sec6_tag), FadeIn(sec6_desc), Create(arm_full))
        # Xoay toàn bộ cánh tay quanh vai (Base Joint)
        self.play(Rotate(arm_full, angle=0.4, about_point=DOWN * 1.5 + LEFT * 2, run_time=0.9, rate_func=ease_in_out_cubic))
        # Xoay riêng cẳng tay và kẹp quanh khuỷu (Elbow Joint)
        fore_grp = VGroup(arm_fore, claw)
        self.play(Rotate(fore_grp, angle=-0.7, about_point=UP * 0.5 + LEFT * 1.5, run_time=0.9, rate_func=ease_out_back))
        self.wait(0.5)
        self.play(FadeOut(sec6_tag), FadeOut(sec6_desc), FadeOut(arm_full), FadeOut(fore_grp))

        # =========================================================================
        # CHƯƠNG 7: KINETIC TYPOGRAPHY (CHỮ ĐỘNG ĐA PHONG CÁCH)
        # =========================================================================
        sec7_tag = Text("● BÀI HỌC 7: KINETIC TYPOGRAPHY & LETTER STAGGER", font="Arial", weight="BOLD", font_size=26, color="#FFE600").to_edge(UP, buff=0.7)
        
        # 1. Letter Stagger Pop
        word_ai = Text("A R T I F I C I A L", font="Arial", weight="BOLD", font_size=52, color="#06B6D4").shift(UP * 0.5)
        # 2. Tracking Expansion
        word_intel = Text("INTELLIGENCE", font="Arial", weight="BOLD", font_size=38, color="#FFFFFF").next_to(word_ai, DOWN, buff=0.4)
        # 3. Highlighter Badge Wipe
        highlight_box = RoundedRectangle(corner_radius=0.15, height=0.75, width=6.5, color="#FFE600", fill_color="#FFE600", fill_opacity=0.25, stroke_width=2).move_to(word_intel.get_center())

        self.play(FadeIn(sec7_tag))
        self.play(Write(word_ai, run_time=0.9, rate_func=ease_out_quad))
        self.play(
            FadeIn(word_intel, shift=UP * 0.3, rate_func=ease_out_back),
            word_intel.animate.stretch(1.2, 0) # Tracking expansion dãn chữ
        )
        self.play(Create(highlight_box, run_time=0.6, rate_func=ease_in_out_cubic))
        self.wait(0.6)
        self.play(FadeOut(sec7_tag), FadeOut(word_ai), FadeOut(word_intel), FadeOut(highlight_box))

        # =========================================================================
        # CHƯƠNG 8: 3D MULTI-PLANE PARALLAX CAMERA (CHIỀU SÂU ĐA TẦNG)
        # =========================================================================
        sec8_tag = Text("● BÀI HỌC 8: 3D MULTI-PLANE PARALLAX (Z-SPACE DEPTH)", font="Arial", weight="BOLD", font_size=26, color="#06B6D4").to_edge(UP, buff=0.7)
        sec8_desc = Text("Lớp nền (Background) di chuyển chậm, lớp tiền cảnh (Foreground) lướt cực nhanh", font="Arial", font_size=20, color="#94A3B8").next_to(sec8_tag, DOWN, buff=0.2)
        
        bg_grid = VGroup(*[
            Line(LEFT * 6, RIGHT * 6, color="#1E293B", stroke_width=1).shift(UP * i)
            for i in [-2, -1, 0, 1, 2]
        ])
        mid_card = RoundedRectangle(corner_radius=0.2, height=2.2, width=4.0, color="#06B6D4", fill_color="#0F172A", fill_opacity=0.85, stroke_width=2.5)
        mid_txt = Text("MIDGROUND LAYER", font="Arial", weight="BOLD", font_size=24, color="#38BDF8").move_to(mid_card.get_center())
        mid_layer = VGroup(mid_card, mid_txt)
        
        fg_particle = Dot(radius=0.4, color="#FFE600").shift(DOWN * 2 + RIGHT * 4)

        self.play(FadeIn(sec8_tag), FadeIn(sec8_desc), FadeIn(bg_grid), FadeIn(mid_layer), FadeIn(fg_particle))
        
        # Camera Pan Parallax: Các tầng di chuyển với vận tốc khác nhau (Z-Space)
        self.play(
            bg_grid.animate(rate_func=ease_in_out_cubic, run_time=1.8).shift(LEFT * 0.8),       # Nền chậm (v=0.8)
            mid_layer.animate(rate_func=ease_in_out_cubic, run_time=1.8).shift(LEFT * 2.2),     # Giữa vừa (v=2.2)
            fg_particle.animate(rate_func=ease_in_out_cubic, run_time=1.8).shift(LEFT * 7.5),   # Trước nhanh (v=7.5)
        )
        self.wait(0.5)
        self.play(FadeOut(sec8_tag), FadeOut(sec8_desc), FadeOut(bg_grid), FadeOut(mid_layer), FadeOut(fg_particle))

        # =========================================================================
        # CHƯƠNG 9: KẾT THÚC VÀ TỔNG KẾT
        # =========================================================================
        final_box = RoundedRectangle(corner_radius=0.2, height=2.5, width=9.2, color="#10B981", fill_color="#0F172A", fill_opacity=0.9, stroke_width=3)
        final_title = Text("CHẾ TÁC HOÀN TOÀN TỰ ĐỘNG BẰNG CODE", font="Arial", weight="BOLD", font_size=36, color="#10B981").shift(UP * 0.4)
        final_sub = Text("100% Vector Motion Graphics • Không cần đồ họa thủ công • Sẵn sàng cho YouTube Viral", font="Arial", font_size=20, color="#FFFFFF").next_to(final_title, DOWN, buff=0.3)
        final_grp = VGroup(final_box, final_title, final_sub)

        self.play(FadeIn(final_grp, shift=UP * 0.5, rate_func=ease_out_back))
        self.wait(1.5)

if __name__ == "__main__":
    scene = EnvatoMotionDesignMasterclass()
    scene.render()
