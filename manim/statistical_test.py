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
        self.ticks = (
            VGroup(
                Text("×", color=RED).scale_to_fit_height(1),
                Text("✓", color=GREEN).scale_to_fit_height(1),
            )
            .move_to(self.poly)
            .next_to(self.poly, DOWN)
        ).set_opacity(0)
        self.add(self.ticks)
        self.random = (
            VGroup(Tex("Not random", color=RED), Tex("Random", color=GREEN))
            .scale(1.2)
            .move_to(self.ticks)
            .next_to(self.ticks, DOWN)
            .set_opacity(0)
        )
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
        self.wheel.stroke_width = self.wheel.background_stroke_width = (
            self.wheel.sheen_factor
        ) = 0
        self.add(self.wheel)

    def verdict(self, scene, verdict):
        tick = self.ticks[verdict].set_opacity(1)
        scene.play(FadeIn(tick, shift=DOWN, scale=0.3))
        is_random = self.random[verdict].set_opacity(1)
        scene.play(FadeIn(is_random))
        scene.wait(1)
        return FadeOut(VGroup(tick, is_random))

    def get_input_position(self, string):
        return string.copy().next_to(self.poly, UP).origin()

    def eat_string(self, string):
        return (
            string.animate.move_to(self.poly)
            .align_to(self.poly, UP)
            .shift(0.2 * DOWN)
            .scale(0.4)
        )

    def thinking(self, talking=None):
        self.wheel.save_state()
        angular_velocity = -1.5
        cutoff = 0.5
        run_time = 3

        def fn(obj: VMobject, alpha):
            seconds = alpha * run_time
            opacity_alpha = min(1, min(seconds, run_time - seconds) / cutoff)
            obj.restore()
            obj.set_opacity(smooth(opacity_alpha))
            obj.rotate(seconds * angular_velocity)

        anims = []
        if talking:
            run_time = 6
            hey = VGroup(talking.next_to(self.wheel).shift(0.6 * DOWN + 1.5 * RIGHT))
            hey.add(
                ArcBetweenPoints(
                    self.wheel.get_right() + 0.1 * RIGHT + 0.1 * DOWN,
                    hey[0].get_left() + 0.1 * LEFT,
                    angle=0.5,
                ).set_z_index(2)
            )
            anims.append(
                Succession(
                    Wait(1),
                    FadeIn(
                        hey,
                        rate_func=lambda x: smooth(
                            min(1, min(x, 1 - x) * (run_time - 1) / cutoff)
                        ),
                        run_time=run_time - 1,
                    ),
                ),
            )
        anims.append(
            UpdateFromAlphaFunc(self.wheel, fn, rate_func=linear, run_time=run_time)
        )

        return AnimationGroup(*anims)

    def make_string(self, scene, string):
        string = Tex(string).scale(1.2)
        string.next_to(self, UP, buff=0.3)
        scene.play(Write(string))
        return string

    def feed_string(self, scene, string, verdict, talking=None):
        if type(string) == str:
            string = self.make_string(scene, string)
        copy = string.copy()
        scene.add(copy)
        scene.play(self.eat_string(string))
        scene.play(self.thinking(talking))
        scene.play(self.verdict(scene, verdict), FadeOut(copy))
        scene.play(FadeOut(string))


class StatisticalTest(Scene):
    def construct(self):
        funnel = Funnel()
        self.add(funnel)
        self.play(Write(funnel))
        funnel.feed_string(self, "00000000", False)
        funnel.feed_string(self, "1010110010111", True)
        funnel.feed_string(self, "010101010101", False)
        self.play(FadeOut(funnel))
        self.wait(5)


with open("pi.txt") as f:
    PI = "".join(f.read().split())


class FeedMePi(Scene):
    def construct(self):
        self.funnel = Funnel().shift(2 * LEFT)
        self.add(self.funnel)
        self.play(Write(self.funnel))

        tex = Tex(r"Hey, this is $\pi$!\\That's not random!", tex_environment=None)
        self.funnel.feed_string(self, "314159265358979", False, talking=tex)

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
        self.play(
            pi.animate(rate_func=rate_functions.ease_in_out_quart).shift(
                pi[0][idx].get_center()[0] * LEFT
            ),
            run_time=3,
        )

        subpi = pi[0][idx - 5 : idx + 6].copy()
        self.play(subpi.animate.scale(1.2).next_to(self.funnel, UP, buff=0.3))

        tex = Tex(
            r"No time to check the first\\$n^{10}$ digits of $\pi$ :(",
            tex_environment=None,
        )
        self.funnel.feed_string(self, subpi, True, talking=tex)

        self.play(FadeOut(pi))

        VGroup(self.funnel.ticks, self.funnel.random).set_opacity(0)
        self.play(FadeOut(self.funnel))
        self.wait(5)
