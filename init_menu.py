import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main import app, db
from models import Plat

MENU_PAR_DEFAUT = [
    # Aucun plat par defaut : le menu est gere manuellement depuis l'administration.
]


def initialiser_menu(vider_existant=True):
    with app.app_context():
        try:
            if vider_existant:
                nombre_supprimes = Plat.query.delete()
                db.session.commit()
                print(f"{nombre_supprimes} plat(s) existant(s) supprimé(s).")

            for item in MENU_PAR_DEFAUT:
                plat = Plat(
                    nom=item["nom"],
                    description=item["description"],
                    prix=item["prix"],
                    categorie=item["categorie"]
                )
                db.session.add(plat)

            db.session.commit()
            print(f"{len(MENU_PAR_DEFAUT)} plats ajoutés avec succès.")

            print("\n--- Menu initialisé ---")
            for plat in Plat.query.order_by(Plat.categorie, Plat.nom).all():
                print(f"[{plat.categorie}] {plat.nom} - {plat.prix:.2f} €")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'initialisation du menu : {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    vider = True
    if len(sys.argv) > 1 and sys.argv[1].lower() in ('--ajouter', '-a', 'append'):
        vider = False
    success = initialiser_menu(vider_existant=vider)
    sys.exit(0 if success else 1)
