# -*- coding: utf-8 -*-
"""
Script de Teste Completo - EDM ARCHETYPE LAB
Executa o pipeline completo (Pesquisa -> Embalagem -> Roteiro -> Storyboard -> Auditoria)
SEM gerar imagens, videos ou audios.

Uso: .venv\\Scripts\\python.exe run_test.py [tema opcional]
"""
import sys
import os
import io
import logging
import textwrap

# Forca UTF-8 no stdout para evitar UnicodeEncodeError no Windows (cp1252)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configura logging simples sem emojis
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("EDM_TEST")

# Garante que o src/ esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BORDER = "=" * 78

def print_section(title: str, content: str):
    """Printa uma secao formatada no terminal."""
    print(f"\n{BORDER}")
    print(f"  {title}")
    print(BORDER)
    for line in content.split("\n"):
        if len(line) > 74:
            for wrapped in textwrap.wrap(line, 74):
                print(f"  {wrapped}")
        else:
            print(f"  {line}")
    print(BORDER)

def run_pipeline(tema: str):
    from src.core.engine import build_graph

    logger.info("Compilando Grafo LangGraph (6 agentes)...")
    graph = build_graph()
    logger.info("Grafo compilado! Iniciando pipeline...")

    initial_state = {
        "goal": tema,
        "current_status": "init",
        "research_sources": [],
        "audit_log": [],
        "active_agents": [],
    }

    print_section(
        "[START] EDM ARCHETYPE LAB - Pipeline Iniciado",
        f"Tema: {tema}\nModo: Texto apenas (sem geracao de midia)"
    )

    final_state = {}

    for event in graph.stream(initial_state, {"recursion_limit": 25}):
        for node_name, state_update in event.items():
            status = state_update.get("current_status", "")
            logger.info(f"[NODE OK] [{node_name}] -> Status: {status}")
            final_state.update(state_update)

    # --- Exibir resultados de cada etapa ---

    # 1. Contexto Factual (Researcher)
    factual = final_state.get("factual_context", "")
    if factual:
        print_section("[1] RESEARCHER - Contexto Factual Coletado", factual[:1500])

    # 2. Packaging / CTR
    pkg = final_state.get("packaging", {})
    if pkg:
        titles = "\n".join([f"  - {t}" for t in pkg.get("titles", [])])
        thumb = pkg.get("thumbnail_concept", "")
        palette = pkg.get("color_palette", "")
        print_section(
            "[2] PACKAGING CTR - Titulos e Thumbnail",
            f"TITULOS:\n{titles}\n\nTHUMBNAIL: {thumb}\n\nPALETA: {palette}"
        )

    # 3. Script Skeleton (Architect)
    skeleton = final_state.get("script_skeleton", {})
    if skeleton:
        beats = "\n".join([f"  [{i+1}] {b}" for i, b in enumerate(skeleton.get("beats", []))])
        loops = "\n".join([f"  - {l}" for l in skeleton.get("open_loops", [])])
        print_section(
            "[3] SCRIPT ARCHITECT - Esqueleto Narrativo",
            f"BEATS:\n{beats}\n\nOPEN LOOPS (Ganchos retidos):\n{loops}"
        )

    # 4. TTS Prose (Scriptwriter)
    prose = final_state.get("tts_prose", "")
    words = final_state.get("word_count", 0)
    if prose:
        print_section(
            f"[4] TTS SCRIPTWRITER - Roteiro Completo ({words} palavras)",
            prose[:3000]
        )

    # 5. Visual Blocks (Storyboarder)
    blocks = final_state.get("visual_blocks", [])
    if blocks:
        summary = []
        for i, b in enumerate(blocks[:5]):
            shot = b.get("shot_metadata", {})
            summary.append(
                f"  SHOT {i+1}: {shot.get('shot_id','?')} | "
                f"Camera: {shot.get('camera_movement','?')} | "
                f"Vel: {shot.get('scroll_velocity','?')} | "
                f"Audio: {shot.get('audio_type','?')}"
            )
        if len(blocks) > 5:
            summary.append(f"  ... e mais {len(blocks)-5} blocos.")
        print_section(
            f"[5] VISUAL STORYBOARDER - {len(blocks)} Blocos Visuais",
            "\n".join(summary)
        )

    # 6. Auditoria
    score = final_state.get("retention_score", 0)
    feedback = final_state.get("auditor_feedback", "")
    status_final = final_state.get("current_status", "")
    result = "APROVADO" if score >= 85 else "REPROVADO"
    print_section(
        f"[6] RETENTION AUDITOR - Nota: {score}/100 [{result}]",
        f"Status Final: {status_final}\n\nFeedback:\n{feedback}"
    )

    print(f"\n{BORDER}")
    print(f"  PIPELINE CONCLUIDO | Status: {status_final} | Score: {score}/100")
    print(BORDER)

    return final_state

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tema = " ".join(sys.argv[1:])
    else:
        tema = "A Psicologia Sombria da Triada Negra: Como Narcisistas, Psicopatas e Maquiavelicos Controlam Suas Relacoes"

    run_pipeline(tema)
