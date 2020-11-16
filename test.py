from fuzzy import FuzzyTriangular, LinguisticVariable, FuzzySystem

servicio = LinguisticVariable('Servicio', 
                                pobre=FuzzyTriangular(-1, 0, 4),
                                bueno=FuzzyTriangular(0, 5, 10), 
                                excelente=FuzzyTriangular(6, 10, 11))
comida = LinguisticVariable('Comida',
                                rancia=FuzzyTriangular(-1, 0, 4),
                                deliciosa=FuzzyTriangular(6, 10, 11))
propina = LinguisticVariable('Propina', 
                                poca=FuzzyTriangular(-1, 0, 4),
                                promedio=FuzzyTriangular(0, 5, 10),
                                generosa=FuzzyTriangular(6, 10, 11))

SistemaPropina = FuzzySystem(input=(servicio, comida), output=(propina,))

SistemaPropina %= servicio.pobre | comida.rancia, propina.poca  
SistemaPropina %= servicio.bueno & ~ comida.rancia, propina.promedio 
SistemaPropina %= servicio.excelente | comida.deliciosa, propina.generosa

print(SistemaPropina)

SistemaPropina.mamdani(3, 8)[0].plot((-1, 11))
SistemaPropina.larsen(3, 8)[0].plot((-1, 11))
