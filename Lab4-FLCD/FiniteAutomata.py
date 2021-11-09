class FiniteAutomata:

    def __init__(self, states, alphabet, q0, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.q0 = q0
        self.final_states = final_states
        self.transitions = transitions

    @staticmethod
    def getLine(line):
        return line.strip().split(' ')[2:]

    @staticmethod
    def readFromFile(fileName):
        with open(fileName) as file:
            states = FiniteAutomata.getLine(file.readline())
            alphabet = FiniteAutomata.getLine(file.readline())
            q0 = FiniteAutomata.getLine(file.readline())[0]
            final_states = FiniteAutomata.getLine(file.readline())
            file.readline()
            transitions = {}
            for line in file:
                src = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[0]
                route = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(', ')[1]
                dst = line.strip().split('->')[1].strip()

                if (src, route) in transitions.keys():
                    # take into consideration duplicates:
                    if dst not in transitions[(src, route)]:
                        transitions[(src, route)].append(dst)
                else:
                    transitions[(src, route)] = [dst]
            return FiniteAutomata(states, alphabet, q0, final_states, transitions)

    def isDfa(self):
        for k in self.transitions.keys():
            if len(self.transitions[k]) > 1:
                return False
        return True

    def isAccepted(self, sequence):
        if self.isDfa():
            current = self.q0
            for symbol in sequence:
                print(current, symbol)
                if (current, symbol) in self.transitions.keys():
                    current = self.transitions[(current, symbol)][0]
                else:
                    return False
            return current in self.final_states
        return False

    def __str__(self):
        return "states = { " + ', '.join(self.states) + " }\n" \
                                              "alphabet = { " + ', '.join(self.alphabet) + " }\n" \
                                                                             "q0 = { " + self.q0 + " }\n" \
                                                                                                   "final_states = { " + ', '.join(
            self.final_states) + " }\n" \
                      "transitions = { " + str(self.transitions) + " } "