import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def saveClubs():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c)

def saveCompetitions():
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        
        # Convertir en entiers pour les calculs
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])
        
        # Vérification pour les nombres positifs
        if placesRequired <= 0:
            flash('Please enter a positive number of places.')
            return render_template('booking.html', club=club, competition=competition), 400
        
        # Vérification des points du club
        if placesRequired > club_points:
            flash(f'Not enough points! You have {club_points} points but want to book {placesRequired} places.')
            return render_template('booking.html', club=club, competition=competition), 400
        
        # Vérification des places disponibles
        if placesRequired > competition_places:
            flash(f'Not enough places available! Only {competition_places} places left.')
            return render_template('booking.html', club=club, competition=competition), 400
        
        # Mettre à jour les points du club et les places de la compétition
        club['points'] = str(club_points - placesRequired)
        competition['numberOfPlaces'] = str(competition_places - placesRequired)
        
        # Sauvegarder les modifications
        saveClubs()
        saveCompetitions()
        
        
    
    except (IndexError, ValueError) as e:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 400


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)