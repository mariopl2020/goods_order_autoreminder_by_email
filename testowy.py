import builtins

def printuj():
    imie = input()
    nazwa = input()
    return nazwa


def test_printuj():
    input_values = [2, 3]

    def mock_input():
        return input_values.pop(0)

    builtins.input = mock_input
    wynik = printuj()
    return wynik
    # assert wynik == 3


print(test_printuj())