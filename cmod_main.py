from cmod_web import ChromeDriverMan
from cmod_data import DataManager
import logging
import os
import dotenv

logging.basicConfig(filename='warning.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

'''def take_screenshot(driver, picname):
    try:
        driver.save_screenshot(picname)
        print("Screenshot saved as:", picname)
    except Exception as e:
        print("Error occurred while taking screenshot:", e)'''

data_man = DataManager()
date1, date2, ag, cc, task_path, list_of_subdir = data_man.get_data_one(0)

#download_dir = list_of_subdir[1].replace("\\\\", "\\")
#downloa_dir = r'{}'.format(download_dir)
#downloa_dir = 'r"' + download_dir + '"'
#download_dir = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS BAIXA\TASK0467217\TASK0467217-51612"
download_dir = list_of_subdir[0]


ch_driver = ChromeDriverMan(download_dir)

driver = ch_driver.get_driver()
ch_driver.get_page()
ch_driver.login()
task_path, list_of_dir = ch_driver.fill_information_cmod(0)

for ieacht in list_of_dir:
    if ieacht == '\\\\192.168.24.17\\Carga\\Bradesco\\CPI\\LANBACEM-TI\\DOCUMENTOS FRANCESINHA\\TASK0584550\\Controle':
        
        ch_driver.rename_n_save(ieacht)
        
    else:
        pass

ch_driver.get_item_list(list_of_dir[0])
ch_driver.add_card()



    