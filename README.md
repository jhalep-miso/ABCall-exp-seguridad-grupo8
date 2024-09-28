# Proyecto de Microservicios ABCall - Grupo 8

Este proyecto contiene varios microservicios y utiliza Nginx como API Gateway para redirigir las solicitudes a los microservicios correspondientes. 

TODO

## Requisitos Previos

- Python 3.x
- Pip
- Virtualenv
- Docker
- docker-compose

## Configuración del Ambiente

### Paso 1: Clonar el Repositorio

Clona este repositorio en tu máquina local:

```sh
git clone https://github.com/jhalep-miso/ABCall-exp-seguridad-grupo8.git
cd ABCall-exp-seguridad-grupo8
```

### Paso 2: Crear y Activar un Entorno Virtual

Crea un entorno virtual y actívalo:

```sh
python -m venv venv
venv\Scripts\activate
```
### Paso 3: Instalar los Requisitos

```sh
pip install -r requirements.txt
```

## Configuración y Ejecución de los Microservicios


### 1: Ejecuta el comando para levantar los contenedores

```sh
docker-compose up --build
```

### 2: Ejecuta el script para simular modificaciones de integridad al servicio de facturas en otra terminal
TODO

```sh
./simulate-modifications.sh
```

Si la ejecución da problemas por falta de permisos puedes ejecutar el comando 

```
chmod +x ./simulate-modifications.sh 
```

### 3: Verificar que los archivos de logs están generándose y guardándose en la carpeta logs

```
ls logs
```

# 4: Generar visualización de modificaciones no autorizadas vs detección de las mismas
Una vez hayan suficientes logs disponibles puedes ejecutar el siguiente comando para visualizar las fallas generadas y su detección

```
python plot.py
```

# Finalizar la ejecución
Puedes detener la simulación de fallas usando Ctrl+C en la terminal donde se está ejecutando

Los microservicios pueden detenerse usando el comando
```
docker-compose down
```

### Solución de Problemas

- Si tienes problemas con puertos ya utilizados, puedes modificarlos en el archivo `docker-compose.yml`