from flask import Flask, render_template, request, redirect, url_for
import os
import random
from playsound import playsound
import pymysql


app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "sqlite:///{}".format(os.path.join(project_dir, "commentdatabase.db"))

#app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#app.config['WHOOSH_BASE'] = 'whoosh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://18_kozhara:your_password@127.0.0.1/your_db'


db = SQLAlchemy(app)
i = 1
def mydefault():
    global i
    i += 1
    return i
comments = None


class Comment(db.Model):
    __searchable__ = ['temat']
    id = db.Column(db.Integer, primary_key=True, default = mydefault())
    pseudonim = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, primary_key=True)
    komentarz = db.Column(db.String(300), nullable=False)
    temat = db.Column(db.String(80), nullable=False)
  
    def __repr__(self):
        return "<Pseudonim: {0}, komentarz {1}, email {2}, temat {3}.>".format(self.pseudonim, self.komentarz, self.email, self.temat)
    

@app.route('/18_kozhara/poradnik_dwujezyczni', methods=["GET", "POST"])
def add_comment():
    global comments
    #comments = None
    if request.method == 'POST':
        if request.form:
            comment = Comment(pseudonim = request.form.get("name"), email = request.form.get("email"), komentarz = request.form.get("message"), temat = request.form.get("subject"))
            db.session.add(comment)
            db.session.commit()
    comments = Comment.query.all()
    #return redirect('/18_kozhara/poradnik_dwujezyczni')
    return redirect(url_for('main'))
    return render_template("index.html", comments = comments)
    



#wa.whoosh_index(app, Comment)

"""Gra Memory"""

class Card:
    def __init__(self, name):
        self.name = name
    status = 'closed'    

class Talia:
    def __init__(self):
        self.nazwy = ['krowa', 'jez', 'flamingo', 'lis', 'pies', 'ptaszek', 'pszczola', 'kaczka', 'zaba', 'waz', 'krowa', 'jez', 'flamingo', 'lis', 'pies', 'ptaszek', 'pszczola', 'kaczka', 'zaba', 'waz']
        self.karty = self.utworz_talie()
        
    def utworz_talie(self):
        karty = list() 
        for i in range(0,20):
            karty.append(Card(self.nazwy[i])) 
        karty = random.sample(karty, len(karty))
        dictionary = dict(zip([x for x in range(20)], karty))
        return dictionary
        
talia = Talia() 
odkryte = 0 
temp = 0 
@app.route("/", methods = ['GET', 'POST'])
def main(): 
    global comments
    comments = Comment.query.all()
    return render_template('index.html', comments = comments)

@app.route("/memory")
def gra_memory():
    global talia
    global odkryte
    #global temp
    return render_template('memory.html', talia = talia, odkryte = odkryte)

"""@app.route("/<ajdi>", methods = ['GET','POST']) 
def otworz(ajdi):
    global talia
    global odkryte
    global temp
    
    lista_audio=[]
    for key in talia.karty:
        if key == int(ajdi):
            talia.karty[key].status = 'opened'
            if talia.karty[key].name == 'kaczka':
                lista_audio = ['/static/music/memory/kaczka.mp3','static/music/memory/duck.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
                
            elif talia.karty[key].name == 'waz':
                 lista_audio = ['/static/music/memory/waz.mp3','/static/music/memory/snake.mp3']
                 wybor = random.choice(lista_audio)
                 playsound(wybor)
            elif talia.karty[key].name == 'flamingo':
                lista_audio = ['/static/music/memory/flaming.mp3','/static/music/memory/flamingo.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'jez':
                lista_audio = ['/static/music/memory/jez.mp3','/static/music/memory/hedgehog.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'krowa':
                lista_audio = ['/static/music/memory/krowa.mp3','/static/music/memory/cow.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'lis':
                lista_audio = ['/static/music/memory/lis.mp3','/static/music/memory/fox.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'pies':
                lista_audio = ['/static/music/memory/pies.mp3','/static/music/memory/dog.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'pszczola':
                lista_audio = ['/static/music/memory/pszczola.mp3','/static/music/memory/bee.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'ptaszek':
                lista_audio = ['/static/music/memory/ptak.mp3','/static/music/memory/bird.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
            elif talia.karty[key].name == 'zaba':
                lista_audio = ['/static/music/memory/zaba.mp3','/static/music/memory/frog.mp3']
                wybor = random.choice(lista_audio)
                playsound(wybor)
                
           
            odkryte +=1 
        if odkryte == 2:
            if wygrana():
                    render_template("wygrana.html")
            lista_pomocnicza = list()
            for key in talia.karty:
                if talia.karty[key].status == 'opened':
                    lista_pomocnicza.append(talia.karty[key])
            if lista_pomocnicza[0].name == lista_pomocnicza[1].name:
                for key, value in talia.karty.copy().items():
                    if value == lista_pomocnicza[0] or value == lista_pomocnicza[1]:
                        talia.karty[key].status = 'over'
                        odkryte = 0
                        if wygrana() == True:
                            render_template("wygrana.html")
            else:
                pass
    return render_template('memory.html', talia = talia, odkryte = odkryte, wybor = wybor, lista_audio = lista_audio)"""

@app.route("/<ajdi>", methods = ['GET','POST']) 
def otworz(ajdi):
    global talia
    global odkryte
    global temp 
    for key in talia.karty:
        if key == int(ajdi):
            talia.karty[key].status = 'opened'

            odkryte +=1 
        if odkryte == 2:
            lista_pomocnicza = list()
            for key in talia.karty:
                if talia.karty[key].status == 'opened':
                    lista_pomocnicza.append(talia.karty[key])
            if lista_pomocnicza[0].name == lista_pomocnicza[1].name:
                for key, value in talia.karty.copy().items():
                    if value == lista_pomocnicza[0] or value == lista_pomocnicza[1]:
                        talia.karty[key].status = 'over'
                        temp+=1
                        odkryte = 0
                        
            else:
                pass
    return render_template('memory.html', talia = talia, odkryte = odkryte, temp = temp)

@app.route("/schowaj", methods = ['GET','POST'])
def schowaj():
    global talia
    global odkryte
    for key in talia.karty:
        if talia.karty[key].status == 'opened':
            talia.karty[key].status = 'closed'
    odkryte = 0
    return render_template('memory.html', talia = talia, odkryte = odkryte) 

@app.route("/newgame")
def nowa_gra():
    global talia
    global temp
    global odkryte
    talia = Talia()
    odkryte = 0
    temp = 0
    for key in talia.karty.keys():
        talia.karty[key].status = 'closed'
    return render_template('memory.html', talia = talia, odkryte = odkryte, temp = temp)    

########################################################################################################################################################################################################################        

""""Samotna wyspa"""

przedmioty = ['kompas', 'noz', 'ksiazka', 'zapalki', 'topor', 'lina', 'namiot', 'aparat', 'mieso', 'latarka', 'woda', 'koc', 'radio', 'gitara', 'lupa', 'okulary_sloneczne', 'pies', 'papier_toaletowy' ]
zadania = [
            'Jest już ciemno i musisz nocować w lesie.',
            'Od samego rana jesteś głodny. Nagle zauważasz na drzewie wiązkę bananów. Niestety, trzymają się za mocno na drzewie.',
            'Na wyspie panuje straszny upał.',
            'Zgubiłeś się w tropicznym lesie.',
            'Wybierasz się na wycieczkę do jaskini.',
            'Zobaczyłeś ładnego motyla.',
            'Chcesz wybudować most przez rzekę.',
            'Czujesz się smutno i samotnie na wyspie.',
            'Potrzebujesz rozpalić ognisko.',
            'Zraniłeś się i potrzebujesz przewiązać ranę.',
            'Zgłodniałeś, a w pobliżu nie ma żadnych owoców.',
            'Zgubiłeś koszyk ze swoimi rzeczami w lesie.',
            'Udało Ci się, znalazłeś statek, w całkiem dobrym stanie. Musisz tylko przymocować żagle.'

    
           ]
zadania_EN = [
                'It is getting dark and you have to sleep in the forest.',
                'You are hungry the whole morning. Suddenly, you notice some bananas on the tree. Unfortunately, they hold too tight.',
                'It is very hot on the island today.',
                'You got lost in the tropical forest.',
                'You are going on adventure to the cave.',
                'You saw a beautiful butterfly.',
                'You want to built a bridge across the river.',
                'You feel sad and lonely on the island.',
                'You need to lit a fire.',
                'You are hurt and you need to tie up the wound.',
                'You are hungry, and there are no fruits anywhere.',
                'You lost a basket with your belongins in the forest.',
                'You made it and find a ship in a good state. Only thing you need to do is to fasten the sails.'
    ]
numer_gry = 1
licznik_rund = 1
game = {'id': numer_gry, 'moje_przedmioty': [], 'moje_wyzwanie': str(), 'runda': licznik_rund, 'wygrana': 'brak'}

@app.route("/wyspa",  methods=['GET', 'POST'])
def gra_samotna_wyspa():
    global numer_gry
    global przedmioty
    global game
    global zadania
    game = {'id': numer_gry, 'moje_przedmioty': [], 'moje_wyzwanie': str(), 'runda': licznik_rund, 'wygrana': 'brak'}
    numer_gry +=1
    some_bool = bool(game['moje_przedmioty'])
    if request.method == 'POST':
        form = request.form.getlist('moje_przedmioty')
        for item in form:
            game['moje_przedmioty'].append(item)
        if len(game['moje_przedmioty']) >=1:
               some_bool = True
   
   
    return render_template('island.html', przedmioty = przedmioty, game = game, some_bool = some_bool)

@app.route('/wylosuj')
def wylosuj_wyzwanie():
    
    global zadania
    global game
    global przedmioty
    global zadania_EN
    zadanie = random.choice(zadania)
    game['moje_wyzwanie'] = zadanie
    return redirect("wyzwanie")

@app.route('/wyzwanie', methods=['GET', 'POST'])
def wyzwanie():
    global zadania
    global game
    global przedmioty
    indeks = zadania.index(game['moje_wyzwanie'])
    if request.method == 'POST':
        wybrane = request.form['wybrane']
        if game['moje_wyzwanie'] == zadania[0]:
            
            if wybrane == 'namiot' or wybrane == 'latarka':
               game['wygrana'] = True
            else:
                game['wygrana'] = False
        elif game['moje_wyzwanie'] == zadania[1]:
            if wybrane == 'noz' or wybrane == 'lina' or wybrane == 'topor':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False
        elif game['moje_wyzwanie'] == zadania[2]:
            if wybrane == 'woda' or wybrane == 'okulary_sloneczne':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False
        elif game['moje_wyzwanie'] == zadania[3]:
            if wybrane == 'kompas' or wybrane == 'pies':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False 
                 game['wygrana'] = False
        elif game['moje_wyzwanie'] == zadania[4]:
            if wybrane == 'zapalki' or wybrane == 'latarka':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False 
        elif game['moje_wyzwanie'] == zadania[5]:
            if wybrane == 'aparat' or wybrane == 'lupa':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False 
        elif game['moje_wyzwanie'] == zadania[6]:
            if wybrane == 'noz' or wybrane == 'topor':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False
        elif game['moje_wyzwanie'] == zadania[7]:
            if wybrane == 'ksiazka' or wybrane == 'gitara' or wybrane == 'pies':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False  
        elif game['moje_wyzwanie'] == zadania[8]:
            if wybrane == 'zapalki' or wybrane == 'lupa':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False  
        elif game['moje_wyzwanie'] == zadania[9]:
            if wybrane == 'papier_toaletowy' or wybrane == 'koc':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False  
        elif game['moje_wyzwanie'] == zadania[10]:
            if wybrane == 'mieso':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False  
        elif game['moje_wyzwanie'] == zadania[11]:
            if wybrane == 'pies' or wybrane == 'kompas':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False 
        elif game['moje_wyzwanie'] == zadania[12]:
            if wybrane == 'lina':
                game['wygrana'] = True
            else:
                 game['wygrana'] = False                      
        return render_template("challenge.html", game = game, wybrane = wybrane, indeks = indeks)
    return render_template("challenge.html", game = game, indeks=indeks, zadania_EN = zadania_EN)

@app.route("/dobierz", methods=['GET', 'POST']) 
def dobierz():
    global game
    global indeks
    if request.method == 'POST':
        dobrany = request.form['przedmioty']
        game['moje_przedmioty'].append(dobrany)           
        if game['runda'] < 5:
            game['runda']+=1
            game['wygrana'] = 'brak'
            wylosuj_wyzwanie()
        else:
            return render_template('wygrana.html', game = game)
        return  redirect("wyzwanie")
    
    return render_template('dobierz.html', przedmioty = przedmioty, game = game)

@app.route('/next')  
def nastepne_wyzwanie():
     global game

     if game['runda'] < 5 and len(game['moje_przedmioty'])!= 0:
            game['runda']+=1
            game['wygrana'] = 'brak'
            game['moje_przedmioty'].remove(random.choice(game['moje_przedmioty']))
            wylosuj_wyzwanie()            
            return redirect("wyzwanie")
     elif len(game['moje_przedmioty']) == 0:
          game['wygrana'] == False
          return render_template('wygrana.html', game = game)
     else:
            return render_template('wygrana.html', game = game)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111, debug = True)
