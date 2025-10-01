from magicLang import lexer

programa =  '''
                , ; { } [ ]
                0 + 9 - * / %
                Verdadero
                adivinar
                < > <= >=
                y o == != no
                forjar hechizo invocar conjurar veces ritual fallido encantar
            '''

lexer.input(programa)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)