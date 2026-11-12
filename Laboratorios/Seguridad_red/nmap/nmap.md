# Laboratorio: NMap

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).

## NMap

[Nmap](https://nmap.org/) es un programa de código abierto que sirve para rastrear puertos y máquinas en una red (probablemente sea la herramienta de hacking que aparece en más películas: [https://nmap.org/movies/](https://nmap.org/movies/)). Con Nmap se pueden descubrir fácilmente muchas características de las máquinas que están visibles en la red: qué máquinas están encendidas, qué puertos tiene abiertos una máquina concreta, qué servicios está ejecutando y qué versiones de los mismos, qué sistema operativo y qué versión usa, etc.

Instala NMap:

```bash
sudo apt install nmap traceroute -y
```

Describe los comandos necesarios para descubrir lo siguiente:

> ¿Qué puertos están abiertos en `scanme.nmap.org` y en tu servidor de Google Cloud, qué servicios y qué versión de esos servicios?

Primero, he decidido escanear los 1000 puertos más comunes y ver cuales estan abiertos con: 

```bash
nmap scanme.nmap.org
```

Después, para el primero, he averiguado que los puertos 22, 80 y 9929 estan abiertos y utilizan respectivamente las últimas versiones de los servicios SSH, HTTP y NPING-ECHO. Para saber eso, he utilizado el siguiente comando:

```bash
nnmap -sV scanme.nmap.org
```

De la misma forma, he descubierto que en mi VM estan abiertos los puertos 22 y 443, utilizando respectivamente las versiones OpenSSH 10.2 y Apache 2.4.66 y servicios SSH y SSL/HTTP. El comando ha sido:

```bash
nnmap -sV IP_DE_TU_VM
```

Si ocurre que el escaneo normal no puede ver los puertos Docker, entonce sintroducelos manualmente. Por ejemplo:

```bash
nmap -sV -p 21,22,80,81,443,8889,8890 IP_DE_TU_VM
```

> ¿Qué máquinas están activas en la red desde tu máquina hasta tu servidor remoto? (Pista: traceroute).

```bash
traceroute -n IP_DE_TU_VM
```

Con esto, muestra cada salto (hop) del camino: router, equipos del operador, los de Google, hasta llegar a la VM. Las líneas con *** son routers que no responden.

```bash
sudo nmap -sn --traceroute IP_DE_TU_VM
```

Este otro comando sirve para ver unicamente las máquinas activas. EN mi caso, tengo 2 máquinas activas.

> ¿Qué puertos tiene abiertos una de las máquinas activas de la red?

```bash
nmap Ip_router
```

En mi caso: 23, 53, 80, 443, 52869.

> ¿Qué versiones de los servicios está usando una de las máquinas activas de la red?

```bash
nmap -sV Ip_router
```

> ¿Qué sistema operativo tiene una de las máquinas activas de la red?

```bash
sudo nmap -O Ip_router
```

> ¿Qué sistema operativo tiene tu servidor en Google Cloud (según NMap)?

```bash
sudo nmap -O IP_DE_TU_VM
```
Si teienes fallos para que te responda, suele ser porque casi todos los puertos estan filtrados. Prueba a hacer la detección con al menos un puerto abierto y otro cerrado.

```bash
sudo nmap -O --osscan-guess -p 22,81 IP_DE_TU_VM
```

> ¿Qué sistema operativo tiene `scanme.nmap.org`?

```bash
sudo nmap -O scanme.nmap.org
```

> Una vez determinado el sistema operativo, ¿qué vulnerabilidades tiene? (Pista: [https://cve.mitre.org](https://cve.mitre.org/)).

```bash
nmap -sV --script vuln -p 22,81,8890 $VM -oN p8-vulnerabilidades.txt
```

> ¿Cómo se puede usar NMap para detectar si una máquina tiene un firewall?

Si encuentra un puerto filtered, indica que esta filtrando algo por una firewall. Para comprobarlo:


```bash
nmap --reason -p 22,80,81,8889,8890 $VM -oN p9-reason.txt
sudo nmap -sA -p 22,80,81,8889,8890 $VM -oN p9-ack.txt
```