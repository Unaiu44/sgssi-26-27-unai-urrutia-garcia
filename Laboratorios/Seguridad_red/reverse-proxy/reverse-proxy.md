# Laboratorio: Proxy inverso en Google Cloud

## Requisitos previos

- Proyecto de Google Cloud con créditos activos (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).
- Pareja de claves SSH pública y privada.

## Introducción

Este laboratorio despliega un servidor web protegido por un proxy inverso mediante Squid, con dos niveles de red separados:

- **Nivel proxy**: una instancia Compute Engine con Squid, accesible desde internet por SSH y HTTP. Es el único punto de entrada.
- **Nivel backend**: una instancia Compute Engine con Apache, sin IP externa, accesible únicamente desde el proxy.

El objetivo es practicar cómo un proxy inverso oculta y protege al servidor real, y cómo puede almacenar en caché sus respuestas.

## Crear la red VPC y las subredes

En el menú de navegación, ir a `VPC network` > `VPC networks` > `Create VPC network`:

- Nombre: `proxy-vpc`.
- Modo de creación de subredes: `Custom`.
- Añadir una subred:
  - Nombre: `proxy-subnet`.
  - Región: una región dentro de Europa.
  - Rango de direcciones IPv4: `10.0.1.0/24`.
- Añadir una segunda subred:
  - Nombre: `backend-subnet`.
  - Región: la misma región que `proxy-subnet`.
  - Rango de direcciones IPv4: `10.0.2.0/24`.

Pulsar `Create`.

## Crear las reglas de firewall

Ir a `VPC network` > `Firewall` > `Create firewall rule`.

Regla para el nivel proxy:

- Nombre: `proxy-allow-web`.
- Red: `proxy-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `proxy-server`.
- Filtro de origen: `IPv4 ranges`, rango `0.0.0.0/0`.
- Protocolos y puertos: `TCP`, puertos `22, 80`.

Regla para el nivel backend:

- Nombre: `proxy-allow-backend`.
- Red: `proxy-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `backend-server`.
- Filtro de origen: `IPv4 ranges`, rango `10.0.1.0/24` (la subred `proxy-subnet`).
- Protocolos y puertos: `tcp`, puerto `80`.

Regla para administrar el backend a través del proxy (SSH):

- Nombre: `proxy-allow-backend-ssh`.
- Red: `proxy-vpc`.
- Dirección de tráfico: `Ingress`.
- Destinos: `Specified target tags`, etiqueta `backend-server`.
- Filtro de origen: `IPv4 ranges`, rango `10.0.1.0/24` (la subred `proxy-subnet`).
- Protocolos y puertos: `tcp`, puerto `22`.

## Crear Cloud NAT para el backend

El backend no tiene IP externa, pero necesita salir a internet para instalar Apache. Ir a `Network services` > `Cloud NAT` > `Get started`:

- Nombre de la pasarela: `backend-nat`.
- Red: `proxy-vpc`.
- Región: la misma que `backend-subnet`.
- Cloud Router: `Create new router`, nombre `backend-router`.

Pulsar `Create`.

## Crear la instancia del servidor backend

Ir a `Compute Engine` > `VM instances` > `Create instance`.

- Nombre: `backend-web`.
- Región/zona: la misma región que `backend-subnet`.
- Serie: `E2`, tipo de máquina: `e2-micro`.
- `OS and storage`: `Ubuntu 26.04 LTS Minimal` como sistema operativo.
- `Networking`:
  - Etiqueta de red: `backend-server`.
  - En `Network interfaces`, seleccionar la red `proxy-vpc` y la subred `backend-subnet`.
  - IP interna primaria: reservar una IP interna estática (`Reserve static internal IP address`) con la dirección `10.0.2.10`.
  - IP externa: `None`.
- `Security` > `Manage access`: añadir la clave pública SSH (`Add manually generated SSH keys`).
- `Advanced options` > `Management` > `Automation`: pegar el siguiente script de arranque:

```bash
sudo apt-get update
sudo apt-get install -y apache2
echo "<h1>Servidor backend: $(hostname)</h1>" | sudo tee /var/www/html/index.html
sudo systemctl restart apache2
```

Crear la instancia. Esperar a que arranque.

## Crear la instancia del proxy inverso

Ir a `Compute Engine` > `VM instances` > `Create instance`.

- Nombre: `proxy-web`.
- Región/zona: la misma región que `proxy-subnet`.
- Serie: `E2`, tipo de máquina: `e2-micro`.
- `OS and storage`: `Ubuntu 26.04 LTS Minimal` como sistema operativo.
- `Networking`:
  - Activar el tráfico HTTP (`Allow HTTP traffic`).
  - Etiqueta de red: `proxy-server`.
  - En `Network interfaces`, seleccionar la red `proxy-vpc` y la subred `proxy-subnet`.
  - Reservar una IP externa estática (`External IPv4 address` > `Reserve static external IP address`).
- `Security` > `Manage access`: añadir la clave pública SSH (`Add manually generated SSH keys`).
- `Advanced options` > `Management` > `Automation`: pegar el siguiente script de arranque, que instala Squid y lo configura como proxy inverso del backend `10.0.2.10`:

```bash
sudo apt-get update
sudo apt-get install -y squid
sudo tee /etc/squid/squid.conf > /dev/null <<'CONF'
http_port 80 accel defaultsite=10.0.2.10 no-vhost
cache_peer 10.0.2.10 parent 80 0 no-query originserver name=backend
acl all_sites src all
http_access allow all_sites
cache_peer_access backend allow all_sites
cache_mem 64 MB
CONF
sudo systemctl restart squid
```

Crear la instancia. Visitar `http://IP_EXTERNA_PROXY` y debería aparecer la página del servidor backend, aunque este no tenga IP externa.

## Probar el proxy inverso

1. Desde el equipo local, comprobar las cabeceras añadidas por Squid y la caché (repetir el comando dos veces):

```bash
curl -I http://IP_EXTERNA_PROXY
```

   Deben aparecer las cabeceras `Via` y `X-Cache`. En la primera petición `X-Cache: MISS`, y en las siguientes `X-Cache: HIT`, lo que indica que el proxy responde sin consultar al backend.

HTTP/1.1 200 OK

Content-Length: 39

Content-Type: text/html

Date: Tue, 03 Nov 2026 15:57:15 GMT

Server: Apache/2.4.66 (Ubuntu)

Last-Modified: Tue, 03 Nov 2026 15:45:41 GMT

ETag: "27-65f6127a66f0d"

Accept-Ranges: bytes

Age: 5

Cache-Status: proxy-web;hit;detail=match

Via: 1.1 proxy-web (squid/7.7)

Connection: keep-alive


2. Comprobar que el backend no es accesible directamente: no tiene IP externa, y `curl http://10.0.2.10` solo funciona desde `proxy-web`.

3. Conectarse por SSH a `proxy-web` y consultar el registro de Squid: `sudo tail /var/log/squid/access.log`. Se verán las peticiones con `TCP_MISS` y `TCP_HIT`/`TCP_MEM_HIT`.

1793721189.616      4 82.130.129.208 TCP_MISS/200 363 GET http://10.0.2.10/ - FIRSTUP_PARENT/10.0.2.10 text/html

1793721189.759      1 82.130.129.208 TCP_MISS/404 569 GET http://10.0.2.10/favicon.ico - FIRSTUP_PARENT/10.0.2.10 text/html

1793721435.273      3 82.130.129.208 TCP_REFRESH_UNMODIFIED/200 333 HEAD http://10.0.2.10/ - FIRSTUP_PARENT/10.0.2.10 text/html

1793721440.388      0 82.130.129.208 TCP_MEM_HIT/200 333 HEAD http://10.0.2.10/ - HIER_NONE/- text/html

4. Desde `proxy-web`, conectarse por SSH a `backend-web` (`ssh USUARIO@10.0.2.10`, con reenvío de agente `ssh -A`) y consultar `sudo tail /var/log/apache2/access.log`: solo aparece la IP del proxy (`10.0.1.x`) como cliente, y las peticiones en caché no llegan.

10.0.1.2 - - [03/Nov/2026:15:52:38 +0000] "GET /squid-internal-dynamic/netdb HTTP/1.1" 404 528 "-" "-"

10.0.1.2 - - [03/Nov/2026:15:53:09 +0000] "GET / HTTP/1.1" 200 322 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"

10.0.1.2 - - [03/Nov/2026:15:53:09 +0000] "GET /squid-internal-periodic/store_digest HTTP/1.1" 404 528 "-" "-"

10.0.1.2 - - [03/Nov/2026:15:53:09 +0000] "GET /favicon.ico HTTP/1.1" 404 527 "http://34.118.106.89/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0"

10.0.1.2 - - [03/Nov/2026:15:57:15 +0000] "HEAD / HTTP/1.1" 304 248 "-" "curl/8.5.0"

10.0.1.2 - - [03/Nov/2026:15:58:09 +0000] "GET /squid-internal-periodic/store_digest HTTP/1.1" 404 528 "-" "-"

## Limpieza

Para evitar costes, eliminar las dos instancias, la IP estática del proxy, la pasarela `backend-nat` y el router `backend-router`, las reglas de firewall y la red `proxy-vpc`.
