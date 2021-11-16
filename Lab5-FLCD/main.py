from Parser import Parser


def display():
    print('Press 1 for displaying the entire grammar')
    print('Press 2 for displaying the non-terminals')
    print('Press 3 for displaying the terminals')
    print('Press 4 for displaying start symbol')
    print('Press 5 for displaying for ALL productions')
    print('Press 6 for displaying for specific production')

    print('Press 0 for exit')


def main():
    global inputUser
    parser = Parser()
    parser.readFile('files/g1.txt')
    try:
        parser.checkCFG()
    except Exception as ex:
        print(ex)
        return
    while True:
        display()
        try:
            inputUser = int(input())
        except Exception:
            print('It`s not a valid choice')
        if inputUser == 0:
            break
        if inputUser == 1:
            print(parser)
        if inputUser == 2:
            print(parser.nonTerminals)
        if inputUser == 3:
            print(parser.terminals)
        if inputUser == 4:
            print(parser.startingSymbol)
        if inputUser == 5:
            for key in parser.productions.keys():
                print(str(key) + "->" + str(parser.productions[key]))
        if inputUser == 6:
            nn = input()
            try:
                print(parser.getSpecificProduction(nn))
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    main()