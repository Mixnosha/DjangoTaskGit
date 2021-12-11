def morsecod (word):
    morse = {
    'a' : '.-', 'b' : '-...', 'c' : '-.-.', 
    'd' : '-..', 'e' : '.', 'f' : '..-.', 
    'g' : '--.', 'h' : '....', 'i' : '..', 
    'j' : '.---', 'k' : '-.-', 'l' : '.-..', 
    'm' : '--', 'n' : '-.', 'o' : '---', 'p' : '.--.',
    'q' : '--.-', 'r' : '.-.', 's' : '...', 't' : '-',
    'u' : '..-', 'v' : '...-', 'w' : '.--', 'x' : '-..-',
    'y' : '-.--', 'z' : '--..', '.' : '.-.-.-',
    '?' : '..--..', ',' : '--..--', ' ' : '/'
    }
    for i in word:
        if i not in morse:
            print ("no character data")
        else:
            print (morse[i] , end='  ')

#morsecod(input('Write word: '))

def fibonachi ():
    num1 = 1;
    num2 = 1;
    print (num1 , num2 , sep='  ', end='  ')
    for i in range(99):
        print(num1 + num2, end='  ')    
        num1 , num2 = num2 , num2 + num1;
        
#fibonachi();

def combination (list1 , list2):
    reslist = []
    for i in range(len(list1)):
        reslist.append(list1[i])
        reslist.append(list2[i])  
    return reslist

ls = [1 , 2 , 3, 4 ]
ls2 = ["a" , 'b' , 'c']

#print  (combination(ls , ls2))

def combo (list1 , list2):
    reslist = []
    if (len(list1) == len(list2)):
        for i in range(len(list1)):
            reslist.append(list1[i])
            reslist.append(list2[i])  
        return reslist
    elif (len(list1) > len(list2)):
        for i in range(len(list2)):
            reslist.append(list1[i])
            reslist.append(list2[i])
        for i in range(len(list2) , len(list1)):
            reslist.append(list1[i])
        return reslist
    else:
        for i in range(len(list1)):
            reslist.append(list1[i])
            reslist.append(list2[i])
        
        for i in range(len(list1) , len(list2)):
            reslist.append(list2[i])
        return reslist
    

#print(combo(ls , ls2))

def odd_elements (list1):
    odd = []
    for i in range(len(list1)):
        if i % 2 == 0:
            odd.append(list1[i])
    return odd

#print (odd_elements(ls))
ms = ['mas' , 'abc']
def reverse (list1):
    r_list = list1[::-1]
    for i , value  in enumerate(r_list):
        r_list[i] = value[::-1]
    return r_list
print (reverse(ms))      

def reverse2 (list1):
    return list1[::-1]

#print (reverse2(ms))


