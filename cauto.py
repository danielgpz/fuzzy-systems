from fuzzy import FuzzyTrapezoidal, FuzzyTriangular, FuzzySigmoidal, FuzzySigmoidal2, FuzzySigmoidal3,\
                    LinguisticVariable, FuzzySystem

# Variable que representa el nivel de las aguas del rio en %(0-100)
nivel = LinguisticVariable('nivel_del_rio',
                            bajo=FuzzySigmoidal2(0, 40),
                            normal=FuzzySigmoidal3(0, 40, 60, 100), 
                            crecido=FuzzySigmoidal(60, 100))

# Varaible que representa el pronostico del clima en cuanto a las precipitaciones
# valor de la probabilidad(0-1)
pdl = LinguisticVariable('probabilidad_de_lluvia',
                        baja=FuzzyTrapezoidal(-1, 0, .1, .5),
                        probable=FuzzyTriangular(.1, .5, .9),
                        alta=FuzzyTrapezoidal(.5, .9, 1, 2))

# Intensidad de las lluvias que se avecinan, % en que aumenta el nivel del rio(0-10)
idl = LinguisticVariable('intensidad_de_lluvia',
                        leves=FuzzyTrapezoidal(-1, 0, 1, 6),
                        intensas=FuzzyTrapezoidal(1, 6, 100, 101))

# Cantidad de agua que se destina a la presa, % del nivel que se disminuye(0-7)
desvio = LinguisticVariable('desvio_a_la_presa',
                            lento=FuzzyTriangular(-1, 0, 2),
                            normal=FuzzyTriangular(0, 2, 7),
                            rapido=FuzzyTriangular(2, 7, 8))

RioCauto = FuzzySystem(input=(nivel, pdl, idl), output=(desvio,))

RioCauto %= nivel.bajo, desvio.lento  
RioCauto %= nivel.normal & (pdl.baja | pdl.probable), desvio.lento
RioCauto %= nivel.normal & pdl.alta & idl.leves, desvio.lento 
RioCauto %= nivel.normal & pdl.alta & idl.intensas, desvio.normal 
RioCauto %= nivel.crecido, desvio.rapido

print(RioCauto)

from random import expovariate, random
from matplotlib import pyplot

def interval(a, b, points=10000):
    step = (b - a)/points
    return [a + i * step for i in range(points)] + [b]

probs = [0.5] * 42 + [0.7] * 21 + [0.8] * 42
rains = [3.0] * 42 + [1.0] * 21 + [5.0] * 42
levels_mcoa = [60]
levels_lboa = [60]

for p, r in zip(probs, rains):
    levelm = levels_mcoa[-1]
    levell = levels_lboa[-1]
    md, = RioCauto.mamdani(levelm, p, r)
    ls, = RioCauto.larsen(levell, p, r)
    mcoa = md.coa(interval(0, 7))
    lboa = ls.boa(interval(0, 7))
    rain = (random() <= p) * expovariate(1/r)
    levels_mcoa.append(levelm - mcoa + rain)
    levels_lboa.append(levell - lboa + rain)

pyplot.figure()
pyplot.xlabel("Dia")
pyplot.ylabel("Nivel del rio")
pyplot.plot(levels_mcoa, label="Mamdani+COA")
pyplot.plot(levels_lboa, label="Larsen+BOA")
pyplot.legend()
pyplot.show()
