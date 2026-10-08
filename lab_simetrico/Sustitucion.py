# Counter: clase de la librería estándar que cuenta cuántas veces aparece
# cada elemento de una colección (aquí, cada letra).
from collections import Counter
# textwrap: módulo para partir textos largos en líneas de un ancho máximo.
import textwrap
 
# El criptograma. Las comillas triples """ permiten escribir un texto de
# varias líneas (con saltos de línea incluidos) dentro de una sola cadena.
cripto = """RIJ AZKKZHC PIKCE XT ACKCUXJHX SZX, E NZ PEJXKE, PXGIK XFDKXNEQE RIPI RIPQEHCK ET OENRCNPI AXNAX ZJ RKCHXKCI AX CJAXDXJAXJRCE AX RTENX, E ACOXKXJRCE AXT RITEQIKERCIJCNPI OKXJHXDIDZTCNHE AX TE ACKXRRCIJ EJEKSZCNHE.
 
AZKKZHC OZX ZJ OERHIK AX DKCPXK IKAXJ XJ XT DEDXT AX TE RTENX IQKXKE XJ REHETZJVE XJ GZTCI AX 1936. DXKI AZKKZHC, RIPI IRZKKX RIJ TEN DXKNIJETCAEAXN XJ TE MCNHIKCE, JI REVI AXT RCXTI. DXKNIJCOCREQE TE HKEACRCIJ KXvITZRCIJEKCE AX TE RTENX IQKXKE. NZ XJIKPX DIDZTEKCAEA XJHKX TE RTENX HKEQEGEAIKE, KXOTXGEAE XJ XT XJHCXKKI PZTHCHZACJEKCI XJ QEKRXTIJE XT 22 AX JIvCXPQKX AX 1936, PZXNHKE XNE CAXJHCOCRERCIJ. NZ PZXKHX OZX NCJ AZAE ZJ UITDX IQGXHCvI ET DKIRXNI KXvITZRCIJEKCI XJ PEKRME. NCJ AZKKZHC SZXAI PEN TCQKX XT REPCJI DEKE SZX XT XNHETCJCNPI, RIJ TE RIPDTCRCAEA AXT UIQCXKJI AXT OKXJHX DIDZTEK V AX TE ACKXRRCIJ EJEKSZCNHE, HXKPCJEKE XJ PEVI AX 1937 TE HEKXE AX TCSZCAEK TE KXvITZRCIJ, AXNPIKETCLEJAI E TE RTENX IQKXKE V OERCTCHEJAI RIJ XTTI XT DINHXKCIK HKCZJOI OKEJSZCNHE."""
 
# Letras del castellano de más a menos frecuente (tabla de la diapositiva 13)
# Es una cadena: cada carácter es una letra, ordenadas por frecuencia
# de uso en español. Servirá de "diccionario" para la primera hipótesis.
frecuencia_es = "eaolsndruitcpmyqbhgfvjñzxkw"
 
# 1. Ordenamos las letras del criptograma de más a menos frecuente
# La expresión entre paréntesis es un "generador": recorre cada carácter c del
# criptograma y se queda solo con los que son letras (c.isalpha()), ignorando
# espacios, comas, puntos y números. Counter los cuenta y devuelve algo como
# {"X": 85, "E": 70, ...}.
cuenta = Counter(c for c in cripto if c.isalpha())
# .most_common() devuelve una lista de pares (letra, veces) ya ordenada de
# más a menos frecuente. La "list comprehension" siguiente se queda solo con
# la letra de cada par (el número de veces ya no hace falta).
letras_cifradas = [letra for letra, veces in cuenta.most_common()]
 
# 2. Clave inicial: la más frecuente del criptograma -> la más frecuente del español, etc.
# zip() empareja las dos secuencias posición a posición:
#   1ª letra cifrada más común con "e", 2ª con "a", 3ª con "o"...
# dict() convierte esos pares en un diccionario {letra_cifrada: letra_clara}.
# Esta es nuestra primera suposición de la clave; seguramente tendrá errores
# que corregiremos a mano. (Si una secuencia es más corta que la otra,
# zip se detiene en la más corta.)
clave = dict(zip(letras_cifradas, frecuencia_es))
 
# 3. Bucle interactivo: mostramos el texto y corregimos hasta que se lea bien
# "while True" crea un bucle infinito; solo se sale con el "break" de más abajo.
while True:
    # Línea en blanco para separar visualmente cada ronda.
    print()
    # Dividimos el criptograma en párrafos usando la línea vacía ("\n\n")
    # como separador.
    for parrafo in cripto.split("\n\n"):
        # textwrap.wrap parte el párrafo en trozos de máximo 70 caracteres
        # (sin cortar palabras), para que quepa bien en la pantalla.
        for linea in textwrap.wrap(parrafo, 70):
            print(linea)                                        # criptograma (original)
            # Aquí se aplica la clave. Para cada carácter c de la línea,
            # clave.get(c, c) busca su traducción en el diccionario; si no la
            # tiene (espacios, comas, números), devuelve el propio carácter c
            # (ese es el segundo argumento, el valor por defecto).
            # "".join(...) vuelve a unir todos los caracteres en una cadena.
            print("".join(clave.get(c, c) for c in linea))      # lo que llevamos descifrado
            # Línea en blanco entre cada par (cifrado / descifrado).
            print()
 
    # input() muestra el mensaje y espera a que el usuario escriba algo.
    cambio = input("Cambio (por ejemplo K=r) o 'q' para salir: ")
    # Si escribe "q", salimos del bucle.
    if cambio == "q":
        break
 
    # Validación: el formato debe tener exactamente un signo "=".
    # .count("=") cuenta cuántas veces aparece. Si no es 1, avisamos y
    # "continue" salta al principio del bucle para volver a pedir el cambio.
    if cambio.count("=") != 1:
        print("Formato incorrecto. Escribe por ejemplo: K=r")
        continue
    # .split("=") parte el texto por el "=" y devuelve dos trozos, que
    # guardamos en dos variables a la vez: "K=r" -> cifrada="K", clara="r".
    cifrada, clara = cambio.split("=")
    # Comprobamos que la letra cifrada exista como clave en el diccionario.
    # Si el usuario escribe una letra que no está en el criptograma, avisamos.
    if cifrada not in clave:
        print("Esa letra no está en el criptograma (usa la letra tal cual aparece arriba, en mayúscula).")
        continue
    # Si la letra clara ya la usaba otra letra cifrada, se intercambian
    # Una sustitución es biyectiva: dos letras cifradas no pueden representar
    # la misma letra clara. Por eso, si "clara" ya está asignada a otra letra
    # cifrada ("otra"), le damos a esa "otra" la letra clara que tenía antes
    # "cifrada" (un intercambio) y paramos de buscar con break.
    for otra in clave:
        if clave[otra] == clara:
            clave[otra] = clave[cifrada]
            break
    # Ahora sí, asignamos la nueva letra clara a la letra cifrada elegida.
    clave[cifrada] = clara
 
# Al salir del bucle, mostramos la clave final del diccionario
# (de letra cifrada -> letra clara).
print("Clave final (cifrada -> clara):", clave)

