import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

# Stockage en mémoire des réservations (serait perdu au redémarrage)
bookings = []  # historique des réservations

def loadClubs():
    """Charge la liste des clubs depuis le fichier JSON"""
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def loadCompetitions():
    """Charge la liste des compétitions depuis le fichier JSON"""
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'something_special'  # Clé secrète pour les sessions et flash messages

# Chargement des données au démarrage
competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    """Page d'accueil avec formulaire de connexion"""
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    """Traite la connexion d'un club et affiche le tableau de bord"""
    email = request.form['email']
    password = request.form['password']
    
    try:
        # Recherche du club par email
        club = [club for club in clubs if club['email'] == email][0]
        
        # Vérification simple du mot de passe
        if club.get('password') != password:
            flash("Invalid email or password")
            return redirect(url_for('index'))
            
    except IndexError:
        # Aucun club trouvé avec cet email
        flash("Club not found with this email")
        return redirect(url_for('index'))
    
    # Connexion réussie - affichage du tableau de bord
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Page de réservation de places pour une compétition"""
    try:
        # Recherche du club et de la compétition
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except IndexError:
        # Erreur si club ou compétition non trouvé
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=None, competitions=competitions)

def saveClubs():
    """Sauvegarde les données des clubs dans le fichier JSON"""
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)

def saveCompetitions():
    """Sauvegarde les données des compétitions dans le fichier JSON"""
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """Traite l'achat de places pour une compétition"""
    try:
        # Récupération des données du formulaire
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        # Conversion des valeurs numériques
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        # Vérification: nombre de places positif
        if placesRequired <= 0:
            flash('Please enter a positive number of places.')
            return render_template('booking.html', club=club, competition=competition)

        # Vérification: limite de 12 places par réservation
        if placesRequired > 12:
            flash('You cannot book more than 12 places in one booking.')
            return render_template('booking.html', club=club, competition=competition)

        # Vérification: points suffisants
        if placesRequired > club_points:
            flash(f'Not enough points! You have {club_points} points.')
            return render_template('booking.html', club=club, competition=competition)

        # Vérification: places disponibles
        if placesRequired > competition_places:
            flash(f'Not enough places available! Only {competition_places} left.')
            return render_template('booking.html', club=club, competition=competition)

        # Vérification: compétition non passée
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            flash('Cannot book places for past competitions.')
            return render_template('booking.html', club=club, competition=competition)

        # Mise à jour des points et places
        club['points'] = str(club_points - placesRequired)
        competition['numberOfPlaces'] = str(competition_places - placesRequired)
        
        # Enregistrement de la réservation dans l'historique
        booking_record = {
            'club': club['name'],
            'competition': competition['name'],
            'places': placesRequired,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'competition_date': competition['date']
        }
        bookings.append(booking_record)

        # Sauvegarde des modifications
        saveClubs()
        saveCompetitions()

        # Confirmation de réservation
        flash(f'Great - booking complete! {placesRequired} places booked for {competition["name"]}.', 'success')
        return render_template('welcome.html', club=club, competitions=competitions)

    except (IndexError, ValueError):
        # Gestion des erreurs (données manquantes ou conversion échouée)
        flash("Something went wrong - please try again")
        return redirect(url_for('index'))

@app.context_processor
def inject_now():
    """Injecte la date/heure actuelle dans tous les templates"""
    return {'now': datetime.now()}

@app.route('/booking_history')
def booking_history():
    """Affiche l'historique des réservations d'un club"""
    club_name = request.args.get('club')
    if not club_name:
        flash('Club not specified.')
        return redirect(url_for('index'))
    
    # Filtrage des réservations par club
    club_bookings = [b for b in bookings if b['club'] == club_name]
    
    return render_template('booking_history.html', 
                         bookings=club_bookings, 
                         club_name=club_name)

@app.route('/points')
def points_display():
    """Affiche le tableau des points de tous les clubs"""
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    """Déconnexion - redirection vers la page d'accueil"""
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Lancement de l'application en mode debug
    app.run(debug=True)