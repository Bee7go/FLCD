from tabulate import tabulate

# input definition
# first line the initial nonTerminal
# second line the terminals with spaces between elements
# third line the nonTerminals
# next lines the productions
ERROR = "ERROR"
ACCEPT = "ACCEPT"
PROCESSING = "PROCESSING"


class Lr0Parser:

    def __init__(self, file_path):
        file_program = self.read_program(file_path)
        self.terminals = file_program[0]
        self.nonTerminals = file_program[1]
        self.productions = {}
        self.transactions = file_program[2:]
        for elements in self.transactions:
            if elements[0] in self.productions:
                self.productions[elements[0]].append(elements[1:])
            else:
                self.productions[elements[0]] = [elements[1:]]
        self.data = [self.terminals, self.nonTerminals, self.productions]
        dotted = self.dotMaker()

        self.initial_closure = {"S'": [dotted["S'"][0]]}
        self.closure(self.initial_closure, dotted["S'"][0])


    def dotMaker(self):
        self.dottedproductions = {'S\'': [['.', 'S']]}
        for nonTerminal in self.productions:
            self.dottedproductions[nonTerminal] = []
            for way in self.productions[nonTerminal]:
                self.dottedproductions[nonTerminal].append(["."] + way)

        print("dottedProduction: ", self.dottedproductions)
        return self.dottedproductions


    def closure(self, closure_map, transition_value):
        dot_index = transition_value.index(".")
        transitions_map = self.dottedproductions
        if dot_index + 1 == len(transition_value):
            return
        after_dot = transition_value[dot_index + 1]
        if after_dot in self.nonTerminals:
            non_terminal = after_dot
            if non_terminal not in closure_map:
                print("closure_map: ", closure_map)
                print("non_terminal: ", non_terminal)
                closure_map[non_terminal] = transitions_map[non_terminal]
                print("closure_map: ", closure_map)

            else:
                print("else closure_map: ", closure_map)
                print("else non_terminal: ", non_terminal)
                closure_map[non_terminal] += transitions_map[non_terminal]
                print("else closure_map: ", closure_map)

            for transition in transitions_map[non_terminal]:
                self.closure(closure_map, transition)


    @staticmethod
    def shiftable(transition):
        dot_index = transition.index(".")
        if len(transition) > dot_index + 1:
            return True
        return False


    @staticmethod
    def shift_dot(transition):
        transition = transition[:]
        dot_index = transition.index(".")
        if not Lr0Parser.shiftable(transition):
            raise Exception("Should I shift it back ?")
        if len(transition) > dot_index + 2:
            remainder = transition[dot_index + 2:]
        else:
            remainder = []
        transition = transition[:dot_index] + [transition[dot_index + 1]] + ["."] + remainder
        return transition


    def canonical_collection(self):
        self.actions_and_goto_by_state_id = {}
        self.queue = [{
            "state": self.initial_closure,
        }]
        self.states = []
        self.state_parents = {}
        while len(self.queue) > 0:
            self.goto_all(**self.queue.pop(0))
        reduced = self.get_reduced()
        for k in reduced:
            red_k = list(reduced[k].keys())
            if red_k[0] != "S'":
                trans = red_k + reduced[k][red_k[0]][0][:-1]
                reduce_index = self.transactions.index(trans) + 1
                self.actions_and_goto_by_state_id[k] = {terminal: f"r{reduce_index}" for terminal in self.terminals}
                self.actions_and_goto_by_state_id[k]["$"] = f"r{reduce_index}"
            else:
                self.actions_and_goto_by_state_id[k] = {"$": "accept"}
        del self.state_parents[0]
        for key in self.state_parents:
            parent = self.state_parents[key]
            if parent["parent_index"] in self.actions_and_goto_by_state_id:
                self.actions_and_goto_by_state_id[parent["parent_index"]][parent["before_dot"]] = key
            else:
                self.actions_and_goto_by_state_id[parent["parent_index"]] = {parent["before_dot"]: key}
        table = {f"S{index}": self.actions_and_goto_by_state_id[index] for index in range(len(self.states))}
        self.print_table(table)



    def goto_all(self, state, parent=-1, parent_key="-1"):
        if state not in self.states:
            self.states.append(state)
            index = len(self.states) - 1
            self.state_parents[index] = {
                "parent_index": parent,
                "before_dot": parent_key
            }
            self.print_dict(state, f"state {index}")
            for key in state:
                for transition_value in state[key]:
                    if self.shiftable(transition_value):
                        self.goto_one(key, transition_value, index)
        else:
            if parent in self.actions_and_goto_by_state_id:
                self.actions_and_goto_by_state_id[parent][parent_key] = self.states.index(state)
            else:
                self.actions_and_goto_by_state_id[parent] = {parent_key: self.states.index(state)}


    def goto_one(self, key, transition_value, parent=-1):
        shifted_transition = self.shift_dot(transition_value)
        closure_map = {key: [shifted_transition]}
        self.closure(closure_map, shifted_transition)
        self.queue.append({
            "state": closure_map,
            "parent": parent,
            "parent_key": shifted_transition[shifted_transition.index(".") - 1]
        })


    def get_reduced(self):
        self.reduced = {}
        for state in self.states:
            state_key = list(state.keys())[0]
            if len(state[state_key]) and len(state[state_key][0]) \
                    and state[state_key][0][-1] == ".":
                if len(state) > 1 or len(state[state_key]) > 1:
                    self.conflict(state)
                self.reduced[self.states.index(state)] = state
        return self.reduced


    def conflict(self, state):
        transitions = []
        state_index = self.states.index(state)
        for key in state:
            for transition in state[key]:
                transitions.append(transition)
        conflicted = None
        for transition in transitions:
            index = transition.index(".")
            if index == len(transition) - 1:
                continue
            for node in transition[index + 1:]:
                if node in self.terminals:
                    conflicted = transition[index]
                print(f"Conflict at state {state_index}. {state} at column {conflicted}")
                exit(1)
        raise Exception(f"Conflict at state {state_index}. {state} unknwon column")


    @staticmethod
    def read_program(file_path):
        file1 = open(file_path, 'r')
        lines = file1.readlines()
        file1.close()
        return [line.replace("\n", "").replace("\t", "").split(" ") for line in lines]


    @staticmethod
    def print_dict(hashmap, message=None, deepness=""):
        if message is not None:
            print(deepness + message)
        for key in hashmap:
            print(f"{deepness}{key} : {hashmap[key]}")



    def print_table(self, hashmap):
        headers = ["State"] + ["Action " + term for term in self.terminals] + ["Action $"] + ["Go to " + nterm for nterm
                                                                                              in self.nonTerminals]
        keys = self.terminals + ["$"] + self.nonTerminals
        rows = []
        for state_key in hashmap:
            row = [state_key] + [hashmap[state_key][key] if key in hashmap[state_key] else "" for key in keys]
            rows.append(row)
        tab = tabulate(rows, headers, tablefmt="pretty")
        file_tab = tabulate(rows, headers, tablefmt="html")
        print(tab)
        self.write_to_file(file_tab, "canonical_table.html")

    def write_to_file(self, content, name):
        with open(name, 'w') as out_file:
            out_file.write(content)



    def print_data(self, index=-1):
        if index == -1:
            exit()
        else:
            print(self.data[index - 1])


    def print_production(self, non_terminal):
        data = self.data[2]
        if non_terminal in data:
            for row in data[non_terminal]:
                print(f"{non_terminal} -> {row}")
        else:
            print("Wrong non terminal!")


    def parse_string(self, s):
        self.canonical_collection()
        print(s)
        string = s + "$"
        queue = [c for c in string]
        working_stack = ["$", 0]
        output_band = []
        status = PROCESSING  # or ACCEPT or ERROR
        rows = [[self.list_to_string(working_stack), self.list_to_string(queue),
                 self.list_to_string(output_band, ",")]]
        while status == PROCESSING:
            pop = queue.pop(0) if queue[0] != "$" else "$"

            last_working_stack_element = working_stack[-1]
            intersection = self.actions_and_goto_by_state_id[last_working_stack_element][pop]
            if intersection == "accept":
                status = ACCEPT
                break
            if type(intersection) == int:
                # this means that the intersection is a shift
                working_stack.append(pop)
                working_stack.append(intersection)
            else:
                # this means that the intersection is a reduce
                production_index = int(intersection.replace("r", ""))
                output_band.insert(0, production_index)
                reduce_transition = self.transactions[production_index - 1]
                non_terminal = reduce_transition[0]
                replaceable_string = reduce_transition[1:]
                working_stack_length = len(working_stack)
                replaceable_string_length = len(replaceable_string)
                without_final_partition = working_stack[:working_stack_length - (2 * replaceable_string_length)]
                working_stack = without_final_partition
                state_index = working_stack[-1]
                working_stack.append(non_terminal)
                goto = self.actions_and_goto_by_state_id[state_index][non_terminal]
                working_stack.append(goto)
            rows.append([self.list_to_string(working_stack), self.list_to_string(queue),
                         self.list_to_string(output_band, ",")])
        if status == ACCEPT:
            print(output_band)
            rows.append(["accepted", self.list_to_string(queue),
                         self.list_to_string(output_band, ",")])
            print("Accepted")
            headers = ["Work stack", "Input stack", "Output band"]
            print(tabulate(rows, headers, tablefmt="pretty"))
            file_tab = tabulate(rows, headers, tablefmt="html")
            self.write_to_file(file_tab, "parsed_table.html")
        if status == ERROR:
            print("Error in string")

    @staticmethod
    def list_to_string(l, joiner=""):
        if len(l) == 0:
            return "empty"
        return joiner.join([str(element) for element in l])


def show_menu():
    lr0 = Lr0Parser("files/g1.txt")

    print("""
    1 - print terminals
    2 - print non terminals
    3 - print productions
    4 - print productions for a given non terminal
    5 - canonical collection
    6 - parse string
    7 - exit
    """)
    menu = {
        "1": lambda: lr0.print_data(1),
        "2": lambda: lr0.print_data(2),
        "3": lambda: lr0.print_data(3),
        "4": lambda: lr0.print_production(input("Please give a non terminal:")),
        "5": lambda: lr0.canonical_collection(),
        "6": lambda: lr0.parse_string(input("Please give a string:")),
        "7": exit
    }
    while True:
        option = input("Choose an option:")
        if option in menu:
            menu[option]()
        else:
            print("Wrong option")


if __name__ == '__main__':
    show_menu()