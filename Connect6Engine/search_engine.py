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

        possibles = []
        seen = set(possibles)
        n = 2
        
        print("Recorrer")
        for i in range(1, Defines.GRID_NUM - 1):
            for j in range(1, Defines.GRID_NUM - 1):
                x = Defines.GRID_NUM - 1 - j
                y = i
                stone = self.m_board[x][y]
                        
                if stone is not Defines.NOSTONE:
                    indices = 1

                    for k in range(0,n):
                        start_xy = [x+n-k, y+n-k]
                        inc = -1

                        for h in range(0,4):

                            for f in range(0, 2*(n-k)):
                                if (start_xy[0] < 20 and start_xy[0] > 0) and (start_xy[1] < 20 and start_xy[1] > 0):

                                    if self.m_board[start_xy[0]][start_xy[1]] == Defines.NOSTONE and tuple([start_xy[0], start_xy[1]]) not in seen:
                                        possibles.append([start_xy[0], start_xy[1]])
                                        seen.add(tuple([start_xy[0], start_xy[1]]))


                                # elif inc < 0:
                                #     start_xy[indices] += inc*(2*(n-k) - f+1)
                                #     break
                                
                                start_xy[indices] += inc
                            
                            if h == 1:
                                inc = 1
                            
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
