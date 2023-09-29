from tools import *
from defines import *

class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0

    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):

        print("\n\n ME DICE EL COLOR ", str(ourColor))
    
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
            move1 = self.find_possible_move()
            bestMove.positions[0].x = move1[0]
            bestMove.positions[0].y = move1[1]
            bestMove.positions[1].x = move1[0]
            bestMove.positions[1].y = move1[1]
            make_move(self.m_board,bestMove,ourColor)
            
            '''#Check game result
            if (is_win_by_premove(self.m_board, bestMove)):
                #Self wins.
                return Defines.MININT + 1;'''
            
            move2 = self.find_possible_move()
            bestMove.positions[1].x = move2[0]
            bestMove.positions[1].y = move2[1]
            make_move(self.m_board,bestMove,ourColor)

        return alpha
        
    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        
        # Lista de posibilidades
        possibles = []

        # Tabla Hash de la lista de posibilidades (consultas en O(1))
        seen = set(possibles)

        # N vecinos cercanos
        n = 2

        # Doble para recorrer todas las posiciones del tablero 
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
                                    
                                    # Si la casilla a explorar es un hueco y no está en la lista de posibles (con la tabla Hash)
                                    if self.m_board[start_xy[0]][start_xy[1]] == Defines.NOSTONE and tuple([start_xy[0], start_xy[1]]) not in seen:

                                        # Se añade a la lista de posibles y la tabla Hash
                                        possibles.append([start_xy[0], start_xy[1]])
                                        seen.add(tuple([start_xy[0], start_xy[1]]))


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
                    
                    # print("\n\n")
                    # print(possibles)
                    # print(seen)
                    # print("\n\n")
 
               # if stone == Defines.NOSTONE:    
                    # if (x + 1 < 20 and (self.m_board[x+1][y] == Defines.BLACK or self.m_board[x+1][y] == Defines.WHITE)) or  (x - 1 > 0 and (self.m_board[x-1][y] == Defines.BLACK or self.m_board[x-1][y] == Defines.WHITE)) or  (y + 1 < 20 and (self.m_board[x][y+1] == Defines.BLACK or self.m_board[x][y+1] == Defines.WHITE)) or  (y - 1 > 0 and (self.m_board[x][y-1] == Defines.BLACK or self.m_board[x][y-1] == Defines.WHITE)) or ((x + 1 < 20 and y + 1 < 20) and ((self.m_board[x+1][y+1] == Defines.BLACK or self.m_board[x+1][y+1] == Defines.WHITE))) or ((x + 1 < 20 and y - 1 >0) and ((self.m_board[x+1][y-1] == Defines.BLACK or self.m_board[x+1][y-1] == Defines.WHITE))) or ((x - 1 > 0 and y + 1 < 20) and ((self.m_board[x-1][y+1] == Defines.BLACK or self.m_board[x-1][y+1] == Defines.WHITE))) or ((x - 1 > 0 and y - 1 > 0) and ((self.m_board[x-1][y-1] == Defines.BLACK or self.m_board[x-1][y-1] == Defines.WHITE))):
                    #     print(" 3", end="")
                    #     possibles.append([x, y])
                    
            #         else:
            #             print(" -", end="")
            #     elif stone == Defines.BLACK:
            #         print(" O", end="")
            #     elif stone == Defines.WHITE:
            #         print(" *", end="")
               
            # print(" ") 

        # print(possibles)       

        
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
        
                if(self.m_board[i][j] == Defines.NOSTONE):
                    return (i,j)
        return (-1,-1)

def flush_output():
    import sys
    sys.stdout.flush()
