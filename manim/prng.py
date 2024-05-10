from utils.funnel import Funnel
from utils.util_general import *

set_default_colors()
label_scale = 0.8


class AnnotatedArrow(Arrow):
    def __init__(self, text: str, *args, text_scale=1, buff=0.25, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: if needed, position text based on the direction of the arrow
        self.text = (
            Tex(text, color=BASE00)
            .scale(text_scale)
            .next_to(self.get_center(), UP, buff=buff)
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
            self.text = Tex(r"{{Nisan-Wigderson \\}}{{ PRNG}}", color=BASE2)
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

    def set_seed(self, seed: str, buff=1.5, scale=1):
        if seed is None:
            new_seed = nil_object()
        else:
            new_seed = Tex(seed, color=BASE00).scale(scale)
        new_seed.move_to(self.box).next_to(self.box, LEFT, buff=buff)

        if isinstance(self.seed, Dot):
            self.seed = None
            self.remove(self.seed)

        if self.seed is not None:
            old_seed = self.seed
            self.seed = new_seed
            self.add(self.seed)
            return LaggedStart(
                old_seed.animate.shift(DOWN * 0.5).set_opacity(0),
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
                text_scale=label_scale * scale,
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
        ).scale(0.8)
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

    def set_input(self, input: str, pos: int, no_text=False, write=True):
        if not input:
            new_input = nil_object()
        else:
            new_input = (
                Tex(input, color=(BASE00 if input != "." else BACKGROUND_COLOR))
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
                (Write(new_input) if write else FadeIn(new_input)),
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
                buff=0.15,
            )
            self.add(self.arrows[pos])
            self.add(self.arrows[pos].text)
            # Create the arrow only once most of the text is written
            return LaggedStart(
                (Write(self.inputs[pos]) if write else FadeIn(self.inputs[pos])),
                Create(self.arrows[pos]),
                lag_ratio=0.3,
            )
        else:
            return Write(self.inputs[pos]) if write else FadeIn(self.inputs[pos])

    def set_output(self, output: str, color=BASE00, scale=1):
        if not output:
            new_output = nil_object()
        else:
            new_output = (
                Tex(output, color=(BASE00 if output != "." else BACKGROUND_COLOR))
                .scale(label_scale * scale)
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
                GrowArrow(self.arrows[2]),
                lag_ratio=0.3,
            )
        else:
            return Write(self.inputs[2])

    def set_label_color(self, color):
        VGroup(*self.inputs, *self.arrows).set_color(color)
        for arrow in self.arrows:
            if isinstance(arrow, AnnotatedArrow):
                arrow.text.set_color(color)


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
        COLOR_SAME = GREEN
        COLOR_DIFFERENT = RED

        plan_tex = Tex(
            r"Pseudorandom generator $\implies \text{P} = \text{BPP}$.  "
        ).shift(2 * UP)
        self.play(Write(plan_tex))
        self.wait()
        self.play(FadeOut(plan_tex))
        self.wait()

        algo = Algo().shift(3 * RIGHT)

        self.play(Create(algo))
        self.wait()

        self.play(
            algo.set_input(
                r"{{$($}}{{$x$}}{{$+1)^2 $}}{{$\,\overset{?}{=}\,$}}{{$ x$}}{{${}^2 + 2$}}{{$x$}}{{$\, + 1$}}",
                0,
            )
        )
        self.wait()

        self.play(algo.set_input("1010101101100001", 1))
        self.wait()

        prn = (
            PRNG()
            .scale(0.6)
            .move_to(algo.inputs[1])
            .next_to(algo.inputs[1], LEFT)
            .shift(0.5 * LEFT)
        )
        # self.play(Write(prn))
        # self.play(Circumscribe(prn.box))
        # print(prn.box.get_center())
        self.play(prn.set_seed("0110", buff=1, scale=0.8), run_time=0.0001)
        prn_ar = Arrow(
            start=ORIGIN,
            end=1.0 * RIGHT,
            color=BASE00,
        ).shift(prn.get_edge_center(RIGHT) + 0.1 * LEFT)

        self.play(
            algo.set_input("1010011101010001", 1, no_text=True, write=False),
            FadeIn(Group(prn, prn_ar)),
        )
        self.wait()

        self.play(
            Circumscribe(Group(*algo.inputs[0][0:3]), color=RED),
            Circumscribe(Group(*algo.inputs[0][4:]), color=RED),
        )
        self.wait()

        self.play(
            algo.set_input("1010101101100001", 1, write=False),
            FadeOut(Group(prn, prn_ar)),
        )
        self.wait()

        self.play(
            algo.set_input("1010011101010001", 1, no_text=True, write=False),
            FadeIn(Group(prn, prn_ar)),
        )
        self.wait()

        self.play(
            algo.set_input("0000000000000000", 1, write=False),
            FadeOut(Group(prn, prn_ar)),
        )
        self.wait()

        forty = Tex(r"$42$", color=text_color).scale(1.3).to_edge(UP, buff=1.5)
        self.play(Write(forty))

        old_input = algo.inputs[0].copy()
        new_input = (
            Tex(
                r"{{$($}}{{$42$}}{{$+1)^2 $}}{{$\,\overset{?}{=}\,$}}{{$ 42$}}{{${}^2 + 2\cdot $}}{{$42$}}{{$\, + 1$}}",
                color=text_color,
            )
            .scale(0.7)
            .move_to(old_input)
            .align_to(old_input, RIGHT)
        )
        copies = [forty.copy() for _ in range(3)]
        self.play(
            Transform(algo.inputs[0], new_input),
            *[
                copy.animate.scale(1 / 1.3 * 0.7).move_to(new_input[i])
                for i, copy in zip([1, 4, 6], copies)
            ],
        )
        self.remove(*copies)
        self.wait()
        new_input2 = (
            Tex(
                r"{{$1849$}}{{$\,$}}{{$\overset{?}{=}$}}{{$\,$}}{{$1849$}}{{$\,$}}",
                color=text_color,
            )
            .scale(0.7)
            .move_to(old_input)
            .align_to(old_input, RIGHT)
        )
        self.play(Transform(algo.inputs[0], new_input2))
        self.wait()

        self.play(algo.set_output("=", color=COLOR_SAME, scale=2), FadeOut(forty))
        self.wait()

        self.play(
            algo.set_input(r"$(x+1)^2 \overset{?}{=} (x-1)^2$", 0),
            algo.set_input("1010101101100001", 1, write=False),
        )
        self.wait()

        self.play(algo.set_output(r"$\ne$", color=COLOR_DIFFERENT, scale=2))
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
        # self.remove(*[algo.arrows[i].text for i in range(2)])
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
            GrowArrow(prng_ar),
        )
        self.wait()

        self.play(
            prng_algo.set_input(
                r"{{$(x+1)^2$}}{{$\, \overset{?}{=}\,$}}{{$ (x-1)^2$}}", 0, no_text=True
            )
        )
        self.wait()

        # self.play(prng_algo.set_output("=", color=COLOR_SAME, scale=2))
        # self.wait()

        # self.play(prng_algo.set_input(r"$(x+1)^2 \overset{?}{=} (x-1)^2$", 0))
        # self.wait()

        # self.play(prng_algo.set_output("?", scale=2))
        # self.wait()

        self.play(prng_algo.set_output(r"$\ne$", color=COLOR_DIFFERENT, scale=2))
        self.wait()

        prob_tex2 = (
            Tex(r"$p\ge 1\%$")
            .scale(label_scale)
            .next_to(prng_algo.inputs[2], DOWN)
            .align_to(prng_algo.inputs[2], LEFT)
        )
        self.play(Write(prob_tex2))
        self.wait()

        self.play(
            Circumscribe(prng_algo.inputs[0][0], color=RED),
            Circumscribe(prng_algo.inputs[0][2], color=RED),
        )
        self.wait()

        prob_tex2_new = (
            Tex(r"$p< 1\%$")
            .scale(label_scale)
            .next_to(prng_algo.inputs[2], DOWN)
            .align_to(prng_algo.inputs[2], LEFT)
        )
        recc = SurroundingRectangle(prob_tex2_new, color=RED)
        self.play(Create(recc))
        self.play(Transform(prob_tex2, prob_tex2_new))
        self.wait()

        self.play(
            prng_algo.set_output("=", color=COLOR_SAME, scale=2),
            Transform(
                prob_tex2,
                Tex(r"p$> 99\%$")
                .scale(label_scale)
                .next_to(prng_algo.inputs[2], DOWN)
                .align_to(prng_algo.inputs[2], LEFT),
            ),
            FadeOut(recc),
        )
        self.wait()

        self.next_section(skip_animations=False)

        algo_group2 = Group(prng_algo, prng, prng_ar, prob_tex2)
        for i in [0, 1]:
            algo.arrows[i].text.set_opacity(0)
        self.play(
            FadeOut(algo_group2),
            algo_group1.animate.move_to(ORIGIN),
        )

        self.play(
            algo.set_input("", 1),
            algo.set_output(""),
            FadeOut(prob_tex),
        )
        self.wait()
        funnel = Funnel().scale(2.2 * RIGHT + 1.5 * UP).set_z_index(-1)
        VGroup(funnel.ticks, funnel.random).scale(1.5 / 2.2 * RIGHT + UP).scale(0.75)
        self.play(
            Write(funnel),
            algo.animate.scale(0.7)
            .move_to(funnel)
            .align_to(funnel, UP)
            .shift(0.2 * DOWN)
            .set_label_color(BASE03),
        )

        self.play(
            Circumscribe(algo.inputs[0], color=RED),
        )
        self.wait()

        string = funnel.make_string(self, "10100110001")
        string_copy = string.copy()
        self.add(string_copy)
        self.play(
            string.animate.set_color(BASE03).scale(0.5).next_to(algo.arrows[1], LEFT)
        )
        algo.set_output(r"$\ne$", scale=2, color=BASE03)
        self.play(Write(algo.inputs[2].next_to(algo.arrows[2])))
        ok_copy = (
            VGroup(funnel.ticks[1], funnel.random[1])
            .copy()
            .set_opacity(1)
            .shift(0.3 * UP)
        )
        verdict_copy = algo.inputs[2].copy()
        self.play(verdict_copy.animate.become(ok_copy))
        self.wait()

        comment = (
            Tex(r"$\ge 99\%$ probability \\ for random bits", color=text_color)
            .next_to(algo.inputs[2], DOWN, buff=1)
            .shift(1 * RIGHT)
        )
        ar_comment = Arrow(
            start=comment.get_edge_center(UP),
            end=algo.inputs[2].get_edge_center(DOWN),
            color=text_color,
        )
        self.play(Write(comment), Create(ar_comment))
        self.wait()
        comment.generate_target()
        comment.target.shift(2 * DOWN)
        self.play(
            MoveToTarget(comment),
            Transform(
                ar_comment,
                Arrow(
                    start=comment.target.get_edge_center(LEFT),
                    end=comment.target.get_edge_center(LEFT) + 1.5 * LEFT,
                    color=text_color,
                ),
            ),
        )
        self.wait()

        self.play(FadeOut(verdict_copy, algo.inputs[2], comment, ar_comment))
        self.wait()

        algo.set_output(r"$=$", scale=2, color=BASE03)
        self.play(Write(algo.inputs[2].next_to(algo.arrows[2])))
        ok_copy = (
            VGroup(funnel.ticks[0], funnel.random[0])
            .copy()
            .set_opacity(1)
            .shift(0.3 * UP)
        )
        verdict_copy = algo.inputs[2].copy()
        self.play(verdict_copy.animate.become(ok_copy))
        self.wait()

        comment = (
            Tex(
                r"$\ge 99\%$ probability \\ for Nissan-Wigderson \\ pseudorandom bits",
                color=text_color,
            )
            .next_to(algo.inputs[2], DOWN, buff=1)
            .shift(1 * RIGHT)
        )
        ar_comment = Arrow(
            start=comment.get_edge_center(UP),
            end=algo.inputs[2].get_edge_center(DOWN),
            color=text_color,
        )
        self.play(Write(comment), Create(ar_comment))
        self.wait()
        comment.generate_target()
        comment.target.shift(2 * DOWN)
        self.play(
            MoveToTarget(comment),
            Transform(
                ar_comment,
                Arrow(
                    start=comment.target.get_edge_center(LEFT),
                    end=comment.target.get_edge_center(LEFT) + 1.5 * LEFT,
                    color=text_color,
                ),
            ),
        )
        self.wait()

        self.play(
            FadeOut(verdict_copy),
            FadeOut(comment),
            FadeOut(ar_comment),
            FadeOut(string),
            FadeOut(string_copy),
        )
        self.wait()

        images = (
            Group(
                *[
                    ImageMobject("img/" + str + ".jpg").scale_to_fit_height(2)
                    for str in ["nisan", "wigderson"]
                ]
            )
            .arrange(RIGHT, buff=0.1)
            .to_edge(LEFT)
        )
        cross_tex = Tex(r"$\times$", color=RED).scale(18).move_to(funnel).shift(2 * UP)
        self.play(FadeIn(images))
        self.play(arrive_from(cross_tex, UP))
        self.wait()
        self.play(
            FadeOut(images),
            FadeOut(cross_tex),
            FadeOut(funnel),
            algo.animate.move_to(ORIGIN).set_label_color(text_color),
        )
        self.wait()

        prng.scale(0.7).move_to(algo.get_corner(DL) + 1.8 * LEFT + 0.45 * UP)
        prng_ar = Arrow(
            start=ORIGIN,
            end=1.0 * RIGHT,
            color=BASE00,
        ).shift(prng.get_edge_center(RIGHT) + 0.1 * LEFT)
        prng_ar2 = Arrow(
            start=ORIGIN,
            end=1.0 * RIGHT,
            color=BASE00,
        ).next_to(prng.box, LEFT, buff=0.1)

        self.play(
            Create(prng),
            GrowArrow(prng_ar2),
            Write(Tex(r"0110", color=text_color).scale(0.7).next_to(prng_ar2, LEFT)),
            Write(
                Tex(r"10100110001", color=text_color).scale(0.7).next_to(prng_ar, RIGHT)
            ),
            GrowArrow(prng_ar),
        )
        self.wait()

        more = (
            Tex(r"$p\ge 1\%$", color=text_color)
            .next_to(algo.inputs[2], DOWN, buff=1)
            .shift(1 * RIGHT)
        )
        self.play(Write(more))
        return

        ### TODO

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )
        self.wait()
        self.play(FadeIn(algo_group2))
        self.wait()

        self.play(
            algo.set_output(r"$\ne$", color=COLOR_DIFFERENT, scale=2),
            Transform(
                prob_tex2,
                Tex(r"$\ge 1\%$ probability")
                .scale(label_scale)
                .next_to(prng_algo.inputs[2], DOWN),
            ),
        )
        self.wait()
