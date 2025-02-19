class Obra:
    def __init__(self, nome, desc, anoCriacao, periodo, compositor, duracao, _id):
        self.nome = nome
        self.desc = desc
        self.anoCriacao = anoCriacao
        self.periodo = periodo
        self.compositor = compositor
        self.duracao = duracao
        self._id = _id


def parse_line(line):
    columns = []
    temp = ""
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ';' and not in_quotes:
            columns.append(temp.strip())
            temp = ""
        else:
            temp += char
    columns.append(temp.strip())
    return columns

def load_csv(filepath):
    results = []
    buffer = ""
    with open(filepath,'r',encoding='utf-8') as file:
        content = file.readlines()
        header = content[0].strip()
        num_columns = len(parse_line(header))  # determina o nr. de colunas a partir do header

        for line in content[1:]:  # ignorar o header
            line = line.strip()
            if not line:
                continue
            buffer += line
            columns = parse_line(buffer.strip())
            if len(columns) == num_columns:  # verificar o nr. correto de colunas
                results.append(Obra(*columns))
                buffer = ""

    return results

def inverter_nome(comp):
    if ',' in comp:
        last,first = comp.split(',')
        return f'{first.strip()} {last.strip()}'
    return comp


def compositores_ordem(obras):
    return sorted(set(inverter_nome(obra.compositor) for obra in obras))

def obras_period(obras):
    return { p : sum(1 for obra in obras if obra.periodo == p)
            for p in set(obra.periodo for obra in obras) }

def period_title_obras(obras):
    titles = {}
    for obra in obras:
        titles.setdefault(obra.periodo,[]).append(obra.nome)

    for period in titles:
        titles[period].sort()

    return titles



def main():
    filepath = "obras.csv"
    obras = load_csv(filepath)
    while True:
        print()
        print("=== MENU ===")
        print("1. Compositores por ordem alfabética")
        print("2. Número de obras por periodo")
        print("3. Obras por período")
        print("0. Sair")

        choice = input("Insira a opçãO: ")

        if choice == "1":
            comps = compositores_ordem(obras)
            print()
            print("=== COMPOSITORES ===")
            for comp in comps:
                print(comp)
        elif choice == "2":
            periods = obras_period(obras)
            print()
            print("=== NÚMERO DE OBRAS POR PERÍODO ===")
            for period in periods.keys():
                print(f"{period.upper()}:")
                print(periods[period])
        elif choice == "3":
            titles = period_title_obras(obras)
            print()
            print("=== OBRAS POR PERÍODO ===")
            for title in titles.keys():
                print()
                print(f"{title.upper()}:")
                for obra in titles[title]:
                    print(obra)
        elif choice == "0":
            print("A sair...")
            break
        else:
            print("Escolha inváilda.")

if __name__ == "__main__":
    main()

