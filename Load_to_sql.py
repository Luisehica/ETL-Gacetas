import psycopg2
import csv
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# connect with database
logging.info("Connecting with DB")
conn = psycopg2.connect("host=database-1.cj5pk51sbc9a.us-west-1.rds.amazonaws.com port=5432 dbname=Gacetas user=postgres password=inspiraCO2022")
cur = conn.cursor()

logging.info("Database Connected")

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
logging.info('Ingest finished')
conn.commit()
