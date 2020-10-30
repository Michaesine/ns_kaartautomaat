def opvragen_stationslijst():
    # Deze functie maakt connectie met met SGA, Een tabellen systeem van NS Reisinformatie en haalt hier de huidige
    # actieve stations op.

    import http.client
    import urllib.parse
    import urllib.error
    import json

    'Import nodige modules'

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'd631dceaf58f49d78191f677e84e189e',
    }
    'Plaatst primairy key in de header'

    params = urllib.parse.urlencode({
    })
    'Geeft de nodige parameter mee aan de url'
    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", "/reisinformatie-api/api/v2/stations?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except:
        print("Er is iets foutgegaan")
    'Opent de connectie en doet het request om de stationslijst op te halen. Deze krijgen we terug als binairy'

    with open("NSStationsLijst.json", "w", encoding="utf-8") as json_file:
        json.dump(data.decode(), json_file, indent=4)
        json_file.close()
    'Dumpt de data  in een json file'

    with open("NSStationsLijst.json", "r") as json_fileData:
        stationsSTR = (json.load(json_fileData))
        stations = json.loads(stationsSTR)
        payload = stations.get("payload")

        json_fileData.close()
    'Haalt de data weer uit de json file en returnt de payload als dict'
    return payload


def opvragen_departures(stationsverkorting):
    import http.client
    import urllib.parse
    import json

    key = {'Ocp-Apim-Subscription-Key': 'd631dceaf58f49d78191f677e84e189e'}

    params = urllib.parse.urlencode({
        'maxJourneys': 25,
        'station': stationsverkorting
    })

    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", "/reisinformatie-api/api/v2/departures?" + params, headers=key)
        response = conn.getresponse()
        responsetext = response.read()
        data = json.loads(responsetext)
        'Maakt connectie met NS om de volgende 25 departures op te halen van het station wat is ingevoerd.'
        conn.close()
    except Exception as e:
        print("Fout: {} {}".format(e.errno, e.strerror))

    payload = data['payload']
    departurelst = payload['departures']
    return departurelst


def opvragen_vertrek_informatie():
    # Pak de invoer van de textbox
    invoer = textbox.get()
    # Als de invoer in de textbox niet in deze dict staat, krijg een error message (showinfo)
    if invoer not in stationdict:
        showinfo(title='Foutmelding', message="Dit station bestaat niet.")
    else:
        # Als de invoer wel bestaat in de dict
        # Verander de invoer (stationsnaam) naar de afkorting van desbetreffend station
        stationafk = stationdict[invoer]
        # Roep de functie aan die de departures returned
        deps = opvragen_departures(stationafk)
        # Lijst van departures begint op 0 en word incremented met 1 elke loop
        num = 0
        # Plek van de values, word ook incremented met 30 px elke loop
        y = 80
        # Defineer de headers voor de lijst:
        headers = ('{:10} | {:25} | {:10} | {:20} |'.format('Vertrektijd', 'Eind Station', 'Spoor', 'Materieel'))
        # De cover die de value van de laatste query bedekt
        coverlabel = Label(bg='#003082')
        coverlabel.place(x=390, height=900, y=10, width=1010)
        # De naam aan de bovenkant van de GUI, voor duidelijkheid over welk station het gaat
        naamlabel = Label(bg='#FFC917', text=f"Actuele vertrekken vanaf station {invoer}",
                          font=("Lucida Console", 20, "underline", "bold"))
        naamlabel['font'] = myFont
        # De headers van elke value
        headerlabel = Label(bg='#FFC917', text=headers, font=("Lucida Console", 20, "underline", "bold"))
        headerlabel['font'] = myFont
        # Plaats de labels op de window
        naamlabel.place(x=400, y=50)
        headerlabel.place(x=400, y=80)
        # De loop die alle json values aan variabels koppelt
        for i in deps:
            direction = deps[num]["direction"]
            actualdatetime = deps[num]["actualDateTime"]
            actualdatetime = actualdatetime.split("T")[1]
            actualdatetime = actualdatetime.split("+")[0]
            plannedtrack = deps[num]["plannedTrack"]
            shortcategoryname = deps[num]["product"]["shortCategoryName"]
            cancelled = deps[num]["cancelled"]
            # In plaats van 0 en 1, worden nee en ja geprint
            if cancelled == 0:
                cancelled = "Nee"
            elif cancelled == 1:
                cancelled = "Ja"
            # Increment num met 1
            num += 1
            # Defineer de values aan de headers
            values = (
                ' {:10} | {:25} | {:10} | {:20} |'.format(actualdatetime, direction, plannedtrack, shortcategoryname
                                                          ))
            # Increment de y met 30 elke loop
            y += 30
            # Valuelabel die de values plaatst op de GUI
            valuelabel = Label(text=values, bg='#FFC917')
            valuelabel['font'] = myFont
            valuelabel.place(x=400, y=y)
    return deps


# Import alle modules die gebruikt worden in de code, en print een foutmelding als dat niet lukt
try:
    import datetime
    from tkinter import *
    import json
    from tkinter.messagebox import showinfo
    import tkinter.font as font
except:
    print("Kan een of meerdere modules niet importeren.")
# Open de master window
master = Tk()
# De font die gebruikt word
myFont = font.Font(family='Lucida Console')
# Titel van de master window
master.title("NS-Kaartautomaat")
# Grootte van de master window in px
master.geometry('1200x900')
# Lock windows size
master.resizable(width=False, height=False, )
# Gele achtergrond
master.configure(bg='#fcc63f')
# Blauw label aan de onderkant
ll = Label(master, bg="#003082", height=3, text='')
ll.pack(fill='x', side=BOTTOM)
# Blauw label aan de bovenkant
lU = Label(master, bg="#003082", height=3, text='')
lU.pack(fill='x', side=TOP)
# Blauw label aan de linker zijkant
lS = Label(master, bg="#003082", width=1, height=1400, text='')
lS.pack(fill='x', side=LEFT)
# Blauw label aan de rechter zijkant
RS = Label(master, bg="#003082", width=1, height=1400, text='')
RS.pack(fill='x', side=RIGHT)
# Blauw label als scheiding
SS = Label(master, bg="#003082", width=1, height=1400, text='')
SS.place(x=400)

# Voor elke value in de API call uit opvragen_stationslijst(), stop de lang (Meest complete stationsnaam) en de code
# (afkorting) in een dict

stationdict = {}
for i in opvragen_stationslijst():
    stationdict[i["namen"]["lang"]] = i["code"]
opvragen_stationslijst()

# Plaats het NS logo
nsLogoCanvas = Canvas(master, bd=0, highlightthickness=0, bg='#FFC917', width=370, height=143)
nsLogoCanvas.place(x=14, y=60)
nsLogoImg = PhotoImage(file='./ns.png')
nsLogoCanvas.create_image(0, 0, anchor='nw', image=nsLogoImg)

# Textbox & Button ander station opvragen
textbox = Entry(justify=CENTER)
textbox.insert(0, 'Utrecht Centraal', )
textbox.place(x=125, y=750, width=150, )
button = Button(master, text="Haal informatie op", command=opvragen_vertrek_informatie)
button.place(x=125, y=775, width=150)

# Datum van vandaag, word gebruikt in de GUI later
timeAndDate = datetime.datetime.now()
date = timeAndDate.strftime("%d-%m-%Y ")
time = timeAndDate.strftime("%H:%M")

# Post stationsnaam, datum, en tijd
stationsNaamLabel = Label(master, bg='#FFC917', fg='#003082', font=('Helvetic', 16, 'bold', 'italic'),
                          text='Welkom op station Utrecht Centraal')
stationsNaamLabel.place(x=20, y=230)
datumLabel = Label(master, bg='#FFC917', fg='#003082', font=('Helvetic', 16, 'bold', 'italic'), text=date)
tijdLabel = Label(master, bg='#FFC917', fg='#003082', font=('Lucida Console', 50, 'bold'), text=time)
tijdLabel.place(x=100, y=300)

# Loop van de master window
master.mainloop()
