# Relatório

## Introdução

O presente relatório descreve o processo de desenvolvimento de um compilador para a linguagem Pascal Standard, realizado no âmbito do trabalho prático da Unidade Curricular de Processamento de Linguagens. Este projeto teve como objetivo principal desenvolver uma ferramenta capaz de analisar, interpretar e traduzir código Pascal para um formato executável por uma máquina virtual. O processo de compilação é dividido em várias fases fundamentais, incluindo a análise léxica, a análise sintática, a análise semântica e a geração de código.

## Análise Léxica

A análise léxica é a primeira fase do processo de compilação. A sua principal função é ler o código-fonte do programa Pascal e convertê-lo numa sequência de componentes léxicos, designados por *tokens*. Cada token representa uma unidade indivisível da linguagem, como uma palavra-chave, um identificador, um número ou um operador.

Para a implementação deste analisador léxico, recorreu-se à biblioteca `ply.lex` para Python. Esta ferramenta facilita a definição de tokens através de expressões regulares e funções associadas.

### Tokens Reconhecidos

O analisador léxico é capaz de reconhecer os seguintes tokens:

* **Identificadores e Literais:**
    * `ID`: Nomes de variáveis, funções, etc. (ex.: `variavel`, `SomaValores`)
    * `NUMBER`: Números inteiros (ex.: `123`, `0`, `42`)
    * `REAL_NUMBER`: Números reais (ex.: `3.14`, `0.5`, `123.456`)
    * `STRING`: Cadeias de caracteres delimitadas por plicas (ex.: `'Olá Mundo'`, `'Teste'`)
    * `TRUE`, `FALSE`: Literais booleanos

* **Palavras Reservadas (Keywords):**
    * `PROGRAM`, `BEGIN`, `END`, `VAR`, `FUNCTION`, `PROCEDURE`
    * `IF`, `THEN`, `ELSE`, `WHILE`, `DO`, `FOR`, `TO`, `DOWNTO`
    * `WRITELN`, `READLN`, `WRITE`, `READ`
    * `INTEGER`, `STRTYPE` (para `string`), `REAL`, `CHAR`, `BOOLEAN`
    * `ARRAY`, `OF`
    * `MOD`, `DIV` (divisão inteira)
    * `NOT`, `AND`, `OR`

* **Operadores e Delimitadores:**
    * `PLUS` (`+`), `MINUS` (`-`), `TIMES` (`*`), `DIVIDE` (`/`)
    * `ASSIGN` (`:=`)
    * `EQ` (`=`), `NE` (`<>` ou `!=`), `LT` (`<`), `LE` (`<=`), `GT` (`>`), `GE` (`>=`)
    * `LPAREN` (`(`), `RPAREN` (`)`)
    * `LBRACKET` (`[`), `RBRACKET` (`]`)
    * `SEMI` (`;`), `COLON` (`:`), `COMMA` (`,`), `DOT` (`.`)
    * `RANGEDOTS` (`..`)

* **Comentários:**
    * `COMMENT`: Comentários delimitados por `{ ... }` ou `(* ... *)`, ignorados pelo programa.

## Análise Sintática

Após a análise léxica, o analisador sintático (parser) recebe esta sequÊncia de tokens, e verifica se a sequência obtida respeita as regras gramaticais da linguagem Pascal. Se a estrutura for válida, é construída uma Árvore Sintática Abstrata (AST), que representa hierarquicamente o programa e serve de base para as fases seguintes da compilação.

Para a implementação deste analisador sintático, recorreu-se à biblioteca `ply.yacc` para Python.

### Gramática da Linguagem

A seguir, apresenta-se a gramática que define a estrutura dos programas Pascal reconhecidos pelo compilador:

```
program : PROGRAM ID SEMI program_body DOT

program_body : declaration_part block

declaration_part : var_declaration
                 | function_declaration_list
                 | var_declaration function_declaration_list
                 | function_declaration_list var_declaration
                 | empty

function_declaration_list : function_declaration_list function_declaration
                          | function_declaration

function_declaration : FUNCTION ID LPAREN parameter_list RPAREN COLON type SEMI function_body SEMI

function_body : var_declaration BEGIN statement_list END

parameter_list : parameter_list SEMI parameter
               | parameter
               | empty

parameter : id_list COLON type

block : BEGIN statement_list END

var_declaration : VAR var_list SEMI
                | empty

var_list : var_list SEMI var_item
         | var_item

var_item : id_list COLON type

iD_list : id_list COMMA ID
        | ID

type : INTEGER
     | STRTYPE
     | BOOLEAN
     | CHAR
     | REAL
     | array_type

array_type : ARRAY LBRACKET expression RANGEDOTS expression RBRACKET OF type

statement_list : statement_list SEMI statement
               | statement
               | empty

statement : assignment_statement
          | writeln_statement
          | write_statement
          | readln_statement
          | read_statement
          | for_statement
          | while_statement
          | compound_statement
          | if_statement
          | function_call_statement
          | empty

assignment_statement : ID ASSIGN expression
                     | array_access ASSIGN expression

writeln_statement : WRITELN LPAREN write_args RPAREN
                  | WRITELN

write_statement : WRITE LPAREN write_args RPAREN

readln_statement : READLN LPAREN read_args RPAREN
                 | READLN

read_statement : READ LPAREN read_args RPAREN

read_args : read_args COMMA read_arg
          | read_arg

read_arg : ID
         | array_access

if_statement : IF expression THEN statement
             | IF expression THEN statement ELSE statement

while_statement : WHILE expression DO statement

write_args : write_args COMMA write_arg
           | write_arg

write_arg : expression

for_statement : FOR ID ASSIGN expression direction expression DO statement

direction : TO
          | DOWNTO

compound_statement : BEGIN statement_list END

expression : or_expression

or_expression : or_expression OR and_expression
              | and_expression

and_expression : and_expression AND not_expression
               | not_expression

not_expression : NOT comparison_expression
               | comparison_expression

comparison_expression : comparison_expression EQ additive_expression
                      | comparison_expression NE additive_expression
                      | comparison_expression LT additive_expression
                      | comparison_expression LE additive_expression
                      | comparison_expression GT additive_expression
                      | comparison_expression GE additive_expression
                      | additive_expression

additive_expression : additive_expression PLUS multiplicative_expression
                    | additive_expression MINUS multiplicative_expression
                    | multiplicative_expression

multiplicative_expression : multiplicative_expression TIMES unary_minus_factor
                          | multiplicative_expression DIVIDE unary_minus_factor
                          | multiplicative_expression MOD unary_minus_factor
                          | multiplicative_expression DIV unary_minus_factor
                          | unary_minus_factor

unary_minus_factor : MINUS factor
                   | factor

factor : NUMBER
       | REAL_NUMBER
       | ID
       | TRUE
       | FALSE
       | STRING
       | LPAREN expression RPAREN
       | ID LPAREN call_arguments RPAREN
       | array_access

function_call_statement : ID LPAREN call_arguments RPAREN

call_arguments : call_arguments COMMA expression
               | expression
               | empty

array_access : ID LBRACKET expression RBRACKET

empty : ε
```

O analisador sintático reportou 6 conflitos durante a construção das tabelas de parsing. Estes conflitos e as respetivas resoluções são as seguintes:

Dois conflitos são do tipo "shift/reduce". O primeiro ocorre ao processar a palavra-chave FUNCTION no início de uma secção de declarações. Neste caso, o parser opta pela ação "shift", tratando FUNCTION como parte da declaração, o que corresponde ao comportamento esperado. O segundo é o clássico problema do "dangling ELSE", em que um ELSE pode ser associado a mais do que um IF. Aqui, o parser também resolve por "shift", associando o ELSE ao IF mais próximo, que é a abordagem convencional.

Os quatro conflitos restantes são do tipo "reduce/reduce". Estes resultam sobretudo de ambiguidades causadas por regras que admitem a derivação da sequência vazia (empty) na gramática. O ply resolve automaticamente estas ambiguidades, escolhendo uma das possíveis reduções com base na ordem das regras na gramática ou o lookahead.

Embora o ideal seja uma gramática livre de conflitos, as estratégias de resolução tomadas pelo ply nestes casos tendem a produzir o comportamento de parsing correto para as construções típicas da linguagem Pascal.

## Análise Semântica

Após a construção da AST pelo analisador sintático, passamos à fase de análise semântica. O principal objetivo desta fase é verificar a coerência e o significado do programa, garantindo que este obedece às regras de tipo da linguagem Pascal e que todas as utilizações de identificadores (variáveis, funções, etc.) se encontram válidas.

Neste compilador, a análise semântica é realizada principalmente pelo módulo `anasem.py`. As suas responsabilidades incluem:

* **construção da tabela de símbolos:** é construída uma tabela de símbolos que armazena informações cruciais sobre cada identificador declarado no programa. Isto inclui o nome do identificador, o seu tipo (ex.: `integer`, `string`, `array of integer`), o seu endereço de memória (para variáveis globais) e, no caso de *arrays*, os seus limites e tipo de elemento. Para funções (embora a sua declaração completa não estejam totalmente implementadas na geração de código da versão atual), a tabela de símbolos armazena a sua assinatura (parâmetros e tipo de retorno). A função pré-definida `length` é registada na tabela.
* **verificação de tipos:** o analisador semântico percorre a AST para inferir e verificar os tipos das expressões. Por exemplo, garante que os operandos de uma operação aritmética são compatíveis (ex.: não se pode somar diretamente uma `string` a um `integer` sem conversão) e que o tipo de uma expressão atribuída a uma variável é compatível com o tipo declarado dessa variável.
* **verificação de declarações:** assegura que todos os identificadores utilizados numa expressão ou comando foram previamente declarados.
* **avaliação de expressões constantes:** para declarações de *arrays*, onde os limites devem ser constantes, o analisador avalia essaas expressões.

Se forem detetados erros semânticos (ex.: utilização de variável não declarada, incompatibilidade de tipos), o processo de compilação é interrompido com uma mensagem de erro apropriada.

## Geração de Código

A fase final do processo de compilação é a geração de código. Nesta etapa, a representação intermédia do programa (a AST, já validada semanticamente) é traduzida para um código de baixo nível que pode ser executado pela máquina virtual.

O módulo `tradutor.py` é responsável por esta tradução. O processo de geração de código envolve:

* **travessia da AST:** o tradutor percorre a AST, nó a nó.
* **consulta à tabela de símbolos:** para cada identificador encontrado (ex.: numa atribuição ou expressão), o tradutor consulta a tabela de símbolos para obter informações como o seu endereço de memória ou tipo.
* **mapeamento para instruções da VM:** com base no tipo de nó da AST e nas informações da tabela de símbolos, o tradutor emite a sequência correspondente de instruções da máquina virtual. Por exemplo:
    * Uma atribuição (`:=`) traduz-se na avaliação da expressão do lado direito, seguida de uma instrução `STOREG` (para variáveis globais) ou `STOREN` (para elementos de *array*).
    * Operações aritméticas (`+`, `*`, `div`) são mapeadas para as instruções aritméticas da VM (`ADD`, `MUL`, `DIV`), com atenção à promoção de tipos (ex.: `ITOF` para converter inteiro para real antes de uma operação de ponto flutuante).
    * Estruturas de controlo como `IF-THEN-ELSE` e `WHILE` são implementadas utilizando instruções de salto condicional (`JZ` - jump if zero) e incondicional (`JUMP`) da VM, com a geração de *labels* para os destinos dos saltos.
    * Chamadas a procedimentos de entrada/saída como `WRITELN` e `READLN` são traduzidas para as instruções `WRITES`, `WRITEI`, `WRITEF`, `WRITELN`, `READ`, `ATOI`, `ATOF`, etc., da VM.

O resultado final desta fase é um ficheiro de texto (`.vm`) contendo o código da máquina virtual pronto a ser executado. O tradutor também adiciona comentários ao código VM gerado para facilitar a sua leitura e depuração.

## Estrutura do Compilador

O ficheiro `compiler.py` orquestra todo o processo de compilação. Ele invoca sequencialmente:

1.  O analisador léxico (`analex.py`) para tokenizar o código fonte.
2.  O analisador sintático (`anasin.py`) para construir a AST.
3.  O analisador semântico (`anasem.py`) para construir a tabela de símbolos e realizar verificações semânticas.
4.  O tradutor (`tradutor.py`) para gerar o código da máquina virtual.

O compilador aceita um ficheiro Pascal (`.pas`) como entrada e, se bem-sucedido, produz um ficheiro de código da máquina virtual (`.vm`) como saída.

## Conclusão

O desenvolvimento deste compilador para um subconjunto da linguagem Pascal Standard permitiu aplicar e consolidar conhecimentos fundamentais de Processamento de Linguagens, desde a análise léxica até à geração de código para uma máquina virtual. A utilização da biblioteca `ply` simplificou a implementação das fases iniciais, enquanto a análise semântica e a geração de código exigiram um mapeamento rigoroso das estruturas da linguagem para as instruções da máquina virtual.

Apesar de o compilador já suportar variáveis de vários tipos, operações aritméticas e lógicas, estruturas de controlo e arrays unidimensionais, há margem para futuras melhorias, como a implementação completa de subprogramas e a otimizações de código.

Este projeto constituiu uma experiência prática enriquecedora, proporcionando uma compreensão aprofundada das diferentes etapas e desafios inerentes à construção de um compilador.

## Autores
* João Ricardo Oliveira Macedo : A104080
* Filipe Lopes Fernandes : A104185
* José Miguel Dias Pereira : A89596
