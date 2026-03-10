import pathlib
import requests

DATA_PDF_DIR = pathlib.Path("data/pdfs")
DATA_PROCESSED_DIR = pathlib.Path("data/processed")
GROBID_URL = "http://localhost:8070"

def process_pdf_with_grobid(pdf_path: pathlib.Path) -> pathlib.Path:
    """
    Envía un PDF a GROBID (servicio processFulltextDocument)
    y guarda el TEI XML en data/processed/ con el mismo nombre base.
    """
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    url = f"{GROBID_URL}/api/processFulltextDocument"
    files = {"input": open(pdf_path, "rb")}

    response = requests.post(url, files=files)
    response.raise_for_status()  # lanza error si algo va mal

    output_path = DATA_PROCESSED_DIR / (pdf_path.stem + ".tei.xml")
    output_path.write_text(response.text, encoding="utf-8")

    print(f"Procesado {pdf_path.name} -> {output_path.name}")
    return output_path

def process_all_pdfs():
    pdfs = sorted(DATA_PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print("No se han encontrado PDFs en data/pdfs/")
        return

    for pdf in pdfs:
        process_pdf_with_grobid(pdf)

def analyze_tei_results():
    """Llama al analizador de TEI."""
    from tei_analyzer import analyze_all_tei, print_stats
    results = analyze_all_tei()
    print_stats(results)

def full_pipeline():
    """Pipeline completo: PDFs -> TEI -> Análisis."""
    process_all_pdfs()
    print("\n" + "="*50)
    print("Iniciando análisis de TEI...")
    analyze_tei_results()

if __name__ == "__main__":
    full_pipeline()  # ¡Ejecuta TODO!
