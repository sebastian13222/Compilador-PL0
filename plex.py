from sly import Lexer
import sys
from rich.table import Table
from rich.console import Console

class pl0Lexer(Lexer):
    tokens = {
        # Palabras reservadas
        BEGIN, END, IF, THEN, ELSE, WHILE, DO,
        PRINT, WRITE, READ, RETURN, SKIP, BREAK,
        FUN, INT_TYPE, FLOAT_TYPE, STRING_TYPE,

        # Operador de asignación
        ASIGN,
        # Operadores lógicos
        NOT, AND, OR, 

        # Operadores de relación
        LESS_EQUAL, GREATER_EQUAL, EQUAL, NOT_EQUAL,

        # Literales
        NAME, INTEGER, FLOAT, STRING, 

    }
    
    # Ignorar espacios en blanco y tabulaciones
    ignore = ' \t'

    # Operadores
    literals = '+-*/,:;()[]><'

    # Palabras clave y palabras reservadas
    BEGIN = r'begin( |\t|\n)\b'
    END = r'end\b'
    IF = r'if\b'
    THEN = r'then\b'
    ELSE = r'else\b'
    WHILE = r'while\b'
    DO = r'do( |\t|\n)\b'
    PRINT = r'print\b'
    WRITE = r'write\b'
    READ = r'read\b'
    RETURN = r'return\b'
    SKIP = r'skip\b'
    BREAK = r'break\b'
    FUN = r'fun\b'
    INT_TYPE = r'int\b'
    FLOAT_TYPE = r'float\b'
    STRING_TYPE = r'string\b'

    # Operador de asignación
    ASIGN = r':='

    # Operadores relacionales
    NOT_EQUAL = r'!='
    LESS_EQUAL = r'<='
    GREATER_EQUAL = r'>='
    EQUAL = r'=='

    # Operadores lógicos
    AND = r'and\b'
    OR = r'or\b'
    NOT = r'not\b'

    # Definir patrones para tokens
    NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
    FLOAT = r'(0\.[0-9]+([eE][+\-]?[0-9]+)?|[1-9][0-9]*\.[0-9]+([eE][+\-]?[0-9]+)?|[1-9][0-9]*[eE][+\-]?[0-9]+)\b'
    INTEGER = r'([1-9][0-9]*|0)\b'
    STRING = r'"(.+[^\\e])"'

    # funcion para llevar los saltos de linea
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # funcion para ignorar comentarios
    @_(r'/\*(.|\n)*?\*/')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    # funcion para ignorar e identificar malos comentarios
    @_(r'/\*(.|\n)+')
    def ignore_badcomment(self, t):
        print(f"Comentario imcompleto en la linea: {self.lineno}")
        print(f"Comentario : {t.value}")
        self.lineno += t.value.count('\n')

    # funcion para ignorar e identificar enteros mal escritos
    @_(r'[0]\d+.*')
    def ignore_badnumberint(self, t):
        print(f"Numero mal escrito {t.value}, en la linea: {self.lineno}")
        self.lineno += t.value.count('\n')

    # funcion para ignorar e identificar flotantes mal escritos
    @_(r'0+\.[\.]*[0-9]+([eE][\.]*[+\-]*[+\-]?[0-9]+)?|[0-9]+\.[\.]*[0-9]+([eE][\.]*[+\-]*[+\-]?[0-9]+)?|[0-9][0-9]*[eE][\.]*[+\-]*[+\-]?[0-9]+|[\.]+[0-9]+([eE][\.]*[+\-]*[+\-]?[0-9]+)?')
    def ignore_badnumberfloat(self, t):
        print(f"Numero mal escrito {t.value}, en la linea: {self.lineno}")
        self.lineno += t.value.count('\n')

    #funcion para ignorar malos strings
    
    @_(r'".+')
    def ignore_badstring(self,t):
        print(f"String mal escrito en la linea: {self.lineno}")
        print(f"String: {t.value}")
        self.lineno += t.value.count('\n')

    @_(r'(\/\*)\.*(\*\/)')
    # Función para manejar errores de tokens no válidos
    def error(self, t):
        print(f"Token no válido: '{t.value[0]}' en la línea {self.lineno}")
        self.index += 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python pl0_lexer.py archivo.pl0")
    else:
        archivo = sys.argv[1] 

        try:
            with open(archivo, 'r') as file:
                text = file.read()
            print("Contenido del archivo:")
            print(text)
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no se encontró.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {str(e)}")
            
    lexer = pl0Lexer()

table = Table(title='Análisis Léxico')
table.add_column('type',style='cyan')
table.add_column('value')
table.add_column('lineno', justify='right',style='green')

for t in lexer.tokenize(text):
    value = t.value if isinstance(t.value, str) else str(t.value)
    table.add_row(t.type,
                  value,
                  str(t.lineno))
    
console = Console()
console.print(table)