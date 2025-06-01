program TesteLiterais;

var
  int_num1: integer;
  real_num1: real;
  str_val1: string;
  char_val1: char;
  bool_val1: boolean;

begin
  writeln('olá!');
  writeln('literal inteiro: ', 12345);
  writeln('literal real: ', 3.14159);
  writeln('literal string: ', 'isto é uma string de teste.');
  writeln('literal char: ', 'X');
  writeln('literal booleano (true): ', true);
  writeln('literal booleano (false): ', false);
  
  int_num1 := 987;
  real_num1 := 1.23;
  str_val1 := 'outra string';
  char_val1 := 'Y';
  bool_val1 := true;

  writeln('variável inteira: ', int_num1);
  writeln('variável real: ', real_num1);
  writeln('variável string: ', str_val1);
  writeln('variável char: ', char_val1);
  writeln('variável booleana: ', bool_val1);

  write('isto é um teste ');
  write('para o procedimento write.');
  writeln; 
  writeln;

  writeln('--- fim de teste ---');
end.
