program TesteEstruturasControlo;

var
  int_num1, int_num2, int_resultado, loop_contador, loop_var_for: integer;
  real_num1: real;
  bool_cond: boolean;

begin
  int_num1 := 100;
  real_num1 := 12.5; 
  
  writeln('--- secção 5: estruturas de controlo ---');

  writeln('--- if-then-else (int_num1=100) ---');
  if int_num1 > 50 then
    writeln('if: int_num1 é maior que 50 (correto)')
  else
    writeln('if: int_num1 não é maior que 50 (incorreto)');

  if int_num1 < 50 then
    writeln('if: int_num1 é menor que 50 (incorreto)')
  else
    begin
      writeln('if-else: int_num1 não é menor que 50 (correto)');
      if (int_num1 = 100) and (real_num1 > 10.0) then
        writeln('if aninhado: int_num1 é 100 e real_num1 > 10.0 (correto)');
    end;
  writeln;

  writeln('--- while loop ---');
  loop_contador := 1;
  int_resultado := 0;
  while loop_contador <= 5 do
  begin
    write('iteração while: ', loop_contador, '; ');
    int_resultado := int_resultado + loop_contador;
    loop_contador := loop_contador + 1;
  end;
  writeln;
  writeln('soma do ciclo while (1 a 5, esperado 15): ', int_resultado);
  writeln;

  writeln('--- for loop ---');
  writeln('for loop (1 to 4):');
  int_resultado := 1;
  for loop_var_for := 1 to 4 do
  begin
    write('for (to) iteração: ', loop_var_for, '; ');
    int_resultado := int_resultado * loop_var_for;
  end;
  writeln;
  writeln('produto do ciclo for to (1*2*3*4, esperado 24): ', int_resultado);

  writeln('for loop (3 downto 0):');
  for loop_var_for := 3 downto 0 do
  begin
    write('for (downto) iteração: ', loop_var_for, '; ');
  end;
  writeln;
  
  bool_cond := true;
  if bool_cond then writeln('if simples com booleano (T)');

  if not bool_cond then 
    writeln('este não deve imprimir')
  else 
    writeln('else de if com booleano (T)');


  writeln('--- fim da secção 5 ---');
  writeln;

  writeln('--- testeEstruturasControlo concluído ---');
end.
