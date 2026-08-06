import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DB_PATH = os.path.join("memory", "viral_knowledge_bank", "knowledge_base.json")
PATTERNS_MD_PATH = os.path.join("memory", "viral_knowledge_bank", "patterns.md")

class ViralLearningEngine:
    """
    Motor de Aprendizado e Aprimoramento Contínuo de Roteiros Virais.
    Extrai padrões narrativos (hooks, analogias, micro-twists, imersão sensorial)
    de novos roteiros e atualiza dinamicamente a base de conhecimento do canal.
    """
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.data = self._load_database()

    def _load_database(self) -> Dict[str, Any]:
        """Carrega a base de dados JSON ou cria uma estrutura padrão se não existir."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar knowledge_base.json: {e}")
        
        return {
            "version": "1.0.0",
            "last_updated": "",
            "analyzed_videos_count": 0,
            "patterns": {
                "hooks": [],
                "analogies": [],
                "micro_twists": [],
                "sensory_beats": [],
                "ctas": []
            }
        }

    def save_database(self) -> None:
        """Salva o banco de dados no disco."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        logger.info(f"Viral Knowledge Bank atualizado com sucesso em: {self.db_path}")

    def get_top_patterns(self) -> Dict[str, Any]:
        """Retorna os padrões de maior sucesso para injeção nos prompts da esteira."""
        return self.data.get("patterns", {})

    def format_patterns_for_prompt(self) -> str:
        """Formata os padrões virais acumulados para inclusão direta no prompt de roteirização."""
        patterns = self.get_top_patterns()
        
        hooks_text = "\n".join([f"  - [{h.get('type')}] {h.get('adapted_for_channel', h.get('pattern'))}" for h in patterns.get("hooks", [])[:3]])
        analogies_text = "\n".join([f"  - Compare '{a.get('concept')}' a '{a.get('domestic_comparison')}'" for a in patterns.get("analogies", [])[:3]])
        twists_text = "\n".join([f"  - [{t.get('trigger')}] {t.get('adapted_for_channel', t.get('phrase'))}" for t in patterns.get("micro_twists", [])[:3]])
        ctas_text = "\n".join([f"  - {c.get('adapted_for_channel', c.get('template'))}" for c in patterns.get("ctas", [])[:2]])
        
        return f"""
APRENDIZADOS ACUMULADOS DOS MAIORES VÍDEOS VIRAIS DO YOUTUBE (VIRAL KNOWLEDGE BANK):
1. HOOKS E PARADOXOS DE RETENÇÃO:
{hooks_text}

2. ANALOGIAS DOMÉSTICAS DO DIA A DIA:
{analogies_text}

3. MICRO-TWISTS & INVERSÃO DE EXPECTATIVAS:
{twists_text}

4. SOFT CTAs ORGÂNICOS DE MEIO DE VÍDEO:
{ctas_text}
"""

    def ingest_script_text(self, script_title: str, script_text: str, source_niche: str = "Geral") -> Dict[str, Any]:
        """
        Analisa a transcrição de um vídeo viral usando o OmniRoute e extrai novos padrões narrativos.
        """
        from src.connectors.llm_router import generate_response
        
        logger.info(f"Analisando novo roteiro viral: '{script_title}' ({source_niche})...")
        
        prompt = f"""
Você é um Engenheiro de Retenção do YouTube especialista em extrair padrões narrativos virais.
Analise a transcrição abaixo do vídeo viral '{script_title}' (Nicho: {source_niche}).

TRANSCRIÇÃO DO VÍDEO VIRAL:
{script_text[:4000]}

Extraia os elementos-chave em formato JSON estruturado com as seguintes chaves:
1. "hooks": lista de objetos com {{"type", "pattern", "example_phrase", "adapted_for_psychology"}}
2. "analogies": lista de objetos com {{"concept", "domestic_comparison", "example_phrase"}}
3. "micro_twists": lista de objetos com {{"trigger", "phrase", "adapted_for_psychology"}}
4. "sensory_beats": lista de objetos com {{"type", "template_phrase"}}
5. "ctas": lista de objetos com {{"type", "template_phrase"}}

Retorne APENAS o JSON válido.
"""
        try:
            res = generate_response(prompt=prompt, system_prompt="Você é um analista supremo de viracidade no YouTube.", agent_role="packaging")
            # Procura por JSON na resposta
            start_idx = res.find("{")
            end_idx = res.rfind("}")
            if start_idx != -1 and end_idx != -1:
                extracted_json = json.loads(res[start_idx:end_idx+1])
                
                # Incorpora ao banco de dados
                patterns = self.data.setdefault("patterns", {})
                for cat in ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas"]:
                    if cat in extracted_json and isinstance(extracted_json[cat], list):
                        patterns.setdefault(cat, []).extend(extracted_json[cat])
                        
                self.data["analyzed_videos_count"] = self.data.get("analyzed_videos_count", 0) + 1
                self.save_database()
                logger.info(f"Ingestão concluída com sucesso para '{script_title}'.")
                return extracted_json
        except Exception as e:
            logger.error(f"Erro durante a ingestão do roteiro viral: {e}")
            
        return {}
