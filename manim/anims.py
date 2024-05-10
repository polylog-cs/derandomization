# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from pathlib import Path

from prng import *
from utils.util_general import *


class Polylogo(Scene):
    def construct(self):
        set_default_colors()
        authors = Tex(
            r"\textbf{Richard Hladík, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)
        channel_name_without_o = Tex(r"p\hskip 5.28pt lylog", color=text_color)
        channel_name_without_o.scale(4).shift(1 * UP)

        logo_solarized = (
            SVGMobject("img/logo-solarized.svg")
            .scale(0.55)
            .move_to(2 * LEFT + 0.95 * UP + 0.49 * RIGHT)
        )
        self.play(
            Write(authors),
            Write(channel_name),
        )
        self.play(FadeIn(logo_solarized))
        self.add(channel_name_without_o)
        self.remove(channel_name)

        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


class TheoremStatement(Scene):
    def construct(self):
        set_default_colors()

        h = 2.5
        people = Group(
            *[
                Group(
                    ImageMobject("img/" + str + ".jpg").scale_to_fit_height(h),
                    Tex(name, color=text_color, font_size=35),
                ).arrange(DOWN)
                for str, name in zip(
                    ["nisan", "wigderson", "blum", "micali", "yao"],
                    [
                        "Noam Nisan",
                        "Avi Wigderson",
                        "Manuel Blum",
                        "Silvio Micali",
                        "Andy Yao",
                    ],
                )
            ]
        ).arrange(RIGHT, buff=0.3)

        for i in range(2):
            if i == 0:
                r = range(0, 2)
            else:
                r = range(2, len(people))
            self.play(
                AnimationGroup(
                    *[arrive_from(people[i], RIGHT) for i in r],
                    lag_ratio=0.31,
                )
            )
            self.wait()
        # fade out all people
        self.play(
            *[FadeOut(p) for p in people[2:]],
            Group(*people[:2]).animate.scale(0.7).to_corner(UL),
        )
        self.wait()
        hypothesis, conclusion = [
            Tex(t, color=text_color, font_size=50)
            for i, t in enumerate(
                [
                    "Under an assumption that most people believe,",
                    r"any problem that can be solved\\"
                    r"efficiently with randomness\\"
                    r"can also be solved efficiently without it.",
                ]
            )
        ]
        Group(hypothesis, conclusion).arrange(DOWN).shift(1 * DOWN)

        self.play(Write(hypothesis))
        self.play(Write(conclusion))
        self.wait()

        self.play(
            conclusion.animate.become(
                Tex(r"{{$P$}}{{$\,=\,$}}{{$BPP$}}", color=text_color, font_size=80)
                .shift(DOWN * 0.3)
                .shift(1 * DOWN)
            ),
        )
        self.wait()
        hypothesis_formal_str = (
            r"If there is a problem solvable in time $2^{n}$\\"
            "that cannot be solved  with a circuit "
            "of size $2^{0.0001n}$,"
        )
        hypothesis_formal = (
            Tex(hypothesis_formal_str, color=text_color, font_size=50)
            .shift(UP)
            .shift(1 * DOWN)
        )

        hypothesis_original = hypothesis.copy()
        self.play(hypothesis.animate.become(hypothesis_formal))
        self.wait()
        self.play(hypothesis.animate.become(hypothesis_original))
        self.wait()

        conclusion[0].save_state()
        self.play(
            conclusion[0].animate.scale(3).next_to(conclusion[1], LEFT),
        )
        self.wait()

        examples_tex = (
            Tex(
                r"{{\raggedright Sorting \\}}{{ Shortest path \\}}{{ $\dots$}}",
                color=text_color,
            )
            .next_to(conclusion[0], LEFT)
            .shift(0.5 * DOWN)
        )
        self.play(
            AnimationGroup(
                *[Write(e) for e in examples_tex],
                lag_ratio=0.5,
            )
        )
        self.wait()

        conclusion[-1].save_state()
        self.play(
            conclusion[0].animate.restore(),
            conclusion[-1].animate.scale(3).next_to(conclusion[1], RIGHT),
        )
        self.wait()

        self.play(conclusion[-1].animate.restore())
        self.wait()

        examples2_tex = (
            Tex(r"{{Polynomial testing}}{{?????}}", color=text_color)
            .next_to(conclusion[2], RIGHT)
            .shift(0.5 * RIGHT)
        )

        self.remove(conclusion)
        conclusion = Tex(
            r"{{$P$}}{{$\,\stackrel{?}{=}\,$}}{{$BPP$}}", font_size=80
        ).move_to(conclusion)
        Group(hypothesis, conclusion).shift(0.5 * UP)

        self.add(conclusion)
        self.remove(hypothesis, people[0], people[1])
        self.wait()

        self.play(
            Write(examples2_tex[0]),
        )
        self.wait()

        examples2_tex[0].save_state()
        self.play(
            examples2_tex[0].animate.align_to(examples_tex, DL).shift(0.1 * DOWN),
            FadeOut(examples_tex[2]),
        )
        examples2_tex[1].next_to(examples2_tex[0], RIGHT)
        self.play(Write(examples2_tex[1]))
        self.wait()

        self.play(
            examples2_tex[0].animate.restore(),
            FadeOut(examples2_tex[1]),
        )
        self.wait()

        self.play(
            Transform(
                conclusion,
                Tex(
                    r"{{$P$}}{{$\,\stackrel{?}{\not=} \,$}}{{$BPP$}}", font_size=80
                ).move_to(conclusion),
            )
        )
        self.wait()

        self.play(
            FadeIn(people[0]),
            FadeIn(people[1]),
            Transform(
                conclusion,
                Tex(r"{{$P$}}{{$\,= \,$}}{{$BPP$}}", font_size=80).move_to(conclusion),
            ),
            Write(hypothesis.shift(0.5 * DOWN)),
            FadeOut(examples_tex),
            FadeOut(examples2_tex[0]),
        )
        self.wait()


class ShowCode(Scene):
    def construct(self):
        text = Path("../code/get_random_bits2.py").read_text()
        code = make_code(text).to_edge(RIGHT)

        self.play(FadeIn(code))
        self.wait()

        ar = Arrow(
            start=1.5 * LEFT,
            end=ORIGIN,
            color=RED,
        ).next_to(code[2][5], LEFT)

        self.play(Create(ar))
        self.wait()
        self.play(ar.animate.next_to(code[2][-1], LEFT))
        self.wait()

        self.wait(5)


class PrngIntro(Scene):
    def construct(self):
        set_default_colors()

        prng = PRNG().shift(1 * LEFT)
        self.play(FadeIn(prng))
        self.wait()
        prng.set_seed("0110")
        self.play(
            Write(prng.seed),
            Create(prng.seed_arrow),
        )
        self.wait()
        ar = Arrow(
            start=prng.box.get_right(),
            end=prng.box.get_right() + 1.5 * RIGHT,
            color=text_color,
        )
        self.play(Create(ar))

        # create a tex object with 5 lines, each containing 10 random bits
        pseudorandom_str = r"\raggedright "
        for i in range(10):
            pseudorandom_str += (
                r"$" + "".join([str(random.randint(0, 1)) for _ in range(24)]) + r"$"
            )
            pseudorandom_str += r"\\ "

        pseudorandom_tex = Tex(
            pseudorandom_str, color=text_color, font_size=40
        ).next_to(ar, RIGHT)

        self.play(Write(pseudorandom_tex), run_time=5)
        self.wait()
        not_random_tex = (
            Tex(r"{{Not random!}}", color=text_color, font_size=60)
            .next_to(pseudorandom_tex, UP, buff=0.5)
            .shift(1 * LEFT)
        )

        bf = 0.7

        self.play(
            FadeOut(prng),
            FadeOut(ar),
            Write(not_random_tex),
            pseudorandom_tex.animate.shift(1 * LEFT),
        )
        self.wait()

        pseudorandom_str = r"\raggedright "
        for i in range(10):
            pseudorandom_str += (
                r"$" + "".join([str(random.randint(0, 1)) for _ in range(24)]) + r"$"
            )
            pseudorandom_str += r"\\ "

        random_tex = Tex(pseudorandom_str, color=text_color, font_size=40).move_to(
            -1 * pseudorandom_tex.get_center()
        )
        is_random_tex = Tex(r"{{Random}}", color=text_color, font_size=60).next_to(
            random_tex, UP, buff=0.5
        )

        self.play(Write(random_tex), Write(is_random_tex), run_time=1)
        self.wait()

        # hard_tex = Tex(r"Hard to \\ distinguish", color=text_color, font_size=50)
        # self.play(
        #     Write(hard_tex),
        #     run_time = 1
        #     )
        # self.wait()


fs = 50


class PolynomialsIntro(Scene):
    def construct(self):
        set_default_colors()

        polynomials = Group(
            *[
                Tex(str, color=text_color, font_size=fs)
                for str in [
                    r"{{$(x-2)^3$}}{{$ + $}}{{$x(x-2)$}}",
                    r"{{$(x+4)(x+2)(x-1)$}}{{$ - $}}{{$10x^2 + 8x$}}",
                ]
            ]
        ).arrange(DOWN, buff=1)

        self.play(
            AnimationGroup(
                *[FadeIn(p) for p in polynomials],
                lag_ratio=0.5,
            )
        )
        self.wait()

        p1 = [
            Tex(str, color=text_color, font_size=fs).move_to(polynomials[0])
            for str in [
                r"{{$x^3 - 6x^2 + 12x - 8$}}{{$ + $}}{{$x(x-2)$}}",
                r"{{$x^3 - 6x^2 + 12x - 8$}}{{$ + $}}{{$x^2 - 2x$}}",
                r"{{$x^3 - 5x^2 + 10x - 8$}}",
            ]
        ]

        p2 = [
            Tex(str, color=text_color, font_size=fs).move_to(polynomials[1])
            for str in [
                r"{{$(x^2 + 6x + 8)(x-1)$}}{{$ - $}}{{$10x^2 + 8x$}}",
                r"{{$x^3 + 5x^2 + 2x - 8$}}{{$ - $}}{{$10x^2 + 8x$}}",
                r"{{$x^3 - 5x^2 + 10x - 8$}}",
            ]
        ]

        for i, p in enumerate([p1, p2]):
            for j in range(3):
                self.play(
                    Transform(polynomials[i], p[j]),
                )
                self.wait(0.3)
            self.wait()

        same = Tex("Same polynomial!", color=GREEN, font_size=fs).next_to(
            polynomials, RIGHT, buff=0.5
        )
        self.play(Write(same))
        self.wait()
        self.play(
            *[FadeOut(o) for o in self.mobjects],
        )
        self.wait()


class PolynomialsMultiplyingOut(Scene):
    def construct(self):
        set_default_colors()
        self.next_section(skip_animations=False)

        len = 20
        polynomials = []
        polynomials.append(
            [
                Tex(r"$(x+2)^{20\,000}$", color=text_color, font_size=fs),
                Tex(r"$(x+1)^{10\,000}\cdot$", color=text_color, font_size=fs),
                *[
                    Tex(r"$(x+1)\cdot$", color=text_color, font_size=fs)
                    for _ in range(len)
                ],
            ]
        )
        polynomials.append(
            [
                Tex(r"$.$", color=text_color, font_size=fs).scale(0.0001),
                Tex(
                    r"$(x^3 + 5x^2 + 8x + 5)^{10\,000}$", color=text_color, font_size=fs
                ),
                *[
                    Tex(r"$(x^3 + 5x^2 + 8x + 5)\cdot$", color=text_color, font_size=fs)
                    for _ in range(len)
                ],
            ]
        )

        bf = 0.1
        self.play(
            FadeIn(
                Group(polynomials[0][1], polynomials[0][0])
                .arrange(RIGHT, buff=bf)
                .shift(0.5 * UP)
            ),
            FadeIn(
                Group(polynomials[1][1], polynomials[1][0])
                .arrange(RIGHT, buff=bf)
                .shift(0.5 * DOWN)
            ),
        )
        self.wait()

        for i in range(0, len):
            new_polynomials = [
                Tex(
                    r"$(x+1)^{" + str(10000 - i - 1) + r"}\cdot$",
                    color=text_color,
                    font_size=fs,
                ),
                Tex(
                    r"$(x^3 + 5x^2 + 8x + 5)^{" + str(10000 - i - 1) + r"}\cdot$",
                    color=text_color,
                    font_size=fs,
                ),
            ]
            for it in range(2):
                polynomials[it][0].generate_target()
                polynomials[it][0].target.shift(0.4 * RIGHT)
                polynomials[it][1].generate_target()
                polynomials[it][1].target = new_polynomials[it].next_to(
                    polynomials[it][0].target, LEFT, buff=bf
                )

                polynomials[it][2 + i].next_to(polynomials[it][1].target, LEFT, buff=bf)
                polynomials[it][2 + i].generate_target()

                for j in range(i - 1, -1, -1):
                    polynomials[it][2 + j].generate_target()
                    polynomials[it][2 + j].target.next_to(
                        polynomials[it][2 + j + 1].target, LEFT, buff=bf
                    )

            anims = []
            for it in range(1):
                anims += [
                    MoveToTarget(polynomials[it][0]),
                    MoveToTarget(polynomials[it][1]),
                    *[
                        MoveToTarget(polynomials[it][2 + j]) for j in range(i)
                    ],  # Simplified range
                    Create(polynomials[it][2 + i]),
                ]

            self.play(
                *anims,
                run_time=0.3,  # Correct placement and formatting of run_time
            )


class PolynomialsIntro2(Scene):
    def construct(self):
        set_default_colors()
        self.next_section(skip_animations=False)

        polynomials = Group(
            *[
                Tex(str, color=text_color, font_size=fs)
                for str in [
                    r"{{$($}}{{$x$}}{{$+1)^{10\,000}($}}{{$x$}}{{$+2)^{20\,000}$}}{{$\;$}}",
                    r"{{$($}}{{$x$}}{{${}^3 + 5$}}{{$x$}}{{${}^2 + 8$}}{{$x$}}{{$ + 5)^{10\,000}$}}{{$\;$}}",
                ]
            ]
        ).arrange(DOWN, buff=1)

        self.play(
            AnimationGroup(
                *[FadeIn(p) for p in polynomials],
                lag_ratio=0.5,
            )
        )
        self.wait()

        # animation for generating a random integer
        test_int = 42987
        len = 10
        random_ints = [random.randint(0, 100000) for _ in range(len)]
        random_ints_tex = [
            Tex(str(i), color=text_color, font_size=fs)
            .move_to(polynomials[0].get_center())
            .shift(2 * UP)
            for i in random_ints + [test_int]
        ]

        run_time = 0.2
        for i in range(len + 1):
            self.add_sound(random_click_file())
            if i == 0:
                self.play(FadeIn(random_ints_tex[0]), run_time=run_time)
            else:
                self.play(
                    Transform(random_ints_tex[0], random_ints_tex[i]), run_time=run_time
                )

        self.wait()

        val1 = ((test_int + 1) ** 10000) % (10**9 + 7)
        val2 = ((test_int + 2) ** 20000) % (10**9 + 7)
        val3 = val1 * val2 % (10**9 + 7)
        val4 = (test_int**3 + 5 * test_int**2 + 8 * test_int + 5) % (10**9 + 7)
        val5 = val4**10000 % (10**9 + 7)

        p1 = [
            Tex(str, color=text_color, font_size=fs).move_to(polynomials[0])
            for str in [
                r"{{$($}}{{$42987$}}{{$+1)^{10\,000}($}}{{$42987$}}{{$+2)^{20\,000}$}}{{$\;$}}",
                r"{{$($}}{{$42987$}}{{$+1)^{10\,000}($}}{{$42987$}}{{$+2)^{20\,000}$}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{$\,$}}{{$"
                + str(val1)
                + r"$}}{{$\,\cdot\,($}}{{$42987$}}{{$+2)^{20\,000}$}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{$\,$}}{{$"
                + str(val1)
                + r"$}}{{$\,\cdot\, $}}{{"
                + str(val2)
                + r"}}{{$\,$}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{ }}{{$"
                + str(val3)
                + r"$}}{{ }}{{ }}{{ }}{{$\;\;\;\; \pmod{10^9+7}$}}",
            ]
        ]

        p2 = [
            Tex(str, color=text_color, font_size=fs).move_to(polynomials[1])
            for str in [
                r"{{$($}}{{$42987$}}{{${}^3 + 5\cdot$}}{{$42987$}}{{${}^2 + 8\cdot$}}{{$42987$}}{{$ + 5)^{10\,000}$}}{{$\;$}}",
                r"{{$($}}{{$42987$}}{{${}^3 + 5\cdot$}}{{$42987$}}{{${}^2 + 8\cdot$}}{{$42987$}}{{$ + 5)^{10\,000}$}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{$($}}{{$"
                + str(val4)
                + r"$}}{{$ $}}{{$ $}}{{$ $}}{{$ $}}{{$ )^{10\,000}$}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{ }}{{$"
                + str(val5)
                + r"$}}{{$ $}}{{$ $}}{{$ $}}{{$ $}}{{$ $}}{{$\;\;\;\; \pmod{10^9+7}$}}",
                r"{{ }}{{$"
                + str(val3)
                + r"$}}{{ }}{{ }}{{ }}{{$ $}}{{$ $}}{{$\;\;\;\; \pmod{10^9+7}$}}",
            ]
        ]

        num_copies = [random_ints_tex[0].copy() for _ in range(5)]

        self.play(
            FadeOut(random_ints_tex[0]),
            Transform(polynomials[0], p1[0]),
            Transform(polynomials[1], p2[0]),
            *[
                num_copies[i].animate.move_to(p1[0][pos])
                for i, pos in enumerate([1, 3])
            ],
            *[
                num_copies[2 + i].animate.move_to(p2[0][pos])
                for i, pos in enumerate([1, 3, 5])
            ],
        )
        self.remove(
            *num_copies,
        )
        self.wait()

        self.play(
            Transform(polynomials[0], p1[1]),
            Transform(polynomials[1], p2[1]),
        )
        self.wait()

        for j in range(3):
            self.play(
                Transform(polynomials[0], p1[2 + j]),
            )
            self.wait()

        for j in range(2):
            self.play(
                Transform(polynomials[1], p2[2 + j]),
            )
            self.wait()

        self.play(
            *[Indicate(polynomials[i][1], color=text_color) for i in range(2)],
        )
        self.wait()
        self.play(
            polynomials.animate.shift(3 * LEFT),
        )
        different = Tex("Different polynomials!", color=RED, font_size=fs).next_to(
            polynomials, RIGHT, buff=1
        )
        self.play(Write(different))
        self.wait()
        self.play(
            FadeOut(different),
            Transform(polynomials[1], p2[-1].shift(3 * LEFT + 2 * UP)),
            polynomials[0].animate.shift(2 * UP),
        )
        self.wait()
        same = (
            Tex(
                r"{{Same polynomial! \\ }}{{(probably)\\}}{{probability $>99\%$\\}}",
                color=GREEN,
                font_size=fs,
            )
            .move_to(different)
            .align_to(different, LEFT)
            .shift(2 * UP)
        )

        for i in range(2):
            self.play(Write(same[i]))
            self.wait()

        self.wait()

        simple_polynomials = (
            Group(
                *[
                    Tex(str, color=c, font_size=fs)
                    for str, c in zip(
                        [
                            r"{{$x^2 + 1$}}",
                            r"{{$3 - x$}}",
                        ],
                        [BLUE, BLUE],
                    )
                ]
            )
            .arrange(DOWN, buff=0.5)
            .shift(1 * DOWN)
        )

        p1 = [
            Tex(str, color=text_color, font_size=fs).move_to(simple_polynomials[0])
            for str in [r"{{$1^2 + 1$}}", r"{{$2$}}"]
        ]

        p2 = [
            Tex(str, color=text_color, font_size=fs).move_to(simple_polynomials[1])
            for str in [
                r"{{$1 + 1$}}",
                r"{{$2$}}",
            ]
        ]

        self.play(
            AnimationGroup(
                *[FadeIn(p) for p in simple_polynomials],
                lag_ratio=0.5,
            )
        )
        self.wait()

        # for j in range(2):
        #     self.play(
        #         Transform(simple_polynomials[0], p1[j]),
        #         Transform(simple_polynomials[1], p2[j]),
        #     )
        #     self.wait(0.5)
        # self.wait()

        self.next_section(skip_animations=False)

        # Create axes
        axes = (
            Axes(
                x_range=[-3, 3, 1],  # x_min, x_max, x_step
                y_range=[-5, 10, 1],  # y_min, y_max, y_step
                x_length=7,
                y_length=5,
                axis_config={
                    # "color": BLUE,
                    "include_ticks": False,  # Applies globally if not overridden
                },
                x_axis_config={
                    "include_ticks": True,  # Enable ticks on x-axis
                    "include_numbers": True,  # Enable number labels on x-axis
                    "numbers_to_include": [
                        -3,
                        -2,
                        -1,
                        0,
                        1,
                        2,
                        3,
                    ],  # Specific numbers to label
                    # k"number_scale_value": 0.5,  # Adjust the scale of numbers
                },
                y_axis_config={
                    "include_ticks": False,  # Continue to remove ticks from y-axis
                    "include_numbers": False,  # Continue to remove numbers from y-axis
                },
                tips=False,  # No arrow tips
            )
            .scale(0.7)
            .to_edge(DOWN, buff=0.5)
        )

        # Create the graph
        graph1 = axes.plot(lambda x: x**2 + 1, color=BLUE)
        graph2 = axes.plot(lambda x: 3 - x, color=BLUE)

        # Create labels
        graph_label1 = axes.get_graph_label(graph1, label="x^2+1")
        graph_label2 = axes.get_graph_label(graph2, label="3-x")

        # Draw the axes and the graph
        self.play(
            Create(axes),
            *[Create(graph) for graph in [graph1, graph2]],
            simple_polynomials[0]
            .animate.move_to(graph_label1.get_center())
            .shift(0 * UP),
            simple_polynomials[1]
            .animate.move_to(graph_label2.get_center())
            .shift(0 * UP),
        )
        self.wait(1)  # Wait for 1 second

        intersections = [
            axes.coords_to_point(-2, 5),  # Point (-2, 5)
            axes.coords_to_point(1, 2),  # Point (1, 2)
        ]

        # Create dots at intersections
        dots = VGroup(*[Dot(point, color=YELLOW) for point in intersections])
        self.play(*[Flash(dot, color=RED) for dot in dots])
        self.wait()

        same[2].align_to(same[0], LEFT).align_to(same[1], UP)
        self.play(
            Transform(same[1], same[2]),
        )
        self.wait()


class PseudocodeBruteforce(Scene):
    def construct(self):
        pseudocode = Tex(
            Path("../code/bruteforce_all_seeds.tex").read_text(),
            tex_environment=None,
        )
        self.play(FadeIn(pseudocode), run_time=1)
        self.wait(3)

        pos1 = 5 * LEFT + 0.1 * UP
        ar = Arrow(start=pos1, end=pos1 + 1.5 * RIGHT, color=RED)
        self.play(Create(ar), run_time=1)
        self.wait()
        x = 0.66
        self.play(ar.animate.shift(x * DOWN), run_time=1)
        self.wait()
        self.play(ar.animate.shift((1.15 - x) * DOWN), run_time=1)
        self.wait()
        self.play(ar.animate.shift(0.66 * DOWN), run_time=1)
        self.wait(3)


class Final(Scene):
    def construct(self):
        thanks_text = "Big thanks to everyone who gave us feedback on an early version of this video!"
        patrons_thanks_text = "Our amazing Patrons:"
        patrons_text = [
            "Thomas Dubach",
            "Adam Zielinski",
            "Mika chu",
            "Hugo Madge León",
            "George Chahir",
            "Anh Dung Le",
            "Adam Dřínek",
            "Amit Nambiar",
            "Pepa Tkadlec",
            "sjbtrn",
            "George Mihaila",
            "Tomáš Sláma",
        ]
        support_tex = "Thank you for your support!"

        thanks_tex = Tex(thanks_text, color=TEXT_COLOR).scale(0.8).to_edge(UP)
        patrons_thanks_tex = (
            Tex(patrons_thanks_text, color=TEXT_COLOR)
            .scale(0.8)
            .next_to(thanks_tex, DOWN, buff=1)
        )
        patrons_tex = (
            VGroup(*[Tex(t, color=TEXT_COLOR).scale(0.8) for t in patrons_text])
            .arrange_in_grid(cell_alignment=LEFT)
            .next_to(patrons_thanks_tex, DOWN, buff=0.5)
        )
        support_tex = (
            Tex(support_tex, color=TEXT_COLOR)
            .scale(1.2)
            .next_to(patrons_tex, DOWN, buff=1)
        )
        self.add(patrons_thanks_tex, patrons_tex, support_tex)
        self.wait(5)


class Recap(Scene):
    def construct(self):
        set_default_colors()

        prng = PRNG("NW").scale(0.8)
        truly = Tex(r"Random bits", color=text_color, font_size=fs)

        bits = []
        for i in range(2):
            bits_str = ""
            for j in range(3):
                bits_str += (
                    "".join([str(random.randint(0, 1)) for _ in range(20)]) + r" \\ "
                )
            bits.append(Tex(bits_str, color=text_color, font_size=40))

        truly_group = Group(truly, bits[0]).arrange(DOWN, buff=0.5)
        prng_group = Group(prng, bits[1]).arrange(DOWN, buff=0.5)

        all_group = Group(truly_group, prng_group).arrange(RIGHT, buff=3)
        prng_group.to_edge(UP, buff=0.5)
        truly_group.align_to(prng_group, DOWN)

        self.play(FadeIn(prng), Write(bits[1]))
        self.wait()

        self.play(FadeIn(truly), Write(bits[0]))
        self.wait()

        truly_algo = Algo().move_to(20 * RIGHT)
        self.add(truly_algo)
        self.play(
            truly_algo.set_input(
                r"{{$(x+1)^2$}}{{$\, \overset{?}{=}\,$}}{{$ (x-1)^2$}}", 0, no_text=True
            ),
            truly_algo.set_input(r".", 1, no_text=True),
            truly_algo.set_output(
                r".",
            ),
            run_time=0.0001,
        )
        self.remove(truly_algo)
        truly_algo.scale(0.6).next_to(truly_group, DOWN, buff=1)

        self.play(
            FadeIn(truly_algo),
        )
        self.wait()
        truly_bits = bits[0].copy()
        self.play(
            truly_bits.animate.scale(0.5).next_to(truly_algo.arrows[1], LEFT, buff=0.2)
        )
        self.wait()

        prng_algo = truly_algo.copy()
        self.play(prng_algo.animate.next_to(prng_group, DOWN, buff=1))
        self.wait()

        prng_bits = bits[1].copy()
        self.play(
            prng_bits.animate.scale(0.5).next_to(prng_algo.arrows[1], LEFT, buff=0.2)
        )
        self.wait()

        truly_p = (
            Tex(r"$p > 99\%$", color=text_color)
            .scale(0.7)
            .next_to(truly_algo.inputs[2], DOWN, buff=0.5)
        )
        truly_n = (
            Tex(r"$\not =$", color=text_color)
            .scale(0.7)
            .next_to(truly_algo.arrows[2], RIGHT, buff=0.2)
        )
        self.play(Write(truly_n), Write(truly_p))
        self.wait()

        prng_p = (
            Tex(r"$p < 1\%$", color=text_color)
            .scale(0.7)
            .next_to(prng_algo.inputs[2], DOWN, buff=0.5)
        )
        prng_n = (
            Tex(r"$\not =$", color=text_color)
            .scale(0.7)
            .next_to(prng_algo.arrows[2], RIGHT, buff=0.2)
        )
        self.play(Write(prng_n), Write(prng_p))
        self.wait()

        rectangles = [SurroundingRectangle(p, color=RED) for p in [truly_p, prng_p]]
        self.play(*[Create(r) for r in rectangles])
        self.wait()

        self.play(*[FadeOut(r) for r in rectangles])
        self.wait()

        self.play(
            Create(rectangles[1]),
        )
        self.play(
            Transform(
                prng_p, Tex(r"$p \ge 1\%$", color=text_color).scale(0.7).move_to(prng_p)
            )
        )
        self.wait()


class AfterRecap(Scene):
    def construct(self):
        set_default_colors()

        algo = Algo().shift(20 * RIGHT)
        prng = PRNG("NW").scale(0.8).shift(20 * RIGHT)
        self.play(
            algo.set_input(r".", 0, no_text=True),
            algo.set_input(r"00001101111", 1, no_text=True),
            algo.set_output(r"."),
            prng.set_seed("10110"),
            run_time=0.001,
        )
        ar = algo.arrows[0].copy().next_to(algo.inputs[1], LEFT, buff=0.2)
        prng.next_to(ar, LEFT, buff=0.2)
        t = Group(algo, prng, ar)
        self.remove(t)
        self.play(FadeIn(t.scale(0.8).move_to(ORIGIN)))
        self.wait()

        self.play(
            Circumscribe(prng.seed, color=RED),
        )

        bracetext = BraceText(
            prng.seed,
            r"$O(\log n)$ bits",
            brace_direction=UP,
            color=text_color,
            buff=0.1,
        )
        self.play(FadeIn(bracetext))
        self.wait()


class ZeroKnowledge(Scene):
    def construct(self):
        set_default_colors()

        zero_tex = Tex(r"Zero-knowledge proofs", color=text_color, font_size=100)
        self.play(Write(zero_tex))
        self.wait()
