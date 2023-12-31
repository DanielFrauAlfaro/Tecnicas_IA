from tools import *
from defines import *
import math
import numpy as np
import time



class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.ourColor = 0

        # Ventana de búsqueda de amenazas
        self.start_possible_x = 1
        self.start_possible_y = Defines.GRID_NUM - 1

        self.end_possible_x = Defines.GRID_NUM - 1
        self.end_possible_y = 1

        # Contador de turnos
        self.turn = 0

        # Turnos anteriores
        self.pre_move = [StoneMove(), StoneMove()]

# MAX PARAMS: [13, 8, 2, 34, 36, 4] --> 11105668.0

        # Parámetros
        self.m_score = 13        # Ponderación score MAX 
        self.m_score_2 = 34      # Ponderacion score MIN

        self.m_riv = 36          # Base del conteo de amenazas de MAX
        self.m_pos = 8          # Base del conteo de amenazas de MIN

        self.m_med_pos = 2      # Conteo de medias amenazas
        self.m_med_riv = 4      # Conteo de medias amenazas
        

    # Getter de los parámetros
    def get_params(self):
        return [self.m_score, self.m_pos, self.m_med_pos, self.m_score_2, self.m_riv, self.m_med_riv]

    # Setter de los parámetros
    def set_params(self, params):
        self.m_score = params[0]
        self.m_pos = params[1]
        self.m_med_pos = params[2]

        self.m_score_2 = params[3]
        self.m_riv = params[4]
        self.m_med_riv = params[5]
        
    # Reinicia el search_engine
    def restart(self):
        self.start_possible_x = 1
        self.start_possible_y = Defines.GRID_NUM - 1

        self.end_possible_x = Defines.GRID_NUM - 1
        self.end_possible_y = 1

        self.turn = 0
        self.pre_move = [StoneMove(), StoneMove()]


    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0


    # Función para el Alpha - Beta
    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
        
        self.ourColor = ourColor
        self.m_alphabeta_depth = 2
        
        #Check game result
        if (is_win_by_premove(self.m_board, preMove)):
            print("ALGUIEN HA GANADO")

            if (ourColor == self.m_chess_type):
                #Opponent wins.
                return 0
            else:
                #Self wins.
                return Defines.MININT + 1

        self.pre_move[0] = preMove
        if self.turn == 0:
            self.pre_move[1] = preMove

        self.turn += 2
        
        alpha = 0
        # Primer turno
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10

        # Turno normal
        else:
            # Busca el movimiento
            move = self.find_possible_move(self.m_alphabeta_depth)
            alpha = move[0]

            bestMove.positions[0].x = move[1][0][0]
            bestMove.positions[0].y = move[1][0][1]
            bestMove.positions[1].x = move[1][1][0]
            bestMove.positions[1].y = move[1][1][1]

            self.pre_move[1] = bestMove

        return alpha
    
    # Comprueba si el tablero está vacío (primer movimiento)
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
    
    # Encuentra un movimiento para el agente
    def find_possible_move(self, depth, turn = 0):

        flag = False

        winning_move = []

        # Jugador
        h_threats = []
        seen_h_threats = set(h_threats)
        
        v_threats = []
        seen_v_threats = set(v_threats)

        d_threats = []
        seen_d_threats = set(d_threats)

        d2_threats = []
        seen_d2_threats = set(d2_threats)

        num_threats = [np.zeros(19),
                    np.zeros(19), 
                    np.zeros(38),
                    np.zeros(38)]

        # Busca amenazas propias, de manera que si encuentra dos amenazas propias hará el movimiento ganador
        for i in range(1, Defines.GRID_NUM - 1):

            # Si encuentra un movimiento, detiene la búsqueda
            if flag:
                break

            for j in reversed(range(1, Defines.GRID_NUM - 1)):
                
                # Contador de fichas del jugador (count_x) y huecos (count_e_x)
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

                list_e_h = []
                list_e_v = []
                list_e_d = []
                list_e_d2 = []

                right_e_h = 0
                right_e_v = 0
                right_e_d = [0,0]
                right_e_d2 = [0,0]
                
                
                # Iteradores
                x = Defines.GRID_NUM - 1 - j
                y = i

                for k in (range(0,6)):
                    # Jugador
                    # Horizontal: está cambiado para que haga [y,x]
                    if x + 6 <= 20 and tuple([x + k,y]) not in seen_v_threats:
                        stone = self.m_board[x + k][y]

                        if stone is self.ourColor:
                            count_v +=  1

                        elif stone is Defines.NOSTONE:
                            count_e_v += 1
                            list_e_v.append([x + k, y])

                            right_e_v = x+k

                    # Vertical
                    if y + 6 <= 20 and tuple([x,y + k]) not in seen_h_threats:
                        stone = self.m_board[x][y+k]

                        if stone is self.ourColor:
                            count_h +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_h += 1
                            list_e_h.append([x, y + k])

                            right_e_h = y + k

                    # Diag
                    if y + 6 <= 20 and x + 6 <= 20  and tuple([x + k,y + k]) not in seen_d_threats:
                        stone = self.m_board[x + k][y + k]

                        if stone is self.ourColor:
                            count_d +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_d += 1
                            list_e_d.append([x + k, y + k])

                            right_e_d = [x + k,y + k]

                    # Diag 2
                    if x - 6 >= 0 and y + 6 <= 20  and tuple([y + k,x - k]) not in seen_d2_threats:
                        stone = self.m_board[y + k][x - k]

                        if stone is self.ourColor:
                            count_d2 +=  1
                            
                        elif stone is Defines.NOSTONE:
                            count_e_d2 += 1
                            list_e_d2.append([y + k, x - k])

                            right_e_d2 = [y + k,x - k]

                # En el caso en el que se detecte una amenaza en profundidad 0, guarda el movimiento y detiene la búsqueda   
                # Jugador
                if count_v == 4 and count_e_v == 2: 
                    #h_threats.append([x,right_e_h])
                    seen_v_threats.add(tuple([right_e_v, y]))
                    num_threats[0][y-1] += 1

                    flag = True
                    winning_move = list_e_v
                    break

                
                    
                if count_h == 4 and count_e_h == 2:
                    #v_threats.append([right_e_v, x])
                    seen_h_threats.add(tuple([x, right_e_h]))
                    num_threats[1][x-1] += 1


                    flag = True
                    winning_move = list_e_h
                    break
                    
                
                if count_d == 4 and count_e_d == 2:
                    #d_threats.append([right_e_d[0], right_e_d[1]])
                    seen_d_threats.add(tuple([right_e_d[0], right_e_d[1]]))
                    num_threats[2][x - y -2] += 1

                    flag = True
                    winning_move = list_e_d
                    break

                    
                if count_d2 == 4 and count_e_d2 == 2:
                    #d2_threats.append([right_e_d2[0], right_e_d2[1]])
                    seen_d2_threats.add(tuple([right_e_d2[0], right_e_d2[1]]))
                    num_threats[3][x + y -2] += 1


                    flag = True
                    winning_move = list_e_d2
                    break

        # Lista de posibilidades
        possibles = []

        # Tabla Hash de la lista de posibilidades (consultas en O(1))
        seen = set(possibles)

        # N vecinos cercanos
        n = 2

        idx = 0

        # Doble bucle para recorrer todos los movimientos previos del tablero 
        for o in reversed(self.pre_move):
            if idx == 1:
                n = 3
            idx += 1
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

                                        # Actualiza la ventana de búsqueda
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
        
        # Inicialización del score
        score = [0, [[-1, -1], [-1, -1]]]

        # Si tiene un movimiento ganador, lo hace y gana
        if flag:
            return [1000000, winning_move]
        else:
            self.transp = {}
            score = self.max(possibles, depth, -math.inf, math.inf) # Aplica NEGAMAX

        return score
    

    # Función MAX para la búsqueda en el espacio de estados
    def max(self, possibles, depth, alpha, beta, turn = 1):
        score = [0, [[-1, -1], [-1, -1]]]

        # Caso base: profundidad == 0
        if depth == 0:

            # Busca las amenazas y ofrece una puntuación al tablero
            score[0] = self.threats(self.ourColor)
            
            return score


        # Exploración
        else:
            transp = {}
            score[0] = -math.inf
            move = StoneMove()
            color = self.ourColor
            
            # Cambia el color de la búsqueda según 'turn'
            if turn == -1:
                if self.ourColor == Defines.WHITE:
                    color = Defines.BLACK
                else:
                    color = Defines.WHITE

            idx_i = 0
            
            # Por cada valor posible, establece todas las combinaciones posibles
            for i in possibles:
                
                # Remueve el primero de la lista para que no repita valores en las siguientes llamadas
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

                    # Variable para indicar si se encuentra en la tabla
                    found = False

                    # Keys de la tabla de transposicion
                    ij = ((i[0], i[1]), (j[0], j[1]), color)
                    ji = ((j[0], j[1]), (i[0], i[1]), color)

                    # Obtiene el valor de la tabla
                    idx_ij = transp.get(ij)

                    # Variable auxiliar del score
                    score_aux = [0, [[-1, -1], [-1, -1]]]

                    # Si el movimiento está en la tabla, coge su resultado
                    if idx_ij != None:
                        found = True
                        score_aux[0] = idx_ij

                    # Si no encuentra un valor, expande y guarda el resultado en la tabla
                    if not found:
                        score_aux = self.max(possibles_aux, depth-1, -alpha, -beta, turn * -1)
                        score_aux[0] = -score_aux[0]

                        transp[ij] = score_aux[0]
                        transp[ji] = score_aux[0]
                    
                    # Actualiza los valores
                    score_aux[1]= [i, j]

                    make_move(self.m_board, move, Defines.NOSTONE)

                    # Poda Alfa - Beta
                    if score_aux[0] > score[0]:
                        score = score_aux

                    if score[0] >= beta:
                        return score
                    
                    if score[0] > alpha:
                        alpha = score[0]

                    
                    if alpha >= beta:
                        return score
                
                # Reinserta el valor
                possibles.insert(idx_i, i)
                idx_i += 1

        return score
    

    # Identifica las amenazas de MAX y MIN y las combina con una suma ponderada
    def threats(self, color):
        color_2 = color
        
        # Elige el color MAX y MIN
        if color ==Defines.WHITE:
            color_2 = Defines.BLACK
        else:
            color_2 = Defines.WHITE

        # Jugador
        seen_h_threats = set([])
        
        seen_v_threats = set([])

        seen_d_threats = set([])

        seen_d2_threats = set([])

        # Rival
        seen_h_threats_2 = set([])
        
        seen_v_threats_2 = set([])

        seen_d_threats_2 = set([])

        seen_d2_threats_2 = set([])

        # Ventana con los valores modificados para ampliarlos en 2 casillas
        # Y
        start_i = max(self.start_possible_y - 2, 1)
        end_i = min(self.end_possible_y + 2, Defines.GRID_NUM - 1)


        start_j = max(Defines.GRID_NUM - 1 - self.start_possible_x - 2, 1)
        
        if start_j < 1:
            start_j = 1

        end_j = min(Defines.GRID_NUM - 1 - self.end_possible_x + 2, Defines.GRID_NUM - 1)


        score = 0
        score_2 = 0

        # Tabla Hash de amenazas
        threats_dict = {}
        
        # Recorre la ventana
        for i in range(start_i, end_i):
            for j in reversed(range(start_j, end_j)):
                # Contador de fichas de los jugadores (count_x) y huecos (count_e_x)
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

                #    Ventana de 6: si está dentro de los límites y no han visto la amenaza, incrementa si es un hueco
                # o una ficha propia en cada dirección
                for k in (range(0,6)):
                    # Jugador
                    # Horizontal: está cambiado para que haga [y,x]
                    if x + 6 <= 20 and tuple([x + k,y]) not in seen_v_threats:
                        stone = self.m_board[x + k][y]

                        if stone is color:
                            count_v +=  1

                        elif stone is Defines.NOSTONE:
                            count_e_v += 1

                            right_e_v = x+k

                    # Vertical
                    if y + 6 <= 20 and tuple([x,y + k]) not in seen_h_threats:
                        stone = self.m_board[x][y+k]

                        if stone is color:
                            count_h +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_h += 1

                            right_e_h = y + k

                    # # Diag
                    if y + 6 <= 20 and x + 6 <= 20  and tuple([x + k,y + k]) not in seen_d_threats:
                        stone = self.m_board[x + k][y + k]

                        if stone is color:
                            count_d +=  1
                        elif stone is Defines.NOSTONE:
                            count_e_d += 1

                            right_e_d = [x + k,y + k]

                    # # Diag 2
                    if x - 6 >= 0 and y + 6 <= 20  and tuple([y + k,x - k]) not in seen_d2_threats:
                        stone = self.m_board[y + k][x - k]

                        if stone is color:
                            count_d2 +=  1
                            
                        elif stone is Defines.NOSTONE:
                            count_e_d2 += 1

                            right_e_d2 = [y + k,x - k]
                    


                    # Rival
                    # Horizontal: está cambiado para que haga [y,x]
                    if x + 6 <= 20 and  tuple([x + k,y]) not in seen_v_threats_2:
                        stone = self.m_board[x + k][y]

                        if stone is color_2:
                            count_v_2 +=  1
                            

                        elif stone is Defines.NOSTONE:
                            count_e_v_2 += 1

                            right_e_v_2 = x+k
                                         
                    # Vertical
                    if y + 6 <= 20 and tuple([x,y + k]) not in seen_h_threats_2:
                        stone = self.m_board[x][y+k]

                        if stone is color_2:
                            count_h_2 +=  1
                            
                        elif stone is Defines.NOSTONE:
                            count_e_h_2 += 1

                            right_e_h_2 = y + k
                            
                    # Diag    
                    if y + 6 <= 20 and x + 6 <= 20  and tuple([x + k,y + k]) not in seen_d_threats_2:
                        stone = self.m_board[x + k][y + k]

                        if stone is color_2:
                            count_d_2 +=  1

                        elif stone is Defines.NOSTONE:
                            count_e_d_2 += 1

                            right_e_d_2 = [x + k,y + k]

                    # Diag 2   
                    if x - 6 >= 0 and y + 6 <= 20  and tuple([x - k,y + k]) not in seen_d2_threats_2:
                        stone = self.m_board[x - k][y + k]

                        if stone is color_2:
                            count_d2_2 +=  1
                            
                            
                            
                        elif stone is Defines.NOSTONE:
                            count_e_d2_2 += 1

                            right_e_d2_2 = [x - k,y + k]

                # Cuenta amenazas en cada dirección y la almacena en la tabla Hash 
                # Si encuentra 6 alineadas, genera puntuación máxima y acaba el bucle
                # Genera puntuación para las amenazas parciales       
                # Jugador
                # Horizontal
                if count_v == 4 and count_e_v == 2: 

                    if threats_dict.get("pos_h_" + str(y-1)) is not None:
                        threats_dict["pos_h_" + str(y-1)] += 1
                    else:
                        threats_dict["pos_h_" + str(y-1)] = 1

                    seen_v_threats.add(tuple([right_e_v, y]))

                elif count_v == 6:
                    
                    score = 1000000000
                    break
                
                elif count_v == 3 and count_e_v >= 3:
                    score += self.m_med_pos


                # Vertical                
                if count_h == 4 and count_e_h == 2:
                    if threats_dict.get("pos_v_" + str(x-1)) is not None:
                        threats_dict["pos_v_" + str(x-1)] += 1
                    else:
                        threats_dict["pos_v_" + str(x-1)] = 1

                    seen_h_threats.add(tuple([x, right_e_h]))
                    
                elif count_h == 6:
                    
                    score = 1000000000
                    break
                
                elif count_h == 3 and count_e_h >= 3:
                    score += self.m_med_pos
                


                # Diagonal
                if count_d == 4 and count_e_d == 2:
                    if threats_dict.get("pos_d_" + str(x - y - 2)) is not None:
                        threats_dict["pos_d_" + str(x - y - 2)] += 1
                    else:
                        threats_dict["pos_d_" + str(x - y - 2)] = 1

                    seen_d_threats.add(tuple([right_e_d[0], right_e_d[1]]))

                elif count_d == 6:
                    
                    score = 1000000000
                    break

                elif count_d == 3 and count_e_d >= 3:
                    score += self.m_med_pos



                # Diagonal 2
                if count_d2 == 4 and count_e_d2 == 2:
                    if threats_dict.get("pos_d2_" + str(x + y - 2)) is not None:
                        threats_dict["pos_d2_" + str(x + y - 2)] += 1
                    else:
                        threats_dict["pos_d2_" + str(x + y - 2)] = 1

                    seen_d2_threats.add(tuple([right_e_d2[0], right_e_d2[1]]))

                elif count_d2 == 6:
                    
                    score = 1000000000
                    break
                    
                elif count_d2 == 3 and count_e_d2 >= 3:
                    score += self.m_med_pos



                # Rival
                # Horizontal
                if count_v_2 == 4 and count_e_v_2 == 2: 
                    if threats_dict.get("riv_h_" + str(y - 1)) is not None:
                        threats_dict["riv_h_" + str(y - 1)] += 1
                    else:
                        threats_dict["riv_h_" + str(y - 1)] = 1

                    seen_v_threats_2.add(tuple([right_e_v_2, y]))
                
                elif count_v_2 == 6:
                    
                    score_2 = 1000000000
                    break
            
                elif count_v_2 == 3 and count_e_v_2 >= 3:
                    score_2 += self.m_med_riv


                # Vertical
                if count_h_2 == 4 and count_e_h_2 == 2:
                    if threats_dict.get("riv_v_" + str(x - 1)) is not None:
                        threats_dict["riv_v_" + str(x - 1)] += 1
                    else:
                        threats_dict["riv_v_" + str(x - 1)] = 1

                    seen_h_threats_2.add(tuple([x, right_e_h_2]))

                elif count_h_2 == 6:
                    
                    score_2 = 1000000000
                    break
                    
                elif count_h_2 == 3 and count_e_h_2 >= 3:
                    score_2 += self.m_med_riv



                # Diagonal
                if count_d_2 == 4 and count_e_d_2 == 2:
                    if threats_dict.get("riv_d_" + str(x - y - 2)) is not None:
                        threats_dict["riv_d_" + str(x - y - 2)] += 1
                    else:
                        threats_dict["riv_d_" + str(x - y - 2)] = 1

                    seen_d_threats_2.add(tuple([right_e_d_2[0], right_e_d_2[1]]))
                
                elif count_d_2 == 6:
                    
                    score_2 = 1000000000
                    break
                    
                elif count_d_2 == 3 and count_e_d_2 >= 3:
                    score_2 += self.m_med_riv


                # Diagonal 2
                if count_d2_2 == 4 and count_e_d2_2 == 2:
                    if threats_dict.get("riv_d2_" + str(x + y - 2)) is not None:
                        threats_dict["riv_d2_" + str(x + y - 2)] += 1
                    else:
                        threats_dict["riv_d2_" + str(x + y - 2)] = 1

                    seen_d2_threats_2.add(tuple([right_e_d2_2[0], right_e_d2_2[1]]))
                
                elif count_d2_2 == 6:
                    
                    score_2 = 1000000000
                    break

                elif count_d2_2 == 3 and count_e_d2_2 >= 3:
                    score_2 += self.m_med_riv


        # Genera las puntuaciones en base a las amenazas
        for key, value in threats_dict.items():
            if key[0] == "p":
                score += self.m_pos ** value
            else:
                score_2 += self.m_riv ** value

        return  score * self.m_score - score_2 * self.m_score_2
            

def flush_output():
    import sys
    sys.stdout.flush()
