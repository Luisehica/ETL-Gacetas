from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import datetime
import time
import csv
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

options = Options
options.headless = True
DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('http://svrpubindc.imprenta.gov.co/senado/')

data = [['numero_gaceta', 'entidad', 'fecha_publicacion', 'pagina']]
logging.info("Starting scrapping gaceta")

j = 2
fecha_publicacion = '29/06/2021'

while True:
    if j>1:
        for i in range(10):
            # Extract info
            numero = driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/form/fieldset/div/div/div[2]/table/tbody/tr['+str(i+1)+']/td[1]/label').text
            entidad = driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/form/fieldset/div/div/div[2]/table/tbody/tr['+str(i+1)+']/td[2]/label').text
            fecha_publicacion = driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/form/fieldset/div/div/div[2]/table/tbody/tr['+str(i+1)+']/td[3]/label').text
            fecha_publicacion = datetime.strptime(fecha_publicacion, '%d/%m/%Y').date()
            
            pagina = j-1
            row = [numero, entidad, fecha_publicacion, pagina]

            logging.info(row)
            data.append(row)
            
            #Download file
            #driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/form/fieldset/div/div/div[2]/table/tbody/tr['+str(i+1)+']/td[5]/button[1]').click()

    #next page
    time.sleep(1)
    logging.info("next page: "+str(j))
    driver.find_element_by_xpath('/html/body/div[2]/div/table/tbody/tr[4]/td/form/fieldset/div/div/div[3]/span[5]').click()
    j += 1
    time.sleep(1)

    # Stop criteria
    ultima_fecha = fecha_publicacion
    fecha_parada = datetime.strptime('27/01/2021', '%d/%m/%Y').date()
    stop_criteria = ultima_fecha < fecha_parada
    if stop_criteria:
        break



with open('gacetas.csv', 'w', encoding='utf-8') as csv_file:
    rowwriter = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    for row in data:
        rowwriter.writerow(row)


logging.info("Scrapped finished")
driver.close()