from statistical_test import Funnel
from utils.util_general import *

set_default_colors()
label_scale = 0.8


class AnnotatedArrow(Arrow):
    def __init__(self, text: str, *args, text_scale=1, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: if needed, position text based on the direction of the arrow
        self.text = (
            Tex(text, color=BASE00).scale(text_scale).next_to(self.get_center(), UP)
        )

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(GrowArrow(self), Write(self.text))


class PRNG(VGroup):
    def __init__(self, name="PRNG"):
        super().__init__()
        self.box = Rectangle(
            color=BLUE, fill_color=BLUE, fill_opacity=1, width=2.5, height=1.5
        )
        self.text = Tex(name, color=BASE2)
        if name == "NW":
            self.text = Tex(r"{{Nissan-Wigderson \\}}{{ PRNG}}", color=BASE2)
            self.text[0].scale(0.5)
        self.add(self.box)
        self.add(self.text)

        self.seed = None
        self.seed_arrow = None

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(Create(self.box), Write(self.text))

    def set_seed(self, seed: str, buff=1.5):
        new_seed = (
            Tex(seed, color=BASE00)
            .move_to(self.box.get_center())
            .next_to(self.box, LEFT, buff=buff)
        )
        if seed == ".":
            new_seed.set_opacity(0)

        if self.seed is not None:
            old_seed = self.seed
            self.seed = new_seed
            self.add(self.seed)
            return LaggedStart(
                old_seed.animate.shift(DOWN * 0.5).fade(1),
                Write(new_seed),
            )
            # return self.seed.animate.become(new_seed)
        self.seed = new_seed
        self.add(self.seed)

        if self.seed_arrow is None:
            self.seed_arrow = AnnotatedArrow(
                start=self.seed.get_edge_center(RIGHT),
                end=self.box.get_edge_center(LEFT),
                color=BASE00,
                text="seed",
                text_scale=label_scale,
            )
            self.add(self.seed_arrow)
            self.add(self.seed_arrow.text)
            # Create the arrow only once most of the text is written
            return LaggedStart(
                Write(self.seed),
                Create(self.seed_arrow),
                lag_ratio=0.3,
            )
        else:
            return Write(self.seed)


class Algo(VGroup):
    def __init__(self):
        super().__init__()
        self.box = Rectangle(
            color=RED, fill_color=RED, fill_opacity=1, width=2.5, height=1.5
        )
        self.text = Tex("A", color=BASE2).scale(1.5)
        self.add(self.box)
        self.add(self.text)

        self.arrows = [None, None, None]
        self.inputs = [None, None, None]

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(Create(self.box), Write(self.text))

    def set_input(self, input: str, pos: int, no_text=False):
        if not input:
            new_input = nil_object()
        else:
            new_input = (
                Tex(input, color=BASE00)
                .scale(label_scale)
                .next_to(self.box, LEFT, buff=1.5)
                .shift((-1 + 2 * pos) * label_scale * self.box.height * 0.5 * DOWN)
            )

        if self.inputs[pos] is not None:
            old_input = self.inputs[pos]
            self.inputs[pos] = new_input
            self.add(self.inputs[pos])
            return LaggedStart(
                old_input.animate.shift(DOWN * 0.5).fade(1),
                Write(new_input),
            )

        self.inputs[pos] = new_input
        self.add(self.inputs[pos])

        if self.arrows[pos] is None:
            self.arrows[pos] = AnnotatedArrow(
                start=self.inputs[pos].get_edge_center(RIGHT),
                end=self.box.get_edge_center(LEFT)
                + (-1 + 2 * pos) * label_scale * self.box.height * 0.5 * DOWN,
                color=BASE00,
                text=(
                    ("input" if pos == 0 else r"\baselineskip=1em random\\bits")
                    if no_text == False
                    else ""
                ),
                text_scale=0.8 * label_scale,
            )
            self.add(self.arrows[pos])
            self.add(self.arrows[pos].text)
            # Create the arrow only once most of the text is written
            return LaggedStart(
                Write(self.inputs[pos]),
                Create(self.arrows[pos]),
                lag_ratio=0.3,
            )
        else:
            return Write(self.inputs[pos])

    def set_output(self, output: str):
        if not output:
            new_output = nil_object()
        else:
            new_output = (
                Tex(output, color=BASE00)
                .scale(label_scale)
                .next_to(self.box, RIGHT, buff=1.5)
            )

        if self.inputs[2] is not None:
            old_output = self.inputs[2]
            self.inputs[2] = new_output
            self.add(self.inputs[2])

            return LaggedStart(
                old_output.animate.shift(DOWN * 0.5).fade(1),
                Write(new_output),
            )
        self.inputs[2] = new_output
        self.add(self.inputs[2])

        if self.arrows[2] is None:
            self.arrows[2] = Arrow(
                end=self.inputs[2].get_edge_center(LEFT),
                start=self.box.get_edge_center(RIGHT),
                color=BASE00,
            )
            self.add(self.arrows[2])

            # Create the arrow only once most of the text is written
            return LaggedStart(
                Write(self.inputs[2]),
                Create(self.arrows[2]),
                lag_ratio=0.3,
            )
        else:
            return Write(self.inputs[2])

    def set_label_color(self, color):
        VGroup(*self.inputs, *self.arrows).set_color(color)


class PRNGIntro(Scene):
    def construct(self):
        prng = PRNG().shift(LEFT)
        self.play(Create(prng))
        self.wait()
        self.play(prng.set_seed("011001"))
        self.wait()

        seed_brace = BraceLabel(
            prng.seed,
            r"$O(\log n)$ random bits",
            label_constructor=Tex,
            brace_direction=UP,
            buff=0.4,
        )
        seed_brace.label.shift(RIGHT)
        self.play(seed_brace.creation_anim(label_anim=Write))
        self.wait()

        out_strs = []
        for it in range(4):
            output_str = ""
            for i in range(1):
                for j in range(16):
                    if it < 3:
                        output_str += random.choice("01")
                    else:
                        if j % 2 == 0:
                            output_str += "0"
                        else:
                            output_str += "0"
                output_str += r"\\ "
            out_strs.append(output_str)

        output = Tex(out_strs[0], color=BASE00).shift(RIGHT * 4)
        self.play(
            LaggedStart(
                Create(
                    AnnotatedArrow(
                        "",  # I don't think this needs explanation
                        start=prng.get_edge_center(RIGHT),
                        end=output.get_edge_center(LEFT),
                        color=BASE00,
                    )
                ),
                Create(output),
                lag_ratio=0.3,
            )
        )
        self.wait()

        output_brace = BraceLabel(
            output,
            "$n$ pseudorandom bits",
            label_constructor=Tex,
            brace_direction=UP,
            buff=0.4,
        )
        self.play(output_brace.creation_anim(label_anim=Write))
        self.wait()

        for seed, output_str in [
            ("110000", out_strs[1]),
            ("101011", out_strs[2]),
        ]:
            self.play(prng.set_seed(seed), FadeOut(output))
            output = Tex(output_str, color=BASE00).shift(RIGHT * 4)
            self.play(Write(output))
            self.wait()

        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != output],
            output.animate.move_to(ORIGIN),
        )
        self.wait()

        is_tex = Tex(r"Is this random? ", color=text_color).next_to(output, UR, buff=1)
        ar = Arrow(
            start=is_tex.get_edge_center(LEFT),
            end=output.get_corner(UR),
            color=text_color,
        )
        self.play(Write(is_tex), Create(ar))
        self.wait()

        self.play(
            Transform(output, Tex(out_strs[3], color=BASE00).move_to(ORIGIN)),
        )
        self.wait()


class BPP(Scene):
    def construct(self):
        set_default_colors()

        self.next_section(skip_animations=True)
        plan_tex = Tex(
            r"Pseudorandom generator $\Rightarrow \text{P} = \text{BPP}$.  "
        ).shift(2 * UP)
        self.play(Write(plan_tex))
        self.wait()
        self.play(FadeOut(plan_tex))
        self.wait()

        algo = Algo().shift(2 * RIGHT)

        self.play(Create(algo))
        self.wait()

        self.play(algo.set_input(r"$(x+1)^2 \overset{?}{=} x^2 + 2x + 1$", 0))
        self.wait()

        self.play(algo.set_input("1010101101100001", 1))
        self.wait()

        self.play(algo.set_output("SAME"))
        self.wait()

        self.play(algo.set_input(r"$(x+1)^2 \overset{?}{=} (x-1)^2$", 0))
        self.wait()

        self.play(algo.set_output("DIFFERENT"))
        self.wait()

        prob_tex = (
            Tex(r"$p\ge 99\%$")
            .scale(label_scale)
            .next_to(algo.inputs[2], DOWN)
            .align_to(algo.inputs[2], LEFT)
        )
        self.play(Write(prob_tex))
        self.wait()

        algo_group1 = Group(algo, prob_tex)
        self.play(
            algo_group1.animate.to_edge(UP),
        )
        self.play(
            *[FadeOut(algo.arrows[i].text) for i in range(2)],
        )
        self.remove(*[algo.arrows[i].text for i in range(2)])
        self.wait()

        prng_algo = Algo().shift(DOWN).shift(3 * RIGHT)
        self.play(Create(prng_algo))
        self.wait()

        prng = (
            PRNG()
            .scale(0.7)
            .next_to(prng_algo, LEFT)
            .shift(label_scale * prng_algo.box.height * 0.5 * DOWN)
            .shift(4.2 * LEFT)
        )
        self.play(Create(prng))
        self.wait()

        self.play(prng.set_seed("0110", buff=1))
        self.wait()

        prng_ar = Arrow(
            start=ORIGIN,
            end=1.0 * RIGHT,
            color=BASE00,
        ).shift(prng.get_edge_center(RIGHT) + 0.1 * LEFT)
        self.play(
            prng_algo.set_input("10100110001", 1, no_text=True),
            Create(prng_ar),
        )
        self.wait()

        self.play(
            prng_algo.set_input(
                r"$(x+1)^2 \overset{?}{=} x^2 + 2x + 1$", 0, no_text=True
            )
        )
        self.wait()

        self.play(prng_algo.set_output("SAME"))
        self.wait()

        self.play(prng_algo.set_input(r"$(x+1)^2 \overset{?}{=} (x-1)^2$", 0))
        self.wait()

        self.play(prng_algo.set_output("?"))
        self.wait()

        self.play(prng_algo.set_output("DIFFERENT"))
        self.wait()

        prob_tex2 = (
            Tex(r"$p\le 1\%$")
            .scale(label_scale)
            .next_to(prng_algo.inputs[2], DOWN)
            .align_to(prng_algo.inputs[2], LEFT)
        )
        self.play(Write(prob_tex2))
        self.wait()

        self.play(
            prng_algo.set_output("SAME"),
            Transform(
                prob_tex2,
                Tex(r"p$\ge 99\%$")
                .scale(label_scale)
                .next_to(prng_algo.inputs[2], DOWN)
                .align_to(prng_algo.inputs[2], LEFT),
            ),
        )
        self.wait()

        algo_group2 = Group(prng_algo, prng, prng_ar, prob_tex2)
        self.play(
            FadeOut(algo_group2),
            algo_group1.animate.move_to(ORIGIN),
        )

        self.next_section()

        algo.set_z_index(5)
        self.play(
            algo.set_input("", 1),
            algo.set_output(""),
            FadeOut(prob_tex),
        )
        self.wait()
        funnel = Funnel().scale(2).shift(DOWN)
        self.play(
            Write(funnel),
            algo.animate.scale(0.5)
            .move_to(funnel.get_top())
            .shift(DOWN)
            .set_label_color(BLACK),
        )

        ### TODO

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )
        self.wait()
        self.play(FadeIn(algo_group2))
        self.wait()

        self.play(
            prng_algo.set_output("DIFFERENT"),
            Transform(
                prob_tex2,
                Tex(r"$\ge 1\%$ probability")
                .scale(label_scale)
                .next_to(prng_algo.inputs[2], DOWN),
            ),
        )
        self.wait()
