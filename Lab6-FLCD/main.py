from Parser import Parser

def show_menu():
    lr0 = Parser("files/g1.txt")

    print("""
    1 - print terminals
    2 - print non terminals
    3 - print productions
    4 - print productions for a given non terminal
    5 - canonical collection
    6 - exit
    """)
    menu = {
        "1": lambda: lr0.print_data(1),
        "2": lambda: lr0.print_data(2),
        "3": lambda: lr0.print_data(3),
        "4": lambda: lr0.print_production(input("Please give a non terminal:")),
        "5": lambda: lr0.canonical_collection(),
        "6": exit
    }
    while True:
        option = input("Choose an option:")
        if option in menu:
            menu[option]()
        else:
            print("Wrong option")


if __name__ == '__main__':
    show_menu()