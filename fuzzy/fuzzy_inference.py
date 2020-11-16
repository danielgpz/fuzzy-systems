from .fuzzy_logic import FuzzyPredicate
from .fuzzy_number import FuzzyMinWith, FuzzyProductWith, FuzzyMax
from matplotlib import pyplot

class FuzzySet(FuzzyPredicate):
    def __init__(self, domain: str, degree: str, member_function, fuzzy_system=None):
        self.domain = domain
        self.degree = degree
        self.member_function = member_function
        self.fuzzy_system = fuzzy_system

    def __call__(self, *args, **values):
        return self.member_function(values[self.domain])

    def __ilshift__(self, other: FuzzyPredicate):
        try:
            fuzzy_system = self.fuzzy_system
            fuzzy_system.add_rule(other, self)
        except AttributeError:
            raise ValueError(f'<{self}> does not belongs to any system')
        return self

    def __str__(self):
        return f'{self.domain} is {self.degree}'

    def plot(self, interval=(0, 1), points=1000):
        a, b = interval
        step = (b - a)/points
        pyplot.figure()
        xs = [a + x * step for x in range(points + 1)]
        ys = [self.member_function(x) for x in xs]
        pyplot.xlabel(self.domain)
        pyplot.ylabel(self.degree)
        pyplot.axis([a, b, 0, 1])
        pyplot.plot(xs, ys)
        pyplot.show()

class LinguisticVariable:
    def __init__(self, name: str, **categories):
        self.name = name
        self.fuzzy_system = None
        self.categories = categories

    def __getattr__(self, category: str):
        return FuzzySet(self.name, category, self.categories[category], fuzzy_system=self.fuzzy_system)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f'<{self.name}>: ' + ', '.join(c for c in self.categories)

class FuzzyRule:
    def __init__(self, antecedent: FuzzyPredicate, consequence: FuzzySet):
        self.antecedent = antecedent
        self.consequence = consequence

    def __str__(self):
        return f'{self.antecedent} => {self.consequence}'

class FuzzySystem:
    def __init__(self, *variables):
        self.rules = []
        self.input_variables = variables[:-1]
        self.output_variable = variables[-1]

        for var in self.input_variables:
            var.fuzzy_system = self
        self.output_variable.fuzzy_system = self

    def add_rule(self, antecedent: FuzzyPredicate, consequence: FuzzySet):
        if consequence.domain != self.output_variable.name:
            raise ValueError(f'Variable <{consequence.domain}> is not an output varaible')
        self.rules.append(FuzzyRule(antecedent, consequence))

    def mamdani(self, *values):
        vector = {var.name: value for var, value in zip(self.input_variables, values)}
        agregt = FuzzyMax(*(FuzzyMinWith(rule.antecedent(**vector), rule.consequence.member_function)
                for rule in self.rules))

        return FuzzySet(self.output_variable.name, "Mamdani", agregt, self)

    def larsen(self, *values):
        vector = {var.name: value for var, value in zip(self.input_variables, values)}
        agregt = FuzzyMax(*(FuzzyProductWith(rule.antecedent(**vector), rule.consequence.member_function)
                for rule in self.rules))
        
        return FuzzySet(self.output_variable.name, "Larsen", agregt, self)

    def __str__(self):
        return f'Input:\n' + '\n'.join(f'  {var}' for var in self.input_variables) +\
            f'\nOuput:\n  {self.output_variable}\nRules:\n' + '\n'.join(f'  {rule}' for rule in self.rules)