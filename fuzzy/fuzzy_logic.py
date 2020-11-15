class FuzzyObject:
    def __call__(self, *args, **kwargs):
        pass

    def __and__(self, other):
        return FuzzyAnd(self, other)

    def __or__(self, other):
        return FuzzyOr(self, other)

    def __invert__(self):
        return FuzzyComplement(self)

class FuzzyAnd(FuzzyObject):
    def __init__(self, left: FuzzyObject, right: FuzzyObject):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        return min(self.left(*args, **kwargs), self.right(*args, **kwargs))

    def __str__(self):
        return f'({self.left}) and ({self.right})'

class FuzzyOr(FuzzyObject):
    def __init__(self, left: FuzzyObject, right: FuzzyObject):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        return max(self.left(*args, **kwargs), self.right(*args, **kwargs))

    def __str__(self):
        return f'({self.left}) or ({self.right})'

class FuzzyComplement(FuzzyObject):
    def __init__(self, object: FuzzyObject):
        self.object = object

    def __call__(self, *args, **kwargs):
        return 1 - self.object(*args, **kwargs)

    def __str__(self):
        return f'~ ({self.object})'
