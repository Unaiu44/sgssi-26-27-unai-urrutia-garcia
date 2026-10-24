# Laboratorio: TOR, ONION

## Requisitos previos

- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Servidor remoto Google Cloud configurado, con Apache funcionando y el firewall permitiendo conexiones.

## Deep Web

La red habitual y conocida (Clearnet) está formada por direcciones conocidas (Ej: www.ehu.eus), con contenidos en HTML que están indexados y permiten realizar búsquedas para encontrar lo que nos interese.

La Deep Web (internet profunda) está formada por todos aquellos contenidos que no son directamente accesibles a través de internet. Se estima que de todo el contenido que existe:

- El 10% está en Clearnet (el internet que conocemos).
- El 90% está en la Deep Web.

Contenido de la Deep Web:

- Información confidencial o protegida (No suelen estar indexados por buscadores ni se puede acceder directamente a ellos): registros sanitarios, registros académicos, datos bancarios, etc.
- Información "suelta": por ejemplo un archivo HTML que no esté enlazado desde ningún otro.
- Información en formatos no HTML que un navegador no puede leer.
- Contenido no publicable (Censura): contenidos que no pueden publicarse libremente porque pueden acarrear consecuencias.
- Contenido ilegal y/o desagradable (Darknet): tráfico de armas, drogas, personas; material pedófilo; malware; alquiler de hackers, matones, etc.; películas snuff.

Para acceder a la Deep Web hace falta un software especial que proporcione privacidad, anonimato y ejerza de proxy.

Existen varias alternativas que darán acceso a distintos contenidos de la Deep Web: TOR, I2P, Freenet, Zeronet, etc.

## TOR

TOR (The Onion Router) ofrece un método para navegar de forma segura, ya que se oculta la IP de fuente y destino de los nodos que forman la [red](https://community.torproject.org/). Los sitios Onion son direcciones alfanuméricas muy largas, no legibles para humanos, a las que se puede acceder mediante HTTP(S), después de que los paquetes hayan viajado por varios nodos ONION, ocultando el origen y destino de los paquetes. 

Cada vez que hay que hacer una conexión, se calcula un camino aleatorio basado en los nodos de la red:

![TOR](tor.png)

La información se cifra a capas (como una cebolla) con las claves públicas de los distintos nodos, de modo que cada nodo sólo puede ver cuál es el siguiente:

![capas](capas.png)

Utilizando la red TOR se puede acceder a URLs que son inaccesibles de otro modo:

- Dominio `.onion`.
- URLs alfanuméricas: `http://3g2upl4pq6kufc4m.onion/`.

Para encontrar contenidos hay que usar buscadores específicos o sitios donde se recopilen las URLs:

- Buscador Torch (`http://xmh57jrzrnw6insl.onion/`).
- The Hidden Wiki (`http://kpvz7ki2v5agwt35.onion`).

## Navegador TOR

Para acceder a sitios ONION hay que usar un navegador TOR. Descarga el [navegador TOR oficial](https://www.torproject.org/download/) y úsalo para conectarte a [diferentes sitios](https://community.torproject.org/es/onion-services/), como por ejemplo el [New York Times](https://www.nytimesn7cgmftshazwhfgzm37qxb44r64ytbb2dj3x62d2lljsciiyd.onion/).

> ¿Por qué crees que abundan los periódicos entre los sitios que ofrecen servicios ONION?

Los medios ofrecen servicios onion para que sus lectores accedan sin que nadie sepa que leén, y para sortear la censura en países que bloquean sus webs. También permiten que fuentes y informantes contacten con la redacción de forma anónima.

## Servicio ONION en Google Cloud

### Instalar TOR

Para instalar TOR en el servidor sigue las [instrucciones comunes](https://community.torproject.org/onion-services/setup/install/) (Hay que tener en cuenta que para instalar TOR hay que configurar unos [repositorios APT específicos](https://support.torproject.org/apt/tor-deb-repo/)).

Un vez instalado TOR, para verificar su funcionamiento, ejecutar en el servidor:

```bash
curl -x socks5h://localhost:9050 -s https://check.torproject.org/api/ip
```

Debería devolver algo así:

```json
{"IsTor":true,"IP":"xxx.xxx.xxx.xxx"}
```

Para realizar esta parte de la práctica, solo hay que seguir las ordenes del enunciado. Si el link no os funciona, probar con este: https://support.torproject.org/little-t-tor/getting-started/installing/ . Para hacer las comprobaciones, utiliza los comandos de esta parte de la práctica.

### Configurar servicio ONION

Sigue las [instrucciones comunes](https://community.torproject.org/onion-services/setup/) para configurar el servicio ONION. Ten en cuenta que:

- Apache debe estar funcionando y el firewall debe permitir conexiones. Conviene crear una página web nueva para verificar la conexión mediante ONION.
- Hay que editar el archivo de configuración de TOR para añadir un nuevo Hidden Service.
- Para comprobar la conexión ONION deberás usar la dirección ONION generada en el Hidden Service y el navegador TOR.

Esta es la parte más dificil y extensa de la práctica. Para ello, debemos de suponer que ya hemos realizado exitosamente el anterior laboratorio donde configuramos una pagina web en Apache. Si es así, sigue los siguientes pasos:

1. Crear página web de prueba en Apache

Desde la maquina virtual ejecuta el siguiente comando: 

```bash
sudo nano /var/www/html/onion.html
```

Y una vez dentro, escribe lo que quieres que salga en la pagina web, por ejemplo:

```html
<h1>Mi servicio onion funciona</h1>
<p>Si ves esto desde el Navegador Tor, la practica esta lista.</p>
```

Para comprobar que Apache la sirve, ejecuta:

```bash
curl http://localhost/onion.html
```

Si te aparece solo las líneas de la web, entonces es correcto, sino, es posible que no te funciones porque Apache en practicas anteriores hacia redirecciones de HTTP a HTTPS, y eso en esta práctica nos estorba. Por ello, sigue estos pasos:

1.1 Hacer que Apache escuche en el puerto 8080:

```bash
sudo nano /etc/apache2/ports.conf
```

Aañdir al final del archivo: Listen 127.0.0.1:8080

1.2 Crear el sitio para onion:

```bash
sudo nano /etc/apache2/sites-available/onion.conf
```

Y escribe dentro:

```
<VirtualHost 127.0.0.1:8080>
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/onion_error.log
    CustomLog ${APACHE_LOG_DIR}/onion_access.log combined
</VirtualHost>
```

1.3 Activar el sitio y recargar Apache

```bash
sudo a2ensite onion.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

1.4 Probar que funciona:

```bash
curl http://127.0.0.1:8080/onion.html
```

Ahora que sabemos que funciona, seguimos.

2. Decirle a Tor que cree el servicio onion:

```bash
sudo nano /etc/tor/torrc
```

Veras un archivo muy largo. TIenes que buscar dos lineas y quitarles el #. Las lineas son:

```
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:80
```

Nota: Si creaste el puerto 8080, deberas de poner solo el segundo 80 a 8080. 

3. Reiniciar tor y revisar estado:

```bash
sudo systemctl restart tor
sudo systemctl status tor
```

Si todo es correcto, deberia aparecer 'active' en verde.

4. Leer tu dirección onion:

```bash
sudo cat /var/lib/tor/hidden_service/hostname
```

Si todo es correcto, debería mostrar algo como: abcdefghijklmnopqrstuvwxyz234567abcdefghijklmnopqrstuvwx.onion

5. Visitarla con el Navegador Tor:

Para ello, descargala desde: https://www.torproject.org/download/

Una vez descargada, deberas de buscar el archivo 'start-tor-browser.desktop'. Puedes ejecutarlo desde la terminal si te metes en la carpeta y pones:

```bash
./start-tor-browser.desktop
```

Te saldra una nueva pestaña y pulsa en 'Continuar'.

Por último, pon en el navegador: http://TU_DIRECCION.onion/onion.html.

La dirección la has sacado en el cuarto paso. Es posible que tarde un poco en conectar, pero si has hecho todo bien, te saldra la página web que creaste.

