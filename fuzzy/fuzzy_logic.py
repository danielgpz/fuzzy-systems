class FuzzyPredicate:
    def __call__(self, *args, **kwargs):
        pass

    def __and__(self, other):
        return FuzzyAnd(self, other)

    def __or__(self, other):
        return FuzzyOr(self, other)

    def __invert__(self):
        return FuzzyNegation(self)

class FuzzyAnd(FuzzyPredicate):
    def __init__(self, left: FuzzyPredicate, right: FuzzyPredicate):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        return min(self.left(*args, **kwargs), self.right(*args, **kwargs))

    def __str__(self):
        return f'({self.left}) and ({self.right})'

class FuzzyOr(FuzzyPredicate):
    def __init__(self, left: FuzzyPredicate, right: FuzzyPredicate):
        self.left = left
        self.right = right

    def __call__(self, *args, **kwargs):
        return max(self.left(*args, **kwargs), self.right(*args, **kwargs))

    def __str__(self):
        return f'({self.left}) or ({self.right})'

class FuzzyNegation(FuzzyPredicate):
    def __init__(self, object: FuzzyPredicate):
        self.object = object

    def __call__(self, *args, **kwargs):
        return 1 - self.object(*args, **kwargs)

    def __str__(self):
        return f'~ ({self.object})'
