from prng import *
from utils.funnel import *
from utils.util_general import *

from manim.mobject.svg.brace import BraceText

with open("pi.txt") as f:
    PI = "".join(f.read().split())


class StatisticalTest(Scene):
    def construct(self):
        funnel = Funnel(r"\#0 : \#1")
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
            r"bigrams",
        ).move_to(funnel)
        self.play(FadeOut(funnel, shift=5 * LEFT), FadeIn(funnel2, shift=5 * LEFT))
        funnel2.feed_string(
            self, string, False, talking=r"00: 0\,\%\\01: 50\,\%\\10: 50\,\%\\11: 0\%"
        )
        self.wait(5)


class Pi(Scene):
    def do_that_thingy_with_the_funnelses(self, funnels, copies, scale=0.4):
        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[
                        funnel.eat_string(copy, run_time=1.5, scale=scale)
                        for copy, funnel in zip(copies, funnels)
                    ],
                    lag_ratio=0.2,
                ),
                AnimationGroup(
                    *[
                        AnimationGroup(
                            funnel.thinking(run_time=4, cutoff=0.8),
                            funnel.verdict(True, True),
                            lag_ratio=0.4,
                        )
                        for copy, funnel in zip(copies, funnels)
                    ],
                    # lag_ratio=0.05,
                ),
                lag_ratio=1,
            )
        )

    def write_funnels(self, funnels):
        self.play(
            AnimationGroup(
                *[Write(funnel.poly) for funnel in funnels],
                lag_ratio=0.2,
            )
        )

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

        self.write_funnels(funnels)
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
                self.play(prng.set_seed(None))
                prng_ar = Arrow(
                    start=prng.get_right(),
                    end=rand_string_tex.get_left(),
                )
                self.play(GrowArrow(prng_ar))

            self.play(Write(rand_string_tex))
            self.wait()

            self.do_that_thingy_with_the_funnelses(funnels, copies)
            self.add_sound("audio/polylog_success.wav")

            anims = []
            if i == 0:
                anims += [FadeOut(rand_string_tex)]
            self.play(
                *[funnel.hide_stuff(all=i == 1) for funnel in funnels],
                *[FadeOut(copy) for copy in copies],
                *anims,
            )
            self.wait()

        self.funnel = Funnel(r"\baselineskip=.9em $\pi$-checking\\ test").shift(
            1 * DOWN
        )
        self.play(FadeIn(self.funnel))
        # self.play(
        #    rand_string_tex.animate.scale(1.2).next_to(self.funnel, UP, buff=0.3),
        # )
        self.wait()

        tex = Tex(r"Hey, this is $\pi$!\\That's not random!", tex_environment=None)
        self.funnel.feed_string(
            self,
            rand_string_tex.copy(),
            False,
            talking=tex,
            add_string=False,
            simple=True,
        )

        self.next_section(skip_animations=False)
        self.play(
            FadeOut(rand_string_tex),
            self.funnel.hide_stuff(all=True),
            Group(prng, prng_ar).animate.shift(3 * RIGHT + 1 * DOWN),
        )

        idx = 473
        self.play(prng.set_seed(bin(idx)[2:]))
        seed = Tex("$k = 473$").move_to(prng.seed).align_to(prng.seed, RIGHT)
        self.wait()
        self.play(prng.seed.animate.become(seed))
        self.wait()

        pi = Tex(r"\hsize=200cm $\pi$ = " + PI[:600])
        marks = []
        for i in range(10, len(pi[0]) - 3, 10):
            mark = (
                VGroup(Line(UP, DOWN).scale(0.15), Tex(str(i)).scale(0.5))
                .arrange(DOWN, buff=0.1)
                .next_to(pi[0][i + 3], DOWN, buff=0.1)
            )
            marks.append(mark)

        pi_group = Group(pi, *marks).set_z_index(-5)
        pi_group.to_edge(UP, buff=0.5)

        hide1 = (
            Square(color=BACKGROUND_COLOR)
            .move_to(pi_group)
            .scale(0.5)
            .set_fill(BACKGROUND_COLOR, 1)
            .to_edge(LEFT, buff=0)
        )
        hide2 = hide1.copy().to_edge(RIGHT, buff=0)
        pi_group.next_to(hide1)
        self.add(hide1, hide2)
        self.play(FadeIn(pi_group))

        self.play(
            pi_group.animate(rate_func=rate_functions.ease_in_out_quart).shift(
                pi[0][idx + 3 + 8].get_center()[0] * LEFT
            ),
            run_time=5,
        )

        subpi = pi[0][idx + 3 : idx + 3 + 16].copy()
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
        # subpi.save_state()
        # self.play(subpi.animate.scale(1.2 * 0.8).next_to(self.funnel, UP, buff=0.3))

        tex = Tex(
            r"Testing the first $n^{10}$ digits \\ of $\pi$\\",
            # r"No time to check the first\\$n^{10}$ digits of $\pi$ :(",
            tex_environment=None,
        ).scale(0.8)
        self.funnel.feed_string(
            self, subpi, False, talking=tex, simple=True, disappear=False
        )

        self.next_section(skip_animations=False)

        funnels.scale(0.8).shift(0.2 * DOWN)
        brace_funnels = (
            BraceText(
                Group(funnels[2].poly, funnels[-1].poly),
                r"tests faster \\ than $n^{10}$",
                brace_direction=RIGHT,
            )
            .next_to(funnels, RIGHT, buff=0.3)
            .shift(0.3 * UP)
        )

        Group(funnels, brace_funnels).move_to(ORIGIN).to_edge(DOWN, buff=0.5)
        self.play(
            self.funnel.hide_stuff(all=True),
        )

        self.write_funnels(funnels)
        self.play(
            FadeIn(brace_funnels),
        )
        self.wait()

        copies = [subpi.copy() for funnel in funnels]

        self.do_that_thingy_with_the_funnelses(funnels, copies)
        self.add_sound("audio/polylog_success.wav")
        self.wait()
        anims = []
        for funnel in funnels:
            anims.append(funnel.hide_stuff(all=True))
            self.remove(funnel)
        self.play(*anims, *[FadeOut(m) for m in self.mobjects])
        for m in self.mobjects:
            self.remove(m)
        self.wait()
        self.next_section(skip_animations=False)

        prng = PRNG(name="NW").scale(1.3).shift(2 * UP + 1.5 * LEFT)
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
            GrowArrow(prng_ar),
        )
        self.wait()

        self.write_funnels(funnels)
        self.play(
            FadeIn(brace_funnels),
        )
        self.wait()

        copies = [rand_string_tex.copy() for funnel in funnels]
        for funnel in funnels:
            funnel.ticks.set_opacity(0)

        self.do_that_thingy_with_the_funnelses(funnels, copies, scale=0.25)
        self.add_sound("audio/polylog_success.wav")
        self.wait()
        self.wait()

        self.play(
            *[FadeOut(copy) for copy in copies],
            *[funnel.hide_stuff(all=True) for funnel in funnels],
            FadeOut(brace_funnels),
        )
        self.wait()

        thm = (
            Tex(
                r"""
\textbf{Theorem} (Nisan-Wigderson PRNG):

Assume that there is a problem solvable in time $2^{n}$ that cannot be solved with a circuit of size $2^{0.0001n}$.

Then, for any polynomial function $f(n)$, there is a pseudorandom generator that runs in polynomial time and its $n$~output bits pass all statistical tests running in time $f(n)$.

""",
                tex_environment=None,
            )
            .scale(0.75)
            .to_edge(DOWN, buff=1.5)
        )
        self.play(Write(thm))

        self.wait(5)
