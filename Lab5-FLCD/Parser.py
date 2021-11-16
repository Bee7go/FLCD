class Parser:
    def __init__(self):
        self.nonTerminals = []
        self.terminals = []
        self.startingSymbol = ""
        self.productions = {}

    def readFile(self, fileName):
        with open(fileName, 'r') as f:
            self.nonTerminals = f.readline().strip().split(' ')
            self.terminals = f.readline().strip().split(' ')
            self.startingSymbol = f.readline().strip().split(' ')[0]
            for line in f:
                all = line.split('-')
                key = all[0].strip()
                values = all[1].split('|')
                self.productions[key] = []
                for val in values:
                    mini_list = []
                    for v in val.strip().split(' '):
                        mini_list.append(v)
                    self.productions[key].append(mini_list)

    # check context free grammar
    def checkCFG(self):
        # validate starting symbol
        if self.startingSymbol not in self.nonTerminals:
            raise Exception('Invalid start symbol: ' + str(self.startingSymbol) + ' not found in not-terminals list.')

        # validate productions
        for key, vals in self.productions.items():
            if key not in self.nonTerminals:
                raise Exception('Invalid production: ' + str(key) + ' not found in not-terminals list.')
            for elem in vals:
                for el in elem:
                    if el not in self.nonTerminals and el not in self.terminals:
                        raise Exception('Invalid production: ' + el + ' not found in terminals or non-terminals')

    # returns a specific production for the given nonTerminal
    def getSpecificProduction(self, nonTerminal):
        if nonTerminal in self.nonTerminals:
            return self.productions[nonTerminal]
        else:
            raise Exception('Invalid non-terminal: ' + nonTerminal + ' not found in not-terminals list.')

    def __str__(self) -> str:
        string = ""
        string += "Non-terminals: " + str(self.nonTerminals) + "\n"
        string += "Terminals: " + str(self.terminals) + "\n"
        string += "Start symbol: " + str(self.startingSymbol) + "\n"
        for key in self.productions.keys():
            string += str(key) + "->" + str(self.productions[key]) + "\n"
        return string
