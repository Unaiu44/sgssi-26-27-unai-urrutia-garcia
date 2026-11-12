# Laboratorio: Firewall

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud.

## Firewall Google Cloud

En este laboratorio desplegaréis vuestro sistema web en el servidor remoto de Google Cloud para aprender a configurar el acceso al mismo a través del firewall que provee Google Cloud por defecto. Para desplegar el proyecto web en el servidor remoto hay que instalar Docker y Docker Compose. Clonad el proyecto web en el servidor de Google Cloud (una vez establecida la conexión SSH): 

```bash
git clone https://github.com/mikel-egana-aranguren/docker-lamp.git
```

Construid la imagen web:

```bash
docker build -t="web" .
```

Desplegad la aplicación mediante Docker Compose:

```bash
docker-compose up
```

Para poder acceder a nuestro proyecto, cargar los datos mediante phpMyAdmin y ver la página web, tenemos que abrir ciertos puertos.

> ¿En qué puertos escucha nuestro proyecto? (Pista: `netstat`).

Se escucha lo siguiente: docker-lamp-web-1 en el puerto 81 (al 80 interno), que es la página web; docker-lamp-phpmyadmin-1 enel puerto 8890 (al 80 interno), que sirve para gestionar la base de datos; y docker-lamp-db-1 en el puerto 8889 (al3306 interno), que es la base de datos MariaDB.

Una vez hayamos comprobado los puertos en los que nuestro proyecto está escuchando, tenemos que abrirlos para poder acceder desde el exterior.

> ¿Cómo se pueden abrir esos puertos en Google Cloud? (Pistas: red de VPC, etiqueta `http-server`, `0.0.0.0/0`).

En un firewall también es posible impedir el tráfico entrante, no solo permitirlo.

> ¿Cómo cerrarías los puertos 80 y 443 al tráfico entrante?

Hay dos formas:

- Opción A: desactivar o borrar las reglas quelos abren. En Firewall busca 'default-alow-http' y 'default-allow-https'. Si abres una, puedes pulsar 'Editar' y en 'Cumplimiento' ponerla como 'Inhabilitada'. Es reversible,y mejor que borrarla.

- Opción B: crear una regla de denegación con más prioridad. Es la más didáctica:

    1. Crear regla firewall
    2. Rellenar:
        - Nombre: deny-http-https
        - Red: default
        - Prioridad 900 (menor que 100, así gana a las reglas de permitir)
        - Dirección de tráfico: Entrada
        - Ación: Denegar
        - Destinos: Todas las instancias de la red
        - Intervalos de IPv4 de origen: 0.0.0.0/0
        -Protocolos y puertos: TCP, 80,443
    3. Crear

Cuidado con bloquear el puerto 22 ya que nos quedariamos sin accesso SSH.

Para comprobar que ha funcionado,poner el siguiente comando ntes y después de crear la regla:

```bash
curl -m 5 http://IP_EXTERNA:80
```

Además del tráfico entrante, en un firewall se puede bloquear el tráfico saliente.

> ¿Cómo impedirías el tráfico saliente a la página [https://en.wikipedia.org](https://en.wikipedia.org/) desde tu servidor de Google Cloud? (Pistas: `wget`, `ping`).

El firewall de Google Cloud permite por defecto todo el tráfico saliente. Para impedir el acceso a Wikipedia crearás una regla de salida que deniegue las conexiones hacia la IP de Wikipedia, con una prioridad que fane la regla imolícita de "permitir todo" (en mi caso, menor que 1000). De tal forma, haremos una regla firewall de salida de tipo denegar, con destino la IP de wikipedia.org. Para comprobar si ha funcionado, habra que ejecutar los comandos 'wget' y 'ping' antes y despues.

1. Instalar ping si no está ya instalado:

```bash
sudo apt install iputils-ping -y
```

2. Comprobar que Wikipedia responde ahora:

```bash
ping -c 3 en.wikipedia.org
wget --timeout=5 --tries=1 -O /dev/null https://en.wikipedia.org
```

Si todo ha ido bien, con el 'ping' veras que se envian 3 paquetes y hay 0% de perdida. Con wget, veras un 200 Ok.

3. Averiguar la IP (IPv4) de Wikipedia:

```bash
getent ahostsv4 en.wikipedia.org
```

4. Crear la regla firewall con los detalles mencionados anteriormente.

5. Comprobar que esta bloqueado (mismos comandos que el paso 2).

Por último, se puede bloquear el tráfico desde una dirección concreta.

> ¿Cómo impedirías el tráfico entrante en el puerto 8890 desde tu IP actual? (Pista: «What is my IP?»).

1. Averiguar tu IP:

```bash
curl ifconfig.me
```

2. Comprobar que ahora entras visitando la web http://IP_EXTERNA_VM:8890. Debe cargar phpMyAdmin.

3. Crear la regla firewall.

4. Comprobar que no carga (volver a visitar la web).

## IPTables

**IPTables** es un módulo perteneciente al kernel de Linux que permite actuar como firewall, ya que se encarga de filtrar los paquetes de datos que entran y salen de la máquina. IPTables funciona mediante reglas que tendremos que definir en función de lo que queramos hacer. Por defecto, las reglas definidas no son persistentes; esto es, al reiniciar el sistema se borran.

Para evitar tener que introducir una y otra vez las mismas reglas, se pueden guardar en un fichero mediante el siguiente comando:

```bash
sudo iptables-save > /home/user/fichero
```

O sino:

```bash
sudo iptables-save | sudo tee ~/reglas-ssh.v4 > /dev/null
```

Tras reiniciar la máquina, se pueden recuperar mediante:

```bash
sudo iptables-restore < /home/user/fichero
```

O sino:

```bash
sudo iptables-restore < ~/reglas-ssh.v4
```

Si quisiéramos que la restauración de reglas se hiciera de manera automática cada vez que se reiniciara el sistema, podríamos crear un script que se ejecutara al iniciar la máquina o modificar la configuración de red para que, al configurar las conexiones, se restauraran automáticamente las reglas de IPTables.

Definid las reglas necesarias para conseguir lo siguiente:

> Que vuestro servidor de Google Cloud solo acepte conexiones SSH desde el servidor de Google Cloud de otro alumno y desde vuestra máquina local.

Desde tu máquina virtual, asegurandote de tener IPTables instalado, ejecuta los siguientes comandos:

```bash
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -s TU_IP -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -s IP_COMPAÑERO -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j DROP
```

Si quieres comprobar que todo ha ido bien, te tendrian que salir si ejecutas:

```bash
sudo iptables -L INPUT -n --line-numbers
```

> Instalad un servicio FTP en vuestro servidor de Google Cloud y configuradlo para que solo acepte conexiones FTP desde máquinas de la red de `ehu.eus`.

1. Teniendo FTP instalado, debes primero editar este archivo para poder filtrar las dos conexiones:

```bash
sudo nano /etc/vsftpd.conf
```

Asegurate de que estas lineas existen y no tienen # delante:

local_enable=YES
write_enable=YES
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=40100
pasv_address=IP_EXTERNA_DE_TU_VM

Después, reinicia el servidor y comprueba que escucha:

```bash
sudo systemctl restart vsftpd
sudo ss -tlnp | grep :21
```

Crea un usuario de prueba porque tu usuario normal solo tiene clave SSH y no contraseña:

```bash
sudo adduser ftpalumno
```

2. Abrir los puertos en Google Cloud (crea una regla)

3. Averiguar el rango de IPs de la EHU:

```bash
host www.ehu.eus
whois 158.227.0.1 | grep -i -E "inetnum|netname|descr"
```

4. Reglas iptables:

```bash
sudo iptables -A INPUT -p tcp --dport 21 -s 158.227.0.0/16 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 40000:40100 -s 158.227.0.0/16 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 21 -j DROP
sudo iptables -A INPUT -p tcp --dport 40000:40100 -j DROP
```

5. Comprobar:

```bash
ftp IP_EXTERNA_VM
```

Desde tu ordenador hara 'timeout', perod esde los ordenadores de la uni debería de dejarte conectarte al usuario que has creado (ftpalumno).

> Que vuestro servidor de Google Cloud no acepte conexiones HTTP (solo HTTPS).

1. Inhabilita reglas que puedan tener conflicto con esta tarea (como denegar https), y asegurate que hay algo escuchando en los puertos 80 y 443:

```bash
sudo ss -tlnp | grep -E ":80 |:443 "
```

2. Regla iptables:

```bash
sudo iptables -A INPUT -p tcp --dport 80 -j DROP
```

3. Comprobar desde tu ordenador:

```bash
curl -m 5 http://IP_EXTERNA_VM
curl -m 5 -k https://IP_EXTERNA_VM
```

> Que en vuestra máquina local no se puedan hacer conexiones salientes a Twitter, Facebook ni YouTube.

1. Se recomienda guardar primero las iptables actuales de vuestro ordenador. Iptables nuevas:

```bash
for d in twitter.com www.twitter.com x.com facebook.com www.facebook.com youtube.com www.youtube.com; do
  sudo iptables -A OUTPUT -d $d -j REJECT
  sudo ip6tables -A OUTPUT -d $d -j REJECT
done
```

2. Comprobar:

```bash
curl -m 5 -I https://www.youtube.com
curl -m 5 -I https://www.ehu.eus
```
