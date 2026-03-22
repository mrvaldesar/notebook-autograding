# AI Autograder Platform 🎓🤖

Una plataforma académica avanzada y multiusuario para la evaluación automática, justa y reproducible de notebooks Jupyter (`.ipynb`) en cursos de Inteligencia Artificial y Ciencia de Datos.

## 🌟 Características Principales

*   **Autenticación y Roles (RBAC):** Accesos definidos para **Profesores** y **Estudiantes**.
*   **Gestión Académica:** Creación de cursos, asignaciones y rúbricas de evaluación dinámicas.
*   **Sistema de Invitaciones (SMTP):** Los profesores pueden invitar a los estudiantes mediante un enlace seguro por correo electrónico para que se registren.
*   **Sandbox de Ejecución (Autograding):** El núcleo del sistema. Ejecuta el código de los estudiantes en contenedores **Docker efímeros** y aislados.
    *   Soporte para múltiples entornos (Básico: Numpy, Pandas, Sklearn | Deep Learning: PyTorch, TensorFlow).
    *   Evaluación de modelos contra **datasets ocultos (test sets)**.
    *   Ejecución asíncrona mediante **Celery + Redis** para no bloquear la interfaz web.
*   **Versionado de Entregas:** Los estudiantes pueden subir múltiples versiones de un mismo notebook; todas quedan registradas en el historial.
*   **Auditoría Completa:** Registro inmutable de inicio de ejecución, notas calculadas, fallos del sistema y overrides manuales para garantizar trazabilidad y transparencia.
*   **Dashboards Modernos:** Interfaz construida en **React** (Material-UI) con vistas adaptadas a cada rol.

---

## 🛠️ Stack Tecnológico

**Backend (Autograder Core & API):**
*   [FastAPI](https://fastapi.tiangolo.com/) (Python) - API rápida y asíncrona.
*   [SQLAlchemy](https://www.sqlalchemy.org/) & [Alembic](https://alembic.sqlalchemy.org/) - ORM y migraciones.
*   [PostgreSQL](https://www.postgresql.org/) - Base de datos relacional robusta.
*   [Celery](https://docs.celeryq.dev/) + [Redis](https://redis.io/) - Colas de tareas asíncronas para la ejecución de notebooks.
*   [Docker](https://www.docker.com/) (SDK for Python) - Orquestación de contenedores efímeros.

**Frontend:**
*   [React 18](https://reactjs.org/) + [TypeScript](https://www.typescriptlang.org/) (Vite).
*   [Material-UI (MUI)](https://mui.com/) - Componentes visuales y diseño responsivo.
*   [React Router Dom](https://reactrouter.com/) - Navegación.
*   [Axios](https://axios-http.com/) - Consumo de la API con interceptores de tokens JWT.

---

## 🚀 Guía de Configuración Rápida

### 1. Requisitos Previos
*   [Docker](https://docs.docker.com/get-docker/) y Docker Compose instalados.
*   Python 3.10+ instalado localmente.
*   Node.js 18+ instalado localmente.

### 2. Levantar la Infraestructura Base (DB & Redis)
Desde la raíz del proyecto, inicializa PostgreSQL y Redis usando Docker Compose:
```bash
docker-compose up -d
```

### 3. Configurar el Backend (FastAPI & Celery)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install email-validator
```

Configura tu archivo de variables de entorno `.env` en la carpeta `backend/`:
```env
POSTGRES_PASSWORD=password
SECRET_KEY=super_secret_key_change_in_production
SMTP_HOST=smtp.gmail.com
SMTP_USER=test@example.com
SMTP_PASSWORD=tu_password_de_aplicacion
FRONTEND_URL=http://localhost:5173
```

Inicia el servidor FastAPI:
```bash
# Iniciar la API
uvicorn main:app --reload --port 8000
```

En otra terminal (dentro del entorno virtual en `backend/`), inicia el worker de Celery:
```bash
# En Linux/macOS
celery -A app.worker.celery_app worker --loglevel=info

# En Windows (obligatorio usar --pool=solo para evitar errores de prefork / WinError 5)
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

### 4. Construir las imágenes Docker del Sandbox
Para que el Worker pueda evaluar, debes construir las imágenes base que usarán los contenedores efímeros:
```bash
cd backend/docker
docker build -t autograder_basic -f Dockerfile.basic .
docker build -t autograder_dl -f Dockerfile.deep_learning .
```

### 5. Configurar el Frontend (React)
Abre otra terminal:
```bash
cd frontend
npm install
npm run dev
```
La aplicación estará disponible en `http://localhost:5173`.

---

## 👥 Flujo de Uso

1.  **Profesor:** El administrador crea un usuario profesor directamente en la base de datos (o mediante un endpoint de superadmin).
2.  **Profesor -> Curso & Tarea:** Inicia sesión, crea un Curso y dentro crea una Tarea (Assignment) seleccionando el entorno Docker deseado.
3.  **Profesor -> Invita Estudiantes:** Usa el botón de "Invitar Estudiante" con su correo. El sistema (SMTP) envía un token firmado.
4.  **Estudiante -> Registro:** El estudiante abre el enlace del correo (`/register?token=...`), completa sus datos (Nombre, Carnet, Password) y crea su cuenta.
5.  **Estudiante -> Entrega:** Ve la tarea asignada y sube su archivo `.ipynb`.
6.  **Autograding Mágico:** FastAPI guarda el archivo y encola la tarea. Celery despierta, levanta un contenedor Docker, inyecta el notebook y el test-set del profesor, ejecuta el código asíncronamente, lo destruye, extrae el output, aplica la rúbrica y guarda la nota y el log de auditoría en la base de datos.
7.  **Resultados:** El estudiante ve su nota inmediatamente reflejada en su Dashboard.

## 🔐 Seguridad y Notas
*   **Sandbox Seguro:** Los contenedores se ejecutan sin montar la raíz del sistema host y se eliminan automáticamente tras finalizar (`remove=True`).
*   **Manejo de Archivos:** Las rutas de los archivos (Uploads) y los Datasets Ocultos se limpian usando `os.path.basename` para evitar Path Traversals.
*   **Logs de Auditoría:** Todas las acciones de evaluación están protegidas mediante registros de tipo Add-Only.

---
Construido con ❤️ para el ecosistema educativo de IA.
