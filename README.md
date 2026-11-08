# QA Infra Portfolio — Docker & Kubernetes para QA Automation

Proyecto de portafolio que demuestra cómo **empaquetar, orquestar y automatizar
la ejecución de una suite de pruebas** usando Docker, Kubernetes y GitHub Actions.

El objetivo no es solo escribir tests, sino demostrar que sé integrarlos en el
ciclo de vida real de un equipo DevOps: imagen reproducible, ejecución efímera
en clúster y pipeline de CI con reportes.

## Stack

- **Python 3.13** + **pytest 8.3.4** + **requests**
- **Docker** — empaquetado de la suite y sus dependencias
- **Kubernetes** (Docker Desktop) — ejecución como `Job` efímero
- **GitHub Actions** — pipeline de CI con build, ejecución y artefacto de reporte

## Estructura

```
qa-infra-portfolio/
├── .github/workflows/qa-infra.yml   # Pipeline de CI
├── k8s/test-job.yaml                # Manifiesto del Job de Kubernetes
├── tests/test_smoke.py              # Suite de tests de humo
├── Dockerfile                       # Imagen reproducible de la suite
├── requirements.txt
├── .dockerignore
└── .gitignore
```

## Cómo ejecutar

### 1. Local con Python

```bash
pip install -r requirements.txt
pytest tests/ -v
```

### 2. Dentro de Docker

```bash
docker build -t qa-infra-tests .
docker run --rm -v "${PWD}/reports:/app/reports" qa-infra-tests
```

El reporte JUnit queda en `reports/junit.xml`.

### 3. En Kubernetes (Job efímero)

```bash
kubectl apply -f k8s/test-job.yaml
kubectl wait --for=condition=complete --timeout=120s job/qa-smoke-tests
kubectl logs job/qa-smoke-tests
kubectl delete job qa-smoke-tests
```

El Job crea un Pod, ejecuta la suite y termina. Los resultados se leen de los logs.

## Pipeline de CI

Cada push a `main` dispara `.github/workflows/qa-infra.yml`, que:

1. Construye la imagen Docker.
2. Ejecuta los tests dentro del contenedor.
3. Sube el reporte `junit.xml` como artefacto descargable.

## Decisiones de diseño

- **Imagen ligera y cacheada**: `python:3.13-slim` y copia de `requirements.txt`
  antes del código para aprovechar la caché de capas.
- **Job con `backoffLimit: 0` y `restartPolicy: Never`**: un fallo de test debe
  fallar rápido, no reintentarse en bucle.
- **Reporte como artefacto**: aunque los tests fallen, el XML se sube; el
  diagnóstico de un fallo es tan valioso como el de un éxito.
- **Sin `time.sleep()`**: cuando se añadan tests de UI (Selenium), se usarán
  esperas explícitas con `WebDriverWait`.

## Roadmap

- [ ] Añadir `docker-compose.yml` con Selenium Grid y tests de UI.
- [ ] Ejecutar el Job de Kubernetes en un clúster `kind` dentro de GitHub Actions.
- [ ] Integrar reportes con `pytest-html`.

## Autor

Juan Mendoza — QA Automation
