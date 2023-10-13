from tools import *
from defines import *
import math
import numpy as np
import time
import itertools


class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.ourColor = 0

        self.start_possible_x = 1
        self.start_possible_y = Defines.GRID_NUM - 1

        self.end_possible_x = Defines.GRID_NUM - 1
        self.end_possible_y = 1

        self.start_found = False

        self.turn = 0
        self.pre_move = [StoneMove(), StoneMove()]

    def before_search(self, board, color, alphabeta_depth, pre_move):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0
        
        if self.turn == 0:
            self.pre_move[1] = pre_move
        self.pre_move[0] = pre_move

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
            
            # self.start_possible_x = 1
            # self.start_possible_y = 1
            # self.end_possible_x = 0
            # self.end_possible_y = 0

            bestMove.positions[0].x = move[1][0][0]
            bestMove.positions[0].y = move[1][0][1]
            bestMove.positions[1].x = move[1][1][0]
            bestMove.positions[1].y = move[1][1][1]

            self.pre_move[1] = bestMove
            

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
        n = 2
        
        # Doble bucle para recorrer todos los movimientos previos del tablero 
        for o in reversed(self.pre_move):
            for i in o.positions:

                # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                x = i.x
                y = i.y
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
                                      
                                    # Si la casilla a explorar es un hueco y no está en la lista de posibles (con la tabla Hash)
                                    if self.m_board[start_xy[0]][start_xy[1]] == Defines.NOSTONE and tuple([start_xy[0], start_xy[1]]) not in seen:

                                        # Se añade a la lista de posibles y la tabla Hash

                                        possibles.insert(n-k-1, [start_xy[0], start_xy[1]])
                                        seen.add(tuple([start_xy[0], start_xy[1]]))

                                        if start_xy[0] > self.start_possible_x:
                                            self.start_possible_x = start_xy[0]
                                        if start_xy[0] < self.end_possible_x:
                                            self.end_possible_x = start_xy[0]
                                        
                                        if start_xy[1] < self.start_possible_y:
                                            self.start_possible_y = start_xy[1]
                                        if start_xy[1] > self.end_possible_y:
                                            self.end_possible_y = start_xy[1]
                                
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

        # print_board(self.m_board)
        # print(possibles)
        flag = False

        list_e_h = []

        list_e_v = []

        list_e_d = []

        list_e_d2 = []

        winning_move = []
        
        for i in range(1, Defines.GRID_NUM - 1):
            if flag:
                break

            for j in range(1, Defines.GRID_NUM - 1):
                
                count_h = 0
                list_e_h = []

                count_v = 0
                list_e_v = []

                count_d = 0
                list_e_d = []

                count_d2 = 0
                list_e_d2 = []


                x = j
                y = i
                
                for k in range(0,6):
                    # Jugador
                    # Vertical
                    if x + 6 < 20 and tuple([x + k,y]):# not in seen_v_threats:
                        stone = self.m_board[x + k][y]

                        if stone is self.ourColor:
                            count_v +=  1
                        elif stone is Defines.NOSTONE:
                            list_e_v.append([x + k, y])

                            right_e_v = x+k

                    # Horizontal: está cambiado para que haga [y,x]
                    if x + 6 < 20 and tuple([y,x + k]):# not in seen_h_threats:
                        stone = self.m_board[y][x+k]

                        if stone is self.ourColor:
                            count_h +=  1
                        elif stone is Defines.NOSTONE:
                            list_e_h.append([y, x + k])

                            right_e_h = x + k

                #     # # Diag
                    if y + 6 < 20 and x + 6 < 20  and tuple([x + k,y + k]):# not in seen_d_threats:
                        stone = self.m_board[x + k][y + k]

                        if stone is self.ourColor:
                            count_d +=  1
                        elif stone is Defines.NOSTONE:
                            list_e_d.append([x + k, y + k])

                            right_e_d = [x + k,y + k]

                #     # # Diag 2
                    if y - 6 >= 0 and x + 6 < 20  and tuple([x + k,y - k]):# not in seen_d2_threats:
                        stone = self.m_board[x + k][y - k]

                        if stone is self.ourColor:
                            count_d2 +=  1
                            
                        elif stone is Defines.NOSTONE:
                            list_e_d2.append([x + k, y-k])

                            right_e_d2 = [x + k,y - k]
                    
                if count_v == 4 and len(list_e_v) == 2: 
                    #h_threats.append([x,right_e_h])
                    # seen_v_threats.add(tuple([right_e_v, y]))

                    flag = True
                    winning_move = list_e_v
                    break

                if count_h == 4 and len(list_e_h) == 2:
                    #v_threats.append([right_e_v, x])
                    # seen_h_threats.add(tuple([y, right_e_h]))

                    flag = True
                    winning_move = list_e_h
                    break

                if count_d == 4 and len(list_e_d) == 2:
                    #d_threats.append([right_e_d[0], right_e_d[1]])
                    # seen_d_threats.add(tuple([right_e_d[0], right_e_d[1]]))
                    
                    flag = True
                    winning_move = list_e_d
                    break

                if count_d2 == 4 and len(list_e_d2) == 2:
                    #d2_threats.append([right_e_d2[0], right_e_d2[1]])
                    # seen_d2_threats.add(tuple([right_e_d2[0], right_e_d2[1]]))

                    flag = True
                    winning_move = list_e_d2
                    break
        
        score = [0, [[10, 10], [10, 10]]]

        if flag:
            print("HE GANADO")
            return [math.inf, winning_move]
        else:
            score = self.max(possibles, depth, -math.inf, math.inf)

        # _ = self.threats(self.ourColor)

        return score
    

    def max(self, possibles, depth, alpha, beta):
        score = [0, [[-1, -1], [-1, -1]]]

        if depth == 0:
            if self.turn >= 0:
                score[0] = self.threats(self.ourColor)

            else:
                for i in range(1, Defines.GRID_NUM - 1):
                    for j in range(1, Defines.GRID_NUM - 1):
                        
                        # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                        x = Defines.GRID_NUM - 1 - j
                        y = i
                        stone = self.m_board[x][y]
                        
                        # Si no hay una pieza, busca el numero de fichas en la fila
                        if stone is not Defines.NOSTONE:
                            score[0] += self.find_file(x,y)
            
            return score

        else:
            score[0] = -math.inf
            move = StoneMove()
            color = self.ourColor

            # if turn == -1:
            #     if self.ourColor == Defines.WHITE:
            #         color = Defines.BLACK
            #     else:
            #         color = Defines.WHITE

            idx_i = 0
            
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
                    score_aux = self.min(possibles_aux, depth-1, alpha, beta)
                    # score_aux[0] = -score_aux[0]
                    score_aux[1]= [i, j]

                    if score_aux[0] > score[0]:
                        score = score_aux

                    if score[0] >= beta:
                        # print("poda max", score[0])
                        return score
                    
                    if score[0] > alpha:
                        alpha = score[0]

                    make_move(self.m_board, move, Defines.NOSTONE)
                
                # possibles.insert(idx_i, i)
                # idx_i += 1



        return score
                    
    def min(self, possibles, depth, alpha, beta):
        score = [0, [[-1, -1], [-1, -1]]]

        if depth == 0:
            if self.turn >=0:
                if self.ourColor is Defines.BLACK:
                    score[0] = self.threats(Defines.BLACK)
                else:
                    score[0] = self.threats(Defines.WHITE)

            else:
                for i in range(1, Defines.GRID_NUM - 1):
                    for j in range(1, Defines.GRID_NUM - 1):
                        
                        # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                        x = Defines.GRID_NUM - 1 - j
                        y = i
                        stone = self.m_board[x][y]
                        
                        # Si no hay una pieza, busca el numero de fichas en la fila
                        if stone is not Defines.NOSTONE:
                            score[0] += self.find_file(x,y)
                
                return score

        else:
            score[0] = math.inf
            move = StoneMove()
            idx = 0

            color = self.ourColor

            if self.ourColor == Defines.BLACK:
                color = Defines.WHITE
            else:
                color = Defines.BLACK
            
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
                    score_aux = self.max(possibles_aux, depth-1, alpha, beta)
                    score_aux[1]= [i, j]

                    if score_aux[0] < score[0]:
                        score = score_aux

                    if score[0] <= alpha:
                        # print("poda Min", score[0])
                        return score
                    
                    if score[0] < beta:
                        beta = score[0]

                    make_move(self.m_board, move, Defines.NOSTONE)

                # possibles.insert(idx, i)
                # idx += 1

        return score

    # def alpha_beta(self, possibles, depth, turn = 0):
    #     score = [0, [[-1, -1], [-1, -1]]]
    #     alpha_beta = [-math.inf, math.inf]
        

    #     if depth == 0:
    #         if self.turn >=6:
    #             score[0] = self.threats()

    #         else:
    #             for i in range(self.start_possible_x, Defines.GRID_NUM - 1):
    #                 for j in range(self.start_possible_y, Defines.GRID_NUM - 1):
                        
    #                     # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
    #                     x = Defines.GRID_NUM - 1 - j
    #                     y = i
    #                     stone = self.m_board[x][y]
                        
    #                     # Si no hay una pieza, busca el numero de fichas en la fila
    #                     if stone is not Defines.NOSTONE:
    #                         score[0] += self.find_file(x,y)

    #         return score

    #     # ----- Recursión ------
    #     else:
            
    #         color = self.ourColor
            
    #         # 0 = Turno de Max
    #         # 1 = Turno de Min

    #         # Si es el turno de Max, guarda para que el siguiente sea el turno de Min
    #         if turn == 0:
    #             color = self.ourColor   # Color de la llamada
    #             turn = 1                # Turno de Min (para la llamada recursiva)
    #             score[0] = -math.inf    # V = -inf

    #         # Si es el turno de Min, guarda para que el siguiente sea el turno de Max
    #         else:
    #             turn = 0                                # Turno de Max para la siguiente iteración
    #             score[0] = math.inf                     # V = inf
    #             if self.ourColor is Defines.BLACK:      # Cambia el valor de la ficha
    #                 color = Defines.WHITE
    #             else:
    #                 color = Defines.BLACK
            
    #         move = StoneMove()
            
    #         # Por cada valor posible, establece todas las combinaciones posibles
    #         for i in possibles:
                
    #             # Remueve el primero de la lista para que no repita valores en las siguientes
    #             possibles.remove(i)

    #             for j in possibles:

    #                 # Establece los movimientos
    #                 move.positions[0].x = i[0]
    #                 move.positions[0].y = i[1]
    #                 move.positions[1].x = j[0]  
    #                 move.positions[1].y = j[1]

    #                 # Hace el movimiento
    #                 make_move(self.m_board, move, color)

    #                 # Quita el valor de posibles de la lista, ya está ocupado
    #                 possibles_aux = possibles.copy()
    #                 possibles_aux.remove(j)

    #                 # ------ EXPAND -----
    #                 score_aux = self.alpha_beta(possibles_aux, depth-1, turn)
    #                 score_aux[1]= [i, j]
                    
    #                 # ------- Poda alfa - beta -------
    #                 # Max: estamos en el caso de que estamos moviendo. Antes del bucle se cambia
    #                 #   la variable
    #                 if turn == 1:

    #                     if score_aux[0] > score[0]:
    #                         score = score_aux
                        
    #                     if score[0] >= alpha_beta[1]:
    #                         return score

    #                     alpha_beta[0] = max(alpha_beta[0], score[0])
                    
    #                 # Min: estamos en el caso que mueve el oponente. Antes del bucle se cambia la variable
    #                 if turn == 0:

    #                     if score_aux[0] < score[0]:
    #                         score = score_aux
                        
    #                     if score[0] <= alpha_beta[0]:
    #                         return score

    #                     alpha_beta[1] = max(alpha_beta[1], score[0])
                    
    #                 # Se vuelve a insertar el elemento para las siguientes iteraciones
    #                 possibles_aux.append(j)

    #                 # Deshace el movimiento
    #                 make_move(self.m_board, move, Defines.NOSTONE)

    #     return score

    # ------ Heuristica 1.0: busca filas --------
    def find_file(self, ini_x = 1, ini_y = 1):
        count = 0        
        
        if ini_x < 1 and ini_y > 20:
            print("\n\n cuidado \n\n")
            return 0

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


        # if count > 0:
        #     print_board(self.m_board)
        #     time.sleep(10)
        return count

    def threats(self, color):
        color_2 = color
        
        if color ==Defines.WHITE:
            color_2 = Defines.BLACK
        else:
            color_2 = Defines.WHITE

        num_threats = [np.zeros(19),
                    np.zeros(19), 
                    np.zeros(38),
                    np.zeros(38)]
        
        # Jugador
        h_threats = []
        seen_h_threats = set(h_threats)
        
        v_threats = []
        seen_v_threats = set(v_threats)

        d_threats = []
        seen_d_threats = set(d_threats)

        d2_threats = []
        seen_d2_threats = set(d2_threats)


        # # # Rival
        num_threats_2 = [np.zeros(19),
                    np.zeros(19), 
                    np.zeros(38),
                    np.zeros(38)]
        

        h_threats_2 = []
        seen_h_threats_2 = set(h_threats_2)
        
        v_threats_2 = []
        seen_v_threats_2 = set(v_threats_2)

        d_threats_2 = []
        seen_d_threats_2 = set(d_threats_2)

        d2_threats_2 = []
        seen_d2_threats_2 = set(d2_threats_2)

        # Y
        start_i = max(self.start_possible_y - 3, 1)
        end_i = min(self.end_possible_y + 3, Defines.GRID_NUM - 1)

        # x = Defines.GRID_NUM - 1 - j
        # y = i
        # stone = self.m_board[x][y]

        start_j = max(Defines.GRID_NUM - 1 - self.start_possible_x - 3, 1)
        
        if start_j < 1:
            start_j = 1

        end_j = min(Defines.GRID_NUM - 1 - self.end_possible_x + 3, Defines.GRID_NUM - 1)
        
        # print(start_i, self.start_possible_y)
        # print(end_i, self.end_possible_y)
        # print(start_j, self.start_possible_x)
        # print(end_j, self.end_possible_x)

        score = 0
        score_2 = 0
        

        for i in range(start_i, end_i):
            for j in reversed(range(start_j, end_j)):
                # Jugador
                count_h = 0
                count_e_h = 0

                count_v = 0
                count_e_v = 0

                count_d = 0
                count_e_d = 0

                count_d = 0
                count_e_d = 0

                count_d2 = 0
                count_e_d2 = 0

                right_e_h = 0
                right_e_v = 0
                right_e_d = [0,0]
                right_e_d2 = [0,0]
                
                # Rival
                count_h_2 = 0
                count_e_h_2 = 0

                count_v_2 = 0
                count_e_v_2 = 0

                count_d_2 = 0
                count_e_d_2 = 0

                count_d_2 = 0
                count_e_d_2 = 0

                count_d2_2 = 0
                count_e_d2_2 = 0

                right_e_h_2 = 0
                right_e_v_2 = 0
                right_e_d_2 = [0,0]
                right_e_d2_2 = [0,0]
                
                # Iteradores
                x = Defines.GRID_NUM - 1 - j
                y = i

                for k in (range(0,6)):
                    # Jugador
                    # Vertical
                    if x + 6 <= 20 and tuple([x + k,y]) not in seen_v_threats:
                        stone = self.m_board[x + k][y]

                        if stone is color:
                            count_v +=  1

                        elif stone is Defines.NOSTONE:
                            count_e_v += 1

                            right_e_v = x+k

                    # Horizontal: está cambiado para que haga [y,x]
                    if y + 6 <= 20 and tuple([x,y + k]) not in seen_h_threats:
                        stone = self.m_board[x][y+k]

                        if stone is color:
                            count_h +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_h += 1

                            right_e_h = y + k

                #     # # Diag
                    if y + 6 <= 20 and x + 6 <= 20  and tuple([x + k,y + k]) not in seen_d_threats:
                        stone = self.m_board[x + k][y + k]

                        if stone is color:
                            count_d +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_d += 1

                            right_e_d = [x + k,y + k]

                #     # # Diag 2
                    if x - 6 >= 0 and y + 6 <= 20  and tuple([y + k,x - k]) not in seen_d2_threats:
                        stone = self.m_board[y + k][x - k]

                        if stone is color:
                            count_d2 +=  1
                            
                        elif stone is Defines.NOSTONE:
                            count_e_d2 += 1

                            right_e_d2 = [y + k,x - k]
                    
                    # Rival
                    # Vertical
                    if x + 6 <= 20 and  tuple([x + k,y]) not in seen_v_threats_2:
                        stone = self.m_board[x + k][y]

                        if stone is color_2:
                            count_v_2 +=  1
                            

                        elif stone is Defines.NOSTONE:
                            count_e_v_2 += 1

                            right_e_v_2 = x+k
                                         

                    # Horizontal: está cambiado para que haga [y,x]
                    if y + 6 <= 20 and tuple([x,y + k]) not in seen_h_threats_2:
                        stone = self.m_board[x][y+k]

                        if stone is color_2:
                            count_h_2 +=  1
                            

                        elif stone is Defines.NOSTONE:
                            count_e_h_2 += 1

                            right_e_h_2 = y + k
                            

                #     # # Diag    /
                    if y + 6 <= 20 and x + 6 <= 20  and tuple([x + k,y + k]) not in seen_d_threats_2:
                        stone = self.m_board[x + k][y + k]

                        if stone is color_2:
                            count_d_2 +=  1

                        elif stone is Defines.NOSTONE:
                            count_e_d_2 += 1

                            right_e_d_2 = [x + k,y + k]

                            

                #     # # Diag 2   \
                    if x - 6 >= 0 and y + 6 <= 20  and tuple([x - k,y + k]) not in seen_d2_threats_2:
                        stone = self.m_board[x - k][y + k]

                        if stone is color_2:
                            count_d2_2 +=  1
                            
                            
                            
                        elif stone is Defines.NOSTONE:
                            count_e_d2_2 += 1

                            right_e_d2_2 = [x - k,y + k]
                            

                            
                # Jugador
                if count_v == 4 and count_e_v == 2: 
                    #h_threats.append([x,right_e_h])
                    seen_v_threats.add(tuple([right_e_v, y]))

                    num_threats[0][y-1] += 1
                
                    
                    
                if count_h == 4 and count_e_h == 2:
                    #v_threats.append([right_e_v, x])
                    seen_h_threats.add(tuple([x, right_e_h]))

                    num_threats[1][x-1] += 1
                    
                if count_d == 4 and count_e_d == 2:
                    #d_threats.append([right_e_d[0], right_e_d[1]])
                    seen_d_threats.add(tuple([right_e_d[0], right_e_d[1]]))
                    
                    num_threats[2][x - y -2] += 1
                    
                if count_d2 == 4 and count_e_d2 == 2:
                    #d2_threats.append([right_e_d2[0], right_e_d2[1]])
                    seen_d2_threats.add(tuple([right_e_d2[0], right_e_d2[1]]))

                    num_threats[3][i + j -2] += 1



                # # Rival
                if count_v_2 == 4 and count_e_v_2 == 2: 
                    #h_threats.append([x,right_e_h])
                    seen_v_threats_2.add(tuple([right_e_v_2, y]))

                    num_threats_2[0][y-1] += 1
                    

    
                if count_h_2 == 4 and count_e_h_2 == 2:
                    #v_threats.append([right_e_v, x])
                    seen_h_threats_2.add(tuple([x, right_e_h_2]))

                    num_threats_2[1][x-1] += 1
                    
                    
                # /
                if count_d_2 == 4 and count_e_d_2 == 2:
                    #d_threats.append([right_e_d[0], right_e_d[1]])
                    seen_d_threats_2.add(tuple([right_e_d_2[0], right_e_d_2[1]]))

                    num_threats_2[2][x - y -2] += 1
                    


                # \ 
                if count_d2_2 == 4 and count_e_d2_2 == 2:
                    #d2_threats.append([right_e_d2[0], right_e_d2[1]])
                    seen_d2_threats_2.add(tuple([right_e_d2_2[0], right_e_d2_2[1]]))
                    
                    num_threats_2[3][i - j -2] += 1
                    

        
        for i in range(len(num_threats[2])):
            # 2
            if num_threats_2[2][i] == 3:
                score_2 += 100
                break
                
                
                
            
            if num_threats_2[2][i] is not None and num_threats_2[2][i] != 0:
                score_2 += num_threats_2[2][i]**num_threats_2[2][i]**num_threats_2[2][i]

            
            # 3
            if num_threats_2[3][i] == 3:
                score_2 += 100
                break
                
                
                
            
            if num_threats_2[3][i] is not None and num_threats_2[3][i] != 0:
                score_2 += num_threats_2[3][i]**num_threats_2[3][i]**num_threats_2[3][i]

            # 0
            if i < len(num_threats[0]):
                if num_threats_2[0][i] == 3:
                    score_2 += 100
                    break
                    
                    
                if num_threats_2[0][i] is not None and num_threats_2[0][i] != 0:
                    score_2 += num_threats_2[0][i]**num_threats_2[0][i]**num_threats_2[0][i]



                if num_threats_2[1][i] == 3:
                    score_2 += 100
                    break
                                    
                if num_threats_2[1][i] is not None and num_threats_2[1][i] != 0:
                    score_2 += num_threats_2[1][i]**num_threats_2[1][i]**num_threats_2[1][i]


                # 0
                if num_threats[0][i] == 3:
                    score = math.inf
                    break

                if num_threats[0][i] is not None and num_threats[0][i] != 0:
                    score += num_threats[0][i]**num_threats[0][i]**num_threats[0][i]
                
                # 1
                if num_threats[1][i] == 3:
                    score = math.inf
                    break
                
                if num_threats[1][i] is not None and num_threats[1][i] != 0:
                    score += num_threats[1][i]**num_threats[1][i]**num_threats[1][i]

            
            # # 2
            if num_threats[2][i] == 3:
                score = math.inf
                break
            
            if num_threats[2][i] is not None and num_threats[2][i] != 0:
                score += num_threats[2][i]**num_threats[2][i]**num_threats[2][i]

            
            # 3
            if num_threats[3][i] == 3:
                score = math.inf
                break
            
            if num_threats[3][i] is not None and num_threats[3][i] != 0:
                score += num_threats[3][i]**num_threats[3][i]**num_threats[3][i]

        # print(score)
        # print(score_2)

        if score_2 > 0:
            return -score_2
        return -score_2
            

def flush_output():
    import sys
    sys.stdout.flush()
