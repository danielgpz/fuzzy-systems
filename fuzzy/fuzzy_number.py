import math

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

class FuzzyBell:
    def __init__(self, mean, varaince):
        self.mean = mean
        self.variance = varaince 

    def __call__(self, value):
        return math.e**(-(value - self.mean)**2/(2 * self.variance))

class FuzzySigmoidal:
    def __init__(self, a, b):
        self.a, self.b = a, b

    def __call__(self, value):
        if value <= self.a:
            return 0
        if value <= (self.a + self.b)/2:
            return 2*((value - self.a)/(self.b-self.a))**2
        if value <= self.b:
            return 1 - 2*((self.b - value)/(self.b - self.a))**2
        return 1

class FuzzySigmoidal2(FuzzySigmoidal):
    def __call__(self, value):
        return 1 - super().__call__(value)

class FuzzySigmoidal3:
    def __init__(self, a, b, c, d):
        self.b, self.c = b, c
        self.left = FuzzySigmoidal(a, b)
        self.right = FuzzySigmoidal2(c, d)

    def __call__(self, value):
        if value <= self.b:
            return self.left(value)
        if value >= self.c:
            return self.right(value)
        return 1

class FuzzySigmoidal4(FuzzySigmoidal3):
    def __call__(self, value):
        return 1 - super().__call__(value)

FuzzyMin = lambda *fs: lambda *args, **kwargs: min((f(*args, **kwargs) for f in fs), default=0)
FuzzyMax = lambda *fs: lambda *args, **kwargs: max((f(*args, **kwargs) for f in fs), default=0)
FuzzyMinWith = lambda v, f: lambda *args, **kwargs: min(f(*args, **kwargs), v)
FuzzyProductWith = lambda v, f: lambda *args, **kwargs: v * f(*args, **kwargs)