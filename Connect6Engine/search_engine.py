from tools import *
from defines import *

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0
        self.ourColor = 0

        self.start_possible_x = 1
        self.start_possible_y = 1
        self.start_found = False

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

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
        
        alpha = 0
        if(self.check_first_move()):
            bestMove.positions[0].x = 10
            bestMove.positions[0].y = 10
            bestMove.positions[1].x = 10
            bestMove.positions[1].y = 10
        else:   
            move = self.find_possible_move(self.m_alphabeta_depth)
            
            self.start_found = False
            self.start_possible_x = 1
            self.start_possible_y = 1

            bestMove.positions[0].x = move[0][0]
            bestMove.positions[0].y = move[0][1]
            bestMove.positions[1].x = move[1][0]
            bestMove.positions[1].y = move[1][1]
            make_move(self.m_board,bestMove,ourColor)

        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self, depth, turn = 0):
        
        score = 0

        if depth == 0:
            for i in range(self.start_possible_x, Defines.GRID_NUM - 1):
                for j in range(self.start_possible_y, Defines.GRID_NUM - 1):
                    
                    # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
                    x = Defines.GRID_NUM - 1 - j
                    y = i
                    stone = self.m_board[x][y]
                    
                    mult = 1

                    score += self.find_file(x,y)*mult
    
        else:
            # Lista de posibilidades
            possibles = []

            # Tabla Hash de la lista de posibilidades (consultas en O(1))
            seen = set(possibles)

            # N vecinos cercanos
            n = 2

            # Doble para recorrer todas las posiciones del tablero 
            # IMPORTANTE: esto empieza por el start_possible para que de expandir el arbol, no busque desde el (1,1)
            for i in range(self.start_possible_x, Defines.GRID_NUM - 1):
                for j in range(self.start_possible_y, Defines.GRID_NUM - 1):
                    
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
                                        
                                        # Indica por donde empezar a buscar en la siguiente iteración
                                        if self.start_found is not True:
                                            self.start_found = True
                                            self.start_possible_x = i
                                            self.start_possible_y = j

                                        # Si la casilla a explorar es un hueco y no está en la lista de posibles (con la tabla Hash)
                                        if self.m_board[start_xy[0]][start_xy[1]] == Defines.NOSTONE and tuple([start_xy[0], start_xy[1]]) not in seen:

                                            # Se añade a la lista de posibles y la tabla Hash
                                            possibles.append([start_xy[0], start_xy[1]])
                                            seen.add(tuple([start_xy[0], start_xy[1]]))

                                            m_move = StoneMove()
                                            m_move.positions[0].x = x
                                            m_move.positions[0].y = y
                                            m_move.positions[1].x = x
                                            m_move.positions[1].y =y

                                            make_move(self.m_board, m_move, self.ourColor)





                                            # TODO: aqui iria la poda alfa beta
                                            score = self.find_possible_move(depth-1)






                                            make_move(self.m_board, m_move, Defines.NOSTONE)



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

        return (-1,-1)

    def find_file(self, ini_x = 1, ini_y = 1):
        count = 0

        # Cambio de coordenadas de [1,1] a [19,1] propia del tablero 
        stone = self.m_board[ini_x][ini_y]
        
        if stone is not self.ourColor and ini_x < 1 and ini_y > 19:
            if stone is Defines.NOSTONE:
                return 0
            else:
                return -1

        # Si encuentra un hueco donde hay una ficha ...   
        else:
            x_row = self.find_file(ini_x-1, ini_y) 
            y_row = self.find_file(ini_x, ini_y+1)
            diag_row = self.find_file(ini_x-1, ini_y+1)
            
            if x_row == -1:
                x_row = 0
            if y_row == -1:
                y_row = 0
            if diag_row == -1:
                diag_row = 0

            if ini_x + 1 < 20 and self.m_board[ini_x + 1][ini_y] is not self.ourColor:
                x_row = 0
            if ini_y - 1 > 0 and self.m_board[ini_x][ini_y - 1] is not self.ourColor:
                y_row = 0
            if ini_x + 1 < 20  and ini_y - 1 > 0 and self.m_board[ini_x + 1][ini_y - 1] is not self.ourColor:
                diag_row = 0
                

            count = 1 + x_row + y_row + diag_row

        return count
                        

            

def flush_output():
    import sys
    sys.stdout.flush()
