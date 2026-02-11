#!/usr/bin/env python3
"""
Vérifie que .env.example contient toutes les variables nécessaires.
"""

import re
from pathlib import Path

def main():
    """Vérifie le fichier .env.example."""
    project_root = Path(__file__).parent
    env_example = project_root / ".env.example"
    
    # Variables requises selon app/config.py
    required_vars = {
        "OPENAI_API_KEY",
        "EMBEDDING_MODEL",
        "CHAT_MODEL",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "SUPABASE_SERVICE_KEY",
        "CHUNK_SIZE",
        "CHUNK_OVERLAP",
        "SEARCH_TOP_K",
    }
    
    if not env_example.exists():
        print("❌ .env.example n'existe pas")
        return 1
    
    # Lire le fichier
    try:
        content = env_example.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Impossible de lire .env.example: {e}")
        return 1
    
    # Extraire les variables définies
    found_vars = set()
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            match = re.match(r'^([A-Z_]+)=', line)
            if match:
                found_vars.add(match.group(1))
    
    print("🔍 Vérification de .env.example...\n")
    print(f"Variables trouvées: {len(found_vars)}")
    print(f"Variables requises: {len(required_vars)}\n")
    
    missing = required_vars - found_vars
    extra = found_vars - required_vars
    
    if missing:
        print(f"❌ Variables manquantes ({len(missing)}):")
        for var in sorted(missing):
            print(f"  - {var}")
        return 1
    
    if extra:
        print(f"⚠️  Variables supplémentaires ({len(extra)}):")
        for var in sorted(extra):
            print(f"  - {var}")
    
    print("\n✅ .env.example contient toutes les variables requises !")
    print("\nVariables présentes:")
    for var in sorted(required_vars):
        print(f"  ✓ {var}")
    
    return 0

if __name__ == "__main__":
    exit(main())

