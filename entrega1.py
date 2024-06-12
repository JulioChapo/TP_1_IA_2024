from simpleai.search import (
    SearchProblem,
    greedy,
    astar,)

def jugar(frascos, dificil=False):
    class SortEmAllProblem(SearchProblem):

        def es_movimiento_valido(self, origen, destino):  # recibe frascos
            if not origen:
                return False

            if len(destino) == 4:  # El destino esta completo
                return False
            if not destino or origen[-1] == destino[-1]:  # Destino vacio or coinciden colores
                return True

            return False

        def actions(self, state):
            frascos = state
            available_actions = []
            cantidad = len(frascos)

            for nOrigen in range(cantidad):
                if len(frascos[nOrigen]) == 4 and len(set(frascos[nOrigen])) == 1: #origen completo
                    continue
                for nDestino in range(cantidad):
                    if nOrigen != nDestino and self.es_movimiento_valido(frascos[nOrigen], frascos[nDestino]):
                        available_actions.append((nOrigen+1, nDestino+1))

            return available_actions

        def result(self, state, action):
            lista_frascos = list(map(list, state))
            origen, destino = action
            origen -= 1
            destino -= 1

            frasco_destino = lista_frascos[destino]
            frasco_origen = lista_frascos[origen]

            while self.es_movimiento_valido(frasco_origen, frasco_destino):  #agrego lo que pueda del mismo color
                frasco_destino.append(frasco_origen.pop())

            tuple_frascos = tuple(map(tuple, lista_frascos))

            return tuple_frascos


        def cost(self, state, action, state2):
            return 1

        def is_goal(self, state):
            for frasco in state:
                if len(frasco) > 0:
                    # Si el frasco no tiene todos iguales Or no esta lleno
                    if len(set(frasco)) != 1 or len(frasco) != 4:
                        return False

            return True

        def heuristic(self, state):
            # Cantidad de frascos incorrectos
            mal = 0
            for frasco in state:
                if frasco and (len(frasco) != 4 or len(set(frasco)) != 1):
                    mal += 1

            return mal

    my_problem = SortEmAllProblem(frascos)
    if dificil:
        resultado = greedy(my_problem, graph_search=True)
    else:
        resultado = astar(my_problem, graph_search=True)

    if resultado:
        pasos = []
        for movimiento,_ in resultado.path():
            pasos.append(movimiento)
        return pasos[1:]
    else:
        return []
