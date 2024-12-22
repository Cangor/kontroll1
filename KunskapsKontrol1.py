import pandas as panda
import sqlite3
import logging

logger = logging.getLogger()

#Här fixar vi configen till vår logger.
logging.basicConfig(
    filename='test_log.log',
    format='[%(asctime)s][%(levelname)s] %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger.warning("Warning message")
logger.debug("Debug message")
logger.info("Info message")

#Här läser vi av datan i en CSV-fil
df = panda.read_csv('mydata.csv')

#Här sätter vi ihop förnamn och efternamn till en ny kolumn.
df['full_name'] = df.name + ' ' + df.lastname
df.full_name.head()

print(df)

#Nu skapar vi en SQLite databas-fil som vi ska skriva data till
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

#Här skapas databasen filen om den inte redan finns, viktigt att alla variablar är desamma som i CSV-filen
cursor.execute('''
CREATE TABLE IF NOT EXISTS data_tabell (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lastname TEXT,
    number INTEGER,
    description TEXT,
    datum DATE,
    full_name TEXT
)
''')

#Nu går vi igenom varje rad för att kopiera över
for i, row in df.iterrows():
    try:
        #Här kollar vi om det redan finns data med samma id i vår databas
        cursor.execute('''
        SELECT 1 FROM data_tabell WHERE id = ?
        ''', (row['id'],))
        result = cursor.fetchone() 

        #Om det redan finns data med samma id så går vi in i result, annars skrivs datan in.
        if result:
            logging.info(f'Finns redan data med {row['id']} i databasen.')
        else:
            cursor.execute('''
            INSERT INTO data_tabell (id, name, lastname, number, description, datum, full_name)
            VALUES (?,?,?,?,?,?, ?)
            ''', (row['id'],row['name'],row['lastname'],row['number'],row['description'],row['datum'],row['full_name']))
            
            logging.info(f'Id {row['id']} har lagts till.')

    except Exception as e:
        logging.error(f'Någonting gick fel med att lägga till id {row['id']}')

#Här lägger vi till datan i databasen.
connection.commit()
logging.info('Klar med skrivning till databasen.')

#Här använder vi SELECT för att välja allt i data tabellen som vi sedan skriver ut.
results = connection.execute("SELECT * FROM data_tabell")
for row in results:
    print(row)

connection.close()

