#!/usr/bin/env python3
"""
Migration des réservations d'une base source vers une base cible.

But : consolider deux déploiements Railway (www.leboucheaoreilles.be et
web-production-85f59.up.railway.app) qui utilisent des bases PostgreSQL
distinctes, en copiant les réservations manquantes de la base source
(celle du domaine .be) vers la base cible (web-production-85f59).

La migration est idempotente : on n'insère que les réservations dont la
`reference` n'existe pas déjà dans la cible (la référence est unique).

Utilisation :
    # Via des variables d'environnement
    set SOURCE_DATABASE_URL=postgresql://user:pass@host/db
    set TARGET_DATABASE_URL=postgresql://user:pass@host/db
    python migrer_reservations.py

    # Ou via des arguments
    python migrer_reservations.py --source postgresql://... --target postgresql://...

    # Mode "à sec" (dry-run) : affiche ce qui serait migré sans rien écrire
    python migrer_reservations.py --source ... --target ... --dry-run

Les URL PostgreSQL sont disponibles dans Railway :
    Service -> Variables -> DATABASE_URL
"""

import argparse
import os
import sys
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Colonnes de la table reservations (cf. models.py)
COLUMNS = [
    "reference",
    "groupe_reference",
    "nom",
    "email",
    "telephone",
    "date",
    "heure",
    "personnes",
    "message",
    "statut",
    "created_at",
]


def normalize_url(url: str) -> str:
    """Utilise psycopg2 comme driver pour une meilleure stabilité SSL,
    comme dans main.py."""
    if url and url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


def connect(url: str, label: str):
    if not url:
        raise ValueError(f"URL de connexion manquante pour {label}")
    engine = create_engine(
        normalize_url(url),
        pool_pre_ping=True,
        pool_recycle=300,
        future=True,
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"[OK] Connexion à {label} réussie.")
    return engine


def get_existing_references(engine) -> set:
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT reference FROM reservations")).fetchall()
    return {r[0] for r in rows}


def fetch_source_reservations(engine):
    cols = ", ".join(COLUMNS)
    with engine.connect() as conn:
        rows = conn.execute(text(f"SELECT {cols} FROM reservations")).fetchall()
    return [dict(zip(COLUMNS, r)) for r in rows]


def insert_reservation(engine, row, dry_run: bool) -> bool:
    cols = ", ".join(COLUMNS)
    params = {c: row[c] for c in COLUMNS}
    placeholders = ", ".join(f":{c}" for c in COLUMNS)
    sql = text(f"INSERT INTO reservations ({cols}) VALUES ({placeholders})")
    if dry_run:
        return True
    with engine.begin() as conn:
        conn.execute(sql, params)
    return True


def main():
    parser = argparse.ArgumentParser(description="Migrer les réservations source -> cible")
    parser.add_argument("--source", default=os.environ.get("SOURCE_DATABASE_URL"),
                        help="DATABASE_URL de la base source (domaine .be)")
    parser.add_argument("--target", default=os.environ.get("TARGET_DATABASE_URL"),
                        help="DATABASE_URL de la base cible (web-production-85f59)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher ce qui serait migré sans rien écrire")
    args = parser.parse_args()

    if not args.source or not args.target:
        print("ERREUR : vous devez fournir --source et --target "
              "(ou les variables SOURCE_DATABASE_URL / TARGET_DATABASE_URL).")
        parser.print_help()
        sys.exit(2)

    print("=" * 60)
    print(f"Mode : {'DRY-RUN (aucune écriture)' if args.dry_run else 'RÉEL (écriture)'}")
    print("=" * 60)

    engine_src = connect(args.source, "SOURCE (www.leboucheaoreilles.be)")
    engine_tgt = connect(args.target, "CIBLE (web-production-85f59)")

    existing = get_existing_references(engine_tgt)
    print(f"Cible : {len(existing)} réservation(s) déjà présente(s).")

    rows = fetch_source_reservations(engine_src)
    print(f"Source : {len(rows)} réservation(s) trouvée(s).")

    to_migrate = [r for r in rows if r["reference"] not in existing]
    already = len(rows) - len(to_migrate)
    print(f"À migrer : {len(to_migrate)} | déjà présentes (ignorées) : {already}")

    if not to_migrate:
        print("Rien à migrer. La cible est déjà à jour.")
        return

    print("-" * 60)
    migrated = 0
    for r in to_migrate:
        insert_reservation(engine_tgt, r, args.dry_run)
        migrated += 1
        print(f"  {'[DRY]' if args.dry_run else '[OK]'} {r['reference']} | "
              f"{r['nom']} | {r['date']} {r['heure']} | {r['personnes']}p | {r['statut']}")

    print("-" * 60)
    print(f"Migration terminée : {migrated} réservation(s) "
          f"{'simulée(s)' if args.dry_run else 'insérée(s)'} dans la cible.")
    if args.dry_run:
        print("Relancez sans --dry-run pour appliquer réellement.")


if __name__ == "__main__":
    main()
