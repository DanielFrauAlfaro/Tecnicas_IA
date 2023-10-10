from defines import *
import itertools

def print_arr(arr):
    for i in range(0,len(arr)):
        for j in range(0, len(arr)):
            print(arr[i][j], " ", end="")
        
        print("")


def threats(arr):
    print_arr(arr)
    ourColor = 'O'
    num_threats = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    

    h_threats = []
    seen_h_threats = set(h_threats)
    
    v_threats = []
    seen_v_threats = set(v_threats)

    d_threats = []
    seen_d_threats = set(d_threats)

    d2_threats = []
    seen_d2_threats = set(d2_threats)

    for i in range(0, len(arr)):
        for j in range(0, len(arr)):
            
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

            x = i
            y = j

            right_e_h = 0
            right_e_v = 0
            right_e_d = [0,0]
            right_e_d2 = [0,0]
            
            
            for k in range(0,6):
            
                # Horizontal
                if y + 6 < 19 and tuple([x,y + k]) not in seen_h_threats:
                    stone = arr[x][y + k]

                    if stone is ourColor:
                        count_h +=  1
                    elif stone is '-':
                        count_e_h += 1

                        right_e_h = y+k

                # # Vertical: está cambiado para que haga [y,x]
                if y + 6 < 19 and tuple([y + k,x]) not in seen_v_threats:
                    stone = arr[y + k][x]

                    if stone is ourColor:
                        count_v +=  1
                    elif stone is '-':
                        count_e_v += 1

                        right_e_v = y + k

                # # Diag
                if y + 6 < 19 and x + 6 < 19  and tuple([x + k,y + k]) not in seen_d_threats:
                    stone = arr[x + k][y + k]

                    if stone is ourColor:
                        count_d +=  1
                    elif stone is '-':
                        count_e_d += 1

                        right_e_d = [x + k,y + k]

                # # Diag 2
                if y - 6 >= 0 and x + 6 < 19  and tuple([x + k,y - k]) not in seen_d2_threats:
                    stone = arr[x + k][y - k]

                    if stone is ourColor:
                        count_d2 +=  1
                        
                    elif stone is '-':
                        count_e_d2 += 1

                        right_e_d2 = [x + k,y - k]
            
            
            if count_h == 4 and count_e_h == 2: 
                #h_threats.append([x,right_e_h])
                seen_h_threats.add(tuple([x,right_e_h]))

                num_threats[0][x] += 1

                
   
            if count_v == 4 and count_e_v == 2:
                #v_threats.append([right_e_v, x])
                seen_v_threats.add(tuple([right_e_v, x]))

                num_threats[1][x] += 1
                
            if count_d == 4 and count_e_d == 2:
                #d_threats.append([right_e_d[0], right_e_d[1]])
                seen_d_threats.add(tuple([right_e_d[0], right_e_d[1]]))
                 
                num_threats[2][right_e_d[1] - right_e_d[0]] += 1
                
                
            if count_d2 == 4 and count_e_d2 == 2:
                #d2_threats.append([right_e_d2[0], right_e_d2[1]])
                seen_d2_threats.add(tuple([right_e_d2[0], right_e_d2[1]]))

                num_threats[3][i + j] += 1

                
        
        # num_threats[0].append(len(h_threats))
        # num_threats[1].insert(len(v_threats), 0)
        # num_threats[2].append(len(d_threats))
    
    print(num_threats[0])
    print("")
    print(num_threats[1])
    print("")
    print(num_threats[2])
    print("")
    print(num_threats[3])

    score = 0

    for (i, j, k, l) in itertools.zip_longest(num_threats[0], num_threats[1], num_threats[2], num_threats[3]):
        if i is not None and i != 0:
            score += i**i
        
        if j is not None and j != 0:
            score += j**j

        if k is not None and k != 0:
            score += k**k

        if l is not None and l != 0:
            score += l**l
            

    print(score)

    return len(h_threats) + len(v_threats) + len(d_threats)



arr = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', '-', 'O', '-', '-', '-', '-', '-', 'O', 'O', 'O', 'O', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', 'O', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', 'O', '-', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', 'O', '-', '-', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '*', '-', '-', '-'], 
       ['-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', 'O', '-', '-', '-', '-', '*', '-', '-', '-', 'O', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', 'O', '-', '-', '-', '-', '-', '-', 'O', '-', '-', 'O', '-', '-', '-'], 
       ['-', '-', '-', '-', 'O', '-', '-', '-', '-', 'O', '-', '-', '-', 'O', '-', 'O', '-', '-', '-'], 
       ['-', '-', '-', 'O', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '*', 'O', 'O', 'O', 'O', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '*', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'O', '-', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
       ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']] 

threats(arr)