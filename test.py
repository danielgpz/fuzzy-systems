from fuzzy import FuzzyTrapezoidal, FuzzyTriangular, FuzzySigmoidal, FuzzySigmoidal2, FuzzyBell,\
                    LinguisticVariable, FuzzySystem

def interval(a, b, points=1000):
    step = (b - a)/points
    return [a + i * step for i in range(points)] + [b]


servicio = LinguisticVariable('Servicio',
                                pobre=FuzzySigmoidal2(0, 4),
                                bueno=FuzzyBell(5, 5), 
                                excelente=FuzzySigmoidal(6, 10))
comida = LinguisticVariable('Comida',
                                rancia=FuzzyTrapezoidal(-1, 0, 1, 4),
                                deliciosa=FuzzyTrapezoidal(6, 9, 10, 11))
propina = LinguisticVariable('Propina',
                                poca=FuzzyTriangular(0, 4.5, 9),
                                promedio=FuzzyTriangular(8, 12.5, 17),
                                generosa=FuzzyTriangular(16, 20.5, 25))

servicio.pobre.plot(interval(0, 10))
servicio.bueno.plot(interval(0, 10))
servicio.excelente.plot(interval(0, 10))
comida.rancia.plot(interval(0, 10))
comida.deliciosa.plot(interval(0, 10))
propina.poca.plot(interval(0, 25))
propina.promedio.plot(interval(0, 25))
propina.generosa.plot(interval(0, 25))

SistemaPropina = FuzzySystem(input=(servicio, comida), output=(propina,))

SistemaPropina %= servicio.pobre | comida.rancia, propina.poca  
SistemaPropina %= servicio.bueno, propina.promedio 
SistemaPropina %= servicio.excelente | comida.deliciosa, propina.generosa

print(SistemaPropina)

mp, = SistemaPropina.mamdani(3, 8)
lp, = SistemaPropina.larsen(3, 8)

mp.plot(interval(0, 25, 25))
lp.plot(interval(0, 25, 25))
