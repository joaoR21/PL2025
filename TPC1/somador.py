import sys

DIGITS = '0123456789'

def somador(l):
    is_ON = True
    soma = 0
    i = 0
    length = len(l)

    while i < length:
        valor = 0
        sinal = 1

        if l[i] == '-':
            sinal = -1
            i += 1

        if l[i] in DIGITS:
            while i < length and l[i] in DIGITS:
                valor = valor * 10 + int(l[i])
                i += 1
            valor *= sinal
            if is_ON:
                soma += valor
        elif l[i:i+2] == 'on':
            is_ON = True
            i += 2
        elif l[i:i+3] == 'off':
            is_ON = False
            i += 3
        elif l[i] == '=':
            print(soma)
            i += 1
        else:
            i += 1

def main():
    for line in sys.stdin:
        somador(line.lower())

if __name__ == '__main__':
    main()