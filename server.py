import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

bookings = []  # historique des réservations

def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Club not found with this email")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=None, competitions=competitions)

def saveClubs():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)

def saveCompetitions():
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        # Vérifications
        if placesRequired <= 0:
            flash('Please enter a positive number of places.')
            return render_template('booking.html', club=club, competition=competition)

        if placesRequired > 12:
            flash('You cannot book more than 12 places in one booking.')
            return render_template('booking.html', club=club, competition=competition)

        if placesRequired > club_points:
            flash(f'Not enough points! You have {club_points} points.')
            return render_template('booking.html', club=club, competition=competition)

        if placesRequired > competition_places:
            flash(f'Not enough places available! Only {competition_places} left.')
            return render_template('booking.html', club=club, competition=competition)

        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            flash('Cannot book places for past competitions.')
            return render_template('booking.html', club=club, competition=competition)

        # Mise à jour
        club['points'] = str(club_points - placesRequired)
        competition['numberOfPlaces'] = str(competition_places - placesRequired)
        
        booking_record = {
            'club': club['name'],
            'competition': competition['name'],
            'places': placesRequired,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'competition_date': competition['date']  # Pour afficher le statut
        }
        bookings.append(booking_record)

        saveClubs()
        saveCompetitions()

        flash(f'Great - booking complete! {placesRequired} places booked for {competition["name"]}.', 'success')
        return render_template('welcome.html', club=club, competitions=competitions)

    except (IndexError, ValueError):
        flash("Something went wrong - please try again")
        return redirect(url_for('index'))

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/booking_history')
def booking_history():
    club_name = request.args.get('club')
    if not club_name:
        flash('Club not specified.')
        return redirect(url_for('index'))
    
    # Filtrer les réservations par club
    club_bookings = [b for b in bookings if b['club'] == club_name]
    
    return render_template('booking_history.html', 
                         bookings=club_bookings, 
                         club_name=club_name)

@app.route('/points')
def points_display():
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
