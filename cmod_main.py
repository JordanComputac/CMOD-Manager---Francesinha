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
        date1, date2, ag, cc, task_path, list_of_subdir_original, list_of_subdir = data_man.get_data_one(0)
        
        for i in range(len(list_of_subdir_original)):
            
            for directory in list_of_subdir:
                if directory.endswith("Controle"):
                    choosen = directory
            
            
            try:
                #download_dir = list_of_subdir[i]
                download_dir = choosen                
                
                ch_driver = ChromeDriverMan(download_dir)

                driver = ch_driver.get_driver()
                ch_driver.get_page()
                ch_driver.login()
                task_path, list_of_dir = ch_driver.fill_information_cmod(i)
                
                if task_path == False:
                    print("Algo errado nao está certo no preenchimento das informacoes no acesso ao portal CMOD")
                    break
                
                jump_qntty = ch_driver.rename_n_save(download_dir)
                    
                #ch_driver.get_item_list(list_of_dir[0])
                ch_driver.add_card(jump_qntty)
            except:
                print("Há alguma interferência, demora de carregamento ou novo elemento no processo, verificar! ")
                logging.warning("Há alguma interferência, demora de carregamento ou novo elemento no processo, verificar! ")
                pass

        if task_path == False:
            print("erro no preenchimento de busca por 'Francesinha - sem nome'")
            break
        print("hello, its'a me, Mario Karte! Acabou um loop de for")

    else:
        time.sleep(15)
        print("Não foi encontrado arquivo excel para ser processado por robô RPA Lanbacen - Francesinha do Bradesco CMOD")
        logging.info("Não foi encontrado arquivo excel para ser processado por robô RPA Lanbacen - Francinha do Bradesco CMOD, fazendo varredura do diretório 'DOCUMENTOS FRANCESINHA'...")

    