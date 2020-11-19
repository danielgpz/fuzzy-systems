from fuzzy import FuzzyTrapezoidal, FuzzyTriangular, FuzzySigmoidal, FuzzySigmoidal2, FuzzyBell,\
                    LinguisticVariable, FuzzySystem

from random import expovariate, random
from matplotlib import pyplot

def interval(a, b, points=10000):
    step = (b - a)/points
    return [a + i * step for i in range(points)] + [b]

# Variable que representa el nivel de las aguas del rio en %(0-100)
nivel = LinguisticVariable('nivel_del_rio',
                            bajo=FuzzySigmoidal2(0, 40),
                            normal=FuzzyBell(50, 50), 
                            crecido=FuzzySigmoidal(60, 100))

# Varaible que representa el pronostico del clima en cuanto a las precipitaciones
# valor de la probabilidad(0-1)
pdl = LinguisticVariable('probabilidad_de_lluvia',
                        baja=FuzzyTrapezoidal(-1, 0, .1, .4),
                        probable=FuzzyTriangular(.3, .5, .7),
                        alta=FuzzyTrapezoidal(.6, .9, 1, 2))

# Intensidad de las lluvias que se avecinan, % en que aumenta el nivel del rio(0-10)
idl = LinguisticVariable('intensidad_de_lluvia',
                        leves=FuzzyTrapezoidal(-1, 0, 1, 3),
                        intensas=FuzzyTrapezoidal(3, 6, 100, 101))

# Cantidad de agua que se destina a la presa, % del nivel que se disminuye(0-7)
desvio = LinguisticVariable('desvio_a_la_presa',
                            lento=FuzzyTriangular(-1, 0, 1.5),
                            normal=FuzzyTriangular(1, 2, 3),
                            rapido=FuzzyTriangular(2, 7, 8))

RioCauto = FuzzySystem(input=(nivel, pdl, idl), output=(desvio,))

RioCauto %= nivel.bajo, desvio.lento  
RioCauto %= nivel.normal & (pdl.baja | pdl.probable), desvio.lento
RioCauto %= nivel.normal & pdl.alta & idl.leves, desvio.lento 
RioCauto %= nivel.normal & pdl.alta & idl.intensas, desvio.normal 
RioCauto %= nivel.crecido, desvio.rapido

# nivel.bajo.plot(interval(0, 100))
# nivel.normal.plot(interval(0, 100))
# nivel.crecido.plot(interval(0, 100))

# pdl.baja.plot(interval(0, 1))
# pdl.probable.plot(interval(0, 1))
# pdl.alta.plot(interval(0, 1))

# idl.leves.plot(interval(0, 10))
# idl.intensas.plot(interval(0, 10))

# desvio.lento.plot(interval(0, 10))
# desvio.normal.plot(interval(0, 10))
# desvio.rapido.plot(interval(0, 10))

print(RioCauto)

probs = [0.5] * 42 + [0.7] * 21 + [0.8] * 42
rains = [3.0] * 42 + [1.0] * 21 + [5.0] * 42
levels = [60]

for p, r in zip(probs, rains):
    level = levels[-1]
    md, = RioCauto.mamdani(level, p, r)
    d = md.coa(interval(0, 7))
    levels.append(level - d + (random() <= p) * expovariate(1/r))

pyplot.plot(levels)
pyplot.show()
