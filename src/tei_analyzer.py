import pathlib
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from collections import Counter
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np


# Añadir stopwords en español
STOPWORDS.update(['the', 'and', 'for', 'are', 'but', 'not', 'with', 'this', 'you', 'that', 
                  'este', 'para', 'con', 'los', 'las', 'del', 'de', 'la', 'el', 'en', 
                  'que', 'una', 'por', 'una', 'más', 'una', 'sobre', 'se', 'no', 'es'])


DATA_PROCESSED_DIR = pathlib.Path("data/processed")
DATA_ANALYSIS_DIR = pathlib.Path("data/analysis")
DATA_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def parse_tei_xml(tei_path: pathlib.Path) -> Dict[str, Any]:
    """Parsea un archivo TEI XML de GROBID y extrae abstract, figuras y links."""
    with open(tei_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml-xml')
    
    # 1. Extraer ABSTRACT (CORRECTO)
    abstract_elem = soup.find('abstract')
    abstract = abstract_elem.get_text(separator=' ', strip=True) if abstract_elem else ""
    
    # 2. Contar FIGURAS (SOLO en el BODY, no en header)
    body = soup.find('body')
    figures = body.find_all('figure') if body else []
    num_figures = len(figures)
    
    # 3. Extraer LINKS (SOLO en BODY, excluir Grobid metadata)
    links = []
    if body:
        # Buscar en tags semánticos del cuerpo del artículo
        for tag in ['ref', 'related', 'bibl', 'ulink', 'extLink', 'ref', 'ptr']:
            for ref in body.find_all(tag):
                href = (ref.get('target') or ref.get('href') or ref.get('xlink:href') or 
                       ref.get('url'))
                if href and re.match(r'https?://|doi\.org', href):
                    # Excluir el link de Grobid y links muy cortos
                    if 'kermitt2/grobid' not in href and len(href) > 15:
                        links.append(href.strip())
        
        # También buscar URLs en texto plano del body (fallbacks)
        body_text = body.get_text()
        text_links = re.findall(r'https?://[^\s<>"]{10,}', body_text)
        for link in text_links:
            if 'kermitt2/grobid' not in link and len(link) > 15:
                links.append(link.strip())
    
    unique_links = list(set(links))[:5]  # Máximo 5 links únicos por artículo
    
    return {
        'filename': pathlib.Path(tei_path).stem,
        'abstract': abstract,
        'num_figures': num_figures,
        'links': unique_links
    }


def generate_wordcloud(all_abstracts: str, output_path: str):
    """Genera nube de palabras de todos los abstracts."""
    wordcloud = WordCloud(
        width=1200, height=800,
        background_color='white',
        max_words=100,
        stopwords=STOPWORDS,
        colormap='viridis',
        random_state=42
    ).generate(all_abstracts)
    
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def generate_figures_bar_chart(results: List[Dict[str, Any]], output_path: str):
    """Barras: figuras por artículo."""
    filenames = [r['filename'][:15] + '...' for r in results]
    num_figures = [r['num_figures'] for r in results]
    
    plt.figure(figsize=(12, 6))
    
    bars = plt.bar(range(len(filenames)), num_figures, 
                   color='#2E86C1', edgecolor='navy', alpha=0.8)
    
    mean_figures = np.mean(num_figures)
    plt.axhline(mean_figures, color='red', linestyle='--', linewidth=2, 
                label=f'Media: {mean_figures:.1f}')
    
    plt.title('Número de Figuras por Artículo', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Artículos', fontsize=12)
    plt.ylabel('Número de Figuras', fontsize=12)
    plt.xticks(range(len(filenames)), filenames, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend()
    
    for bar, count in zip(bars, num_figures):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def analyze_all_tei() -> List[Dict[str, Any]]:
    """Analiza todos los TEI XML y genera visualizaciones."""
    tei_files = list(DATA_PROCESSED_DIR.glob("*.tei.xml"))
    if not tei_files:
        print("No se encontraron archivos .tei.xml en data/processed/")
        return []
    
    results = []
    all_abstracts = ""
    
    for tei_file in tei_files:
        result = parse_tei_xml(tei_file)
        results.append(result)
        all_abstracts += result['abstract'] + " "
        print(f"{result['filename']}: {result['num_figures']} figs, {len(result['links'])} links")
    
    summary_path = DATA_ANALYSIS_DIR / "analysis_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    wordcloud_path = DATA_ANALYSIS_DIR / "wordcloud_abstracts.png"
    generate_wordcloud(all_abstracts, str(wordcloud_path))
    
    bar_chart_path = DATA_ANALYSIS_DIR / "figures_per_article.png"
    generate_figures_bar_chart(results, str(bar_chart_path))
    
    print(f"\nResultados completos:")
    print(f"  {wordcloud_path}")
    print(f"  {bar_chart_path}")
    print(f"  {summary_path}")
    
    return results


def print_stats(results: List[Dict[str, Any]]):
    """Muestra estadísticas."""
    num_figures = [r['num_figures'] for r in results]
    total_figures = sum(num_figures)
    total_links = sum(len(r['links']) for r in results)
    avg_figures = np.mean(num_figures)
    
    print(f"\nESTADÍSTICAS:")
    print(f"Artículos analizados: {len(results)}")
    print(f"Figuras totales: {total_figures}")
    print(f"Figuras promedio: {avg_figures:.1f}")
    print(f"Links únicos totales: {total_links}")


if __name__ == "__main__":
    results = analyze_all_tei()
    print_stats(results)
    print("\nAnálisis COMPLETO")
