# -*- coding: utf-8 -*-
"""
Script de Ingestão e Aprendizado Autônomo de Roteiros Virais - EDM ARCHETYPE LAB

Uso:
  .venv\\Scripts\\python.exe ingest_viral_script.py "Título do Vídeo" "Nicho" "Caminho_ou_Texto_do_Roteiro"
"""
import sys
import os
import io
import logging

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("INGEST_VIRAL")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def process_single_file(engine, title: str, niche: str, text_or_file: str):
    """Processa um único arquivo ou texto de roteiro."""
    script_text = ""
    if os.path.exists(text_or_file) and os.path.isfile(text_or_file):
        with open(text_or_file, "r", encoding="utf-8", errors="ignore") as f:
            script_text = f.read()
    else:
        script_text = text_or_file

    if not script_text.strip():
        logger.error("Texto de transcrição vazio ou arquivo não encontrado.")
        return False

    logger.info(f"Iniciando aprendizado do vídeo viral '{title}' ({niche})...")
    result = engine.ingest_script_text(script_title=title, script_text=script_text, source_niche=niche)
    print("\n=== NOVOS PADRÕES APRENDIDOS ===")
    print(f"Vídeo Analisado: '{title}' ({niche})")
    if isinstance(result, dict):
        for category in ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]:
            items = result.get(category, [])
            if isinstance(items, list):
                print(f"  • {category.upper()}: {len(items)} elemento(s) extraído(s)")
    print(f"\nTotal de Vídeos na Base de Conhecimento: {engine.data.get('analyzed_videos_count', 0)}")
    return True

def process_directory(engine, dir_path: str, niche: str = "Geral"):
    """Varre um diretório e ingere todos os arquivos .txt e .md encontrados."""
    logger.info(f"Varrendo a pasta de roteiros virais: {dir_path}...")
    valid_extensions = (".txt", ".md", ".json")
    files = [f for f in os.listdir(dir_path) if f.endswith(valid_extensions) and not f.startswith(".")]
    
    if not files:
        print(f"\nNenhum arquivo de roteiro (.txt, .md) encontrado na pasta '{dir_path}'.")
        return

    print(f"\nEncontrados {len(files)} arquivo(s) na pasta '{dir_path}':")
    for f in files:
        print(f"  • {f}")
    
    for filename in files:
        file_path = os.path.join(dir_path, filename)
        title = os.path.splitext(filename)[0].replace("_", " ").title()
        print(f"\n--------------------------------------------------")
        print(f"▶ Processando: {filename}...")
        process_single_file(engine, title=title, niche=niche, text_or_file=file_path)

def main():
    from src.connectors.learning_engine import ViralLearningEngine
    
    engine = ViralLearningEngine()
    folder_default = os.path.join(os.getcwd(), "ROTEIROS VIRAIS")

    if len(sys.argv) < 2:
        print("\n=== SISTEMA DE APRENDIZADO DE ROTEIROS VIRAIS ===")
        print("Uso:")
        print("  1. Analisar um roteiro individual: python ingest_viral_script.py <titulo> <nicho> <arquivo_ou_texto>")
        print("  2. Analisar todos da pasta ROTEIROS VIRAIS: python ingest_viral_script.py ROTEIROS VIRAIS")
        print("\nEstado Atual da Base de Conhecimento:")
        print(f"  • Vídeos Analisados: {engine.data.get('analyzed_videos_count', 0)}")
        patterns = engine.get_top_patterns()
        for cat in ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]:
            items = patterns.get(cat, [])
            print(f"  • {cat.upper()}: {len(items)} padrões aprendidos")
        print("\n" + engine.format_patterns_for_prompt())
        
        # Se a pasta ROTEIROS VIRAIS tiver arquivos, pergunta se deseja varrer
        if os.path.exists(folder_default):
            files = [f for f in os.listdir(folder_default) if f.endswith((".txt", ".md"))]
            if files:
                print(f"\n📁 Encontrado(s) {len(files)} roteiro(s) na pasta 'ROTEIROS VIRAIS'. Processando automaticamente...")
                process_directory(engine, folder_default)
        return

    args = sys.argv[1:]
    
    # Se o primeiro argumento for um diretório existente (ex: ROTEIROS VIRAIS)
    if os.path.exists(args[0]) and os.path.isdir(args[0]):
        niche = args[1] if len(args) > 1 else "Geral"
        process_directory(engine, args[0], niche=niche)
        return

    title = ""
    niche = "Geral"
    text_or_file = ""

    if len(args) >= 3:
        title = args[0]
        niche = args[1]
        text_or_file = args[2]
    elif len(args) == 2:
        if os.path.exists(args[1]) or len(args[1]) > 50:
            title = args[0]
            text_or_file = args[1]
        elif os.path.exists(args[0]) or len(args[0]) > 50:
            title = os.path.splitext(os.path.basename(args[0]))[0].replace("_", " ").title()
            niche = args[1]
            text_or_file = args[0]
        else:
            title = args[0]
            niche = args[1]
            text_or_file = ""
    elif len(args) == 1:
        arg = args[0]
        if os.path.exists(arg):
            title = os.path.splitext(os.path.basename(arg))[0].replace("_", " ").title()
            text_or_file = arg
        elif len(arg) > 50 or "\n" in arg:
            title = "Roteiro Importado"
            text_or_file = arg
        else:
            title = arg
            text_or_file = ""

    process_single_file(engine, title=title, niche=niche, text_or_file=text_or_file)

if __name__ == "__main__":
    main()

