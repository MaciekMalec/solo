import random

def arabic_to_roman(number):
    z=len(number)
    # print('the number has ', z, ' digits.') - to debug
    if int(number) in range(1,4000):
        digits=str(number)
        romans='I','X','C','M','V','L','D',' '
        roman=[]
        for i,dig in enumerate(digits):
            x=z-i-1
            y=z-i+3
            # print(f"{dig} - i:{i} - z:{z} - x:{x} - y{y} - r1:{romans[x]} - r2:{romans[y]}") - to debug
            if int(dig)<4 and int(dig)>0:
                for b in range(0,int(dig)):
                    roman.append(romans[x])
            elif int(dig)==4:
                roman.append(romans[x])
                roman.append(romans[y])
            elif int(dig)>4 and int(dig)<9:
                b=5
                roman.append(romans[y])
                while int(dig)>b:
                    roman.append(romans[x])
                    b+=1
            elif int(dig)==9:
                roman.append(romans[x])
                roman.append(romans[x+1])
        rom_number=''.join(roman)
    else:
        rom_number='Can\'t do that'
    
    return rom_number

def roman_to_arabic(roman_number):
    roman=roman_number.upper()
    number=0
    to_add=[]
    error=False
    romans={
        'I':1,
        'X':10,
        'C':100,
        'M':1000,
        'V':5,
        'L':50,
        'D':500
    }
    for i in range(0,len(roman)):
        to_add.append(romans[roman[i]])
        number+=to_add[i]
        if i>0:
            if to_add[i] in [5*to_add[i-1],10*to_add[i-1]]:
                number-=to_add[i-1]*2
            elif to_add[i]>to_add[i-1]:
                error=True
    if error:
        number=('Wrong notation!')
    return number

inp='0'
while inp:
    inp=input('\nType a positive number smaller than 4000\neither in roman or arabic notation or nothing to quit :')
    if inp.isdigit():
        out=arabic_to_roman(inp)
    else:
        out=roman_to_arabic(inp)
    print('\n',inp.upper(), ' -> ', out)
