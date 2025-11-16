🐍 Proyecto CRUD Básico en Python
Python
pytest

Este proyecto es un ejemplo educativo y una plantilla minimalista para implementar las operaciones CRUD (Crear, Leer, Actualizar, Borrar) utilizando las estructuras de datos nativas de Python (diccionarios). Incluye un conjunto de pruebas automatizadas con pytest para garantizar la correcta funcionalidad del código.

Es ideal para principiantes que deseen entender los fundamentos de la manipulación de datos y las pruebas unitarias en Python.

📋 Tabla de Contenidos
Descripción del Proyecto
Características
Requisitos Previos
Instalación y Configuración
Estructura del Proyecto
Ejecución de las Pruebas
Uso del Proyecto
Contribuciones

🎯 Descripción del Proyecto
El núcleo de este proyecto es un conjunto de funciones que operan sobre un diccionario en memoria. Este diccionario actúa como una "base de datos" temporal, permitiéndonos realizar las cuatro operaciones fundamentales de persistencia de datos de forma sencilla y didáctica.

Crear (Create): Añadir un nuevo par clave-valor.
Leer (Read): Consultar el valor asociado a una clave.
Actualizar (Update): Modificar el valor de una clave existente.
Borrar (Delete): Eliminar un par clave-valor del diccionario.
El proyecto está diseñado para ser un punto de partida limpio y comprensible para aplicaciones más complejas.

✨ Características
✅ Operaciones CRUD completas.
🧪 Pruebas unitarias automatizadas con pytest.
📁 Estructura de proyecto simple y clara.
🐍 Código Python 3.7+ limpio y bien documentado.
🖥️ Instrucciones de configuración para Windows, macOS y Linux.
🔧 Requisitos Previos
Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

Python 3.7 o superior: Descargar Python
pip (gestor de paquetes de Python): Generalmente se instala con Python.
Git (opcional): Para clonar el repositorio. Descargar Git
🚀 Instalación y Configuración
Sigue estos pasos para poner el proyecto en marcha en tu máquina local.

1. Clonar el repositorio
Si usas Git, clona el repositorio. Si no, simplemente descarga el código fuente y descomprímelo.

git clone https://github.com/EstebanStudy/registro-productos-crud.git
cd registro-productos-crud.git

2. Crear y activar un entorno virtual
Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto de tu sistema global.

Abre una terminal en la carpeta del proyecto.
Crea el entorno virtual:
python3 -m venv .venv

Actívalo:
source .venv/bin/activate

3. Instalar dependencias
Con el entorno virtual activado (verás (.venv) al inicio de la línea de tu terminal), instala las dependencias necesarias desde el archivo requirements.txt:

pip install -r requirements.txt

Estructura del Proyecto
Una vez configurado, tu proyecto tendrá esta estructura:

proyecto-crud-python/
├── .venv/                 # Entorno virtual (creado por ti)
├── main.py                # Lógica principal: funciones CRUD
├── test_main.py           # Pruebas automatizadas para main.py
└── requirements.txt       # Lista de dependencias del proyecto (pytest)

🧪 Ejecución de las Pruebas
Para verificar que todo funciona correctamente, ejecuta el conjunto de pruebas usando pytest.

Opción 1: Ejecución simple
Este comando ejecutará todas las pruebas y te mostrará un resumen.

pytest

Opción 2: Ejecución detallada (recomendada durante el desarrollo)
Este comando detiene la ejecución en el primer fallo (--maxfail=1), deshabilita advertencias (--disable-warnings) y muestra el resultado de cada prueba de forma detallada (-v).

pytest --maxfail=1 --disable-warnings -v
