# Análisis de Artículos Científicos con GROBID

Extrae abstracts, cuenta figuras y detecta links de artículos científicos usando GROBID + Python.

[![Zenodo](https://zenodo.org/badge/DOI.svg)](https://zenodo.org/badge/latestdoi/YOUR_DOI)

## Instalación y Ejecución

### Requisitos previos
- Python 3.8+
- Git
- Docker (para GROBID)
- PDFs en `data/pdfs/`

### **Método 1: Docker Compose**

```bash
# Clonar y ejecutar TODO automáticamente
git clone https://github.com/Meendooo/OSAI/IndividualAssessment1.git
cd IndividualAssessment1
docker compose up -d
```

Los resultados estarán en data/analysis/:

wordcloud_abstracts.png

figures_per_article.png

analysis_summary.json

```bash
# Ver logs
docker compose logs analyzer

# Parar cuando termines
docker compose down
```

### Método 2: Entorno virtual

1. **Clonar repositorio**
```bash
git clone https://github.com/Meendooo/OSAI/IndividualAssessment1.git
cd IndividualAssessment1
source env/bin/activate  # Linux/Mac
# o
env\Scripts\activate     # Windows
pip install -r requirements.txt
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.2
python src/main.py  # Ya incluye PDFs de data/
python src/tei_analyzer.py
```

### Método 3: Desde cero (sin entorno virtual)
```bash
pip install beautifulsoup4 wordcloud matplotlib numpy pathlib requests
python src/main.py
python src/tei_analyzer.py
```

## Estructura del proyecto

IndividualAssessment1/
├── data/               # Dataset de PDFs y resultados
│   ├── pdfs/           # paper1.pdf ... paper10.pdf
│   ├── processed/      # paper1.tei.xml ... paper10.tei.xml
│   └── analysis/       # wordcloud_abstracts.png, figures_per_article.png, analysis_summary.json
├── src/
│   ├── __init__.py
│   ├── main.py         # Pipeline GROBID → TEI
│   └── tei_analyzer.py # Análisis + visualizaciones
├── docker-compose.yml  # Configuración completa Docker
├── Dockerfile          # Imagen Python + dependencias
├── tests/              # Tests unitarios
├── requirements.txt
└── README.md

## 🧪 Tests Unitarios

```powershell
# Windows (PowerShell)
$env:PYTHONPATH="." ; python -m unittest discover tests

# Linux/Mac
PYTHONPATH="." ; python -m unittest discover tests
```

Resultados esperados:

..
----------------------------------------------------------------------
Ran 2 tests in 0.068s
OK

## Validación de resultados

En esta sección se describe cómo he comprobado que los resultados generados por el programa son correctos.

### 1. Nube de palabras del abstract

- He seleccionado manualmente 2–3 artículos del conjunto.
- He leído sus abstracts y he comprobado que las palabras más frecuentes en el texto aparecen también con mayor tamaño en la nube.
- He verificado que se eliminan palabras vacías (stopwords) en inglés/español según corresponda.

### 2. Número de figuras por artículo

- Para cada PDF he abierto el artículo y he contado manualmente las figuras (Figure, Fig., etc.).
- He comparado ese número con el valor mostrado en la visualización `figures_per_article.png`.
- En caso de discrepancia, he revisado el TEI generado por Grobid y he corregido el código de extracción si era necesario.

### 3. Lista de enlaces encontrados en cada papel

- He abierto 2–3 artículos y he localizado manualmente las URLs presentes en el texto.
- He comprobado que esas URLs aparecen en el fichero de salida (`analysis_summary.json`).
- También he verificado que no se incluyen cadenas que no sean URLs válidas.

### 4. Limitaciones conocidas

- Grobid puede no detectar correctamente todas las figuras o enlaces en PDFs con formato poco estándar.
- Solo he validado manualmente una parte de los artículos por limitaciones de tiempo.
- Algunas expresiones pueden aparecer en la nube de palabras aunque no sean términos semánticamente relevantes.
