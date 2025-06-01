program testeLogica;

var
  int_num1, int_num2, int_num_comp1, int_num_comp2: integer;
  real_num1, real_num_comp1: real;
  str_val1, str_val_comp1: string;
  char_val1, char_val_comp1: char;
  bool_val1, bool_val2, bool_val3, bool_resultado: boolean;

begin
  int_num1 := 100;
  int_num2 := 25;
  real_num1 := 12.5;
  str_val1 := 'Pascal';
  char_val1 := 'A';
  bool_val1 := true;
  bool_val2 := false;
  bool_val3 := true;

  writeln('--- secção 4: operações de comparação e lógicas ---');

  writeln('--- operações de comparação ---');
  int_num_comp1 := 100;
  int_num_comp2 := 25;
  real_num_comp1 := 12.5;
  str_val_comp1 := 'Pascal';
  char_val_comp1 := 'A';

  bool_resultado := int_num_comp1 = 100;          writeln('int_num_comp1 = 100 (T): ', bool_resultado);
  bool_resultado := int_num_comp1 <> int_num_comp2;     writeln('int_num_comp1 <> int_num_comp2 (T): ', bool_resultado);
  bool_resultado := int_num_comp1 < int_num_comp2;      writeln('int_num_comp1 < int_num_comp2 (F): ', bool_resultado);
  bool_resultado := int_num_comp1 > int_num_comp2;      writeln('int_num_comp1 > int_num_comp2 (T): ', bool_resultado);
  bool_resultado := int_num_comp1 <= 100;         writeln('int_num_comp1 <= 100 (T): ', bool_resultado);
  bool_resultado := int_num_comp2 >= 25;          writeln('int_num_comp2 >= 25 (T): ', bool_resultado);

  bool_resultado := real_num_comp1 = 12.5;        writeln('real_num_comp1 = 12.5 (T): ', bool_resultado);
  bool_resultado := real_num_comp1 < 10.0;        writeln('real_num_comp1 < 10.0 (F): ', bool_resultado);

  bool_resultado := str_val_comp1 = 'Pascal';        writeln('str_val_comp1 = ''Pascal'' (T): ', bool_resultado);
  bool_resultado := str_val_comp1 <> 'pascal';       writeln('str_val_comp1 <> ''pascal'' (T, sensível a maiúsculas): ', bool_resultado);
  
  bool_resultado := char_val_comp1 = 'A';            writeln('char_val_comp1 = ''A'' (T): ', bool_resultado);
  bool_resultado := char_val_comp1 < 'B';            writeln('char_val_comp1 < ''B'' (T): ', bool_resultado);
  writeln;

  writeln('--- operações lógicas (bool_val1=true, bool_val2=false, bool_val3=true) ---');
  bool_resultado := bool_val1 and bool_val2;        writeln('bool_val1 and bool_val2 (F): ', bool_resultado);
  bool_resultado := bool_val1 or bool_val2;         writeln('bool_val1 or bool_val2 (T): ', bool_resultado);
  bool_resultado := not bool_val2;              writeln('not bool_val2 (T): ', bool_resultado);
  bool_resultado := (int_num1 > 50) and bool_val1; writeln('(int_num1 > 50) and bool_val1 (T): ', bool_resultado);
  bool_resultado := (int_num1 < 50) or (not bool_val2); writeln('(int_num1 < 50) or (not bool_val2) (T): ', bool_resultado);
  writeln;

  writeln('--- testes de precedência de operadores lógicos e de comparação ---');
  writeln('bool_val1 (true), bool_val2 (false), bool_val3 (true)');
  writeln('int_num1 (100), int_num2 (25)');
  
  bool_resultado := not bool_val1 and bool_val2; 
  writeln('valor esperado (false): ', bool_resultado);
  
  bool_resultado := bool_val1 and not bool_val2;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := bool_val1 or bool_val2 and bool_val3;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := (bool_val1 or bool_val2) and bool_val3;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := not (bool_val1 and bool_val2) or bool_val3;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := int_num1 > int_num2 and bool_val1;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := int_num1 < int_num2 or bool_val1;
  writeln('valor esperado (true): ', bool_resultado);

  bool_resultado := not int_num1 = int_num2 and bool_val1 or bool_val2;
  writeln('valor esperado (true): ', bool_resultado);
  
  bool_resultado := (int_num1 > 0) and (int_num2 < 50) or (char_val1 = 'A') and not (real_num1 < 10.0);
  writeln('valor esperado (true): ', bool_resultado);

  writeln('--- fim da secção 4 ---');
  writeln;

  writeln('--- testeLogica concluído ---');
end.
