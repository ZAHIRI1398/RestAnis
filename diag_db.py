import sys
from sqlalchemy import create_engine, text

URL = "postgresql+psycopg2://postgres:FytxspLIVjaKySPTCxiaJLucIviRzMGg@altaria.proxy.rlwy.net:33198/railway"

engine = create_engine(URL, pool_pre_ping=True, future=True)
with engine.connect() as c:
    tables = [r[0] for r in c.execute(text(
        "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"))]
    print("TABLES:", tables)

    if "reservations" in tables:
        n = c.execute(text("SELECT COUNT(*) FROM reservations")).scalar()
        print("RESERVATIONS COUNT:", n)
        rows = c.execute(text(
            "SELECT id, reference, nom, date, heure, personnes, statut, created_at "
            "FROM reservations ORDER BY created_at DESC LIMIT 20")).fetchall()
        print("--- Dernières 20 réservations ---")
        for r in rows:
            print(" ", r)
    else:
        print("Table 'reservations' absente.")

    if "menu_documents" in tables:
        docs = c.execute(text(
            "SELECT id, nom_fichier, date_upload FROM menu_documents ORDER BY id")).fetchall()
        print("MENU DOCS:", docs)
        pages = c.execute(text(
            "SELECT document_id, numero FROM menu_document_pages "
            "ORDER BY document_id, numero")).fetchall()
        print("MENU PAGES:", pages)

    if "menu" in tables:
        print("PLATS COUNT:", c.execute(text("SELECT COUNT(*) FROM menu")).scalar())
