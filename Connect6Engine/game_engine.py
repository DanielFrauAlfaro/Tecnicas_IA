from defines import *
from tools import *
import sys
from search_engine import SearchEngine
import time
import random
import numpy as np


class GameEngine:
    def __init__(self, name=Defines.ENGINE_NAME):
        if name and len(name) > 0:
            if len(name) < Defines.MSG_LENGTH:
                self.m_engine_name = name
            else:
                print(f"Too long Engine Name: {name}, should be less than: {Defines.MSG_LENGTH}")
        self.m_alphabeta_depth = 2
        self.m_board = t = [ [0]*Defines.GRID_NUM for i in range(Defines.GRID_NUM)]
        self.init_game()
        self.m_search_engine = SearchEngine()
        self.m_best_move = StoneMove()

        self.prev_move = StoneMove()

    def init_game(self):
        init_board(self.m_board)


    def on_help(self):
        print(
            f"On help for GameEngine {self.m_engine_name}\n"
            " name        - print the name of the Game Engine.\n"
            " print       - print the board.\n"
            " exit/quit   - quit the game.\n"
            " black XXXX  - place the black stone on the position XXXX on the board.\n"
            " white XXXX  - place the white stone on the position XXXX on the board, X is from A to S.\n"
            " next        - the engine will search the move for the next step.\n"
            " move XXXX   - tell the engine that the opponent made the move XXXX,\n"
            "              and the engine will search the move for the next step.\n"
            " new black   - start a new game and set the engine to black player.\n"
            " new white   - start a new game and set it to white.\n"
            " depth d     - set the alpha beta search depth, default is 6.\n"
            " vcf         - set vcf search.\n"
            " unvcf       - set none vcf search.\n"
            " help        - print this help.\n")

    def run(self):
        msg = ""
        self.on_help()
        while True:
            msg = input().strip()
            log_to_file(msg)
            if msg == "name":
                print(f"name {self.m_engine_name}")
            elif msg == "exit" or msg == "quit":
                break
            elif msg == "print":
                print_board(self.m_board, self.m_best_move)
            elif msg == "vcf":
                self.m_vcf = True
            elif msg == "unvcf":
                self.m_vcf = False
            elif msg.startswith("black"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.BLACK)
                self.m_chess_type = Defines.BLACK
            elif msg.startswith("white"):
                self.m_best_move = msg2move(msg[6:])
                make_move(self.m_board, self.m_best_move, Defines.WHITE)
                self.m_chess_type = Defines.WHITE
            elif msg == "next":
                self.m_chess_type = self.m_chess_type ^ 3
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    make_move(self.m_board, self.m_best_move, self.m_chess_type)
                    msg = f"move {move2msg(self.m_best_move)}"
                    print(msg)
                    flush_output()
            elif msg.startswith("new"):
                self.init_game()
                if msg[4:] == "black":
                    self.m_best_move = msg2move("JJ")
                    make_move(self.m_board, self.m_best_move, Defines.BLACK)
                    self.m_chess_type = Defines.BLACK
                    msg = "move JJ"
                    print(msg)
                    flush_output()
                else:
                    self.m_chess_type = Defines.WHITE
            elif msg.startswith("move"):
                self.m_best_move = msg2move(msg[5:])
                
                self.prev_move = self.m_best_move

                make_move(self.m_board, self.m_best_move, self.m_chess_type ^ 3)
                if is_win_by_premove(self.m_board, self.m_best_move):
                    print("We lost!")
                if self.search_a_move(self.m_chess_type, self.m_best_move):
                    msg = f"move {move2msg(self.m_best_move)}"
                    make_move(self.m_board, self.m_best_move, self.m_chess_type)
                    print(msg)
                    flush_output()
            elif msg.startswith("depth"):
                d = int(msg[6:])
                if 0 < d < 10:
                    self.m_alphabeta_depth = d
                print(f"Set the search depth to {self.m_alphabeta_depth}.\n")
            elif msg == "help":
                self.on_help()
        return 0

    def search_a_move(self, ourColor, bestMove):
        score = 0
        start = 0
        end = 0

        start = time.perf_counter()
        self.m_search_engine.before_search(self.m_board, self.m_chess_type, self.m_alphabeta_depth, self.prev_move)
        score = self.m_search_engine.alpha_beta_search(self.m_alphabeta_depth, Defines.MININT, Defines.MAXINT, ourColor, bestMove, bestMove)
        end = time.perf_counter()

        print(f"AB Time:\t{end - start:.3f}")
        print(f"Node:\t{self.m_search_engine.m_total_nodes}\n")
        print(f"Score:\t{score:.3f}")
        return True

def flush_output():
    sys.stdout.flush()

def gen_random_vector():
    vec =  [np.random.randint(1  , 30, (1,2))[0], 
            np.random.randint(1  , 10, (1,1))[0],
            np.random.randint(20 , 60, (1,2))[0], 
            np.random.randint(1 , 10, (1,1))[0]]

    return [vec[0][0], vec[0][1], vec[1][0], vec[2][0], vec[2][1], vec[3][0]]

# Create an instance of GameEngine and run the game
if __name__ == "__main__":
    # Hiperparámetros
    N_epochs = 10
    N_pop = 4
    N_turns = 10
    N_fathers_pairs = 2
    N_params = 6
    std_mutation = 2.5
    mutation_limit = 0.3

    search_engine = []

    game_ = GameEngine()

    # Generación de población inicial aleatoria
    for i in range(0, N_pop):
        search_engine_ = SearchEngine()

        params = gen_random_vector()

        search_engine_.set_params(params)

        search_engine.append([0, search_engine_])


    # ---- Algoritmo genético. Entrenamientos ----
    for i in range(0, N_epochs):

        print("EPOCH ", i)

        idx_j = -1

        # Partidas cruzadas
        for j in search_engine:
            print("Evaluating ", idx_j + 1)
            idx_j += 1
            idx_k = 0

            for k in search_engine:
                
                # Si no son el mismo
                if j[1].get_params() != k[1].get_params():
                    print("-- Match ", idx_j, " VS ", idx_k)
                    
                    # Inicializa los movimientos
                    bestMove_1 = StoneMove()
                    bestMove_1.positions[0].x = 10
                    bestMove_1.positions[0].y = 10
                    bestMove_1.positions[1].x = 10
                    bestMove_1.positions[1].y = 10

                    bestMove_2 = StoneMove()
                    bestMove_2.positions[0].x = 10
                    bestMove_2.positions[0].y = 10
                    bestMove_2.positions[1].x = 10
                    bestMove_2.positions[1].y = 10

                    # Puntuación de cada agente
                    score_1 = 0
                    score_2 = 0

                    # Turnos
                    for _ in range(0, N_turns):
                        
                        # Turno de BLACK
                        k[1].before_search(game_.m_board, Defines.BLACK, 2, bestMove_1)
                        score_2 += k[1].alpha_beta_search(2, Defines.MININT, Defines.MAXINT, Defines.BLACK, bestMove_2, bestMove_2)
                        make_move(game_.m_board, bestMove_2, Defines.BLACK)
                        
                        # Gana WHITE
                        if is_win_by_premove(game_.m_board, bestMove_2):
                            make_move(game_.m_board, bestMove_1, Defines.WHITE)
                            print_board(game_.m_board)

                            print("---- Fin partida: Gana ", idx_k)
                            k[0] += 10000
                            j[0] -= 2000

                            break
            
                        print_board(game_.m_board)
                        
                        # Turno de WHITE
                        j[1].before_search(game_.m_board, Defines.WHITE, 2, bestMove_2)
                        score_1 += j[1].alpha_beta_search(2, Defines.MININT, Defines.MAXINT, Defines.WHITE, bestMove_1, bestMove_1)
                        make_move(game_.m_board, bestMove_1, Defines.WHITE)
                        
                        # Gana BLACK
                        if is_win_by_premove(game_.m_board, bestMove_1):
                            make_move(game_.m_board, bestMove_2, Defines.BLACK)
                            print_board(game_.m_board)

                            print("---- Fin partida: Gana ", idx_j)
                            j[0] += 10000
                            k[0] -= 2000

                            break

                        print_board(game_.m_board)

                    
                    # Suma de los scores
                    j[0] += score_1                           
                    k[0] += score_2

                    # Satura a 0
                    j[0] = max(0, score_1)
                    k[0] = max(0, score_2)

                    # Reinicia los agentes
                    k[1].restart()
                    j[1].restart()

                # Reinicia el tablero de juego
                game_.init_game()
                idx_k += 1

        
        print("\nFin de epoca ", i)
        print("")

        # Busca el mejor motor por su puntuación
        max_engine = search_engine[0]
        fitness_scores = []

        for p in search_engine:
            fitness_scores.append(p[0])

            if p[0] > max_engine[0]:
                max_engine = p 

        max_score = max_engine[0]
        fitness_scores.sort(reverse=True)

        print("Search engine: ", search_engine)
        print("Fitness Scores: ", fitness_scores)
        print("")
        print("Max Engine: ", max_engine)
        print("Max Params: ", max_engine[1].get_params())
        print("")

        # Ordena los motores según su putnuación
        parents = []
        for w in fitness_scores:
            for u in search_engine:
                if u[0] == w:
                    parents.append(u)
                    break
        
        # Selecciona los mejores motores
        num_parents = int(N_pop * 0.5)
        parents = parents[:num_parents]

        print("New parents: ", parents)
        print("")

        new_population = []

        # Genera los hijos a partir de los padres
        while len(new_population) < N_pop - num_parents:

            # Selección de padres
            parent1, parent2 = random.sample(parents, 2)
            print("Parent 1: ", parent1[1].get_params())
            print("Parent 2: ", parent2[1].get_params())
            

            # Cruce por punto aleatorio
            crossover_point = random.randint(1, N_params - 1)
            child = SearchEngine()
            
            child_params = parent1[1].get_params()[:crossover_point] + parent2[1].get_params()[crossover_point:]
            child.set_params(child_params)

            # Mutación
            if random.random() < mutation_limit:
                mutation_point = random.randint(0, N_params - 1)
                
                mut_params = gen_random_vector()

                new_child = child.get_params()[:mutation_point] + mut_params[mutation_point:]

                child.set_params(new_child)

            new_population.append([0.0, child])
            
            print("New child: ", child.get_params())
            print("\n\n")
        
        # Combina padres con hijos para obtener la nueva poblacion
        search_engine = parents + new_population
        print("New population: ", search_engine)
        print("")

        # for t in search_engine:
        #     t[0] = int(t[0] / max_score * 100)

        # # Seleccion
        # for _ in range(0, N_pop):
        #     n = [i for i in range(0, len(search_engine)) for j in range(0, int(search_engine[i][0]))]
            

        #     rand = np.random.choice(n, (1,2), replace=False)[0]
        #     print(rand)

        #     new_engine = SearchEngine()
        #     new_params_best = [0 for _ in range(0, N_params)]

        #     relative_best = None
        #     relative_worst = None

        #     if search_engine[rand[0]][0] > search_engine[rand[1]][0]:
        #         relative_best = search_engine[rand[0]]
        #         relative_worst = search_engine[rand[1]]
        #     else:
        #         relative_best = search_engine[rand[1]]
        #         relative_worst = search_engine[rand[0]]


        #     relative_best_params= relative_best[1].get_params()
        #     relative_worst_params = relative_worst[1].get_params()

        #     print("Relative best: ", relative_best_params)
        #     print("Relative worst: ", relative_worst_params)
        #     print("")
            
        #     a = 1

        #     if max_score != 0:
        #         relative_worst[0] = max(0, relative_worst[0])
        #         relative_best[0] = max(0, relative_best[0])
        #         a = relative_best[0] / max_score / 2
        #         b = relative_worst[0] / max_score / 2

        #     print("A: ", a)

        #     # Cruce y mutación
        #     for m in range(0, N_params):
        #         new_params_best[m] = abs(relative_best_params[m] * a + relative_worst_params[m] * b)

        #         new_params_best[m] = np.random.normal(loc = new_params_best[m], scale=std_mutation)

        #         if np.random.rand() < mutation_limit:
        #             print("mutacion best!")
                    
        #             params = gen_random_vector()

        #             search_engine_.set_params(params)


        #     print("New params best: ", new_params_best)
        #     print("")

        #     new_engine.set_params(new_params_best)  
        #     new_population.append([0, new_engine])


        # print("New population: ", new_population)
        # print("")
        
        # Actualizar poblacion
        search_engine = new_population

            
            




    # game_engine.run()
