#!/usr/bin/env python3
"""
Script de test pour valider la structure du projet RAG PDF.
Vérifie les imports, la syntaxe et la cohérence du code.
"""

import ast
import os
import sys
from pathlib import Path

def check_file_syntax(filepath: Path) -> bool:
    """Vérifie que le fichier Python a une syntaxe valide."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            ast.parse(f.read(), filename=str(filepath))
        return True
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe dans {filepath}: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filepath}: {e}")
        return False

def check_imports(filepath: Path) -> list[str]:
    """Extrait les imports d'un fichier Python."""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
    except Exception as e:
        print(f"⚠️  Impossible d'analyser les imports de {filepath}: {e}")
    return imports

def main():
    """Teste la structure du projet."""
    project_root = Path(__file__).parent
    app_dir = project_root / "app"
    
    print("🔍 Vérification de la structure du projet RAG PDF...\n")
    
    # Vérifier les fichiers essentiels
    essential_files = {
        "app/main.py": "Point d'entrée FastAPI",
        "app/config.py": "Configuration",
        "app/models/schemas.py": "Schémas Pydantic",
        "app/routers/ingest.py": "Route d'ingestion",
        "app/routers/chat.py": "Route de chat",
        "app/services/extractor.py": "Service d'extraction PDF",
        "app/services/chunker.py": "Service de découpage",
        "app/services/embeddings.py": "Service d'embeddings",
        "app/services/vectorstore.py": "Service de vector store",
        "app/services/llm.py": "Service LLM",
        "requirements.txt": "Dépendances",
        "Dockerfile": "Configuration Docker",
        "docker-compose.yml": "Docker Compose",
        "sql/setup.sql": "Schéma Supabase",
    }
    
    errors = []
    warnings = []
    
    for filepath_str, description in essential_files.items():
        filepath = project_root / filepath_str
        if filepath.exists():
            print(f"✓ {filepath_str} - {description}")
            if filepath.suffix == '.py':
                if not check_file_syntax(filepath):
                    errors.append(f"Syntaxe invalide: {filepath_str}")
        else:
            print(f"❌ {filepath_str} - MANQUANT ({description})")
            errors.append(f"Fichier manquant: {filepath_str}")
    
    print("\n📦 Vérification des imports...")
    
    # Vérifier les imports dans les fichiers Python
    python_files = list(app_dir.rglob("*.py"))
    all_imports = set()
    
    for py_file in python_files:
        imports = check_imports(py_file)
        all_imports.update(imports)
        if py_file.name != "__init__.py":
            print(f"  {py_file.relative_to(project_root)}: {len(imports)} imports")
    
    # Vérifier les dépendances dans requirements.txt
    print("\n📋 Vérification des dépendances...")
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        with open(req_file, 'r') as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"  {len(deps)} dépendances trouvées:")
        for dep in deps:
            print(f"    - {dep}")
    
    # Vérifier .env.example
    env_example = project_root / ".env.example"
    if env_example.exists():
        print("\n✓ .env.example existe")
    else:
        warnings.append(".env.example manquant")
        print("\n⚠️  .env.example manquant (création recommandée)")
    
    # Résumé
    print("\n" + "="*50)
    if errors:
        print(f"❌ {len(errors)} erreur(s) trouvée(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    elif warnings:
        print(f"⚠️  {len(warnings)} avertissement(s):")
        for warn in warnings:
            print(f"  - {warn}")
        print("✓ Structure globale OK")
        return 0
    else:
        print("✅ Tous les tests de structure sont passés !")
        return 0

if __name__ == "__main__":
    sys.exit(main())

