# This is my attempt to make a mahh-jong game (the riichi variant)
# It is the standard mode to play by myself from time to time for start
# Maybe later will try to make a multiplayer mode



import random

def make_tiles():
    tile_list=[]
    tile_types={
        "White Dragon":'B ',
        "Green Dragon":'F ',
        "Red   Dragon":'C ',
        "East  Wind":'E ',
        "South Wind":'S ',
        "West  Wind":'W ',
        "North Wind":'N '
    }
    for j,k in {'Man':'$','Pin':'@','Sou':'#'}.items():
        for i in range(9):
            tile_types[' '.join([str(i+1),j])]=''.join([k,str(i+1)])
    for tile in tile_types.keys():
        for i in range(4):
            tile_list.append(tile_types[tile])
    print('There are: ',len(tile_list), 'tiles, and ',len(tile_types), 'types.')
    return tile_list, tile_types

def draw_tile(tile_list,hand):
    i=random.randrange(len(tile_list))
    hand.append(tile_list[i])
    del tile_list[i]
    return tile_list, hand

def tile_show(hand):
    print('+-+ '*len(hand))
    for tile in hand:
        print(f'|{tile[1]}|',end=' ')
    print('')
    for tile in hand:
        print(f'|{tile[0]}|',end=' ')
    print('')
    print('+-+ '*len(hand))

def next_tile(tile):
    if tile=='E ':
        next_tile='S '
    elif tile=='S ':
        next_tile='W '
    elif tile=='W ':
        next_tile='N '
    elif tile=='N ':
        next_tile='E '
    elif tile=='B ':
        next_tile='F '
    elif tile=='F ':
        next_tile='C '
    elif tile=='C ':
        next_tile='B '
    else:
        n=int(tile[1])%9+1
        next_tile=tile[0]+str(n)
    return next_tile
            
def check_set(hand):
    sets=[]
    sets1=[]
    kan=False
    hand1=sorted(hand)              
    for tile in hand:
        if tile in hand1
            hand1.remove(tile)
            if tile in hand1:
                hand1.remove(tile)
                if tile in hand1:
                    hand1.remove(tile)
                    if tile in hand1:
                        sets.append(' '.join(['quartet of',tile]))
                        kan=True
                    else:
                        sets.append(' '.join(['triplet of',tile]))
                    for i in range(3):
                        sets1.append(tile)
                else:
                    sets.append(' '.join(['a pair of',tile]))
    hand1=sorted(hand)
    for tile in hand:        
        if tile[0] in ['@','#','$']:
            if int(tile[1])>0:
                a=int(tile[1])
                b=tile[0]
                a1=''.join([b,str(a+1)])
                a2=''.join([b,str(a+2)])
                if a1 in hand1 and a2 in hand1:
                    sets.append(' '.join(['a set of',tile,a1,a2]))
                    sets1.append(tile)
                    sets1.append(a1)
                    sets1.append(a2)
                    hand1.remove(tile)
                    hand1.remove(a1)
                    hand1.remove(a2)
    if len(sets1)==12:
        hand1=sorted(hand)
        for tile in hand1:
            if tile in sets1:
                hand1.remove(tile)
        for tile in hand1:
            hand1.remove(tile)
            if tile in hand1:
                sets=[]
                sets.append(' '.join(['a pair of', tile]))
                for i in range(12):
                    if i%3==0:
                        sets.append('the set of: ')
                    sets.append(sets1[i])
                print('You can win by TSUMO!')
    return sets,kan



lista=[]
typs={}

lista,typs=make_tiles()
for element,value in typs.items():
    print(element, 'is designated as :',value)
print(len(lista))

death_wall=[]
show_wall=[]
for i in range(14):
    draw_tile(lista,death_wall)
    if i==4:
        show_wall.append(death_wall[i])
    elif i<7:
        show_wall.append('  ')

hand1=[]
for i in range(14):
    draw_tile(lista,hand1)

print(len(lista))
# print(death_wall)
ans='1'
discard=[]
hand=sorted(hand1)
while ans!='0':
    tile_show(show_wall)
    tile_show(hand)
    for i in range(len(hand)):
        if i<8:
            print(f' {i+1}  ',end='')
        else:
            print(f' {i+1} ',end='') 
    dora=next_tile(show_wall[4])

    print('\nThe dora is ',dora)
    set_list,kan=check_set(hand)
    if not set_list:
        set_list='nothing'
    print('Your current can have: ',set_list)
    ans=input('Chose tile to discard [either its notation or number]: ')
    if ans:
        if ans in hand:
            to_discard=ans
        elif ans.isdigit():
            if int(ans)>0 and int(ans)<len(hand)+2:
                to_discard=hand[int(ans)-1]
        else:
            for tile in hand:
                if ans in tile:
                    to_discard=tile
    else:
        to_discard=hand[-1]
    if ans in ['0','stop','quit','exit','end','finish']:
        ans='0'
    else:
        y=input(f'Discard {to_discard} [y/n]? ')
    if y in ['','y','Y','yes','Yes','YES']:
        hand.remove(to_discard)
        discard.append(to_discard)
        hand=sorted(hand)
        draw_tile(lista,hand)
    
    
        
