from fuzzy import TriangularFuzzyNumber, LinguisticVariable, FuzzySystem

servicio = LinguisticVariable('Servicio', 
                                pobre=TriangularFuzzyNumber(-1, 0, 4),
                                bueno=TriangularFuzzyNumber(0, 5, 10), 
                                excelente=TriangularFuzzyNumber(6, 10, 11))
comida = LinguisticVariable('Comida',
                                rancia=TriangularFuzzyNumber(-1, 0, 4),
                                deliciosa=TriangularFuzzyNumber(6, 10, 11))
propina = LinguisticVariable('Propina', 
                                poca=TriangularFuzzyNumber(-1, 0, 4),
                                promedio=TriangularFuzzyNumber(0, 5, 10),
                                generosa=TriangularFuzzyNumber(6, 10, 11))

SistemaPropina = FuzzySystem(servicio, comida, propina)

propina.poca     <<= servicio.pobre | comida.rancia  
propina.promedio <<= servicio.bueno & ~ comida.rancia 
propina.generosa <<= servicio.excelente | comida.deliciosa

print(SistemaPropina)