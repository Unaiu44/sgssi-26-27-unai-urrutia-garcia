# Laboratorio: Introducción al cifrado, esteganografía y algoritmos resumen

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: `openssl`, `sha512sum`, `git`, `steghide`, `docker`, `docker compose`.
- Repositorio GitHub de asignatura: puedes subir los programa desarrollados en el laboratorio.

## Esteganografía práctica

En este bloque ocultaremos un mensaje dentro de una imagen contenedora.

Si `steghide` no esta instalado:

```bash
sudo apt update
sudo apt install steghide -y
```

Preparar mensaje:

```bash
echo "SGSSI-26-27 Software is like sex: it's better when it's free" > msg_linus
```

Insertar mensaje con contraseña en imagen `linus.jpg`:

```bash
steghide embed -cf linus.jpg -ef msg_linus -sf linus_steg.jpg
```

Extraccion del mensaje oculto (Primero renombrar archivo original mensaje a `msg_linus_old`):

```bash
steghide extract -sf linus_steg.jpg
less msg_linus
```

Tamaño del contenedor:

```bash
ls -lh linus.jpg linus_steg.jpg
```

## Integridad con funciones hash

Cálculo de resúmenes:

```bash
echo "Este fichero verifica integridad" > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
```

Modifica un solo caracter y vuelve a calcular los resúmenes. ¿Cómo han cambiado?

Han cambiado por completo, no solo un carácterer. Es el efecto avalancha: un cambio mínimo en la entrada altera aproximadamente la mitad de los bits de la salida, de forma impredecible. Por eso los hashes sirven para detectar cualquier modificación, por pequeña que sea.

## Integridad y esteganografia

Compara los hashes de los mensajes usados en la esteganografía: 

```bash
sha256sum msg_linus
sha256sum msg_linus_old
```

¿Coinciden? 

Si. El mensaje extraído es idémtoco bit a bit al original. Esto demuestra que el proceso de ocultar y extraer no pierde ni altera información.

Compara los hashes de los ficheros contenedor:

```bash
sha256sum linus.jpg
sha256sum linus_steg.jpg
```

¿Coinciden? 

No. Aunque las imágenes se ven iguales, la versión con mensaje oculto tiene bytes distintos y el hash lo delata.

Hay un mensaje importante de Buenaventura Durruti para vosotros en una de las imagenes del directorio `durruti`. El mensaje ha sido introducido mediante el programa steghide, con contraseña "durruti". La imagen que contiene el mensaje se corresponde con el Hash (SHA256) `7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb`. ¿Qué archivo es? ¿Qué dice la frase? ¿Como automatizarías la búsqueda si tuvieses muchos archivos en carpetas y subcarpetas?

El archivo se llama imagen 27.jpg. Además, el mensaje de su interior es el siguiente: "Al Fascismo no se le discute, se le destruye." Buenaventura Durruti. Si quisiera automatizar la busqueda y conociese el hash, usaría un find para recorrer todo el árbol: 

```bash
find durruti -type f -exec sha256sum {} + | grep 7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb
```

 Si no conociesemos el hash, habria que probar la contraseña extrayendo cada imagen.

```bash
find durruti -type f -iname "*.jpg" | while read -r f; do
  if steghide extract -sf "$f" -p durruti -xf /tmp/salida.txt -f 2>/dev/null; then
    echo "Mensaje encontrado en: $f"
    cat /tmp/salida.txt
  fi
done
```

En este caso, para realizar el reto durruti, hemos seguido los siguientes pasos:

1. Encontrar el archivo: 
```bash
sha256sum durruti/* | grep 7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb
```

2. Extraer el mensaje
```bash
steghide extract -sf durruti/NOMBRE_DEL_ARCHIVO.jpg -p durruti
```

3. Leer el archivo con cat o less

## Contraseñas y sal

Ejecuta:

```bash
echo -n "ContrasenaSegura" | sha256sum
echo -n "ContrasenaSegura" | sha256sum
```

Observa que el resultado es idéntico.

Uso de sal con OpenSSL:

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

¿Cambian los Hashes?

SI, son completamente distintos, aunque la contraseña sea la misma. Solo ha cambiado la sal y, por el efecto avalancha, todo el hash cambia. Si ejecutas dos veces el comando con la misma sal, sale lo mismo: la sal en sí no lo aleatoriza, lo que aleatoriza es que cada usuario tenga una sal distinta.

En la carpeta `password_hash_demo` tienes una pequeña aplicación web con tres versiones de la misma funcionalidad:

- `plain`: almacena la contraseña en texto plano.
- `hashed`: almacena un hash SHA-256 de la contraseña.
- `salted`: almacena unq sal aleatoria y un hash PBKDF2-HMAC-SHA256.

Para ejecutarla:

```bash
cd password_hash_demo
docker compose up --build
```

Después abre:

- http://localhost:5001/ -> versión insegura (texto plano)
- http://localhost:5002/ -> versión con hash
- http://localhost:5003/ -> versión con sal

Registra el mismo usuario y la misma contraseña en las tres versiones y compara la base de datos o la información mostrada por cada servicio. Fíjate en que:

- En texto plano se ve la contraseña original;
- Con hash, la misma contraseña produce el mismo valor hash para todos los usuarios;
- Con sal, cada usuario tiene una sal distinta, por lo que iguales contraseñas no generan el mismo valor almacenado.

Despliega el proyecto en tu servidor Google Cloud y comprueba que funciona correctamente, y que puedes cambiar la sal a un número definido por tí.

Pasos a seguir:

1. Levantar los servicios:
```bash
cd password_hash_demo
docker compose up --build
```
Nota: Si docker compose no funciona, prueba docker-compose.

2. Registrar el mismo usuario en las tres versiones

Abre el navegador y accede a los 3 sitios web. EN cada una, registra el mismo usuario y la misma contraseña. Para ver bien la diferencia, registra dos usuarios distintos con la misma contraseña en cada versión.

3. Conectate a la máquina
```bash
ssh usuario@IP_DE_TU_SERVIDOR
```

4. Instalar Docker en el servidor y darle permisos
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
```
Cierra sesión y vuelve a entrar

5. Llevar el proyecto al servidor
Dos opciones: clonar el repositorio con git clone o copiar la carpeta desde tu máquina con scp:
```bash
scp -r password_hash_demo usuario@IP_DE_TU_SERVIDOR:~/
```

6. Abrir los puertos en el firewall

7. Arrancar y comprobar
```bash
cd password_hash_demo
docker compose up --build -d
```

8. Buscar donde se genera la sal
```bash
ls app_salted
grep -rn -i "salt" app_salted
```
9. Editar el archivo. 

Cambia la linea de "salt = secret.token_hex(16)" a "salt = "12345"". 

10. Reconstruir y arrancar
```bash
docker compose up --build -d
```

11. Comprobar

Si todo ha ido bien, deberíamos de ber la columna salt con el número en las dos filas y la columna hash con el mismo valor en las dos filas.

## Hashes y Git

Clona, si no lo has hecho ya, el repositorio de la asignatura (Usando SSH):

```bash
git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
cd cd EHU-SGSSI-01/
git log
```

¿Qué identifica el hash del commit?¿Por qué Git detecta cambios de contenido de forma eficiente?

El hash SHA-1 (o SHA-256 en versiones más recientes) de un commit en Git identifica de forma única e inequívoca todo el estado del proyecto en ese momento específico. Este hash se calcula a partir de:

1. El contenido completo del árbol de archivos (tree object)

2. Los metadatos del commit: autor, fecha, mensaje, etc.

3. El hash del commit padre (commits anteriores)

4. Cualquier cambio mínimo en cualquiera de estos elementos

Git utiliza las propiedades criptográficas de las funciones hash para optimizar la detección de cambios:

1. Comparación instantánea por hash

- En lugar de comparar archivo por archivo, Git compara los hashes
- Si dos archivos tienen el mismo hash SHA-1, son matemáticamente idénticos
- Si los hashes difieren, los archivos son definitivamente diferentes

En resumen: Git convierte la costosa operación de "comparar contenido completo" en la rápida operación de "comparar números hash", manteniendo al mismo tiempo la garantía matemática de que la comparación es 100% precisa.
