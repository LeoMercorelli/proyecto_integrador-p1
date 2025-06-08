import operator

# 1) ------------------ CREAMOS LA CLASE PARA LOS NODOS------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


# 2) ------------------ DEFINIMOS OPERADORES------------------
operadores = {
    '+': (1, operator.add),
    '-': (1, operator.sub),
    '*': (2, operator.mul),
    '/': (2, operator.truediv),
    '^': (3, operator.pow),
}


# 3) ------------------ VALIDACION DE LA EXPRESION DEL USUARIO------------------
def es_valida(infija):
    permitidos = [
        '0','1','2','3','4','5','6','7','8','9',
        '+','-','*','/','^','(',')',','
    ]
    
    for carac in infija:
        if carac not in permitidos:
            print(f"Caracter no valido: '{carac}'")
            print("Solo se aceptan numeros, parentesis y operadores.\n")
            return False
    return True


# 4) ------------------ ALGORITMO SHUNTING YARD - INFIJA A POSTFIJA ------------------
def convertir_a_postfija(infija):
    postfija = []
    pila = []
    numero = ''
    for carac in infija: #Recorremos la expresion, caracter por caracter
        if carac.isdigit() or carac == ',': #Preguntamos si el caracter es un numero o una coma
            numero += carac
        else:
            if numero:
                postfija.append(numero)
                numero = ''
            if carac in operadores: #Si elc aracter no es un numero, preguntamos si es un operador
                while (
                    pila and
                    pila[-1] in operadores and
                    operadores[carac][0] <= operadores[pila[-1]][0]
                ):
                    postfija.append(pila.pop())
                pila.append(carac)
            elif carac == '(': #Si el caracter no es un numero y no es u operador, preguntamos si es un '('
                pila.append(carac)
            elif carac == ')': # Si el caracter no es ninguno de los anteriores, confirmamos que sea un ')'
                while pila and pila[-1] != '(':
                    postfija.append(pila.pop())
                pila.pop()

    if numero:  # Si quedo algo acumulado dentro de la variable numero al finalizar el bucle for, lo añadimos a la expresion postfija
        postfija.append(numero)

    while pila:  # Como ultimo paso, enviamos toda la pila, a la expresion postfija. Empezando por el ultimo, hasta el primero.
        postfija.append(pila.pop())

    return postfija


# 5) ------------------ CONSTRUIMOS EL ARBOL USANDO LA EXPRESION POSTFIJA OBTENIDA ------------------
def construir_arbol(postfija):
    pila = []
    for carac in postfija:
        nodo = Nodo(carac) #Creamos el nodo
        if carac in operadores: 
            nodo.derecho = pila.pop() 
            nodo.izquierdo = pila.pop() 
        pila.append(nodo)
    return pila[0]  # devolvemos el unico nodo que queda: la raiz


# 6) ------------------ RESOLVEMOS EL ARBOL RECURSIVAMENTE ------------------
def resolver_nodo(nodo):
    if nodo.valor not in operadores:
        return float(nodo.valor.replace(',', '.'))  # Cambiamos coma por punto
    valor_izq = resolver_nodo(nodo.izquierdo)
    valor_der = resolver_nodo(nodo.derecho)
    return operadores[nodo.valor][1](valor_izq, valor_der) #Retornamos el resultado de la operacion que indica el padre, entre sus dos hijos


##########------------------ PROGRAMA PRINCIPAL ------------------##########
while True:
    while True:
        infija = input("📥 Ingresá la expresión matemática (infija): ")
        infija = infija.replace(' ', '')
        if es_valida(infija): 
            break  

    postfija = convertir_a_postfija(infija)
    print(f"\nExpresión en postfijo: {' '.join(postfija)}") 

    continuar = input("\n¿Deseás continuar o salir del programa? (c/s): ").lower()
    if continuar == 'c':
        raiz = construir_arbol(postfija)
        resultado = resolver_nodo(raiz)
        print(f"\n Resultado final: {resultado}")
        otra = input("\n¿Deseás evaluar otra expresión o salir del programa? (e/s): ").lower()
        if otra != 'e':
            print("Saliendo del programa.")
            break
    else:
        print("Saliendo del programa.")
        break
