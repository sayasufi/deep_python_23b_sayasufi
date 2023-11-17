import cProfile
import io
import pstats
import weakref

from memory_profiler import profile


class DefaultAttr:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SlotsAttr:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


class WeakAttr:
    def __init__(self, x, y):
        self.x = weakref.ref(x)
        self.y = weakref.ref(y)


def profile_deco(func):
    def _wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        func(*args, **kwargs)
        profiler.disable()
        # print(memory_usage((func, args, kwargs)))
        stream = io.StringIO()
        sortby = "cumulative"
        stats = (
            pstats.Stats(profiler, stream=stream)
            .strip_dirs()
            .sort_stats(sortby)
        )
        stats.print_stats("weak_vs_slots.py")
        print(stream.getvalue())

    return _wrapper


@profile_deco
@profile
def run_measure_default(n):
    x, y = {4}, {2}
    c = DefaultAttr(x, y)
    class_list = [DefaultAttr(x, y) for _ in range(n)]
    _ = [cls.x for cls in class_list]
    _ = [setattr(cls, "x", {7}) for cls in class_list]
    _ = [delattr(cls, "x") for cls in class_list]


@profile_deco
@profile
def run_measure_slots(n):
    x, y = {4}, {2}
    c = SlotsAttr(x, y)
    class_list = [SlotsAttr(x, y) for _ in range(n)]
    _ = [cls.x for cls in class_list]
    _ = [setattr(cls, "x", {7}) for cls in class_list]
    _ = [delattr(cls, "x") for cls in class_list]


@profile_deco
@profile
def run_measure_weak(n):
    x, y = {4}, {2}
    c = WeakAttr(x, y)
    class_list = [WeakAttr(x, y) for _ in range(n)]
    _ = [cls.x for cls in class_list]
    _ = [setattr(cls, "x", {7}) for cls in class_list]
    _ = [delattr(cls, "x") for cls in class_list]


if __name__ == "__main__":
    N = 10**5
    run_measure_default(N)
    run_measure_slots(N)
    run_measure_weak(N)
