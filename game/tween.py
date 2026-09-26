from core.object import Object
import math


def _get_property(target: object, property_path: str):
    parts = property_path.split(".")
    current = target
    for name in parts:
        current = getattr(current, name)
    return current


def _set_property(target: object, property_path: str, value):
    parts = property_path.split(".")
    current = target
    for i in range(len(parts) - 1):
        current = getattr(current, parts[i])
    
    setattr(current, parts[-1], value)


def _interpolate(a, b, time):
    return a + (b - a) * time


class EaseType:

    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def quadratic(t):
        t *= 2
        if t < 1:
            return t * t / 2
        else:
            t -= 1
            return -(t * (t - 2) - 1) / 2

    def ease_in_quad(t):
        return t * t

    def ease_out_quad(t):
        return -t * (t - 2)

    def ease_in_cubic(t):
        return t * t * t

    def ease_out_cubic(t):
        t -= 1
        return t * t * t + 1

    def ease_in_out_cubic(t):
        t *= 2
        if t < 1:
            return t * t * t / 2
        else:
            t -= 2
            return (t * t * t + 2) / 2

    def ease_in_quart(t):
        return t * t * t * t

    def ease_out_quart(t):
        t -= 1
        return -(t * t * t * t - 1)

    def ease_in_out_quart(t):
        t *= 2
        if t < 1:
            return t * t * t * t / 2
        else:
            t -= 2
            return -(t * t * t * t - 2) / 2

    def ease_in_quint(t):
        return t * t * t * t * t

    def ease_out_quint(t):
        t -= 1
        return t * t * t * t * t + 1

    def ease_in_out_quint(t):
        t *= 2
        if t < 1:
            return t * t * t * t * t / 2
        else:
            t -= 2
            return (t * t * t * t * t + 2) / 2

    def ease_in_expo(t):
        return math.pow(2, 10 * (t - 1))

    def ease_out_expo(t):
        return -math.pow(2, -10 * t) + 1

    def ease_in_out_expo(t):
        t *= 2
        if t < 1:
            return math.pow(2, 10 * (t - 1)) / 2
        else:
            t -= 1
            return -math.pow(2, -10 * t) - 1

    def ease_in_circ(t):
        return 1 - math.sqrt(1 - t * t)

    def ease_out_circ(t):
        t -= 1
        return math.sqrt(1 - t * t)

    def ease_in_out_circ(t):
        t *= 2
        if t < 1:
            return -(math.sqrt(1 - t * t) - 1) / 2
        else:
            t -= 2
            return (math.sqrt(1 - t * t) + 1) / 2


class _TweenStep:

    def __init__(self, target, property, start_value, end_value, duration, easing_fn):
        self.target = target
        self.property = property
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing_fn = easing_fn
    
    def apply_value(self, time):
        t = self.easing_fn(time)
        value = _interpolate(self.start_value, self.end_value, t)
        _set_property(self.target, self.property, value)


class Tween(Object):

    def __init__(self, renderer):
        super().__init__()
        self._renderer = renderer

        self._steps: list[_TweenStep] = []
        self._current_step = 0
        self._elapsed_in_step = 0
        self._easing_fn = EaseType.linear
        
        self.is_started = False
        self.is_complete = False

    def set_easing(self, easing_fn):
        self._easing_fn = easing_fn
        return self

    def tween_property(self, target, property, end_value, duration):
        if self._steps:
            start_value = self._steps[-1].end_value
        else:
            start_value = _get_property(target, property)

        step = _TweenStep(target, property, start_value, end_value, duration, self._easing_fn)
        self._steps.append(step)
        
        return self
    
    def complete(self):
        self.is_complete = True
        self._renderer._tweens.remove(self)
    
    def update(self, delta):
        if not self._steps:
            self.complete()
            return

        step = self._steps[self._current_step]
        self._elapsed_in_step += delta

        t = self._elapsed_in_step / step.duration
        if t > 1:
            t = 1

        step.apply_value(t)
    
        if self._elapsed_in_step >= step.duration:
            self._current_step += 1
            self._elapsed_in_step = 0

            if self._current_step >= len(self._steps):
                self.complete()

