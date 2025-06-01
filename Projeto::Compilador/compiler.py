import sys
import os
import argparse
import json
from analex import lexer
from anasin import parser
from anasem import semantics 
from tradutor import Translator

def compiler(input, output, debug_AST_path=None):
    """compila um ficheiro Pascal (.pas) para código de máquina virtual (.vm)."""
    try:
        with open(input, 'r', encoding='utf-8') as f:
            pascal_code = f.read()
        print(f"--- a ler ficheiro de entrada: {input} ---")
    except FileNotFoundError:
        print(f"[ERROR]: ficheiro de entrada não encontrado: {input}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR]: não foi possível ler o ficheiro de entrada '{input}': {e}", file=sys.stderr)
        return False

    # 1. análise léxica e sintática
    print("--- a iniciar análise léxica e sintática ---")
    lexer.lineno = 1 
    ast = None
    try:
        ast = parser.parse(pascal_code, lexer=lexer)
        if not ast: 
            print("[ERROR]: falha na análise sintática.", file=sys.stderr)
            return False
    except SyntaxError: 
        print(f"[ERROR]: falha na análise sintática (ver mensagem anterior de anasin.py).", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR]: erro inesperado durante a análise léxica/sintática: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False
    
    print("--- análise léxica e sintática concluída ---")

    if debug_AST_path and ast:
        try:
            with open(debug_AST_path, 'w', encoding='utf-8') as ast_file:
                json.dump(ast, ast_file, indent=2, ensure_ascii=False)
            print(f"--- AST guardada em: {debug_AST_path} ---")
        except Exception as e:
            print(f"[AVISO COMPILADOR]: não foi possível guardar a AST de depuração: {e}", file=sys.stderr)

    # 2. análise semântica
    print("--- a iniciar análise semântica (construção da tabela de símbolos) ---")
    symbol_table = None
    try:
        symbol_table = semantics(ast) 
        print("--- análise semântica (construção da tabela de símbolos) concluída ---")

    except ValueError as ve:
        print(f"[ERROR]: erro durante a análise semântica - {ve}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR]: erro inesperado durante a análise semântica: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

    # 3. geração de código
    print("--- a iniciar tradução para código VM ---")
    VM_code = None
    try:
        translator = Translator(ast, symbol_table) 
        VM_code = translator.translate() 
        
        if VM_code is None: 
             print("[ERROR]: falha na tradução, código VM não gerado (tradutor retornou None).", file=sys.stderr)
             return False

    except ValueError as ve:
        print(f"[ERROR]: erro de tradução - {ve}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR]: erro inesperado durante a tradução: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False
    
    print("--- tradução para código VM concluída ---")

    # 4. escrever código VM para ficheiro de saída
    try:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(VM_code)
        print(f"[SUCCESS]: código VM gerado com sucesso em: {output}")
        return True
    except IOError as e:
        print(f"[ERROR]: não foi possível escrever o ficheiro de saída '{output}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR]: erro inesperado ao escrever o ficheiro de saída: {e}", file=sys.stderr)
        return False

def main():
    arg_parser = argparse.ArgumentParser(description="compilador")
    arg_parser.add_argument("input_file", help="ficheiro de entrada PASCAL (.pas)")
    arg_parser.add_argument("-o", "--output", help="ficheiro de saída .vm (opcional, por defeito <nome_input>.vm)")
    arg_parser.add_argument("--debug", help="guarda a AST num ficheiro JSON (opcional)")

    args = arg_parser.parse_args()

    input = args.input_file
    
    if not input.lower().endswith(".pas"):
        print("[ERROR]: o ficheiro de entrada deve ter a extensão .pas", file=sys.stderr)
        sys.exit(1) 

    base_name = os.path.splitext(os.path.basename(input))[0]
    
    output = args.output
    if not output:
        output = base_name + ".vm"
    elif not output.lower().endswith(".vm"):
        output = os.path.splitext(output)[0] + ".vm"
        print(f"[WARNING]: ficheiro de saída não termina em .vm, a retornar {output}")


    debug = None
    if args.debug:
        if os.path.isdir(args.debug):
            debug = os.path.join(args.debug, base_name + "-ast.json")
        elif args.debug.lower().endswith(".json"):
            debug = args.debug
        else: 
            debug = os.path.splitext(args.debug)[0] + ".json"
        print(f"--- depuração da AST será guardada em: {debug} ---")


    if compiler(input, output, debug):
        sys.exit(0) 
    else:
        sys.exit(1) 

if __name__ == "__main__":
    main()
