from utils.util_general import *

set_default_colors()


class AnnotatedArrow(Arrow):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: if needed, position text based on the direction of the arrow
        self.text = Tex(text, color=BASE00).next_to(self.get_center(), UP)

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(GrowArrow(self), Write(self.text))


class PRNG(VGroup):
    def __init__(self):
        super().__init__()
        self.box = Rectangle(
            color=BLUE, fill_color=BLUE, fill_opacity=1, width=2.5, height=1.5
        )
        self.text = Tex("PRNG", color=BASE2)
        self.add(self.box)
        self.add(self.text)

        self.seed = None
        self.seed_arrow = None

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(Create(self.box), Write(self.text))

    def set_seed(self, seed: str):
        new_seed = Tex(seed, color=BASE00).move_to(self.box.get_center() + LEFT * 4)

        if self.seed is not None:
            old_seed = self.seed
            self.seed = new_seed
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
            )
            # Create the arrow only once most of the text is written
            return LaggedStart(
                Write(self.seed),
                Create(self.seed_arrow),
                lag_ratio=0.3,
            )
        else:
            return Write(self.seed)


class PRNGIntro(Scene):
    def construct(self):
        prng = PRNG().shift(LEFT)
        self.play(Create(prng))
        self.wait()
        self.play(prng.set_seed("011000111"))
        self.wait()

        seed_brace = BraceLabel(
            prng.seed,
            "$O(\log n)$ random bits",
            label_constructor=Tex,
            brace_direction=UP,
            buff=0.4,
        )
        seed_brace.label.shift(RIGHT)
        self.play(seed_brace.creation_anim(label_anim=Write))
        self.wait()

        output = Tex("1010110...1011000", color=BASE00).shift(RIGHT * 4)
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
            "$n$ pseudo-random bits",
            label_constructor=Tex,
            brace_direction=UP,
            buff=0.4,
        )
        self.play(output_brace.creation_anim(label_anim=Write))
        self.wait()

        for seed, output_str in [
            ("110000101", "0010000...1000111"),
            ("101011010", "0101010...0101010"),
        ]:
            self.play(prng.set_seed(seed), FadeOut(output))
            output = Tex(output_str, color=BASE00).shift(RIGHT * 4)
            self.play(Write(output))
            self.wait()
