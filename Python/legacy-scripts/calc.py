def add(number):
    global result
    result += number
    return print (f'Actual number is {result}')

def sub(number):
    global result
    result -= number
    return print (f'Actual number is {result}')

def div(number):
    global result
    if number == 0:
        print ('Cannot division by zero!')
        global x 
        x = -1
    else:
        result /= number 
        return print (f'Actual number is {result}')

def multi(number):
    global result
    result *= number
    return print (f'Actual number is {result}')

def menu():
    while True:
        print('1. Add: ')
        print('2. Sub: ')
        print('3. Div: ')
        print('4. Multi: ')
        print('q QUIT: ')
        switch = input('Input operation: ')
        if switch == 'q':
            print('Exiting...')
            break
        if switch not in {'1', '2', '3', '4'}:
            print('Invalid choice, try again')
            continue
        try:
            number = float(input('Input number: '))
        except ValueError:
            print('Invaild input, please enter a valid number')
            continue

        if switch == '1':
            add(number)
        elif switch == '2':
            sub(number)
        elif switch == '3':
            div(number)
        elif switch == '4':
            multi(number)

if __name__ == "__main__":
    try:
        result = float(input('Input initial number: '))
        menu()
    except ValueError:
        print('Invalid input, exiting program.')