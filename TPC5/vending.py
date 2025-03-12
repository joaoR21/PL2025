import json
import ply.lex as lex
from datetime import datetime
from prettytable import PrettyTable

today = datetime.today()
dt = today.strftime('%Y-%m-%d')

tokens = ('LIST', 'SELECT', 'EXIT', 'COD', 'INSERT', 'MONEY', 'NUM')
t_LIST = r'LISTAR'
t_SELECT = r'SELECIONAR .+'
t_INSERT = r'MOEDA .+'
t_EXIT = r'SAIR'
t_COD = r'[A-Z]\d+'


def t_MONEY(t):
    r'\d+e'
    t.value = float(t.value[:-1])
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = ' \t\n'


def t_error(t):
    print(f'[MÀQ.] InstrUÇão inválida, tente novamente.')
    t.lexer.skip(len(t.value))


lexer = lex.lex()


def load_products():
    try:
        with open("vending.json", "r") as file:
            data = json.load(file)

        table = PrettyTable()
        table.field_names = ["Cód.", "Designação", "Quantidade", "Preço"]

        for item in data["stock"]:
            table.add_row([item["cod"], item["nome"], item["quant"], item["preco"]])

        return data,table
    except FileNotFoundError:
        print("[DEBUG] ficheiro vending.json não encontrado.")
        return None,None


def buy_product(stock, code, saldo):
    for item in stock["stock"]:
        if item["cod"] == code:
            if item["quant"] > 0:
                temp = saldo - item["preco"]
                if temp <= 0:
                    print(f'Saldo insufuciente para satisfazer o seu pedido. Valor = {item["preco"]}e')
                    return saldo
                else:
                    item["quant"] -= 1
                    print(f'Pode retirar o produto dispensado. {item["nome"]}')
                    return temp
            else:
                print(f'[MÁQ.] O produto selecionado já não se encontra disponível.')
                return saldo

    print(f'[MÁQ.] produto com código {code} não encontrado.')
    return saldo


def format_saldo(saldo):
    if saldo >= 1:
        return f"{saldo}e"
    else:
        return f"{int(saldo * 100)}c"


def return_change(saldo):
    if saldo <= 0:
        return "[MÁQ.] Não há troco a devolver."

    coins = [200, 100, 50, 20, 10, 5, 2, 1]
    coin_names = ["2e", "1e", "50c", "20c", "10c", "5c", "2c", "1c"]

    saldo_cents = int(saldo * 100 + 0.5)

    coin_counts = []
    for coin in coins:
        count = saldo_cents // coin
        saldo_cents %= coin
        coin_counts.append(count)

    change_parts = []
    for i in range(len(coins)):
        if coin_counts[i] > 0:
            change_parts.append(f"{coin_counts[i]}X {coin_names[i]}")

    if not change_parts:
        return "[MÁQ.] Não há troco a devolver."

    if len(change_parts) == 1:
        change_text = change_parts[0]
    elif len(change_parts) == 2:
        change_text = f"{change_parts[0]} e {change_parts[1]}"
    else:
        change_text = ", ".join(change_parts[:-1]) + f" e {change_parts[-1]}"

    return f"[MÁQ.] Pode retirar o troco. {change_text}."


def machine():
    stock,table = load_products()

    print(f'[MÁQ.] {dt}, stock carregado, estado atualizado')
    print('[MÁQ.] Bom dia! Estou disponível para atender ao seu pedido')

    saldo = 0.0
    while True:
        try:
            inst = input('>>> ')
            lexer.input(inst)
            token = lexer.token()

            if not token:
                continue

            if token.type == 'EXIT':
                print(return_change(saldo))
                print('[MÀQ.] Até à próxima!')
                break
            elif token.type == 'LIST':
                print(table)
            elif token.type == 'SELECT':
                code = inst.split('SELECIONAR ')[1].strip()
                saldo = buy_product(stock, code, saldo)
                print(f'Saldo = {format_saldo(saldo)}')
            elif token.type == 'INSERT':
                try:
                    valor_str = inst.split('MOEDA ')[1].strip()
                    if valor_str.endswith('c'):
                        valor = float(valor_str[:-1]) / 100
                    else:
                        valor = float(valor_str.replace('e', ''))

                    saldo += valor
                    print(f'[MÁQ.] Saldo = {format_saldo(saldo)}')
                except (ValueError, IndexError):
                    print('[MÀQ.] Valor inválido.')
        except Exception:
            print('[MÀQ.] Ocorreu um erro. Tente novamente.')


if __name__ == '__main__':
    machine()