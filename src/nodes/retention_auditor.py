from src.core.state import AgentState
import logging
import re

logger = logging.getLogger(__name__)

def node_retention_auditor(state: AgentState) -> AgentState:
    """
    Agente 6 (Esteira): Retention Auditor (O Guardião)
    Auditoria profunda do roteiro: conta palavras, calcula média de palavras por frase,
    e verifica a presença de tags de prosódia.
    """
    logger.info("=== Executando Nó: retention_auditor ===")
    
    prose = state.get("tts_prose", "")
    word_count = state.get("word_count", 0)
    
    if not prose:
        return {"retention_score": 0, "auditor_feedback": "Roteiro vazio.", "current_status": "auditor_failed"}
        
    logger.info(f"Analisando densidade de palavras: {word_count} palavras")
    
    # 1. Análise de Fôlego (Palavras por Frase)
    sentences = re.split(r'[.!?]', prose)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        avg_words_per_sentence = 0
    else:
        total_words = sum(len(s.split()) for s in sentences)
        avg_words_per_sentence = total_words / len(sentences)
        
    logger.info(f"Média de palavras por frase: {avg_words_per_sentence:.1f}")
    
    # 2. Análise de Ganchos (Prosódia)
    tags_encontradas = re.findall(r'\[.*?\]', prose)
    tag_count = len(tags_encontradas)
    logger.info(f"Tags de prosódia encontradas: {tag_count}")
    
    # Validação rigorosa
    score = 100
    feedback_notes = []
    
    if word_count < 200:
        score -= 40
        feedback_notes.append(f"Volume criticamente baixo ({word_count} palavras). O assunto não foi esgotado. Expanda a profundidade e a pesquisa factual.")
        
    if avg_words_per_sentence > 15:
        score -= 20
        feedback_notes.append(f"Frases muito longas (média {avg_words_per_sentence:.1f}). Reduza para no máximo 15 palavras por frase.")
        
    if tag_count < (len(sentences) // 4): # Exige pelo menos 1 tag a cada 4 frases
        score -= 20
        feedback_notes.append(f"Poucas tags de prosódia ({tag_count}). Adicione mais pausas [PAUSA_1s] e mudanças de tom para reter a atenção.")
        
    # 3. Análise Visual (Cadência e Movimento)
    visual_blocks = state.get("visual_blocks", [])
    if not visual_blocks:
        score -= 30
        feedback_notes.append("Nenhum bloco visual gerado. O Storyboarder falhou.")
    else:
        for i in range(1, len(visual_blocks)):
            prev_cam = visual_blocks[i-1].get("shot_metadata", {}).get("camera_movement", "").lower()
            curr_cam = visual_blocks[i].get("shot_metadata", {}).get("camera_movement", "").lower()
            
            # Reprovar se houver cadência idêntica seguida
            if prev_cam and curr_cam and prev_cam == curr_cam:
                score -= 15
                feedback_notes.append(f"Cadência visual repetitiva detectada no shot {i}. Movimento '{curr_cam}' usado consecutivamente.")
                break
                
        # Verificar verbos imperativos no primeiro shot
        first_cam = visual_blocks[0].get("shot_metadata", {}).get("camera_movement", "").lower()
        if first_cam and not any(verb in first_cam for verb in ["dolly", "pan", "truck", "orbit", "zoom", "tilt", "static"]):
            score -= 10
            feedback_notes.append(f"Taxonomia de câmera física ausente ou incorreta no gancho inicial: '{first_cam}'.")

    if score < 85:
        logger.warning(f"ALERTA: Roteiro REPROVADO com nota {score}.")
        feedback = " | ".join(feedback_notes)
        next_status = "auditor_failed"
    else:
        logger.info(f"SUCESSO: Roteiro APROVADO com nota {score}.")
        feedback = "Roteiro perfeito e visualmente cadenciado. Pronto para produção."
        next_status = "auditor_approved"
        
    return {
        "retention_score": score, 
        "auditor_feedback": feedback, 
        "current_status": next_status
    }
