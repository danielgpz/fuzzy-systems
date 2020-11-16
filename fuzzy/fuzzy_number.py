class FuzzyTrapezoidal:
    def __init__(self, a, b, c, d):
        assert a <= b <= c <= d, f'Vales {a}, {b}, {c} and {d} must me in order.'
        self.a, self.b, self.c, self.d = a, b, c, d
    
    def __call__(self, value):
        if value <= self.a: return 0
        if value <= self.b: return (value - self.a)/(self.b - self.a)
        if value <= self.c: return 1
        if value <= self.d: return (self.d - value)/(self.d - self.c)
        return 0

class FuzzyTriangular(FuzzyTrapezoidal):
    def __init__(self, a, b, c):
        super().__init__(a, b, b, c)

FuzzyMin = lambda *fs: lambda *args, **kwargs: min(f(*args, **kwargs) for f in fs)
FuzzyMax = lambda *fs: lambda *args, **kwargs: max(f(*args, **kwargs) for f in fs)
FuzzyMinWith = lambda v, f: lambda *args, **kwargs: min(f(*args, **kwargs), v)
FuzzyProductWith = lambda v, f: lambda *args, **kwargs: v * f(*args, **kwargs)