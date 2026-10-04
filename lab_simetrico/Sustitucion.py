
from collections import Counter
import textwrap
 
cripto = """RIJ AZKKZHC PIKCE XT ACKCUXJHX SZX, E NZ PEJXKE, PXGIK XFDKXNEQE RIPI RIPQEHCK ET OENRCNPI AXNAX ZJ RKCHXKCI AX CJAXDXJAXJRCE AX RTENX, E ACOXKXJRCE AXT RITEQIKERCIJCNPI OKXJHXDIDZTCNHE AX TE ACKXRRCIJ EJEKSZCNHE.
 
AZKKZHC OZX ZJ OERHIK AX DKCPXK IKAXJ XJ XT DEDXT AX TE RTENX IQKXKE XJ REHETZJVE XJ GZTCI AX 1936. DXKI AZKKZHC, RIPI IRZKKX RIJ TEN DXKNIJETCAEAXN XJ TE MCNHIKCE, JI REVI AXT RCXTI. DXKNIJCOCREQE TE HKEACRCIJ KXvITZRCIJEKCE AX TE RTENX IQKXKE. NZ XJIKPX DIDZTEKCAEA XJHKX TE RTENX HKEQEGEAIKE, KXOTXGEAE XJ XT XJHCXKKI PZTHCHZACJEKCI XJ QEKRXTIJE XT 22 AX JIvCXPQKX AX 1936, PZXNHKE XNE CAXJHCOCRERCIJ. NZ PZXKHX OZX NCJ AZAE ZJ UITDX IQGXHCvI ET DKIRXNI KXvITZRCIJEKCI XJ PEKRME. NCJ AZKKZHC SZXAI PEN TCQKX XT REPCJI DEKE SZX XT XNHETCJCNPI, RIJ TE RIPDTCRCAEA AXT UIQCXKJI AXT OKXJHX DIDZTEK V AX TE ACKXRRCIJ EJEKSZCNHE, HXKPCJEKE XJ PEVI AX 1937 TE HEKXE AX TCSZCAEK TE KXvITZRCIJ, AXNPIKETCLEJAI E TE RTENX IQKXKE V OERCTCHEJAI RIJ XTTI XT DINHXKCIK HKCZJOI OKEJSZCNHE."""
 
# Letras del castellano de más a menos frecuente (tabla de la diapositiva 13)
frecuencia_es = "eaolsndruitcpmyqbhgfvjñzxkw"
 
# 1. Ordenamos las letras del criptograma de más a menos frecuente
cuenta = Counter(c for c in cripto if c.isalpha())
letras_cifradas = [letra for letra, veces in cuenta.most_common()]
 
# 2. Clave inicial: la más frecuente del criptograma -> la más frecuente del español, etc.
clave = dict(zip(letras_cifradas, frecuencia_es))
 
# 3. Bucle interactivo: mostramos el texto y corregimos hasta que se lea bien
while True:
    print()
    for parrafo in cripto.split("\n\n"):
        for linea in textwrap.wrap(parrafo, 70):
            print(linea)                                        # criptograma (original)
            print("".join(clave.get(c, c) for c in linea))      # lo que llevamos descifrado
            print()
 
    cambio = input("Cambio (por ejemplo K=r) o 'q' para salir: ")
    if cambio == "q":
        break
 
    if cambio.count("=") != 1:
        print("Formato incorrecto. Escribe por ejemplo: K=r")
        continue
    cifrada, clara = cambio.split("=")
    if cifrada not in clave:
        print("Esa letra no está en el criptograma (usa la letra tal cual aparece arriba, en mayúscula).")
        continue
    # Si la letra clara ya la usaba otra letra cifrada, se intercambian
    for otra in clave:
        if clave[otra] == clara:
            clave[otra] = clave[cifrada]
            break
    clave[cifrada] = clara
 
print("Clave final (cifrada -> clara):", clave)

