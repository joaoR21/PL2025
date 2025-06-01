program TesteAritmetica;

var
  int_num1, int_num2, int_num3, int_resultado: integer;
  real_num1, real_num2, real_num3, real_resultado: real;
  a, b, c, d, e: integer;
  ra, rb, rc, rd, re: real;

begin
  int_num1 := 100;
  int_num2 := 25;
  int_num3 := 5;

  real_num1 := 12.5;
  real_num2 := 2.5;
  real_num3 := 2.0;

  writeln('--- secção 3: operações aritméticas ---');

  writeln('--- aritmética com inteiros (int_num1=100, int_num2=25) ---');
  int_resultado := int_num1 + int_num2;       writeln('100 + 25 (esperado 125): ', int_resultado);
  int_resultado := int_num1 - int_num2;       writeln('100 - 25 (esperado 75): ', int_resultado);
  int_resultado := int_num1 * 3;             writeln('100 * 3 (esperado 300): ', int_resultado);
  int_resultado := int_num1 div int_num2;     writeln('100 div 25 (esperado 4): ', int_resultado);
  int_resultado := 101 mod int_num2;         writeln('101 mod 25 (esperado 1): ', int_resultado);
  int_resultado := -int_num1;                writeln('-100 (esperado -100): ', int_resultado);
  writeln;

  writeln('--- aritmética com reais (real_num1=12.5, real_num2=2.5) ---');
  real_resultado := real_num1 + real_num2;    writeln('12.5 + 2.5 (esperado 15.0): ', real_resultado);
  real_resultado := real_num1 - real_num2;    writeln('12.5 - 2.5 (esperado 10.0): ', real_resultado);
  real_resultado := real_num1 * 2.0;         writeln('12.5 * 2.0 (esperado 25.0): ', real_resultado);
  real_resultado := real_num1 / real_num2;    writeln('12.5 / 2.5 (esperado 5.0): ', real_resultado);
  real_resultado := -real_num1;              writeln('-12.5 (esperado -12.5): ', real_resultado);
  writeln;

  writeln('--- aritmética de tipos mistos ---');
  real_resultado := int_num1 + real_num1;     writeln('int_num1(100) + real_num1(12.5) (esperado 112.5): ', real_resultado);
  real_resultado := real_num1 * int_num2;     writeln('real_num1(12.5) * int_num2(25) (esperado 312.5): ', real_resultado);
  real_resultado := int_num1 / 2.0;          writeln('int_num1(100) / 2.0 (esperado 50.0): ', real_resultado);
  writeln;

  writeln('--- testes de precedência de operadores aritméticos ---');
  a := 10; b := 5; c := 2; d := 4; e := 3;

  int_resultado := a + b * c;        writeln('valor esperado (20): ', int_resultado);
  int_resultado := a * b + c;        writeln('valor esperado (52): ', int_resultado);
  int_resultado := (a + b) * c;      writeln('valor esperado (30): ', int_resultado);
  int_resultado := a + b div c;      writeln('valor esperado (12): ', int_resultado);
  int_resultado := a mod b + c;      writeln('valor esperado (2): ', int_resultado);
  int_resultado := a - b * c + d div e; writeln('valor esperado (1): ', int_resultado);
  int_resultado := a * (b + c) div d - e; writeln('valor esperado (14): ', int_resultado);
  int_resultado := a * b div c mod d + e; writeln('valor esperado (4): ', int_resultado);
  writeln;

  ra := 10.0; rb := 5.0; rc := 2.0; rd := 4.0; re := 3.0;

  real_resultado := ra + rb * rc;        writeln('valor esperado (20.0): ', real_resultado);
  real_resultado := ra * rb + rc;        writeln('valor esperado (52.0): ', real_resultado);
  real_resultado := (ra + rb) * rc;      writeln('valor esperado (30.0): ', real_resultado);
  real_resultado := ra / rb - rc;        writeln('valor esperado (0.0): ', real_resultado);
  real_resultado := ra - rb / rc;        writeln('valor esperado (7.5): ', real_resultado);
  real_resultado := (ra - rb) / rc;      writeln('valor esperado (2.5): ', real_resultado);
  real_resultado := ra - rb * rc + rd / re; writeln('valor esperado (1.333...): ', real_resultado);
  real_resultado := ra * (rb + rc) / rd - re; writeln('valor esperado (14.5): ', real_resultado);
  writeln;

  writeln('--- fim da secção 3 ---');
  writeln;

  writeln('--- testeAritmetica concluído ---');
end.
