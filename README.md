# Sistema de Legajos de Personal

## Instalacion y despliegue
    Instalar python3.9 en ubuntu 18.04
    - sudo apt update
    - sudo apt install software-properties-common
    - sudo add-apt-repository ppa:deadsnakes/ppa
    - sudo apt update 
    - sudo apt install python3.9
    Instalar el venv
    - sudo apt install python3.9-venv
    Crear el entorno virtual
    - python3.9 -m venv venv
## Configuracion
    Crear archivo .env y añadir las variables de entorno necesarias para el correcto 
    funcionamiento del proyecto. 
    Variables de entorno básicas:
    +---------------------------------+------------------------------------------------------+
    | ``DATABASE_URL``                | Es la cadena de conexión a la base de datos para     |
    |                                 | PostgreSQL se debe usar la siguiente sintaxys:       |
    |                                 | ``psql://user:password@host:port/database``          |
    +---------------------------------+------------------------------------------------------+
    | ``ALLOWED_HOSTS``                | "*"                                                 |
    +---------------------------------+------------------------------------------------------+

## Instalar requerimientos en virtualenv
- Activar el venv ubicandose dentro del proyecto: source venv/bin/activate 
- pip install -r requirements/base.txt

## Indicaciones para sysadmin

**EJECUTAR**

```
- python manage.py migrate
- python manage.py collectstatic
```

**EJECUTAR SEEDERS (en orden)** (DESDE LA RAIZ DEL PROYECTO)
```
- python manage.py loaddata apps/common/fixtures/ubigeo-pais.json
- python manage.py loaddata apps/common/fixtures/ubigeo-departamento.json
- python manage.py loaddata apps/common/fixtures/ubigeo-provincia.json
- python manage.py loaddata apps/common/fixtures/ubigeo-distrito.json
```
```
- python manage.py loaddata apps/common/fixtures/colegios-profesionales-peru.json
```
```
- python manage.py loaddata apps/persona/seeders/facultades.json
- python manage.py loaddata apps/persona/seeders/departamentos_academicos.json
- python manage.py loaddata apps/persona/seeders/docentes.json
- python manage.py loaddata apps/persona/seeders/datos_generales.json

x python manage.py loaddata apps/persona/seeders/usuarios.json (❌ No funciona)
  Solución: Ejecutar el script sql (postgresql) para insertar usuarios: 👍
    -> Esta ubicado en: apps/scripts-bd/usuarios.sql
```
**ARRANCAR LA APLICACION**
- python manage.py runserver 8080
