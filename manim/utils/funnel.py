from utils.util_general import *


class Funnel(VGroup):
    def __init__(
        self,
        label: VMobject = None,
    ):
        stem_width = 1.5
        stem_height = 1
        funnel_width = 6
        funnel_height = 1.5
        if label is None:
            label = nil_object()
        if type(label) == str:
            label = Tex(label, color=BASE01).scale(1.2)
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
            .align_to(self.poly, DOWN)
            .shift(0.1 * UP)
        )
        self.wheel.stroke_width = self.wheel.background_stroke_width = (
            self.wheel.sheen_factor
        ) = 0
        self.add(self.wheel)
        self.label = label.set_z_index(2).align_to(self.poly, UP).shift(0.3 * DOWN)
        self.add(self.label)

    def verdict(self, scene, verdict, side=False):
        tick = self.ticks[verdict].set_opacity(1)
        is_random = self.random[verdict]
        if verdict == 1:
            scene.add_sound("audio/polylog_success.wav")
        else:
            scene.add_sound("audio/polylog_failure.wav")
        if side:
            VGroup(tick, is_random).shift(2 * UR + 0.3 * DOWN)
        scene.play(
            FadeIn(tick, shift=DOWN, scale=0.3),
            Succession(
                Wait(0.5),
                is_random.animate(run_time=0.001).set_opacity(1),
                FadeIn(is_random),
            ),
        )
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
        if type(talking) == str:
            talking = Tex(talking, tex_environment=None)

        def fn(obj: VMobject, alpha):
            seconds = alpha * run_time
            opacity_alpha = min(1, min(seconds, run_time - seconds) / cutoff)
            obj.restore()
            obj.set_opacity(smooth(opacity_alpha))
            obj.rotate(seconds * angular_velocity)

        anims = []
        if talking:
            run_time = 5
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

    def make_string(self, scene, string, add_string=True):
        string = Tex(string).scale(1.2)
        string.next_to(self, UP, buff=0.3)
        if add_string:
            scene.play(Write(string))
        return string

    def feed_string(
        self,
        scene,
        string,
        verdict,
        talking=None,
        disappear=True,
        think=True,
        add_string=True,
        side=False,
    ):
        if type(string) == str:
            string = self.make_string(scene, string, add_string)
        copy = string.copy()
        scene.play(self.eat_string(string))
        if think:
            scene.play(self.thinking(talking))
        anims = [self.verdict(scene, verdict, side), FadeOut(string)]
        if disappear:
            anims.append(FadeOut(copy))
        scene.play(*anims)
        self.random.set_opacity(0)
        self.ticks.set_opacity(0)
        return copy
