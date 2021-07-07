import psycopg2
import csv
import json
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

### Setup database
with open('credentials.json', 'r') as json_file:
    credentials = json.load(json_file)

# connect with database
logging.info("Connecting with DB")
conn = psycopg2.connect(host=credentials['host'], port=credentials['port'], dbname=credentials['dbname'], user=credentials['user'], password=credentials['password'])
cur = conn.cursor()
# table = cur.execute("SELECT * FROM gacetas LIMIT 10;")
# print(table)
logging.info("Database Connected")
"""
logging.info('Starting to ingest gacetas table')
with open('gacetas_clean.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader) # skip header row
    for i, row in enumerate(reader):
        logging.info("Ingesting row: "+str(i))
        cur.execute(
            "INSERT INTO gacetas VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (str(i), row[0], row[1], row[2], row[3], row[4], row[5])
        )
"""
logging.info('Ingest finished')
conn.commit()
