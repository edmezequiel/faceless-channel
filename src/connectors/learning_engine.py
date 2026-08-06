import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DB_PATH = os.path.join("memory", "viral_knowledge_bank", "knowledge_base.json")
PATTERNS_MD_PATH = os.path.join("memory", "viral_knowledge_bank", "patterns.md")

class ViralLearningEngine:
    """
    Motor de Aprendizado e Aprimoramento Contínuo de Roteiros Virais.
    Extrai padrões narrativos (hooks, analogias, micro-twists, imersão sensorial, ctas, retention_tactics)
    de novos roteiros e atualiza dinamicamente a base de conhecimento do canal.
    """
    
    def __init__(self, db_path: str = DB_PATH, patterns_md_path: str = PATTERNS_MD_PATH):
        self.db_path = db_path
        self.patterns_md_path = patterns_md_path
        self.data = self._load_database()
        if not os.path.exists(self.patterns_md_path):
            self._update_patterns_md()

    @staticmethod
    def _create_default_kb() -> Dict[str, Any]:
        """Cria e retorna a estrutura base de conhecimento padrão com as 6 categorias."""
        return {
            "version": "1.0.0",
            "last_updated": "",
            "analyzed_videos_count": 0,
            "patterns": {
                "hooks": [],
                "analogies": [],
                "micro_twists": [],
                "sensory_beats": [],
                "ctas": [],
                "retention_tactics": []
            }
        }

    def _load_database(self) -> Dict[str, Any]:
        """Carrega a base de dados JSON ou cria uma estrutura padrão se não existir."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    patterns = data.setdefault("patterns", {})
                    for cat in ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]:
                        patterns.setdefault(cat, [])
                    return data
            except Exception as e:
                logger.error(f"Erro ao carregar knowledge_base.json: {e}")
        
        return self._create_default_kb()

    def save_database(self) -> None:
        """Salva o banco de dados no disco de forma atômica e atualiza o arquivo Markdown patterns.md."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        self.data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        temp_path = f"{self.db_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
        os.replace(temp_path, self.db_path)
        logger.info(f"Viral Knowledge Bank atualizado com sucesso em: {self.db_path}")
        
        self._update_patterns_md()

    def _update_patterns_md(self) -> None:
        """Regenera / atualiza em sincronia o arquivo memory/viral_knowledge_bank/patterns.md."""
        md_dir = os.path.dirname(self.patterns_md_path)
        if md_dir:
            os.makedirs(md_dir, exist_ok=True)

        def _clean(val: Any) -> str:
            if val is None:
                return "N/A"
            s = str(val).replace("\n", " ").replace("|", "\\|").strip()
            return s if s else "N/A"

        version = _clean(self.data.get("version", "1.0.0"))
        last_updated = _clean(self.data.get("last_updated", ""))
        analyzed_count = self.data.get("analyzed_videos_count", 0)
        patterns = self.get_top_patterns()

        lines = [
            "# Viral Narrative Patterns — EDM ARCHETYPE LAB",
            "",
            f"> **System**: Viral Knowledge Bank  ",
            f"> **Version**: {version}  ",
            f"> **Last Updated**: {last_updated}  ",
            f"> **Analyzed Videos**: {analyzed_count}  ",
            "",
            "---",
            "",
            "## 🪝 1. Retention Hooks & Scale Contrast (`hooks`)",
            "",
            "Padrões de abertura contraintuitivos projetados para capturar a atenção nos primeiros 5 segundos.",
            "",
            "| ID | Tipo | Fonte / Referência | Padrão Conceitual | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|---|"
        ]

        hooks = patterns.get("hooks", [])
        if not hooks:
            lines.append("| N/A | N/A | N/A | (Nenhum padrão registrado) | (Nenhum padrão registrado) |")
        else:
            for idx, h in enumerate(hooks):
                hid = _clean(h.get("id", f"HOOK_{idx+1:03d}"))
                htype = _clean(h.get("type"))
                hsrc = _clean(h.get("example_source"))
                hpat = _clean(h.get("pattern", h.get("template")))
                hadapt = _clean(h.get("adapted_for_channel", h.get("adapted_for_psychology", h.get("template"))))
                lines.append(f"| `{hid}` | `{htype}` | {hsrc} | {hpat} | *{hadapt}* |")

        lines.extend([
            "",
            "---",
            "",
            "## 💡 2. Everyday Domestic Analogies (`analogies`)",
            "",
            "Tradução de conceitos neurobiológicos ou físicos abstratos para objetos e experiências cotidianas.",
            "",
            "| ID | Conceito Abstrato | Comparação Doméstica | Exemplo Original | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|---|"
        ])

        analogies = patterns.get("analogies", [])
        if not analogies:
            lines.append("| N/A | N/A | N/A | (Nenhuma analogia registrada) | (Nenhuma analogia registrada) |")
        else:
            for idx, a in enumerate(analogies):
                aid = _clean(a.get("id", f"ANA_{idx+1:03d}"))
                aconcept = _clean(a.get("concept"))
                acomparison = _clean(a.get("domestic_comparison"))
                aexample = _clean(a.get("example", a.get("example_phrase")))
                aadapt = _clean(a.get("adapted_for_channel", a.get("example")))
                lines.append(f"| `{aid}` | {aconcept} | {acomparison} | *{aexample}* | *{aadapt}* |")

        lines.extend([
            "",
            "---",
            "",
            "## 🌀 3. Micro-Twists & Expectation Inversion (`micro_twists`)",
            "",
            "Reviravoltas conceituais que quebram o consenso a cada 45-90 segundos.",
            "",
            "| ID | Gatilho de Inversão | Frase Original | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|"
        ])

        twists = patterns.get("micro_twists", [])
        if not twists:
            lines.append("| N/A | N/A | (Nenhum micro-twist registrado) | (Nenhum micro-twist registrado) |")
        else:
            for idx, t in enumerate(twists):
                tid = _clean(t.get("id", f"TWIST_{idx+1:03d}"))
                ttrigger = _clean(t.get("trigger"))
                tphrase = _clean(t.get("phrase", t.get("example_phrase")))
                tadapt = _clean(t.get("adapted_for_channel", t.get("adapted_for_psychology")))
                lines.append(f"| `{tid}` | {ttrigger} | *{tphrase}* | *{tadapt}* |")

        lines.extend([
            "",
            "---",
            "",
            "## 👁️ 4. Sensory Immersion Beats (`sensory_beats`)",
            "",
            "Simulações em primeira pessoa que ativam o córtex sensorial do espectador.",
            "",
            "| ID | Tipo de Imersão | Template / Estrutura | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|"
        ])

        sensory = patterns.get("sensory_beats", [])
        if not sensory:
            lines.append("| N/A | N/A | (Nenhum sensory beat registrado) | (Nenhum sensory beat registrado) |")
        else:
            for idx, s in enumerate(sensory):
                sid = _clean(s.get("id", f"SENS_{idx+1:03d}"))
                stype = _clean(s.get("type"))
                stemplate = _clean(s.get("template", s.get("template_phrase")))
                sadapt = _clean(s.get("adapted_for_channel", s.get("template")))
                lines.append(f"| `{sid}` | `{stype}` | *{stemplate}* | *{sadapt}* |")

        lines.extend([
            "",
            "---",
            "",
            "## 📣 5. Organic Soft CTAs (`ctas`)",
            "",
            "Chamadas para ação integradas ao fluxo narrativo sem quebrar a imersão.",
            "",
            "| ID | Tipo de Posicionamento | Template Original | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|"
        ])

        ctas = patterns.get("ctas", [])
        if not ctas:
            lines.append("| N/A | N/A | (Nenhum CTA registrado) | (Nenhum CTA registrado) |")
        else:
            for idx, c in enumerate(ctas):
                cid = _clean(c.get("id", f"CTA_{idx+1:03d}"))
                ctype = _clean(c.get("type"))
                ctemplate = _clean(c.get("template", c.get("template_phrase")))
                cadapt = _clean(c.get("adapted_for_channel", c.get("template")))
                lines.append(f"| `{cid}` | `{ctype}` | *{ctemplate}* | *{cadapt}* |")

        lines.extend([
            "",
            "---",
            "",
            "## ⏱️ 6. Retention Tactics & Open Loops (`retention_tactics`)",
            "",
            "Táticas temporais e mecânicas de retenção baseadas em pacing e arcos narrativos.",
            "",
            "| ID | Tópico / Tática | Mecanismo de Pacing | Intervalo Temporal | Exemplo Adaptado (EDM ARCHETYPE LAB) |",
            "|---|---|---|---|---|"
        ])

        retention = patterns.get("retention_tactics", [])
        if not retention:
            lines.append("| N/A | N/A | N/A | N/A | (Nenhuma tática de retenção registrada) |")
        else:
            for idx, r in enumerate(retention):
                rid = _clean(r.get("id", f"TAC_{idx+1:03d}"))
                rtactic = _clean(r.get("tactic"))
                rmechanism = _clean(r.get("mechanism"))
                rinterval = _clean(r.get("pacing_interval"))
                radapt = _clean(r.get("adapted_for_channel", r.get("template", r.get("template_phrase"))))
                lines.append(f"| `{rid}` | `{rtactic}` | {rmechanism} | {rinterval} | *{radapt}* |")

        lines.append("")

        content = "\n".join(lines)
        temp_md_path = f"{self.patterns_md_path}.tmp"
        with open(temp_md_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_md_path, self.patterns_md_path)
        logger.info(f"Padrões virais sincronizados com sucesso em: {self.patterns_md_path}")

    def get_top_patterns(self) -> Dict[str, Any]:
        """Retorna os padrões de maior sucesso para injeção nos prompts da esteira."""
        return self.data.get("patterns", {})

    def format_patterns_for_prompt(self) -> str:
        """Formata os padrões virais acumulados para inclusão direta no prompt de roteirização."""
        patterns = self.get_top_patterns()
        
        hooks_text = "\n".join([f"  - [{h.get('type', 'hook')}] {h.get('adapted_for_channel', h.get('pattern', h.get('template', '')))}" for h in patterns.get("hooks", [])[:3]]) or "  - (Nenhum padrão registrado)"
        analogies_text = "\n".join([f"  - Compare '{a.get('concept', '')}' a '{a.get('domestic_comparison', '')}' (Ex: {a.get('adapted_for_channel', a.get('example', ''))})" for a in patterns.get("analogies", [])[:3]]) or "  - (Nenhuma analogia registrada)"
        twists_text = "\n".join([f"  - [{t.get('trigger', 'twist')}] {t.get('adapted_for_channel', t.get('phrase', ''))}" for t in patterns.get("micro_twists", [])[:3]]) or "  - (Nenhum micro-twist registrado)"
        sensory_text = "\n".join([f"  - [{s.get('type', 'sensory')}] {s.get('adapted_for_channel', s.get('template', s.get('template_phrase', '')))}" for s in patterns.get("sensory_beats", [])[:3]]) or "  - (Nenhum sensory beat registrado)"
        ctas_text = "\n".join([f"  - [{c.get('type', 'cta')}] {c.get('adapted_for_channel', c.get('template', c.get('template_phrase', '')))}" for c in patterns.get("ctas", [])[:2]]) or "  - (Nenhum CTA registrado)"
        retention_text = "\n".join([f"  - [{r.get('tactic', r.get('id', 'tactic'))}] {r.get('adapted_for_channel', r.get('template', r.get('mechanism', '')))}" for r in patterns.get("retention_tactics", [])[:3]]) or "  - (Nenhuma tática de retenção registrada)"
        
        return f"""
APRENDIZADOS ACUMULADOS DOS MAIORES VÍDEOS VIRAIS DO YOUTUBE (VIRAL KNOWLEDGE BANK):
1. HOOKS E PARADOXOS DE RETENÇÃO:
{hooks_text}

2. ANALOGIAS DOMÉSTICAS DO DIA A DIA:
{analogies_text}

3. MICRO-TWISTS & INVERSÃO DE EXPECTATIVAS:
{twists_text}

4. IMERSÃO SENSORIAL E SIMULAÇÕES:
{sensory_text}

5. SOFT CTAs ORGÂNICOS DE MEIO DE VÍDEO:
{ctas_text}

6. TÁTICAS DE RETENÇÃO E OPEN LOOPS:
{retention_text}
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
6. "retention_tactics": lista de objetos com {{"tactic", "mechanism", "pacing_interval", "template_phrase"}}

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
                for cat in ["hooks", "analogies", "micro_twists", "sensory_beats", "ctas", "retention_tactics"]:
                    if cat in extracted_json and isinstance(extracted_json[cat], list):
                        patterns.setdefault(cat, []).extend(extracted_json[cat])
                        
                self.data["analyzed_videos_count"] = self.data.get("analyzed_videos_count", 0) + 1
                self.save_database()
                logger.info(f"Ingestão concluída com sucesso para '{script_title}'.")
                return extracted_json
        except Exception as e:
            logger.error(f"Erro durante a ingestão do roteiro viral: {e}")
            
        return {}

