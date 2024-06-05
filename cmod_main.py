from cmod_web import ChromeDriverMan
from cmod_data import DataManager
import logging
import os
import dotenv
import time

logging.basicConfig(filename='warning.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

'''def take_screenshot(driver, picname):
    try:
        driver.save_screenshot(picname)
        print("Screenshot saved as:", picname)
    except Exception as e:
        print("Error occurred while taking screenshot:", e)'''

data_man = DataManager()

while True:
    
    if not data_man.get_data_one(0) == None:
        date1, date2, ag, cc, task_path, list_of_subdir = data_man.get_data_one(0)

        for i in range(len(list_of_subdir)):
            
            try:
                download_dir = list_of_subdir[i]

                ch_driver = ChromeDriverMan(download_dir)

                driver = ch_driver.get_driver()
                ch_driver.get_page()
                ch_driver.login()
                task_path, list_of_dir = ch_driver.fill_information_cmod(i)

                for ieacht in list_of_dir:
                    if ieacht == '\\\\192.168.24.17\\Carga\\Bradesco\\CPI\\LANBACEM-TI\\DOCUMENTOS FRANCESINHA\\TASK0584550\\Controle':
                        ch_driver.rename_n_save(ieacht)            
                    else:
                        print("O caminho para o diretorio de controle pode estar corrompido")
                        logging.warning("O caminho para o diretorio de controle pode estar corrompido")
                        pass
                    
                #ch_driver.get_item_list(list_of_dir[0])
                ch_driver.add_card()
            except:
                print("Há alguma interferência, demora de carregamento ou novo elemento no processo, verificar! ")
                logging.warning("Há alguma interferência, demora de carregamento ou novo elemento no processo, verificar! ")
                pass
        print("hello, its'a me, Mario Karte! Acabou um loop de for")
    else:
        time.sleep(15)
        print("Não foi encontrado arquivo excel para ser processado por robô RPA Lanbacen - Francesinha do Bradesco CMOD")
        logging.info("Não foi encontrado arquivo excel para ser processado por robô RPA Lanbacen - Francinha do Bradesco CMOD, fazendo varredura do diretório 'DOCUMENTOS FRANCESINHA'...")

    