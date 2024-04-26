from manim import *
from utils.util_general import BASE00, BASE2, BLUE


class AnnotatedArrow(Arrow):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: if needed, position text based on the direction of the arrow
        self.text = Tex(text, color=BASE00).next_to(self.get_center(), UP)

    @override_animation(Create)  # Create(PRNG()) will run this method
    def _create(self):
        # For some reason, the default Create(PRNG()) creates the rectangle
        # almost instantly. This looks nicer.
        return AnimationGroup(GrowArrow(self), Create(self.text))


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
        return AnimationGroup(Create(self.box), Create(self.text))

    def set_seed(self, seed: str):
        new_seed = Tex(seed, color=BASE00).move_to(self.box.get_center() + LEFT * 4)

        if self.seed is not None:
            return self.seed.animate.become(new_seed)
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


class TestScene(Scene):
    def construct(self):
        prng = PRNG()
        self.play(Create(prng))
        self.wait()
        self.play(prng.set_seed("011000111"))
        self.wait()
        self.play(prng.set_seed("111100010"))
        self.wait()
