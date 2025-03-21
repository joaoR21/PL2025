# TPC6

Pretende-se construir um analisador sintático em *python* que reconheça expressões matemáticas simples, como p.e. `3 + 2 - (3 * 4)`.  
É possível reconhecer as operações de adição, subtração, multiplicação e divisão.
O programa ainda imprime o resultado da expressão, tendo em conta as prioridades das operações (PEMDAS)  
O programa foi concebido recorrendo à biblioteca `ply`, nomeadamente aos módulos `ply.lex` e `ply.yacc`

## Resultados
O código da solução pode ser encontrado nos seguintes ficheiros.  
[expanalex.py](https://github.com/joaoR21/PL2025/blob/main/TPC6/expanalex.py) - analisador léxico  
[expanasinyacc.py](https://github.com/joaoR21/PL2025/blob/main/TPC6/expanasinyacc.py) - analisador sintático  

## Autor

| Nome  | Número mecanográfico |  
|-------|----------------------|  
| João Ricardo Oliveira Macedo | A104080 |