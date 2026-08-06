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

def main():
    from src.connectors.learning_engine import ViralLearningEngine
    
    engine = ViralLearningEngine()
    
    if len(sys.argv) < 2:
        print("\n=== SISTERMA DE APRENDIZADO DE ROTEIROS VIRAIS ===")
        print("Uso: python ingest_viral_script.py <titulo> <nicho> <arquivo_ou_texto>")
        print("\nEstado Atual da Base de Conhecimento:")
        print(f"  • Vídeos Analisados: {engine.data.get('analyzed_videos_count', 0)}")
        patterns = engine.get_top_patterns()
        for cat, items in patterns.items():
            print(f"  • {cat.upper()}: {len(items)} padrões aprendidos")
        print("\n" + engine.format_patterns_for_prompt())
        return

    title = sys.argv[1]
    niche = sys.argv[2] if len(sys.argv) > 2 else "Geral"
    text_or_file = sys.argv[3] if len(sys.argv) > 3 else ""

    if os.path.exists(text_or_file):
        with open(text_or_file, "r", encoding="utf-8", errors="ignore") as f:
            script_text = f.read()
    else:
        script_text = text_or_file

    if not script_text:
        logger.error("Texto de transcrição vazio ou arquivo não encontrado.")
        return

    logger.info(f"Iniciando aprendizado do vídeo viral '{title}' ({niche})...")
    result = engine.ingest_script_text(script_title=title, script_text=script_text, source_niche=niche)
    print("\n=== NOVOS PADRÕES APRENDIDOS ===")
    print(result)

if __name__ == "__main__":
    main()
