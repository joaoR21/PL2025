# TPC1

Pretende-se um programa em python que some todas as sequências de dígitos que encontre num texto.
Sempre que encontre a string `on`, em qualquer combinação de maiúsculas e minúsculas, o
comportamento é desligado.
Sempre que encontre a string `off`, em qualquer combinação de maiúsculas e minúsculas, o
comportamento é desligado.
Sempre que encontrar o caráter `=`, o resultado da soma é colocado na saída.

O programa deve ser desenvolvido sem recorrer a expressões regulares.

## Resultados
O código da solução pode ser encontrado no seguinte ficheiro: 
[somador.py](https://github.com/joaoR21/PL2025/blob/main/TPC1/somador.py)

Os resultados do programa foram confirmados recorrendo a alguns exemplos.
Por exemplo, a string...

```
-12on34off56=on78?9off00on11=
```

produz o seguinte resultado:

```
22
120
```
