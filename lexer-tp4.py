class Lexer:

    def __init__(self):
        pass

    def verificar(self, palabra):
        if self.__q0(palabra) == 1:
            print("Palabra '" + palabra + "' aceptada.")
        else:
            print("Palabra '" + palabra + "' rechazada.")
    
    def __q0(self, palabra):
        if (len(palabra) > 0):
            if palabra[0] == 'a':
                return self.__q1(palabra[1:])
            elif palabra[0] == 'b':
                return self.__q0(palabra[1:])
        return 0

    def __q1(self, palabra):
        if (len(palabra) > 0):
            if palabra[0] == 'a':
                return self.__q1(palabra[1:])
            elif palabra[0] == 'b':
                return self.__q2(palabra[1:])
        return 0
    
    def __q2(self, palabra):
        if (len(palabra) > 0):
            if palabra[0] == 'a':
                return self.__q1(palabra[1:])
            elif palabra[0] == 'b':
                return self.__q3(palabra[1:])
        return 0
    
    def __q3(self, palabra):
        if (len(palabra) == 0):
            return 1
        else:
            if palabra[0] == 'a':
                return self.__q1(palabra[1:])
            elif palabra[0] == 'b':
                return self.__q0(palabra[1:])
        return 0
    
Lexer().verificar("abb")
Lexer().verificar("abbabaaababb")
Lexer().verificar("aaaabb")
Lexer().verificar("ab")
Lexer().verificar("abbabbb")
Lexer().verificar("abbaab")