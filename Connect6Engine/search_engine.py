from tools import *
from defines import *
import math
import time

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.ourColor = 0

        self.start_possible_x = 1
        self.start_possible_y = 1

        self.end_possible_x = 0
        self.end_possible_y = 0
        self.start_found = False

        self.turn = 0
        self.pre_move = StoneMove()

    def before_search(self, board, color, alphabeta_depth, pre_move):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

        self.pre_move = pre_move

    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):

        print("\n\n ME DICE EL COLOR ", str(ourColor))

        self.ourColor = ourColor

        #Check game result
        if (is_win_by_premove(self.m_board, preMove)):
            print("ALGUIEN HA GANADO")

            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0;
            else:
                #Self wins.
                return Defines.MININT + 1;

        self.turn += 2
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
        else:
            self.m_alphabeta_depth = 2
            
            move = self.find_possible_move(self.m_alphabeta_depth)
            print(move)
            
            self.start_found = False
            self.start_possible_x = 1
            self.start_possible_y = 1
            self.end_possible_x = 0
            self.end_possible_y = 0

            bestMove.positions[0].x = move[1][0][0]
            bestMove.positions[0].y = move[1][0][1]
            bestMove.positions[1].x = move[1][1][0]
            bestMove.positions[1].y = move[1][1][1]
            make_move(self.m_board,bestMove,ourColor)

        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self, depth, turn = 0):
        
        # Lista de posibilidades
        possibles = []

        # Tabla Hash de la lista de posibilidades (consultas en O(1))
        seen = set(possibles)

        # N vecinos cercanos
        n = 1

        # Doble para recorrer todas las posiciones del tablero 
        # IMPORTANTE: esto empieza por el start_possible para que de expandir el arbol, no busque desde el (1,1)
        for i in range(1, Defines.GRID_NUM - 1):
            for j in range(1, Defines.GRID_NUM - 1):
                
                # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                x = Defines.GRID_NUM - 1 - j
                y = i
                stone = self.m_board[x][y]

                # Si encuentra un hueco donde hay una ficha ...   
                if stone is not Defines.NOSTONE:

                    # Variable que indica que parte del cuadrado se incrementa: vertical o horizontal
                    # Variable que indice la dirección en la que se buscan los vecinos
                    indices = 1

                    # Recorre los n cuadrados de vecinos
                    for k in range(0,n):

                        # Inicio de la ventana (coordenadas de esquina inferior izquierda - iteración)
                        #   De fuera hacia dentro
                        start_xy = [x+n-k, y+n-k]

                        # Incremento del recorrido
                        inc = -1


                        # Para los cuatro lados del cuadrado
                        for h in range(0,4):
                            
                            # Para cada casilla de un lado (cada lado tiene 2 veces la distancia al vecino actual (n-k))
                            for f in range(0, 2*(n-k)):


                                # TODO: ver que condición poner primero de las dos siguientes
                                # Si la casilla explorada está dentro del tablero
                                if (start_xy[0] < 20 and start_xy[0] > 0) and (start_xy[1] < 20 and start_xy[1] > 0):
                                    
                                    if self.start_found is not True:
                                            self.start_found = True
                                            self.start_possible_x = i
                                            self.start_possible_y = j

                                    # Si la casilla a explorar es un hueco y no está en la lista de posibles (con la tabla Hash)
                                    if self.m_board[start_xy[0]][start_xy[1]] == Defines.NOSTONE and tuple([start_xy[0], start_xy[1]]) not in seen:

                                        # Se añade a la lista de posibles y la tabla Hash
                                        possibles.append([start_xy[0], start_xy[1]])
                                        seen.add(tuple([start_xy[0], start_xy[1]]))

                                        self.end_possible_x = max(self.end_possible_x, i)
                                        self.end_possible_y = max(self.end_possible_y, j)



                                # Intento de condición de cortar: alomejor faltan al explorar
                                # elif inc < 0:
                                #     start_xy[indices] += inc*(2*(n-k) - f+1)
                                #     break
                                
                                # Incremento de la posición según la dirección (indices)
                                start_xy[indices] += inc
                            
                            # Cambia el incremento para hacer: hacia arriba (izq) - derecha (arriba) - abajo (dcha) - izquierda (abajo) 
                            if h == 1:
                                inc = 1
                            
                            # Cambia el índice para moverse: Y - X - (-Y) - (-X) --> el '-' es para la dirección que marca "indices"
                            if indices == 1:
                                indices = 0
                            else:
                                indices = 1

        score = self.alpha_beta(possibles, depth)

        return score

    def alpha_beta(self, possibles, depth, turn = 0):
        score = [0, [[-1, -1], [-1, -1]]]
        alpha_beta = [-math.inf, math.inf]
        
        # ----- Caso base 1.0 ------
        # if depth == 0:
        #     # Recorriendo desde el inicio de los posibles
        #     for i in range(self.start_possible_x, Defines.GRID_NUM - 1):
        #         for j in range(self.start_possible_y, Defines.GRID_NUM - 1):
                    
        #             # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
        #             x = Defines.GRID_NUM - 1 - j
        #             y = i
        #             stone = self.m_board[x][y]
                    
        #             # Si no hay una pieza, busca el numero de fichas en la fila
        #             if stone is not Defines.NOSTONE:
        #                 score[0] += self.find_file(x,y)

        if depth == 0:
            if self.turn >=6:
                score[0] = self.threats()

            else:
                for i in range(self.start_possible_x, Defines.GRID_NUM - 1):
                    for j in range(self.start_possible_y, Defines.GRID_NUM - 1):
                        
                        # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                        x = Defines.GRID_NUM - 1 - j
                        y = i
                        stone = self.m_board[x][y]
                        
                        # Si no hay una pieza, busca el numero de fichas en la fila
                        if stone is not Defines.NOSTONE:
                            score[0] += self.find_file(x,y)

            return score

        # ----- Recursión ------
        else:
            
            color = self.ourColor
            
            # 0 = Turno de Max
            # 1 = Turno de Min

            # Si es el turno de Max, guarda para que el siguiente sea el turno de Min
            if turn == 0:
                color = self.ourColor   # Color de la llamada
                turn = 1                # Turno de Min (para la llamada recursiva)
                score[0] = -math.inf    # V = -inf

            # Si es el turno de Min, guarda para que el siguiente sea el turno de Max
            else:
                turn = 0                                # Turno de Max para la siguiente iteración
                score[0] = math.inf                     # V = inf
                if self.ourColor is Defines.BLACK:      # Cambia el valor de la ficha
                    color = Defines.WHITE
                else:
                    color = Defines.BLACK
            
            move = StoneMove()
            
            # Por cada valor posible, establece todas las combinaciones posibles
            for i in possibles:
                
                # Remueve el primero de la lista para que no repita valores en las siguientes
                possibles.remove(i)

                for j in possibles:

                    # Establece los movimientos
                    move.positions[0].x = i[0]
                    move.positions[0].y = i[1]
                    move.positions[1].x = j[0]  
                    move.positions[1].y = j[1]

                    # Hace el movimiento
                    make_move(self.m_board, move, color)

                    # Quita el valor de posibles de la lista, ya está ocupado
                    possibles_aux = possibles.copy()
                    possibles_aux.remove(j)

                    # ------ EXPAND -----
                    score_aux = self.alpha_beta(possibles_aux, depth-1, turn)
                    score_aux[1]= [i, j]
                    
                    # ------- Poda alfa - beta -------
                    # Max: estamos en el caso de que estamos moviendo. Antes del bucle se cambia
                    #   la variable
                    if turn == 1:

                        if score_aux[0] > score[0]:
                            score = score_aux
                        
                        if score[0] >= alpha_beta[1]:
                            return score

                        alpha_beta[0] = max(alpha_beta[0], score[0])
                    
                    # Min: estamos en el caso que mueve el oponente. Antes del bucle se cambia la variable
                    if turn == 0:

                        if score_aux[0] < score[0]:
                            score = score_aux
                        
                        if score[0] <= alpha_beta[0]:
                            return score

                        alpha_beta[1] = max(alpha_beta[1], score[0])
                    
                    # Se vuelve a insertar el elemento para las siguientes iteraciones
                    possibles_aux.append(j)

                    # Deshace el movimiento
                    make_move(self.m_board, move, Defines.NOSTONE)

        return score


    # ------ Heuristica 1.0: busca filas --------
    def find_file(self, ini_x = 1, ini_y = 1):
        count = 0        
        
        if ini_x < 1 and ini_y > 19:
            print("\n\n cuidado \n\n")
            return -1

        else:
            stone = self.m_board[ini_x][ini_y]

            if stone is not self.ourColor:

                if stone is Defines.NOSTONE:
                    return 1
                else:
                    return 0

            # Si encuentra un hueco donde hay una ficha ...   
            else:
                x_row = self.find_file(ini_x-1, ini_y) 
                y_row = self.find_file(ini_x, ini_y+1)
                diag_row = self.find_file(ini_x-1, ini_y+1)
                
                if x_row < 0:
                    x_row = 0
                    print("Negarivo x: ", x_row)
                if y_row < 0:
                    y_row = 0
                    print("Negarivo y ", y_row)
                if diag_row < 0:
                    diag_row = 0
                    print("Negarivo diag: ", diag_row)

                if ini_x + 1 < 20 and self.m_board[ini_x + 1][ini_y] is not self.ourColor:
                    x_row = 0
                if ini_y - 1 > 0 and self.m_board[ini_x][ini_y - 1] is not self.ourColor:
                    y_row = 0
                if ini_x + 1 < 20  and ini_y - 1 > 0 and self.m_board[ini_x + 1][ini_y - 1] is not self.ourColor:
                    diag_row = 0
                    
                
                count = 1 + x_row + y_row + diag_row

        return count










    # TODO: HACER EL CALCULO DE LOS NUEVOS VECINOS --> CAMBIO DE LA FUNCION find_possibles
    # TODO: ARREGLAR EL CALCULO DE LAS COLUMNAS EN EL THREATS
    # TODO: VER CUANDO ME ESTÁN ATACANDO Y CAMBIAR ESTRATEGIA --> DARLE MAS VALOR A LAS ESTRATEGIAS QUE BLOQUEEN AL RIVAL
    # TODO: ORDENAR LOS NODOS INTERMEDIOS DEL ARBOL --> APLICAR FUNCIÓN DE EVALUACIÓN A LOS NODOS INTERMEDIOS Y ORDENAR 
    #   SEGÚN EL SIGUIENTE TURNO
    def threats(self):
        num_threats = [[], [], []]
        

        h_threats = []
        seen_h_threats = set(h_threats)
        
        v_threats = []
        seen_v_threats = set(v_threats)

        d_threats = []
        seen_d_threats = set(d_threats)

        for i in range(self.start_possible_x, self.end_possible_x):
            # h_threats = []
            # seen_h_threats = set(h_threats)
            
            # v_threats = []
            # seen_v_threats = set(v_threats)

            # d_threats = []
            # seen_d_threats = set(d_threats)

            for j in range(self.start_possible_y, self.end_possible_y):
                
                count_h = 0
                count_e_h = 0

                count_v = 0
                count_e_v = 0

                count_d = 0
                count_e_d = 0

                x = Defines.GRID_NUM - 1 - j
                y = i
                
                
                for k in range(0,6):
                    

                    # Horizontal
                    if x - 6 > 0 and tuple([x,y]) not in seen_h_threats:
                        stone = self.m_board[x-k][y]

                        if stone is self.ourColor:
                            count_h +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_h +=1

                    # Vertical: está cambiado para que haga [y,x]
                    if x + 6 < 20 and tuple([y,x]) not in seen_v_threats:
                        stone = self.m_board[y][x+k]

                        if stone is self.ourColor:
                            count_v +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_v +=1

                    # Diag
                    if y + 6 < 20 and x - 6 > 0  and tuple([x,y]) not in seen_d_threats:
                        stone = self.m_board[x-k][y+k]

                        if stone is self.ourColor:
                            count_d +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_d +=1

                if count_h == 4 and count_e_h == 2:
                    h_threats.append([x,y])
                    seen_h_threats.add(tuple([x,y]))
                    print("horizontal")

                if count_v == 4 and count_e_v == 2:
                    v_threats.append([y,x])
                    seen_v_threats.add(tuple([y,x]))
                    print("vert")

                if count_d == 4 and count_e_d == 2:
                    d_threats.append([x,y])
                    seen_d_threats.add(tuple([x,y]))
                    print("diag")
            
            # num_threats[0].append(len(h_threats))
            # num_threats[1].insert(len(v_threats), 0)
            # num_threats[2].append(len(d_threats))

        

        return len(h_threats) + len(v_threats) + len(d_threats)
            

def flush_output():
    import sys
    sys.stdout.flush()
