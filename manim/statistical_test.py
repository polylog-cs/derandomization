from prng import *
from utils.util_general import *

with open("pi.txt") as f:
    PI = "".join(f.read().split())


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
            label = Dot(radius=0, fill_opacity=0, stroke_opacity=0)
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


class StatisticalTest(Scene):
    def construct(self):
        funnel = Funnel("\#0 : \#1")
        self.add(funnel)
        self.wait()
        self.play(Write(funnel))
        self.wait()

        funnel.feed_string(
            self, "0000000000000000", False, talking=r"0: 100\,\%\\1: 0\,\%"
        )
        funnel.feed_string(
            self, "1010110010110101", True, talking=r"0: 43.7\,\%\\1: 56.3\,\%"
        )
        string = funnel.feed_string(
            self,
            "1010101010101010",
            True,
            disappear=False,
            talking=r"0: 50\,\%\\1: 50\,\%",
        )
        funnel2 = Funnel(
            r"2-grams",
        ).move_to(funnel)
        self.play(FadeOut(funnel, shift=5 * LEFT), FadeIn(funnel2, shift=5 * LEFT))
        funnel2.feed_string(
            self, string, False, talking=r"00: 0\,\%\\01: 50\,\%\\10: 50\,\%\\11: 0\%"
        )
        self.wait(5)


class Pi(Scene):
    def construct(self):
        self.next_section(skip_animations=False)

        funnel_scale = 0.5
        funnels = (
            VGroup(
                Funnel(),  # r"Serial \\ test"),
                Funnel(),  # r"Gap \\ test"),
                Funnel(),  # r"Frequency \\ test"),
                Funnel(),  # r"Partition \\ test"),
                Funnel(),  # r"Run \\ test"),
                Funnel(),  # r"Permutation \\ test"),
            )
            .arrange_in_grid(rows=2, buff=(1, 0))
            .scale(funnel_scale)
            .to_edge(DOWN, buff=0.5)
        )

        self.play(
            AnimationGroup(
                *[Write(funnel) for funnel in funnels],
                lag_ratio=0.2,
            )
        )
        self.wait()

        for i, txt in enumerate([r"1010110010110101", r"3141592653589793"]):
            rand_string_tex = Tex(txt, color=text_color).to_edge(UP, buff=1.5)
            copies = [rand_string_tex.copy() for funnel in funnels]
            # for copy, funnel in zip(copies, funnels):
            #     copy.create_target()
            #     copy.target.scale(funnel_scale).move_to(funnel).next_to(funnel, UP)

            if i == 1:
                prng = (
                    PRNG(name=r"$\pi$-PRNG")
                    .scale(0.6)
                    .next_to(rand_string_tex, LEFT, buff=1.5)
                )
                self.play(Create(prng))
                self.play(prng.set_seed("."))  # TODO fix
                prng_ar = Arrow(
                    start=prng.get_right(),
                    end=rand_string_tex.get_left(),
                )
                self.play(Create(prng_ar))

            self.play(Write(rand_string_tex))
            self.wait()

            self.play(
                AnimationGroup(
                    *[
                        copy.animate.scale(funnel_scale)
                        .move_to(funnel)
                        .next_to(funnel, UP)
                        for copy, funnel in zip(copies, funnels)
                    ],
                    lag_ratio=0.2,
                )
            )
            self.wait()

            ticks = [
                Text("✓", color=GREEN)
                .scale_to_fit_height(1)
                .align_to(funnel, DR)
                .shift(0.5 * UL)
                for funnel in funnels
            ]
            self.add_sound("audio/polylog_success.wav")
            self.play(
                AnimationGroup(
                    *[FadeIn(tick) for tick in ticks],
                    lag_ratio=0.2,
                )
            )
            anims = []
            if i == 0:
                anims += [FadeOut(rand_string_tex)]
            if i == 1:
                anims += [FadeOut(funnel) for funnel in funnels]
            self.play(
                *[FadeOut(tick) for tick in ticks],
                *[FadeOut(copy) for copy in copies],
                *anims,
            )
            self.wait()

        self.funnel = Funnel(r"$\pi$-checking \\ test").shift(1 * DOWN)
        self.play(FadeIn(self.funnel))
        self.play(
            rand_string_tex.animate.scale(1.2).next_to(self.funnel, UP, buff=0.3),
        )
        self.wait()

        tex = Tex(r"Hey, this is $\pi$!\\That's not random!", tex_environment=None)
        self.funnel.feed_string(
            self, "314159265358979", False, talking=tex, add_string=False, side=True
        )

        self.remove(rand_string_tex)
        self.play(
            FadeOut(self.funnel),
            Group(prng, prng_ar).animate.shift(3 * RIGHT + 1 * DOWN),
        )
        self.play(prng.set_seed("111011001"))
        self.wait()
        idx = 473 + 3  # I dont know why this is 3
        self.play(prng.set_seed(r"$k = \texttt{473}$"))
        self.wait()

        pi = Tex(r"\hsize=200cm $\pi$ = " + PI[:1000]).set_z_index(-1)
        marks = []
        for i in range(48, 100):
            mark = Tex(r"$\texttt{" + str(i * 10 - 480) + r"}$").next_to(
                pi[0][i * 10], DOWN, buff=0.3
            )
            marks.append(mark)

        pi_group = Group(pi, *marks)
        pi_group.to_edge(UP, buff=0.5)

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
        self.play(FadeIn(pi_group))

        self.play(
            pi_group.animate(rate_func=rate_functions.ease_in_out_quart).shift(
                pi[0][idx].get_center()[0] * LEFT
            ),
            run_time=5,
        )

        subpi = pi[0][idx : idx + 16].copy()
        self.play(Circumscribe(subpi, color=RED))
        self.play(subpi.animate.next_to(prng_ar, RIGHT, buff=0.3))
        self.wait()

        brace_subpi = BraceText(subpi, r"$n$ digits").next_to(subpi, DOWN, buff=0.3)
        brace_k = BraceText(prng.seed, r"$1 \le k \le n^{10}$").next_to(
            prng.seed, DOWN, buff=0.3
        )
        self.play(FadeIn(brace_subpi))
        self.wait()
        self.play(FadeIn(brace_k))
        self.wait()

        self.funnel.scale(0.8).shift(0.3 * DOWN)
        self.play(FadeIn(self.funnel), FadeOut(brace_subpi), FadeOut(brace_k))
        subpi.save_state()
        self.play(subpi.animate.scale(1.2 * 0.8).next_to(self.funnel, UP, buff=0.3))

        tex = Tex(
            r"Testing the first $n^{10}$ digits \\ of $\pi$\\",
            # r"No time to check the first\\$n^{10}$ digits of $\pi$ :(",
            tex_environment=None,
        ).scale(0.8)
        self.funnel.feed_string(self, subpi, False, talking=tex, side=True)

        funnels.scale(0.8).shift(0.2 * DOWN)
        brace_funnels = (
            BraceText(
                Group(funnels[2], funnels[-1].copy().shift(1 * UP)),
                r"tests faster \\ than $n^{10}$",
                brace_direction=RIGHT,
            )
            .next_to(funnels, RIGHT, buff=0.3)
            .shift(0.3 * UP)
        )
        Group(funnels, brace_funnels).move_to(ORIGIN).to_edge(DOWN, buff=0.5)
        self.play(
            FadeOut(self.funnel),
            subpi.animate.restore(),
        )

        self.play(
            AnimationGroup(
                *[Write(funnel) for funnel in funnels],
            )
        )
        self.play(
            FadeIn(brace_funnels),
        )
        self.wait()

        copies = [subpi.copy() for funnel in funnels]

        self.play(
            AnimationGroup(
                *[
                    copy.animate.scale(funnel_scale * 0.8)
                    .move_to(funnel)
                    .next_to(funnel, UP)
                    for copy, funnel in zip(copies, funnels)
                ],
                lag_ratio=0.2,
            )
        )
        self.wait()

        ticks = [
            Text("✓", color=GREEN)
            .scale_to_fit_height(1)
            .align_to(funnel, DR)
            .shift(0.5 * UL)
            for funnel in funnels
        ]
        self.add_sound("audio/polylog_success.wav")
        self.play(
            AnimationGroup(
                *[FadeIn(tick) for tick in ticks],
                lag_ratio=0.2,
            )
        )
        self.wait()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()
        self.next_section(skip_animations=False)

        prng = PRNG(name="NW").scale(1.3).shift(2 * UP + 1 * LEFT)
        self.play(Create(prng))
        self.wait()

        self.play(prng.set_seed("11101"))
        self.wait()

        rand_string_tex = Tex("0010101011110110110", color=text_color).next_to(
            prng, RIGHT, buff=1.5
        )

        prng_ar = Arrow(
            start=prng.get_right(),
            end=rand_string_tex.get_left(),
        )
        self.play(
            Write(rand_string_tex),
            Create(prng_ar),
        )
        self.wait()

        self.play(
            AnimationGroup(
                *[Write(funnel) for funnel in funnels],
            )
        )
        self.play(
            FadeIn(brace_funnels.shift(0.5 * DOWN)),
        )
        self.wait()

        copies = [rand_string_tex.copy() for funnel in funnels]

        self.play(
            AnimationGroup(
                *[
                    copy.animate.scale(funnel_scale * 0.8)
                    .move_to(funnel)
                    .next_to(funnel, UP)
                    for copy, funnel in zip(copies, funnels)
                ],
                lag_ratio=0.2,
            )
        )
        self.wait()

        ticks = [
            Text("✓", color=GREEN)
            .scale_to_fit_height(1)
            .align_to(funnel, DR)
            .shift(0.5 * UL)
            for funnel in funnels
        ]
        self.add_sound("audio/polylog_success.wav")
        self.play(
            AnimationGroup(
                *[FadeIn(tick) for tick in ticks],
                lag_ratio=0.2,
            )
        )
        self.wait()

        self.play(
            *[FadeOut(copy) for copy in copies],
            *[FadeOut(tick) for tick in ticks],
            *[FadeOut(funnel) for funnel in funnels],
            FadeOut(brace_funnels),
        )
        self.wait()

        thm = (
            Tex(
                r"\raggedright \textbf{Theorem} (Nissan-Wigderson PRNG): \\ There is a pseudorandom generator that runs in polynomial time and its $n$ output bits pass all statistical tests running in time $n^{10}$. \\ This holds if we assume that there is a problem solvable in time $2^{n}$ that cannot be solved  with a circuit of size $2^{0.0001n}$. "
            )
            .scale(0.8)
            .to_edge(DOWN, buff=1.5)
        )
        self.play(Write(thm))

        self.wait(5)


class NW(Scene):
    def construct(self):
        thm = Tex(
            r"\raggedright Theorem (Nissan-Wigderson PRNG): \\ There is a pseudorandom generator that runs in polynomial time and its output passes all statistical tests that run in time $n^{10}$. \\ This holds if we assume that there is a problem solvable in time $2^{n}$ that cannot be solved  with a circuit of size $2^{0.0001n}$. "
        ).scale(0.8)
        self.play(Write(thm))
        self.wait()
