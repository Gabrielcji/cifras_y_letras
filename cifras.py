
INFINITO = 9999


def busca(objetivo:int, pila:list, resto_op:list, calculo:list, mejor_global:int):
    """
    :param objetivo: Número objetivo
    :param pila: Pila del cálculo
    :param resto_op: Lista con el resto de operandos no usados
    :param calculo: Lista que contiene el cálculo efectuado hasta ahora en notación polaca
    :param mejor_global: Mejor aproximación hasta ahora en el recorrido del árbol
    :return:
        (0, calculo): Resultado exacto y cálculo en notación polaca
        (N, calculo): Mejor aproximación (distancia = N) y cálculo en notación polaca
        (INFINITO, []): Cálculo que no lleva a una mejor aproximación
    """
    # Caso base 1: objetivo encontrado
    if (len(pila) == 1) and (objetivo == pila[0]):
        return 0, calculo
    # Caso base 2: no hay más operandos disponibles
    elif (len(pila) == 1) and (not resto_op):
        if abs(pila[0]-objetivo) < mejor_global:
            return abs(pila[0]-objetivo), calculo
        else:
            return INFINITO, []
    # Caso general
    else:
        calculo_old = calculo
        resto_op_old = resto_op
        mejor = mejor_global
        # Probar con todos los operandos restantes
        i = 0
        calculo_mejor = calculo
        for operando in resto_op_old:
            pila_new = pila + [operando]
            calculo_tmp = calculo_old + [operando]
            resto_op = resto_op_old
            del resto_op[i]
            i = i + 1
            resultado, calculo = busca(objetivo, pila_new, resto_op, calculo_tmp, mejor)
            if resultado == 0:
                return resultado, calculo
            elif resultado < mejor:
                mejor = resultado
                calculo_mejor = calculo

        # Caso base 3: No se pueden aplicar los operadores dado que son binarios
        if len(pila) < 2:
            if mejor < mejor_global:
                return mejor, calculo_mejor
            else:
                return INFINITO, []

        # Probar con todas las operaciones posibles:
        for operador in ['+', '-', '*', '/']:
            if operador == '/':
                if pila[-2] == 0:
                    # La división por 0 no está permitida
                    continue
                elif pila[-1] % pila[-2] != 0:
                    # Solo se admiten divisiones enteras
                    continue
            elif operador == '-' and pila[-1] < pila[-2]:
                # Los números negativos no están permitidos
                continue
            pila_new = pila[:-2]
            pila_new = pila_new + [eval(f"{pila[-1]} {operador} {pila[-2]}")]
            calculo_tmp = calculo_old + [operador]

            resultado, calculo = busca(objetivo, pila_new, resto_op_old, calculo_tmp, mejor)
            if resultado == 0:
                return resultado, calculo
            elif resultado < mejor:
                mejor = resultado
                calculo_mejor = calculo

        if mejor < mejor_global:
            return mejor, calculo_mejor
        else:
            return INFINITO, []


OBJETIVO = 180
OPERANDOS = [1, 5, 6, 7, 9, 10]
PILA = []
CALCULO = []

print(busca(OBJETIVO, PILA, OPERANDOS, CALCULO, INFINITO))
