from FiniteAutomata import FiniteAutomata


class Console:

    def __read_fa(self):
        self.fa = FiniteAutomata.readFromFile('files/fa2.in')

    def __display_all(self):
        print(self.fa)

    def __display_states(self):
        print(self.fa.states)

    def __display_alphabet(self):
        print(self.fa.alphabet)

    def __display_transitions(self):
        print(self.fa.transitions)

    def __display_final_states(self):
        print(self.fa.final_states)

    def __dfa(self):
        print(self.fa.isDfa())

    def run(self):
        self.__read_fa()
        commands = {'1': self.__display_all,
                    '2': self.__display_states,
                    '3': self.__display_alphabet,
                    '4': self.__display_transitions,
                    '5': self.__display_final_states,
                    '6': self.__dfa}
        ok = False
        while not ok:
            print("1.Display FA")
            print("2.Display FA States")
            print("3.Display FA Alphabet")
            print("4.Display FA transitions")
            print("5.Display FA final states")
            print("6.Check DFA")
            print(">>")
            cmd = input()
            if cmd in commands.keys():
                commands[cmd]()
            elif cmd == "exit":
                ok = True
            else:
                continue


ui = Console()
ui.run()