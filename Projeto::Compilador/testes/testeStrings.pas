program TesteStrings;

var
  str_val1, str_val2, str_resultado, str_binaria: string;
  int_resultado, i, int_ascii_val, int_potencia, int_valor_bin: integer;

begin
  str_binaria := '101101';

  writeln('--- operações de string (length e indexação) ---');
  str_val1 := 'TestStr';
  writeln('string str_val1: ', str_val1);
  int_resultado := length(str_val1);
  writeln('length(str_val1) (esperado 7): ', int_resultado);
  int_resultado := length('');
  writeln('length de string vazia (esperado 0): ', int_resultado);
  
  writeln('indexando str_val1 (''TestStr''):');
  if length(str_val1) > 0 then
  begin
    int_ascii_val := ord(str_val1[1]); 
    writeln('ascii de str_val1[1] (''T''): ', int_ascii_val);
    int_ascii_val := ord(str_val1[length(str_val1)]); 
    writeln('ascii de str_val1[length(str_val1)] (''r''): ', int_ascii_val);
    int_ascii_val := ord(str_val1[4]); 
    writeln('ascii de str_val1[4] (''t''): ', int_ascii_val);
    
    writeln('comparando str_val1[1] com literal char ''T'':');
    if str_val1[1] = 'T' then
        writeln('str_val1[1] é ''T'' (correto)')
    else
        writeln('str_val1[1] não é ''T'' (incorreto)');
  end;
  writeln;

  writeln('--- teste de conversão de string binária para inteiro ---');
  writeln('usando string binária: ', str_binaria);
  
  int_valor_bin := 0;       
  int_potencia := 1;         
  if length(str_binaria) > 0 then
  begin
    for i := length(str_binaria) downto 1 do
    begin
      if str_binaria[i] = '1' then
        int_valor_bin := int_valor_bin + int_potencia;
      int_potencia := int_potencia * 2;
    end;
    writeln('binário ''', str_binaria, ''' corresponde ao inteiro: ', int_valor_bin, ' (esperado 45)');
  end
  else
  begin
    writeln('string binária estava vazia.');
  end;
  writeln;

  str_val2 := 'abc';
  str_resultado := str_val1 + str_val2;
  writeln('concatenação: ', str_val1, ' + ', str_val2, ' = ', str_resultado, ' (esperado TestStrabc)');


  writeln('--- fim de teste ---');
end.
