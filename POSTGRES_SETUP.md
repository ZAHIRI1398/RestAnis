# Configuration PostgreSQL - Railway

## ✅ Statut
PostgreSQL a été configuré avec succès sur Railway pour l'environnement de production.

## 📋 Détails de la configuration

### Service PostgreSQL
- **Nom** : Postgres
- **ID Service** : dbc930da-b962-4713-a180-52f60a6ce3e5
- **Hôte** : postgres.railway.internal
- **Port** : 5432 (par défaut PostgreSQL)

### Variables d'environnement connectées à votre application web
- `DATABASE_URL` - URL de connexion PostgreSQL complète
- `PGHOST` - Nom d'hôte
- `PGPORT` - Port
- `PGUSER` - Utilisateur PostgreSQL
- `PGPASSWORD` - Mot de passe PostgreSQL
- `PGDATABASE` - Nom de la base de données

### Tables PostgreSQL
Votre application crée automatiquement les tables suivantes :

1. **menu** - Catalogue des plats
   - id, nom, description, prix, categorie, image

2. **reservations** - Enregistrement des réservations clients
   - id, reference, groupe_reference, nom, email, telephone, date, heure, personnes, message, statut, created_at

3. **menu_documents** - Documents PDF du menu
4. **menu_document_pages** - Pages du menu (images PNG)

## 🔄 Flux de réservation

1. **Client réserve sur le web** → `POST /reservation/creer_reservation`
2. **Réservation enregistrée automatiquement** → Table `reservations` sur PostgreSQL
3. **Email de réception envoyé** → Via Resend API
4. **Admin valide la réservation** → Via tableau de bord `/admin/reservations`
5. **Email de confirmation envoyé** → Au client
6. **Données persistées** → Sur PostgreSQL

## 📊 Consultation des données

### Via Railway
1. Allez à https://railway.com/project/16b352ef-573f-4bcd-951e-947022ff0ef0
2. Sélectionnez le service "Postgres"
3. Allez dans l'onglet "Data" pour voir les tables et les données

### Via Python (local ou via Railway)
```bash
python init_postgres.py
```

### Via ligne de commande
```bash
psql $DATABASE_URL -c "SELECT * FROM reservations;"
```

## ✨ Changements effectués

- ✅ PostgreSQL template déployé sur Railway
- ✅ Variables d'environnement PostgreSQL liées au service web
- ✅ Votre code utilise déjà SQLAlchemy avec PostgreSQL (psycopg2)
- ✅ Tables créées automatiquement au démarrage

## 🚀 Prochaines étapes (optionnel)

1. **Tester une réservation** sur votre site web
2. **Vérifier les données** dans le tableau de bord admin `/admin/reservations`
3. **Consulter PostgreSQL** via Railway ou via `psql`

## 📝 Remarques

- En local : SQLite (`data/restaurant.db`)
- En production (Railway) : PostgreSQL
- Les migrations se font automatiquement avec `db.create_all()`
- Les emails de confirmation sont gérés par Resend (clé API requise dans les variables)

---

**Vos clients peuvent maintenant réserver, et toutes les réservations sont persistées dans PostgreSQL ! 🎉**

