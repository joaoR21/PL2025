program TesteArrays;

var
  arr_int: array[1..5] of integer;
  arr_real: array[0..2] of real;
  arr_str: array[-1..1] of string;
  arr_char: array[1..3] of char;
  i, int_num1, int_temp_val: integer;
  real_input: real;
  char_input: char;
  str_input_default: string;

begin
  int_num1 := 100;
  str_input_default := 'string por defeito';

  writeln('--- secção 6: arrays ---');
  
  writeln('(testeArrays) introduza um real para real_input (ex: 10.5): ');
  readln(real_input);
  writeln('(testeArrays) introduza um char para char_input (ex: X): ');
  readln(char_input);

  writeln('--- array de inteiros (arr_int[1..5]) ---');
  arr_int[1] := 10;
  arr_int[2] := int_num1 div 4; 
  arr_int[3] := arr_int[1] + arr_int[2]; 
  write('introduza valor para arr_int[4]: '); readln(arr_int[4]);
  arr_int[5] := 50;
  writeln('elementos de arr_int:');
  for i := 1 to 5 do
    write(arr_int[i], ' ');
  writeln;
  writeln('arr_int[3] (esperado 35): ', arr_int[3]);
  writeln;

  writeln('--- array de reais (arr_real[0..2]) ---');
  arr_real[0] := 0.5;
  arr_real[1] := real_input + 1.0;
  arr_real[2] := arr_real[0] * 3.0;
  writeln('elementos de arr_real:');
  for i := 0 to 2 do
    write(arr_real[i]:0:2, ' '); 
  writeln;
  writeln;

  writeln('--- array de strings (arr_str[-1..1]) ---');
  arr_str[-1] := 'primeiro';
  arr_str[0] := str_input_default;
  arr_str[1] := 'Pascal' + ' ' + 'Compilador'; 
  writeln('elementos de arr_str:');
  for i := -1 to 1 do
    writeln('arr_str[', i, ']: ', arr_str[i]);
  writeln;

  writeln('--- array de chars (arr_char[1..3]) ---');
  arr_char[1] := 'P';
  arr_char[2] := char_input;
  arr_char[3] := 'A'; 
  writeln('elementos de arr_char:');
  for i := 1 to 3 do
    write(arr_char[i], ' ');
  writeln;
  writeln('--- fim da secção 6 ---');
  writeln;

  writeln('--- testeArrays concluído ---');
end.
