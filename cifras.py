
INFINITO = 9999


def busca(objetivo:int, pila:list, resto_op:list, calculo:list, mejor_global:int, max_operaciones:int):
    """
    :param objetivo: Número objetivo
    :param pila: Pila del cálculo
    :param resto_op: Lista con el resto de operandos no usados
    :param calculo: Lista que contiene el cálculo efectuado hasta ahora en notación polaca
    :param mejor_global: Mejor aproximación hasta ahora en el recorrido del árbol
    :param max_operaciones: Número máximo de operaciones. Limita la profundidad del árbol
    :return:
        (0, calculo): Resultado exacto y cálculo en notación polaca
        (N, calculo): Mejor aproximación (distancia = N) y cálculo en notación polaca
        (INFINITO, []): Cálculo que no lleva a una mejor aproximación
    """
    # Caso base 1: objetivo encontrado
    if (len(pila) == 1) and (objetivo == pila[0]):
        return 0, calculo
    # Caso base 2: no hay más operandos disponibles o se ha alcanzado el máximo de operaciones
    elif (len(pila) == 1) and (not resto_op or max_operaciones == 0):
        return abs(pila[0] - objetivo), calculo
    # Caso base 3: hay demasiados operandos para las operaciones posibles
    elif len(pila) > max_operaciones + 1:
        return INFINITO, []
    # Caso general
    else:
        mejor = mejor_global
        # Probar con todos los operandos restantes
        i = 0
        calculo_mejor = calculo
        for operando in resto_op:
            pila_new = pila + [operando]
            calculo_new = calculo + [operando]
            resto_op_new = resto_op.copy()
            del resto_op_new[i]
            i = i + 1
            res_diferencia, res_calculo = busca(objetivo, pila_new, resto_op_new, calculo_new, mejor, max_operaciones)
            if res_diferencia == 0:
                return res_diferencia, res_calculo
            elif res_diferencia < mejor:
                mejor = res_diferencia
                calculo_mejor = res_calculo

        # Caso base 4: No se pueden aplicar los operadores dado que son binarios
        if len(pila) < 2:
            return mejor, calculo_mejor

        # Probar con todas las operaciones posibles:
        for operador in ['+', '-', '*', '/']:
            if operador == '/':
                if pila[-2] == 0:
                    # La división por 0 no está permitida
                    continue
                elif pila[-2] == 1:
                    # La división por 1 no añade valor
                    continue
                elif pila[-1] % pila[-2] != 0:
                    # Solo se admiten divisiones enteras
                    continue
            elif operador == '*':
                if pila[-1] == 1 or pila[-2] == 1:
                    # El producto por 1 no añade valor
                    continue
            elif operador == '-':
                if pila[-2] == 0:
                    # Restar 0 no añade valor
                    continue
                elif pila[-1] < pila[-2]:
                    # Los números negativos no están permitidos
                    continue
            pila_new = pila[:-2]
            pila_new = pila_new + [eval(f"{pila[-1]} {operador} {pila[-2]}")]
            calculo_new = calculo + [operador]

            res_diferencia, res_calculo = busca(objetivo, pila_new, resto_op, calculo_new, mejor, max_operaciones-1)
            if res_diferencia == 0:
                return res_diferencia, res_calculo
            elif res_diferencia < mejor:
                mejor = res_diferencia
                calculo_mejor = res_calculo

        return mejor, calculo_mejor

def imprime_solucion(diferencia:int, calculo:list):
    """
    Pasa de notación polaca a cálculo operación por operación
    :param diferencia: diferencia con el objetivo
    :param calculo: cálculo en notación polaca
    :return: Nada
    """
    if diferencia == 0:
        print ("He conseguido el número exacto.\n")
    else:
        print (f"He conseguido acercarme a {diferencia}.\n")
    print("Detalle del cálculo:")

    num_operaciones = 0
    if len(calculo) == 1:
        print("No hace falta hacer ninguna operación")

    pila = []
    for x in calculo:
        if type(x) == int:
            pila = [x] + pila
        else:
            num_operaciones += 1
            print(f"{pila[0]} {'x' if x == '*' else x} {pila[1]} = "
                  + str(int(eval(f"{pila[0]} {x} {pila[1]}"))))

            resultado = int(eval(f"{pila[0]} {x} {pila[1]}"))
            pila = [resultado] + pila[2:]

    print(f"He necesitado {num_operaciones} operaciones.")

OBJETIVO = 5
OPERANDOS = [1, 2, 3, 4]
MAX_OPERACIONES = len(OPERANDOS) + 1

print(f"OBJETIVO: {OBJETIVO}")
print(f"OPERANDOS: {OPERANDOS}\n")
res_diferencia, res_calculo = busca(OBJETIVO, [], OPERANDOS, [], INFINITO, MAX_OPERACIONES)
print(f"res_diferencia: {res_diferencia}")
print(f"res_calculo: {res_calculo}")
imprime_solucion(res_diferencia, res_calculo)

