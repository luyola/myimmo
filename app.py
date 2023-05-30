from flask import Flask, render_template, request, redirect, url_for, session
#import  psycopg2


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Appartement, Locataire

# Création de la base de données
engine = create_engine("postgresql://db_user:zola@localhost:5432/flask_db")
# Création de la session
Session = sessionmaker(bind=engine)
db_session = Session()


app = Flask(__name__)
app.config['SECRET_KEY'] = '0e488d3034d02a14eec471a99d6b34f39bb24cbc945af64ecc5f0ec8feb79f44'

# Connexion à la base de données
#conn = psycopg2.connect("postgresql://db_user:zola@localhost:5432/flask_db")
# Création d'un curseur
#cur = conn.cursor()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Vérifier les identifiants de l'utilisateur (remplacez cette étape par votre propre logique d'authentification)
        username = request.form['username']
        password = request.form['password']
        if username == 'Zola' and password == '1234':
            # Si les identifiants sont valides, rediriger vers la page d'accueil
            session['user'] = {'username': 'Zola'}
            return redirect(url_for('accueil'))
        else:
            # Si les identifiants sont invalides, afficher un message d'erreur
            erreur = 'Identifiants invalides'
            return render_template('login.html', erreur=erreur)
    else :
        # Afficher la page de connexion
        return render_template('login.html')

# Page d'accueil

@app.route('/accueil')

def accueil():

    #if 'user' in session:

    if session:

        return render_template('accueil.html')

    else:

        return redirect('/login')



@app.route('/logout')

def logout():
    session.clear()
    # correctement deconnecté
    return redirect('login')



# Page de gestion des appartements
@app.route('/gestion-appartements')
def gestion_appartements():
    if session:
        # Récupération de tous les appartements de la base de données
        appartements = db_session.query(Appartement).all()
        return render_template('gestion_appartements.html', appartements=appartements)

    else:

        return redirect('/login')


@app.route('/add-appartements', methods=['GET', 'POST'])
def add_appartements():
    if session:
        if request.method == 'POST':
            # Récupération des données du formulaire
            adresse = request.form['adresse']
            surface = int(request.form['surface'])
            loyer = int(request.form['loyer'])
            nombre_pieces = int(request.form['nombre_pieces'])
            etage = int(request.form['etage'])

            # Création d'une instance d'Appartement
            nouvel_appartement = Appartement(
                adresse=adresse,
                surface=surface,
                loyer=loyer,
                nombre_pieces=nombre_pieces,
                etage=etage
            )
            # Ajout de l'instance à la session
            db_session.add(nouvel_appartement)
            # Commit de la session pour effectuer l'INSERT dans la base de données
            db_session.commit()
            # Message de succès
            message = "L'appartement a été ajouté avec succès."
            return render_template('add_appartements.html', message=message)
        else :
            return render_template('add_appartements.html')
    else:
        return redirect('/login')



@app.route('/update-appartement/<int:appartement_id>', methods=['GET', 'POST'])
def update_appartement(appartement_id):
    if session:
        # Recherche de l'appartement à modifier par son ID
        appartement = db_session.query(Appartement).get(appartement_id)


        if not appartement:
            # L'appartement n'a pas été trouvé, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
            return redirect('/gestion-appartements')

        if request.method == 'POST':
            # Récupération des données du formulaire
            appartement.adresse = request.form['adresse']
            appartement.surface = int(request.form['surface'])
            appartement.loyer = int(request.form['loyer'])
            appartement.nombre_pieces = int(request.form['nombre_pieces'])
            appartement.etage = int(request.form['etage'])

            # Commit de la session pour effectuer la mise à jour dans la base de données
            db_session.commit()

            # Message de succès
            message = "L'appartement a été modifié avec succès."
            return render_template('update_appartement.html', appartement=appartement, message=message)
        else:
            return render_template('update_appartement.html', appartement=appartement)
    else:
        return redirect('/login')

@app.route('/update-locataire/<int:locataire_id>', methods=['GET', 'POST'])
def update_locataire(locataire_id):
    if session:
        # Recherche de l'appartement à modifier par son ID
        locataires = db_session.query(Locataire).get(locataire_id)

        if not locataires:
            # L'appartement n'a pas été trouvé, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
            return redirect('/gestion-locataires')

        if request.method == 'POST':
            locataires.nom = request.form['nom']
            locataires.prenom = request.form['prenom']
            locataires.date_naissance = request.form['date_naissance']
            locataires.adresse = request.form['adresse']
            locataires.ville = request.form['ville']
            locataires.telephone = request.form['telephone']
            locataires.email = request.form['email']
            locataires.depot_garantie = request.form['depot_garantie']

            # Modification de l'appartement associé au locataire
            appartement_id = request.form['appartement']
            if appartement_id:
                appartement = db_session.query(Appartement).get(appartement_id)
                if appartement:
                    locataires.appartement = appartement
                else:
                    # L'appartement n'a pas été trouvé, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
                    return redirect('/gestion-locataires')
            else:
                # Le locataire n'est pas associé à un appartement
                locataires.appartement = None

            # Commit de la session pour effectuer la mise à jour dans la base de données
            db_session.commit()

            # Message de succès
            message = "Le locataire a été modifié avec succès."
            return render_template('update_locataire.html', locataires=locataires, message=message)

        else:
            # Récupérer la liste des appartements pour le menu déroulant
            appartements = db_session.query(Appartement).all()
            return render_template('update_locataire.html', locataires=locataires, appartements=appartements)
    else:
        return redirect('/login')


@app.route('/delete-appartement/<int:appartement_id>', methods=['GET', 'POST'])
def delete_appartement(appartement_id):
    if session:
        # Recherche de l'appartement à supprimer par son ID
        appartement = db_session.query(Appartement).get(appartement_id)

        if not appartement:
            # L'appartement n'a pas été trouvé, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
            return redirect('/gestion-appartements')

        if request.method == 'POST':
            # Suppression de l'appartement de la base de données
            db_session.delete(appartement)
            db_session.commit()

            # Message de succès
            message = "L'appartement a été supprimé avec succès."
            return redirect('/gestion-appartements')

        return render_template('delete_appartement.html', appartement=appartement)
    else:
        return redirect('/login')



# Page de gestion des locataires
@app.route('/gestion_locataires')
def gestion_locataires():
    if session:
        locataires = db_session.query(Locataire).all()
        return render_template('gestion_locataires.html', locataires=locataires)
    else:
        return redirect('/login')

@app.route('/add-locataires', methods=['GET', 'POST'])
def add_locataires():
    if session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            date_naissance = request.form['date_naissance']
            adresse = request.form['adresse']
            ville = request.form['ville']
            telephone = request.form['telephone']
            email = request.form['email']
            depot_garantie = request.form['depot_garantie']

            locataire = Locataire(nom=nom, prenom=prenom, date_naissance=date_naissance, adresse=adresse, ville=ville,
                              telephone=telephone, email=email, depot_garantie=depot_garantie)
            db_session.add(locataire)
            db_session.commit()
            # Message de succès
            message = "Le locataire a été add avec succès."
            return render_template('add_locataires.html', message=message)

        return render_template('add_locataires.html')
    else:
        return redirect('/login')



# Page de gestion des paiements
@app.route('/gestion-paiements')
def gestion_paiements():
    if session:
        # Récupérer le mois à partir du paramètre d'URL
        #mois = request.args.get('mois', '')
        locataires = db_session.query(Locataire).all()


        return render_template('gestion_paiements.html', locataires=locataires)
    else:
        return redirect('/login')


@app.route('/add-paiements/<int:locataire_id>', methods=['GET', 'POST'])
def add_paiements(locataire_id):
    if session:

        locataires = db_session.query(Locataire).get(locataire_id)
        appartements = db_session.query(Locataire).join(Appartement).filter(locataires == 2).all()

        if request.method == 'POST':


            return redirect('/gestion-paiements')

        else:

            return render_template('add_paiements.html', locataires=locataires, appartements=appartements)

    else:
        return redirect('/login')


@app.route('/update-paiements/<int:paiement_id>', methods=['GET', 'POST'])
def update_paiements(paiement_id):
    if session:
        # Recherche du paiement à modifier par son ID
        paiement = db_session.query(Paiement).get(paiement_id)

        if not paiement:
            # Le paiement n'a pas été trouvé, afficher un message d'erreur ou rediriger vers la page gestion
            return redirect('/gestion-paiements')

        if request.method == 'POST':
            # Mettre à jour les paiements
            paiement.locataire_id = request.form['locataire']
            paiement.montant = request.form['montant']
            paiement.date_paiement = request.form['date']

            db_session.commit()

            # Message de succès
            message = "Le paiement a été modifié avec succès."
            return render_template('update_paiements.html', paiement=paiement, locataires=Locataire.query.all(), message=message)
        else:
            return render_template('update_paiements.html', paiement=paiement, locataires=Locataire.query.all())

    else:
        return redirect('/login')

@app.route('/delete-paiement/<int:paiement_id>', methods=['GET', 'POST'])
def delete_paiement(paiement_id):
        if session:
            #paiement à supprimer par son ID
            paiement = db_session.query(Paiement).get(paiement_id)

            if not paiement:
                # Si le paiement n'a pas été trouvé, afficher un message d'erreur
                return redirect('/gestion-paiements')

            if request.method == 'POST':
                # Supprimer le paiement de la base de données
                db_session.delete(paiement)
                db_session.commit()

                # Message de succès
                message = "Le paiement a été supprimé avec succès."
                return render_template('delete_paiement.html', message=message)
            else:
                return render_template('delete_paiement.html', paiement=paiement)
        else:
            return redirect('/login')


# Page de génération des quittances de loyer

@app.route('/generation-quittances')

def generation_quittances():

    if session:

        return render_template('generation_quittances.html')

    else:

        return redirect('/login')

    # Générer la quittance de loyer sur une période donnée si le locataire est en règle des loyers sur la période



# Page de bilan des comptes

@app.route('/bilan-comptes')

def bilan_comptes():

    if session:

        return render_template('bilan_comptes.html')

    else:

        return redirect('/login')

    # Faire un bilan des comptes des loyers émis par le locataire lorsqu'il quitte le logement



if __name__ == '__main__':

    app.run(debug=True)






"""
@app.route('/')

def index():

    return render_template('index.html', title='Accueil')


@app.route('/profil')

def profil():

    return render_template('profil.html', title='Profil')



@app.route('/login')

def login():

    # formulaire

    #BDD

    session['user'] = {

        'username': 'Zola',

        'email': 'zola.mbala@domain.fr'

    }

    session['user']['role'] = 'admin'

    # MSG connecté

    return redirect(url_for('index'))


@app.route('/logout')

def logout():

    session.clear()

    # correctement deconnecté

    return redirect(url_for('index'))


    gestion_appartements = "/gestion-appartements"

    ajouter_locataires = "/ajouter-locataires"

    gestion_paiements = "/gestion-paiements"

    generation_quittances = "/generation-quittances"

    bilan_comptes = "/bilan-comptes"

    return render_template('index.html', gestion_appartements=gestion_appartements,

                           ajouter_locataires=ajouter_locataires,

                           gestion_paiements=gestion_paiements,

                           generation_quittances=generation_quittances,

                           bilan_comptes=bilan_comptes)
"""