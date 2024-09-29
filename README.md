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


## Autenticación y Autorización

El sistema implementa autenticación mediante JWT para usuarios y servicios. Aquí te mostramos cómo interactuar con los microservicios usando autenticación:

### Registrar un usuario

```sh
curl --location 'http://localhost:5002/auth/register' \
--header 'Content-Type: application/json' \
--data '{
  "username": "newuser",
  "password": "newpassword"
}'
```

### Hacer login de usuario

```sh
curl --location 'http://localhost:5002/auth/login' \
--header 'Content-Type: application/json' \
--data '{
  "username": "newuser",
  "password": "newpassword"
}'
```

### Intentar crear una factura sin el token (esperado: error)

```sh
curl --location 'http://127.0.0.1:5051/facturas' \
--header 'Authorization: Bearer 1234' \
--header 'Content-Type: application/json' \
--data '{
  "usuario_id": 1,
  "nombre": "Factura de prueba",
  "monto": 100.50,
  "detalle": "Detalles de la factura de prueba"
}'

```
Respuesta esperada:

```json
{
    "message": "Token no valido - No ingresar directamente al servicio"
}
```

### Crear Factura con el token correcto

Una vez hayas hecho login y obtenido el token, usa ese token para crear una factura:

```sh
curl --location 'http://localhost:5053/facturas' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <tu_token_jwt>' \
--data '{
  "usuario_id": 1,
  "nombre": "Factura de prueba",
  "monto": 100.50,
  "detalle": "Detalles de la factura de prueba"
}'
```

### Consultar todas las facturas del usuario autenticado

```sh
curl --location 'http://localhost:5053/mis-facturas' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <tu_token_jwt>'
```

Validación:

El sistema debe devolver solo las facturas asociadas al usuario autenticado.

```json
{
  "facturas": [
    {
      "id": 1,
      "nombre": "Factura de prueba",
      "monto": 100.50,
      "detalle": "Detalles de la factura de prueba",
      "estado": "pendiente"
    }
  ]
}
```
