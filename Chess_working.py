# Chess version 1
# Implemented: Chess board and moves
    # Chess board is 8x8 by default, but can be larger or smaller.
    # starting positions are set for 8x8 standard chess game
    # there is code ready to modify the figures but in alpha. not implemented into program yet
    # there is a condition to check if there is a figure to move (can't move empty space)
# next to do
    # conditions to move a specific figures
    # conditions to make white move, then black move
    # check! condition
    # roshade exception
    # timer
    # list of moves
    # ability to undo a move
# Created by Maciek Malec



def chess_board(LENGTH,WIDTH,POSITIONS):
    import string
    if len(POSITIONS)==WIDTH:
        for line in POSITIONS:
            if len(line)==LENGTH:
                error=False
            else:
                error=True
    else:
        error=True
    if error:
        print('error in chess board formating')
    else:
        black='    ',' ','    '
        white='+--+','|','+--+'
        w=0
        print('\n   ',end='')
        li='='*4*WIDTH
        for space in range(WIDTH):
            print(f'  {string.ascii_uppercase[space]} ',end='')
        print(f'\n  #{li}#',end='\n')
        for line in range(LENGTH):
            for i in range(3):
                if i==1:
                    print(line+1, end=' I')
                else:
                    print(' ', end=' I')
                for space in range(WIDTH):
                    if i<1 or i>1:
                        if w==0:
                            print(black[i], end='')
                        else:
                            print(white[i], end='')
                    else:
                        if w==0:        
                            print(f'{black[i]}{POSITIONS[line][space]}{black[i]}',end='')
                        else:
                            print(f'{white[i]}{POSITIONS[line][space]}{white[i]}',end='')
                    w=(w+1)%2
                print('I',end='\n')    
            
            w=(w+1)%2
        print(f'  #{li}#',end='\n')


def chess_figures(figure_types,to_set):
    if len(figure_types)<13:
        figure_types={
            'empty':'  ',
            'white King':' K',
            'white Queen':' Q',
            'white Bishop':' B',
            'white Knight':' N',
            'white Tower':' T',
            'white Pawn':' p',
            'black King':'*K',
            'black Queen':'*Q',
            'black Bishop':'*B',
            'black Knight':'*N',
            'black Tower':'*T',
            'black Pawn':'*p',
        }
    if to_set:
        for figure,value in figure_types:
            print(f'Current {figure} is noted as {value}.',end='')
            new=input(' Type a new notation for this figure (2-characters only): ')
            if len(new)==2:
                figure_types[figure]=new
                print(f'New {figure} now is noted as {new}.')
    else:
        for figure in figure_types:
            print(f'Current {figure} is noted as \"{figure_types[figure]}\".',end='\n')
    return figure_types

def figure_name(notation,figure_types):
    name=list(figure_types.keys())[list(figure_types.values()).index(notation)]
    return name

def line_moves(positions,allowed_spaces,direction,steps,y0,x0):   
    # line moves for tower, bishop and queen in one mode. direction is a set of direction matrices
    moves=[]
    for d in direction:
        for m in range(1,steps):  
            if y0+d[0]*m in range(len(positions)) and x0+d[1]*m in range(len(positions)):
                if positions[y0+d[0]*m][x0+d[1]*m]=='  ':
                    moves.append([y0+d[0]*m,x0+d[1]*m])
                elif positions[y0+d[0]*m][x0+d[1]*m] in allowed_spaces:
                    moves.append([y0+d[0]*m,x0+d[1]*m])
                    break   # stop the loop if there is enemy figure
                else:
                    break   # stop the loop if there is your figure
            else:
                break   # stop the loop if it's outside the board (not necessary)
    return moves

def allowed_moves(positions,figure_types,y0,x0,king):   # king is boolean for check positions
    moves=[]    # list of moves to return
    ymoves=['  ']   # list of space_types available to move with empty space already included
    figure=figure_name(positions[y0][x0],figure_types)
    # figure is the name of the figure from the types which is chosen by its 2$ symbol
    if 'black' in figure:
        for item in figure_types:
            if king or 'white' in item:
                ymoves.append(figure_types[item])
    elif 'white' in figure:
        for item in figure_types:
            if king or 'black' in item:
                ymoves.append(figure_types[item])
    # print(ymoves)         
    if 'King' in figure:    # moves by 1 tile in any direction
        direction=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
        moves=line_moves(positions,ymoves,direction,2,y0,x0)
    if 'Tower' in figure:   # moves horisontally or vertically only and can be blocked
        direction=[[1,0],[0,1],[0,-1],[-1,0]]
        moves=line_moves(positions,ymoves,direction,len(positions),y0,x0)
    if 'Bishop' in figure:  # moves diagonally and can be blocked
        direction=[[1,1],[1,-1],[-1,1],[-1,-1]]
        moves=line_moves(positions,ymoves,direction,len(positions),y0,x0)
    if 'Queen' in figure:
        direction=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
        moves=line_moves(positions,ymoves,direction,len(positions),y0,x0)
    if 'Knight' in figure:
        direction=[[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
        moves=line_moves(positions,ymoves,direction,2,y0,x0)
    if 'Pawn' in figure:
        d=0         # it's the direction coeficient, white go down -> +1, black go up -> -1
        if figure=='white Pawn':
            d=1
        elif figure=='black Pawn':
            d=-1
        if positions[y0+d][x0]=='  ' and king==False:
            moves.append([y0+d,x0])
        if y0==3.5-d*2.5 and positions[y0+d*2][x0]=='  ' and king==False:
            moves.append([y0+2*d,x0])
        for diag in range(2):
            times=1-2*diag
            if x0+times*d in range(len(positions[y0])):
                if positions[y0+d][x0+times*d] in ymoves:
                    if positions[y0+d][x0+times*d]!='  ' or king:
                        moves.append([y0+d,x0+times*d])        
    return moves              

def check_condition(positions,figure_types,turn):
    under_check=False    
    if turn=='white':
        checked='black'
    elif turn=='black':
        checked='white'
    list_of_moves=check_moves(positions,figures,checked,True)[1]
    for move in list_of_moves:
        if figures[' '.join([turn,'King'])]==positions[move[0]][move[1]]:
            under_check=True
    return under_check

def check_moves(positions,figure_types,turn,king):
    import copy
    x,y=[],[]    # starting coordinates of each figure
    lista=[]
    listb=[]
    listc=[]
    for dy in range(len(positions)):  # getting the coordinates from the board
        for dx in range(len(positions[0])):
            if turn in figure_name(positions[dy][dx],figure_types):
                x.append(dx)
                y.append(dy)
    for i in range(len(x)):
        move_list=allowed_moves(positions,figure_types,y[i],x[i],king)
        if len(move_list)>0:
            for item in move_list:
                if king==False:
                    temp=copy.deepcopy(positions)
                    temp[item[0]][item[1]]=temp[y[i]][x[i]]
                    temp[y[i]][x[i]]='  '
                    if check_condition(temp,figure_types,turn)==False:
                        lista.append([y[i],x[i]])
                        listb.append(item)
                    else:
                        listc.append(item)
                else:
                    lista.append([y[i],x[i]])
                    listb.append(item)
    return lista,listb,listc

def move_figure(positions,figure_types,turn,is_check):
    import string
    pickups,putdowns,checks=check_moves(positions,figure_types,turn,False)
    error=True
    if len(putdowns)<1:
        error=False
        is_check_mate=True
    else:
        is_check_mate=False
    while error:
        print(f'It\'s a {turn} turn to move. Input the coordinates of the figure you want to move (e.g. e2 or E2).')
        print('You can input two sets of coordinates-from where to where move (e.g. e2 e4).')
        print('To end this game, type "stop". for full list of available moves type "list".')
        start=input(f'What do you do? ')
        if start=='list':
            move_select=[]
            for i in range(len(pickups)):
                figure=figure_name(positions[pickups[i][0]][pickups[i][1]],figure_types)
                up=''.join([string.ascii_uppercase[pickups[i][1]],str(pickups[i][0]+1)])
                down=''.join([string.ascii_uppercase[putdowns[i][1]],str(putdowns[i][0]+1)])
                move_select.append(' '.join([up,down]))
                print(f'{i+1}- {figure} at {up} {down}',end=' '*(15-len(figure)-len(str(i))))
                if i%5==0:
                    print()
            ans=input(f'\nYou can either select a specific move (by number) or input coordinates: ')
            if ans.isdigit():
                if int(ans)-1 in range(len(move_select)):
                    start=move_select[int(ans)-1]
            else:
                start=ans
        x=[]
        y=[]
        startxy=['0','0',' ','0','0']
        if len(start)==2 or len(start)==5:
            for i in range(len(start)):
                startxy[i]=start[i]
                if startxy[i].upper() in string.ascii_uppercase:
                    x.append(string.ascii_uppercase.index(startxy[i].upper()))
                elif startxy[i]==' ':
                    continue
                elif int(startxy[i])>0:
                    y.append(int(startxy[i])-1)
            print(start[0:2], '-> x=',x,'y=',y)
        if len(x)+len(y)>1 and len(x)==len(y):
            if [y[0],x[0]] in pickups:
                error=False
            else:
                print('Bad selection!')
        if start=='stop':
            error=False
        elif error:
            print('Wrong starting position!')
        else:
            figure=figure_name(positions[y[0]][x[0]],figure_types)
            if turn in figure:
                moves_go=[]
                for i in range(len(putdowns)):
                    if [y[0],x[0]]==pickups[i]:
                        moves_go.append(putdowns[i])
                move_list=[]
                if len(moves_go)>0:
                    for go in moves_go:
                        move_list.append(''.join([string.ascii_uppercase[go[1]],str(go[0]+1)]))
                    if len(x)<2 and len(y)<2:
                        print('Selected figure is ', figure, 'at the position', start)
                        print('Available moves: ',move_list)
                        move=input('put the coordinates where to move: ')
                        if move.upper() in move_list:
                            for i in range(2):
                                if move[i].upper() in string.ascii_uppercase:
                                    x.append(string.ascii_uppercase.index(move[i].upper()))
                                elif int(move[i])>0:
                                    y.append(int(move[i])-1)
                            # print(move,'-> x=',x[1],'y=',y[1])
                        else:
                            print('wrong input!')
                            error=True
                else:
                    print('Can\'t move that figure.')
                    error=True
            else:
                print('Wrong selection!')
                error=True
            if len(x)+len(y)>2 and error==False:
                if [y[1],x[1]] in putdowns:
                    positions[y[1]][x[1]]=positions[y[0]][x[0]]
                    positions[y[0]][x[0]]='  '
                    endxy=''.join([string.ascii_uppercase[x[1]],str(y[1]+1)])
                    print('moving the', figure, 'from position', start[0:2].upper(), 'to position',endxy)
                else:
                    print('Wrong move! Try again.')
                    error=True
    if turn=='white':
        turn='black'
    elif turn=='black':
        turn='white'
    return positions,turn,is_check_mate
    
import string        

figures=chess_figures({},False)    
O=figures['empty']
k=figures['white King']
q=figures['white Queen']
b=figures['white Bishop']
n=figures['white Knight']
t=figures['white Tower']
p=figures['white Pawn']
K=figures['black King']
Q=figures['black Queen']
B=figures['black Bishop']
N=figures['black Knight']
T=figures['black Tower']
P=figures['black Pawn']
    
POSITIONS=[
    [t,n,b,q,k,b,n,t],
    [p,p,O,p,p,p,p,p],
    [O,O,p,O,O,O,O,O],
    [O,O,O,O,O,O,p,O],
    [O,O,O,O,P,q,O,O],
    [O,O,T,O,O,O,O,K],
    [P,P,P,P,P,P,P,P],
    [T,N,B,Q,O,B,N,T]
    ]
         
LENGTH=len(POSITIONS)
WIDTH=len(POSITIONS[0])
move='start'
turn='white'
list_of_figures,list_of_moves,list_of_bad_moves=check_moves(POSITIONS,figures,'black',False)
for i in range(len(list_of_figures)):
    print(list_of_figures[i],list_of_moves[i])
print(list_of_bad_moves)
while move!='stop':
    check_mate=False
    chess_board(LENGTH,WIDTH,POSITIONS)
    under_check=check_condition(POSITIONS,figures,turn)
    if under_check:
        print('Check!')
    POSITIONS,turn,check_mate=move_figure(POSITIONS,figures,turn,under_check)
    if check_mate:
        print('Check Mate!. The',turn,'has won!')
        move='stop'