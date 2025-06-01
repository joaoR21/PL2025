program TesteIO;

var
  int_num1, int_num2, int_outro_num: integer;
  real_num1, real_num2, real_input: real;
  str_val1, str_val2, str_input_default: string;
  char_val1, char_val2, char_input: char;
  bool_val1, bool_val2: boolean;

begin
  str_input_default := 'string de teste por defeito';

  writeln('--- secção 2: declaração de variáveis, atribuição e e/s básica ---');

  int_num1 := 100;
  int_num2 := 25;
  writeln('int_num1 (atribuído 100): ', int_num1);
  writeln('int_num2 (atribuído 25): ', int_num2);

  real_num1 := 12.5;
  real_num2 := 2.5;
  writeln('real_num1 (atribuído 12.5): ', real_num1);
  writeln('real_num2 (atribuído 2.5): ', real_num2);

  str_val1 := 'Pascal';
  str_val2 := 'Compilador';
  writeln('str_val1 (atribuído ''Pascal''): ', str_val1);
  writeln('str_val2 (atribuído ''Compilador''): ', str_val2);
  writeln('str_input_default (atribuído por defeito): ', str_input_default);

  char_val1 := 'A';
  char_val2 := 'Z';
  writeln('char_val1 (atribuído ''A''): ', char_val1);
  writeln('char_val2 (atribuído ''Z''): ', char_val2);

  bool_val1 := true;
  bool_val2 := false;
  writeln('bool_val1 (atribuído true): ', bool_val1);
  writeln('bool_val2 (atribuído false): ', bool_val2);
  writeln;

  writeln('--- testes de entrada ---');
  write('introduza um inteiro para int_outro_num: ');
  readln(int_outro_num);
  writeln('introduziu para int_outro_num: ', int_outro_num);

  write('introduza um número real para real_input: ');
  read(real_input); 
  writeln; 
  writeln('introduziu para real_input: ', real_input:0:2);

  write('introduza um caractere para char_input: ');
  readln(char_input); 
  writeln('introduziu para char_input: ', char_input);
  
  writeln('lendo uma string para str_val1:');
  readln(str_val1);
  writeln('nova str_val1: ', str_val1);


  writeln('--- fim da secção 2 ---');
  writeln;

  writeln('--- testeIO concluído ---');
end.
