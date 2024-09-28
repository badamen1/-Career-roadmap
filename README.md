# Career-roadmap

Bienvenido a Career-roadmap. Sigamos esta guía para una rápida introducción a nuestro proyecto.

## Tabla de contenidos
- [Acerca de](#acerca-de)
- [Cómo instalar](#cómo-instalar)
- [Licencia](#licencia)

## Acerca de

Career-roadmap es una aplicación web desarrollada por **Bayron Mena**, **Jesus Gomez** y **Jean Guillot** como parte del proyecto para “Ingeniería de Software” dirigido por la profesora **Elizabeth Monsalve**.

## Cómo instalar

Para tener una copia de nuestro proyecto, puedes seguir los siguientes pasos:

1. (Opcional) Haz un fork del repositorio.
2. Clona el repositorio.

   ```bash
   git clone https://github.com/badamen1/Career-roadmap.git
   ```

3. Asegúrate de estar en la carpeta:

   ```bash
   cd ./career_roadmap
   ```

4. Crea un entorno virtual en Python:

   ```bash
   python -m venv venv
   ```

5. Activa el entorno virtual:

   ```bash
   ./venv/scripts/activate
   ```

6. Instala las librerías requeridas usando el archivo `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

7. Obtén tu clave de API de OpenAI y guárdala en un archivo `.env` ubicado en la carpeta raíz del proyecto, con la siguiente estructura: `openai_apikey=<tu_clave_openai_api_key>`.

8. Hasta este punto, tu carpeta debería verse así:

   ```bash
   CAREER_ROADMAP/
   ├── career_roadmap/
   ├── roadmap/
   ├── venv/
   ├── .gitignore
   ├── .env
   ├── db.sqlite3
   ├── debug.log
   ├── manage.py
   ├── requirements.txt
   ```

9. Realiza las migraciones de la base de datos:

   ```bash
   python manage.py migrate
   ```

   Este paso creará un archivo `sqlite3`. Esta es la base de datos con todas las tablas y relaciones necesarias.

10. Ejecuta el servidor de desarrollo.

    ```bash
    python manage.py runserver
    ```

11. (Opcional) Para desactivar el entorno virtual después de trabajar:

    ```bash
    deactivate
    ```

## Licencia

Copyright 2024, Bayron Mena, Jesus Gomez, Jean Guillot. Todos los derechos reservados Career-Roadmap.
