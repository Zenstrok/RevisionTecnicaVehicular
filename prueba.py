
def crear_nodo(valor, izquierda=None, derecha=None):
    return [valor, izquierda, derecha]

def insertar(arbol, valor):
    if arbol == None:
        return crear_nodo(valor)
    else:
        if valor[1] < arbol[0][1]:
            arbol[1] = insertar(arbol[1], valor)
        else:
            arbol[2] = insertar(arbol[2], valor)
        return arbol

"""def imprimir_inorden(arbol):
    pila = []
    nodo_actual = arbol

    while True:
        if nodo_actual is not None:
            pila.append(nodo_actual)
            nodo_actual = nodo_actual[1]
        elif pila:
            nodo_actual = pila.pop()
            print(nodo_actual[0], end=" ")
            nodo_actual = nodo_actual[2]
        else:
            break"""

# Ejemplo de uso
arbol = None

arbol = insertar(arbol, [3200, 202381232])
arbol = insertar(arbol, [5600, 345345345])

"""arbol = insertar(arbol, [5700, 2023, 7, 26, 4920])
arbol = insertar(arbol, [5800, 2023, 9, 24, 2956])
arbol = insertar(arbol, [5900, 2023, 6, 22, 3560])"""

print(arbol)