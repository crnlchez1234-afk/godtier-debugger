"""
🧬 AUTO-UPGRADE SYSTEM
Sistema que analiza técnicas nuevas de la web y las integra automáticamente
al código de entrenamiento para mejorar continuamente
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import ast
import logging

logger = logging.getLogger(__name__)


class TechniqueAnalyzer:
    """Analiza técnicas de entrenamiento encontradas en la web"""
    
    def __init__(self):
        self.known_techniques = {
            'lora': {
                'keywords': ['lora', 'low-rank adaptation', 'parameter-efficient'],
                'category': 'fine_tuning',
                'implementation': 'peft.LoraConfig'
            },
            'qlora': {
                'keywords': ['qlora', 'quantized lora', '4-bit'],
                'category': 'fine_tuning',
                'implementation': 'BitsAndBytesConfig'
            },
            'rag': {
                'keywords': ['rag', 'retrieval augmented', 'retrieval-augmented generation'],
                'category': 'architecture',
                'implementation': 'RAG pipeline'
            },
            'quantization': {
                'keywords': ['quantization', 'int8', 'int4', 'nf4', 'fp8'],
                'category': 'optimization',
                'implementation': 'load_in_4bit'
            },
            'attention_optimization': {
                'keywords': ['flash attention', 'memory efficient attention', 'sparse attention'],
                'category': 'optimization',
                'implementation': 'attn_implementation'
            },
            'gradient_checkpointing': {
                'keywords': ['gradient checkpointing', 'memory optimization'],
                'category': 'optimization',
                'implementation': 'gradient_checkpointing_enable'
            }
        }
    
    def analyze_technique(self, knowledge_entry: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza una entrada de conocimiento para extraer técnicas"""
        instruction = knowledge_entry.get('instruction', '').lower()
        context = knowledge_entry.get('context', '').lower()
        metadata = knowledge_entry.get('metadata', {})
        
        detected_techniques = []
        
        # Busca técnicas conocidas
        for tech_name, tech_info in self.known_techniques.items():
            for keyword in tech_info['keywords']:
                if keyword in instruction or keyword in context:
                    detected_techniques.append({
                        'name': tech_name,
                        'category': tech_info['category'],
                        'implementation': tech_info['implementation'],
                        'source': metadata.get('source', 'unknown'),
                        'relevance': metadata.get('relevance', 0.5),
                        'context_snippet': self._extract_snippet(context, keyword)
                    })
                    break
        
        return {
            'techniques': detected_techniques,
            'source_entry': knowledge_entry
        }
    
    def _extract_snippet(self, text: str, keyword: str, window: int = 200) -> str:
        """Extrae snippet de contexto alrededor de keyword"""
        try:
            idx = text.index(keyword)
            start = max(0, idx - window)
            end = min(len(text), idx + len(keyword) + window)
            return text[start:end].strip()
        except ValueError:
            return ""


class TrainingCodeUpgrader:
    """Actualiza código de entrenamiento con nuevas técnicas"""
    
    def __init__(self, training_scripts_dir: Path = None):
        if training_scripts_dir is None:
            self.training_scripts_dir = Path(__file__).parent.parent
        else:
            self.training_scripts_dir = training_scripts_dir
            
        self.upgrade_log = Path(__file__).parent / "upgrades_log.jsonl"
        self.upgrade_log.parent.mkdir(parents=True, exist_ok=True)
    
    def suggest_upgrades(self, techniques: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Genera sugerencias de mejoras basadas en técnicas detectadas"""
        suggestions = []
        
        for tech in techniques:
            if tech['category'] == 'optimization' and tech['relevance'] > 0.7:
                suggestion = {
                    'technique': tech['name'],
                    'action': 'add_optimization',
                    'code_pattern': self._get_code_pattern(tech['name']),
                    'target_files': ['genesis_trainer/genesis_core.py', 'training/*.py'],
                    'priority': 'high' if tech['relevance'] > 0.8 else 'medium',
                    'description': f"Add {tech['name']} optimization from {tech['source']}"
                }
                suggestions.append(suggestion)
            
            elif tech['category'] == 'fine_tuning' and tech['relevance'] > 0.6:
                suggestion = {
                    'technique': tech['name'],
                    'action': 'enhance_fine_tuning',
                    'code_pattern': self._get_code_pattern(tech['name']),
                    'target_files': ['genesis_trainer/genesis_core.py'],
                    'priority': 'high',
                    'description': f"Enhance fine-tuning with {tech['name']}"
                }
                suggestions.append(suggestion)
        
        return suggestions
    
    def _get_code_pattern(self, technique_name: str) -> str:
        """Retorna patrón de código para una técnica"""
        patterns = {
            'quantization': '''
# Auto-upgraded: Quantization optimization
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config
)
''',
            'attention_optimization': '''
# Auto-upgraded: Flash Attention
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    attn_implementation="flash_attention_2",  # or "sdpa"
    torch_dtype=torch.float16
)
''',
            'gradient_checkpointing': '''
# Auto-upgraded: Gradient Checkpointing
model.gradient_checkpointing_enable()
model.config.use_cache = False  # Required with gradient checkpointing
''',
            'lora': '''
# Auto-upgraded: LoRA configuration
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=64,
    lora_alpha=128,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
)
model = get_peft_model(model, lora_config)
'''
        }
        return patterns.get(technique_name, f"# Technique: {technique_name}\n# Implementation pending")
    
    def apply_upgrade(self, suggestion: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
        """Aplica una mejora sugerida al código"""
        result = {
            'technique': suggestion['technique'],
            'action': suggestion['action'],
            'timestamp': datetime.now().isoformat(),
            'dry_run': dry_run,
            'success': False,
            'changes': []
        }
        
        if dry_run:
            logger.info(f"DRY RUN: Would apply {suggestion['technique']} to {suggestion['target_files']}")
            result['success'] = True
            result['changes'].append({
                'file': suggestion['target_files'][0],
                'action': 'would_add',
                'code_snippet': suggestion['code_pattern'][:100]
            })
        else:
            # Aplicar cambios reales (con backup)
            logger.info(f"APPLYING: {suggestion['technique']}")
            
            # Determinar archivo objetivo (priorizar genesis_core.py)
            target_file = None
            for pattern in suggestion['target_files']:
                if "genesis_core.py" in pattern:
                    target_file = self.training_scripts_dir / "genesis_trainer" / "genesis_core.py"
                    break
            
            if not target_file or not target_file.exists():
                # Fallback a generated_training.py si existe
                target_file = self.training_scripts_dir / "genesis_trainer" / "generated_training.py"
            
            if target_file and target_file.exists():
                try:
                    # Backup
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                    backup_path = target_file.with_suffix(f".bak.{timestamp}")
                    target_file.rename(backup_path)
                    
                    # Leer contenido original
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Inyectar código
                    new_content = content
                    
                    # Lógica simple de inyección: Agregar al final de los imports o al final del archivo
                    # Para una implementación real, esto debería ser más inteligente (AST parsing)
                    if "import" in suggestion['code_pattern']:
                        # Inyectar imports después del último import existente
                        last_import_idx = content.rfind("import ")
                        if last_import_idx != -1:
                            end_of_line = content.find("\n", last_import_idx)
                            new_content = content[:end_of_line+1] + "\n" + suggestion['code_pattern'] + "\n" + content[end_of_line+1:]
                        else:
                            new_content = suggestion['code_pattern'] + "\n" + content
                    else:
                        # Agregar al final de la clase GenesisTrainer si existe, o al final del archivo
                        if "class GenesisTrainer" in content:
                            new_content = content + "\n    # Auto-injected method\n" + suggestion['code_pattern'].replace("\n", "\n    ")
                        else:
                            new_content = content + "\n" + suggestion['code_pattern']
                    
                    # Escribir nuevo archivo
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        
                    result['success'] = True
                    result['changes'].append({
                        'file': str(target_file),
                        'action': 'modified',
                        'backup': str(backup_path)
                    })
                    logger.info(f"Successfully modified {target_file}")
                    
                except Exception as e:
                    logger.error(f"Failed to apply upgrade to {target_file}: {e}")
                    # Restaurar backup si falló
                    if backup_path.exists():
                        if target_file.exists():
                            target_file.unlink()
                        backup_path.rename(target_file)
                    result['success'] = False
                    result['error'] = str(e)
            else:
                logger.warning(f"Target file not found for {suggestion['technique']}")
                result['success'] = False
                result['error'] = "Target file not found"
        
        # Log upgrade
        with open(self.upgrade_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
        
        return result


class AutoUpgradeSystem:
    """Sistema principal de auto-mejora continua"""
    
    def __init__(self, knowledge_db_path: str = None):
        if knowledge_db_path is None:
            self.knowledge_db = Path(__file__).parent / "knowledge_db"
        else:
            self.knowledge_db = Path(knowledge_db_path)
        
        self.analyzer = TechniqueAnalyzer()
        self.upgrader = TrainingCodeUpgrader()
        self.upgrades_applied = []
    
    def scan_new_techniques(self) -> List[Dict[str, Any]]:
        """Escanea archivos de conocimiento recientes buscando técnicas nuevas"""
        technique_files = list(self.knowledge_db.glob("technique_knowledge_*.jsonl"))
        
        # Solo archivos de las últimas 24 horas
        recent_files = sorted(technique_files, key=lambda f: f.stat().st_mtime, reverse=True)[:3]
        
        all_techniques = []
        
        for file in recent_files:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line)
                    analysis = self.analyzer.analyze_technique(entry)
                    
                    if analysis['techniques']:
                        all_techniques.extend(analysis['techniques'])
        
        logger.info(f"Found {len(all_techniques)} technique references")
        return all_techniques
    
    def generate_upgrade_plan(self, min_relevance: float = 0.7) -> Dict[str, Any]:
        """Genera un plan de mejoras basado en técnicas encontradas"""
        techniques = self.scan_new_techniques()
        
        # Filtra por relevancia
        high_value_techniques = [t for t in techniques if t['relevance'] >= min_relevance]
        
        # Genera sugerencias
        suggestions = self.upgrader.suggest_upgrades(high_value_techniques)
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'techniques_found': len(techniques),
            'high_value_techniques': len(high_value_techniques),
            'suggestions': suggestions,
            'estimated_improvements': self._estimate_improvements(suggestions)
        }
        
        return plan
    
    def _estimate_improvements(self, suggestions: List[Dict[str, Any]]) -> Dict[str, str]:
        """Estima mejoras potenciales"""
        improvements = {
            'speed': '0%',
            'memory': '0%',
            'quality': '0%'
        }
        
        for sugg in suggestions:
            tech = sugg['technique']
            if tech in ['quantization', 'attention_optimization']:
                improvements['speed'] = '20-50%'
                improvements['memory'] = '30-50%'
            elif tech in ['lora', 'qlora']:
                improvements['memory'] = '40-60%'
                improvements['quality'] = '10-20%'
            elif tech == 'gradient_checkpointing':
                improvements['memory'] = '50-70%'
        
        return improvements
    
    def auto_upgrade(self, dry_run: bool = True) -> Dict[str, Any]:
        """Ejecuta auto-mejora completa del sistema"""
        logger.info("=" * 80)
        logger.info("🧬 AUTO-UPGRADE SYSTEM - Starting")
        logger.info("=" * 80)
        
        # 1. Genera plan
        plan = self.generate_upgrade_plan()
        
        logger.info(f"Found {plan['high_value_techniques']} high-value techniques")
        logger.info(f"Generated {len(plan['suggestions'])} upgrade suggestions")
        
        # 2. Aplica upgrades (dry run por defecto)
        results = []
        for suggestion in plan['suggestions']:
            result = self.upgrader.apply_upgrade(suggestion, dry_run=dry_run)
            results.append(result)
            self.upgrades_applied.append(result)
        
        summary = {
            'plan': plan,
            'results': results,
            'total_upgrades': len(results),
            'successful_upgrades': sum(1 for r in results if r['success']),
            'dry_run': dry_run
        }
        
        logger.info("=" * 80)
        logger.info(f"✅ Completed: {summary['successful_upgrades']}/{summary['total_upgrades']} upgrades")
        logger.info("=" * 80)
        
        return summary


def main():
    """Ejecuta sistema de auto-mejora"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-Upgrade Training System')
    parser.add_argument('--apply', action='store_true', help='Apply upgrades (default is dry-run)')
    parser.add_argument('--min-relevance', type=float, default=0.7, help='Minimum relevance score')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(name)s:%(message)s'
    )
    
    system = AutoUpgradeSystem()
    
    # Ejecuta auto-upgrade
    summary = system.auto_upgrade(dry_run=not args.apply)
    
    # Imprime reporte
    print("\n" + "=" * 80)
    print("🧬 AUTO-UPGRADE SYSTEM - REPORTE")
    print("=" * 80)
    print(f"\nTécnicas encontradas: {summary['plan']['techniques_found']}")
    print(f"Técnicas de alto valor: {summary['plan']['high_value_techniques']}")
    print(f"Mejoras sugeridas: {len(summary['plan']['suggestions'])}")
    print(f"\nMejoras estimadas:")
    for metric, value in summary['plan']['estimated_improvements'].items():
        print(f"  {metric.capitalize()}: +{value}")
    
    if summary['dry_run']:
        print("\n⚠️  DRY RUN - No se aplicaron cambios reales")
        print("Ejecuta con --apply para aplicar mejoras")
    else:
        print(f"\n✅ Aplicadas {summary['successful_upgrades']} mejoras")
    
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
