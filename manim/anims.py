# manim -pql --fps 15 -r 290,180 anims.py Polylogo
from utils.util_general import *


class Polylogo(Scene):
    def construct(self):
        set_default_colors()
        authors = Tex(
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}",
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


class Playground(Scene):
    def construct(self):
        pass


class TheoremStatement(Scene):
    def construct(self):
        set_default_colors()

        h = 2.5
        people = Group(*[
            Group(
                ImageMobject("img/" + str + ".jpg").scale_to_fit_height(h),
                Tex(name, color=text_color, font_size=35),
            ).arrange(DOWN)
            for str, name in zip(
                ["nisan", "wigderson", "blum", "micali", "yao"],
                ["Noam Nisan", "Avi Wigderson", "Manuel Blum", "Silvio Micali", "Andy Yao"],
            )
        ]).arrange(RIGHT, buff=0.3)
        
        for i in range(2):
            if i == 0: 
                r = range(0, 2)
            else:
                r = range(2, len(people)) 
            self.play(
                AnimationGroup(
                    *[
                        arrive_from(people[i], RIGHT)
                        for i in r
                    ],
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
                    "Under some assumptions that most people believe,",
                    r"any problem that can be solved\\"
                    r"efficiently with randomness\\"
                    r"can also be solved efficiently without it.",
                ]
            )
        ]
        Group(hypothesis, conclusion).arrange(DOWN).shift(1*DOWN)

        self.play(Write(hypothesis))
        self.play(Write(conclusion))
        self.wait()

        self.play(
            conclusion.animate.become(
                Tex("$P = BPP$", color=text_color, font_size=80).shift(DOWN * 0.3).shift(1*DOWN)
            ),
        )
        self.wait()
        hypothesis_formal_str = (
            r"If there is a problem solvable in time $2^{n}$\\"
            "that cannot be solved  with a circuit "
            "of size $2^{0.0001n}$,"
        )
        hypothesis_formal = Tex(
            hypothesis_formal_str, color=text_color, font_size=50
        ).shift(UP).shift(1*DOWN)

        hypothesis_original = hypothesis.copy()
        self.play(hypothesis.animate.become(hypothesis_formal))
        self.wait()
        self.play(hypothesis.animate.become(hypothesis_original))
        self.wait()


class ShowCode(Scene):
    def construct(self):
        text = Path("../code/get_random_bits.py").read_text()
        self.add(make_code(text))
        self.wait(5)
