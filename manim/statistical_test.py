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
            .set_fill(BASE01)
            .set_sheen_direction((0, 0, 0))
            .set_opacity(0)
            .set_z_index(2)
            .scale(1.5)
            .move_to(self.poly)
        )
        self.wheel.stroke_width = (
            self.wheel.background_stroke_width
        ) = self.wheel.sheen_factor = 0
        self.add(self.wheel)

    def verdict(self, verdict):
        return (
            self.random[verdict]
            .animate(rate_func=there_and_back_with_pause, run_time=2)
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
            string = Tex(string).scale(1.2)
            string.next_to(self, UP, buff=0.3)
            anims.append(Write(string))
        copy = string.copy().set_opacity(0)
        anims += [
            copy.animate(run_time=0).set_opacity(1),
            self.eat_string(string),
            self.thinking(),
            AnimationGroup(self.verdict(verdict), FadeOut(copy), lag_ratio=0.5),
            FadeOut(string),
            # string.animate(run_time=0).set_opacity(0),
        ]
        return anims


class StatisticalTest(Scene):
    def construct(self):
        funnel = Funnel()
        self.add(funnel)
        self.play(Write(funnel))
        self.play(funnel.feed_string("00000000", False))
        self.play(funnel.feed_string("1010110010111", True))
        self.play(funnel.feed_string("010101010101", False))
        self.play(FadeOut(funnel))
        self.wait(5)


with open("pi.txt") as f:
    PI = "".join(f.read().split())


class FeedMePi(Scene):
    def hijack_animations(self, anims, tex):
        hey = VGroup(tex.next_to(self.funnel.wheel).shift(0.6 * DOWN + 1.5 * RIGHT))
        hey.add(
            ArcBetweenPoints(
                self.funnel.wheel.get_right() + 0.1 * RIGHT + 0.1 * DOWN,
                hey[0].get_left() + 0.1 * LEFT,
                angle=0.5,
            ).set_z_index(2)
        )
        anims[-3] = AnimationGroup(
            anims[-3].set_run_time(5),
            Succession(
                Wait(1), FadeIn(hey, rate_func=there_and_back_with_pause, run_time=4)
            ),
        )
        return anims

    def construct(self):
        self.funnel = Funnel().shift(2 * LEFT)
        self.add(self.funnel)
        self.play(Write(self.funnel))

        anims = self.funnel.feed_string("314159265358979", False)
        tex = Tex(r"Hey, this is $\pi$!\\That's not random!", tex_environment=None)
        self.hijack_animations(anims, tex)
        self.play(Succession(*anims))

        pi = Tex(r"\hsize=200cm $\pi$ = " + PI[:500]).set_z_index(-1)
        pi.to_edge(UP, buff=0.5)
        hide1 = (
            Square(color=BACKGROUND_COLOR)
            .scale(0.3)
            .move_to(pi)
            .set_fill(BACKGROUND_COLOR, 1)
            .to_edge(LEFT, buff=0)
        )
        hide2 = hide1.copy().to_edge(RIGHT, buff=0)
        pi.next_to(hide1)
        self.add(hide1, hide2)
        self.play(FadeIn(pi))

        idx = 432
        self.play(pi.animate.shift(pi[0][idx].get_center()[0] * LEFT), run_time=3)

        subpi = pi[0][idx - 5 : idx + 6].copy()
        self.play(subpi.animate.scale(1.2).next_to(self.funnel, UP, buff=0.3))

        anims = self.funnel.feed_string(subpi, True)
        tex = Tex(
            r"No time to check the first\\$n^{10}$ digits of $\pi$ :(",
            tex_environment=None,
        )
        self.hijack_animations(anims, tex)
        self.play(Succession(*anims))

        self.play(FadeOut(self.funnel))
        self.wait(5)
