from utils.util_general import *


class Funnel(VGroup):
    def __init__(self, stem_width=1.5, stem_height=1, funnel_width=6, funnel_height=1):
        super().__init__()
        self.color = BASE1
        poly_list = [
            (-funnel_width / 2, funnel_height),
            (funnel_width / 2, funnel_height),
            (stem_width / 2, 0),
            (stem_width / 2, -stem_height),
            (-stem_width / 2, -stem_height),
            (-stem_width / 2, 0),
        ]
        self.poly = (
            Polygon(*((x, y, 0) for x, y in poly_list), color=self.color)
            .set_fill(self.color, opacity=1)
            .set_z_index(1)
        )
        self.add(self.poly)
        self.random = VGroup(
            Text("NOT RANDOM", color=RED), Text("RANDOM", color=GREEN)
        ).set_opacity(0)
        self.random.move_to(self.poly).next_to(self.poly, DOWN)
        self.add(self.random)
        self.wheel = (
            SVGMobject("img/gear.svg")
            .scale(0.3)
            .set_fill(BASE02)
            .set_stroke_width(0)
            .set_background_stroke_width(0)
            .set_sheen_direction((0, 0, 0))
            .set_sheen_factor(0)
            .set_opacity(0)
            .set_z_index(2)
            .scale(1.5)
            .move_to(self.poly)
        )
        self.wheel.move_to(self.poly)

    def verdict(self, verdict):
        return (
            self.random[verdict]
            .animate(rate_func=there_and_back, run_time=2)
            .set_opacity(1)
        )

    def get_input_position(self, string):
        return string.copy().next_to(self.poly, UP).origin()

    def eat_string(self, string):
        return (
            string.animate.move_to(self.poly)
            .align_to(self.poly, UP)
            .shift(0.2 * DOWN)
            .scale(0.4)
        )

    def thinking(self):
        self.wheel.save_state()
        angular_velocity = -2
        cutoff = 0.3

        def fn(obj: VMobject, alpha):
            opacity_alpha = min(1, min(alpha, 1 - alpha) / cutoff)
            obj.restore()
            obj.set_opacity(smooth(opacity_alpha))
            obj.rotate(alpha * angular_velocity)

        return UpdateFromAlphaFunc(self.wheel, fn, rate_func=linear, run_time=3)

    def feed_string(self, string, verdict):
        anims = []
        if type(string) == str:
            string = Text(string, color=TEXT_COLOR)
            string.next_to(self, UP, buff=0.4)
            anims.append(FadeIn(string))
        copy = string.copy().set_opacity(0)
        anims += [
            copy.animate(run_time=0.001).set_opacity(1),
            self.eat_string(string),
            self.thinking(),
            AnimationGroup(self.verdict(verdict), FadeOut(copy), lag_ratio=0.5),
        ]
        return Succession(*anims)


class StatisticalTest(Scene):
    def construct(self):
        funnel = Funnel()
        self.add(funnel)
        self.play(funnel.feed_string("0000000", False))
        self.play(funnel.feed_string("00000000101", True))
        self.wait(5)
