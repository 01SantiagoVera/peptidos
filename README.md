# Antimicrobial Predictor

## Descripción

**Antimicrobial Predictor** es una aplicación web diseñada para predecir péptidos antimicrobianos a partir de secuencias de aminoácidos utilizando modelos de aprendizaje automático. Los modelos implementados incluyen **SVM**, **Random Forest**, y **Redes Neuronales**.

El proyecto está desarrollado con **Flask** para el backend y utiliza **Bootstrap** en el frontend. Los modelos de predicción están entrenados y guardados en formato `pickle`, y la aplicación permite cargar secuencias para hacer predicciones en tiempo real.

## Estructura del Proyecto

```bash
antimicrobial_predictor/
├── app/                       # Lógica principal de la aplicación (controladores, modelos, servicios)
│   ├── controllers/
│   │   ├── predictionController.py  
│   ├── models/
│   │   ├── predictionModel.py  
│   ├── services/
│   │   ├── predictionService.py  
│   ├── routes/
│   │   ├── web.py
│   │   ├── api.py
│   ├── config.py
├── config/                    # Configuraciones de la aplicación (variables de entorno, DB)
│   ├── config.py
├── database/
│   ├── db_mysql.py
├── static/                    # Archivos públicos accesibles por el servidor
│   ├── css/
│   ├── js/
│   ├── images/
├── resources/                 # Recursos compartidos (vistas, plantillas)
│   ├── views/                 # Plantillas HTML
│   │   ├── index.html
│   │   ├── layout
│   │   ├── partials/
├── tests/                     # Pruebas unitarias y funcionales
│   ├── test_prediction.py
├── app.py                     # Punto de entrada principal de la app
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación del proyecto
├── .gitignore                 # Archivos a ignorar por Git
└── .env                       # Variables de entorno (credenciales DB, claves API)
```

## Requisitos Previos
- Python 3.10+
- Pip (administrador de paquetes de Python)
- Flask (instalado mediante requirements.txt)

## Instalación
### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/01SantiagoVera/peptidos.git
cd antimicrobial_predictor
```
### Paso 2: Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate      # En Windows
```
### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```
### Paso 4: Configurar variables de entorno
Crear un archivo .env en la raíz del proyecto y agregar tus credenciales:
```bash
SECRET_KEY=mysecretkey
DATABASE_URL=mysql://user:password@localhost/db_name
```
### Paso 5: Ejecutar la aplicación

abre una terminal dentro del directorio del proyecto y ejecuta:
```bash
python app.py
```
La aplicación estará disponible en http://localhost:5000.

## Uso
1. Accede a la interfaz web donde podrás ingresar secuencias de aminoácidos.
2. La aplicación enviará la secuencia al backend y realizará predicciones utilizando los modelos de aprendizaje automático (SVM, Random Forest y Redes Neuronales).
3. Los resultados de la predicción se mostrarán en la interfaz de usuario.

## Estructura del Código
- `app/`: Contiene la lógica principal del proyecto, como controladores, modelos, y servicios.
- `config/`: Almacena las configuraciones globales de la aplicación.
- `database/`: Gestión de la base de datos, incluida la conexión a MySQL.
- `public/`: Recursos públicos como CSS, JavaScript y archivos de imagen.
- `resources/`: Contiene las vistas HTML.
- `tests/`: Pruebas unitarias y funcionales.
- `app.py`: Punto de entrada principal de la aplicación Flask.

## Pruebas
Para ejecutar las pruebas unitarias y funcionales, puedes usar el siguiente comando:
```bash
python -m unittest discover -s tests
```
