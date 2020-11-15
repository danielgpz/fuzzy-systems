from .fuzzy_logic import FuzzyObject

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

class FuzzySet(FuzzyObject):
    def __init__(self, domain: str, degree: str, member_function, fuzzy_system=None):
        self.domain = domain
        self.degree = degree
        self.member_function = member_function
        self.fuzzy_system = fuzzy_system

    def __call__(self, *args, **values):
        return self.member_function(values[self.domain])

    def __ilshift__(self, other):
        try:
            fuzzy_system = self.fuzzy_system
            output_var = fuzzy_system.output_variable
            if self.domain == output_var.name:
                fuzzy_system.add_rule(other, self)
        except AttributeError:
            pass
        return self

    def __str__(self):
        return f'{self.domain} is {self.degree}'

class FuzzyRule:
    def __init__(self, antecedent, consecuence):
        self.antecedent = antecedent
        self.consecuence = consecuence

    def __str__(self):
        return f'{self.antecedent} => {self.consecuence}'

class FuzzySystem:
    def __init__(self, *variables):
        self.rules = []
        self.input_variables = variables[:-1]
        self.output_variable = variables[-1]

        for var in self.input_variables:
            var.fuzzy_system = self
        self.output_variable.fuzzy_system = self

    def add_rule(self, antecedent, consecuence):
        self.rules.append(FuzzyRule(antecedent, consecuence))

    def __str__(self):
        return f'Input:\n' + '\n'.join(f'  {var}' for var in self.input_variables) +\
            f'\nOuput:\n  {self.output_variable}\nRules:\n' + '\n'.join(f'  {rule}' for rule in self.rules)