#!/usr/bin/env python3
"""
Migration : etendre la colonne 'reference' de VARCHAR(20) a VARCHAR(30)
pour accommoder le nouveau format Table1-2026-08-28.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main import app, db

def migrate():
    with app.app_context():
        try:
            print("🔗 Connexion a la base de donnees...")
            db_url = os.environ.get('DATABASE_URL', '')
            is_postgres = 'postgresql' in db_url

            if is_postgres:
                print("📍 Base PostgreSQL detectee.")
                sql = "ALTER TABLE reservations ALTER COLUMN reference TYPE VARCHAR(30);"
            else:
                print("📍 Base SQLite detectee.")
                sql = None  # SQLite ignore la taille du VARCHAR

            if sql:
                print("⏳ Execution du ALTER TABLE...")
                with db.engine.connect() as conn:
                    conn.execute(db.text(sql))
                    conn.commit()
                print("✅ Colonne 'reference' etendue a VARCHAR(30) avec succes!")
            else:
                print("✅ SQLite : aucune modification necessaire (VARCHAR flexible).")

            print("\n✅ Migration terminee avec succes!")

        except Exception as e:
            print(f"\n❌ Erreur lors de la migration:")
            print(f"   {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate()
