from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import PyPDF2
from bs4 import BeautifulSoup
import requests
from cmod_data import DataManager
import time
import logging
import os
import dotenv
import pandas as pd
import traceback
import re
import math


logging.basicConfig(filename='warning.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


class ChromeDriverMan:

    def __init__(self, download_dir):
        
        self.data_man = DataManager()

        current_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(current_dir, '.env')          
        load_dotenv(dotenv_path)

        
        self.user = os.getenv("USER")
        self.psswd = os.getenv("PSSWD")
        self.url = os.getenv("URL_CMOD")
        self.download_dir = os.getenv("DOWNLOAD_DIR")



        self.chrome_options = Options()
        self.data_man = DataManager()
        self.driver = webdriver.ChromeOptions()

        self.download_dir = download_dir
                

        prefs = {
                    "download.default_directory": self.download_dir,
                    "download.prompt_for_download": False, 
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True
                }
        
        self.chrome_options.add_experimental_option("prefs", prefs)

        # Initialize Chrome WebDriver with the configured options
        

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(4)

    def get_driver(self):
        return self.driver
    

    def take_screenshot(self, picname):
        

        try:
            self.driver.save_screenshot(picname)
            print("Screenshot saved as:", picname)
        except Exception as e:
            print("Error occurred while taking screenshot:", e)

    def get_page(self):
        driver = self.get_driver()
        try:            
            driver.get(self.url)

        except:
            print("Algo de errado no login, verificar se VPN está conectada em rede permitida de acesso")
            logging.warning("Algo de errado no login, verificar se VPN está conectada em rede permitida de acesso")
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")
            

    def login(self):
        driver = self.get_driver()

        try:                
            user_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name = 'ecm_widget_layout_NavigatorMainLayout_0_LoginPane_username']")))
            user_name.clear()
            user_name.send_keys(self.user)
        except:
            print("Campo 'Nome do usuário' não foi preenchido corretamente")
            logging.warning("Campo 'Nome do usuário' não foi preenchido corretamente")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")

        try:
            
            user_psswd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name = 'ecm_widget_layout_NavigatorMainLayout_0_LoginPane_password']")))
            user_psswd.clear()
            user_psswd.send_keys(self.psswd)
        except:
            print("Campo 'Senha' não preenchido corretamente")
            logging.warning("Campo 'Senha' não preenchido corretamente")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")
        try:
            btn_login = driver.find_element(By.XPATH, "//span[@widgetid = 'ecm_widget_layout_NavigatorMainLayout_0_LoginPane_LoginButton']")
            btn_login.click()
        except:
            print("Botão de login não pode ser clicado")
            logging.warning("Botão de login não pode ser clicado")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")
    

    def fill_information_cmod(self, row):
        driver = self.get_driver()
        
        
        time.sleep(4)
        #the number 0 passed to func represents the first line of the excel file (first task)
        date1, date2, ag, cc, task_path, list_of_subdir = self.data_man.get_data_one(row)
        
        try:
            list_block = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-dojo-attach-point='featureList']")))
            list_block.click()

            magnifying_glass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@id='dijit_MenuItem_5']")))
            magnifying_glass.click()

            search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ecm_widget_search_SearchSelector_0_filterTextBox']")))
            search_field.click()
            search_field.send_keys('79166 - Francesinha - Sem Nosso Número')
            

        except:
            print("Nao foram encontrados os elementos para pesquisa do parametro '79166 - Francesinha'")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen - Francesinha\CMOD-Manager---Francesinha\error_printo\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")
            return logging.warning("Nao foram encontrados os elementos para pesquisa do parametro '79166'")

        try:
                        
            time.sleep(3)
            open_dropdown_recent = self.driver.find_elements(By.XPATH, "(//*[@class='dijitInline dijitTreeExpando dijitTreeExpandoClosed'])")
            try:
                open_dropdown_recent = open_dropdown_recent[0]
                open_dropdown_recent.click()
            except:
                print("Problema ao buscar elemento de clique 79166 - Francecinha sem numero")
                logging.error("Problema ao buscar elemento de clique 79166 - Francecinha sem numero")
            
            open_dropdown_all = self.driver.find_elements(By.XPATH, "(//*[@class='dijitInline dijitTreeExpando dijitTreeExpandoClosed'])")
            try:
                open_dropdown_all = open_dropdown_all[1]
                open_dropdown_all.click()
            except:
                print("Problema ao buscar elemento de clique 79166 - Francecinha sem numero")
                logging.error("Problema ao buscar elemento de clique 79166 - Francecinha sem numero")
            
            driver.execute_script("document.evaluate(\"//*[contains(text(), '79166')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")

            '''select_cat = self.driver.find_elements(By.XPATH, "(//*[contains(text(), '79166')])")
            select_cat = select_cat[0]
            select_cat.click()

            sellect_par = select_cat.find_element(By.XPATH, '..')
            sellect_par.click()'''

        except:
            print("A procura do parametro '79166 - Francesinha' sofreu uma interrupção, verificar existência deste componente na página")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.warning("Tirando print e salvando ultima interacao...")
            return logging.warning("A procura do parametro '79166 - Francesinha' sofreu uma interrupção, verificar existência deste componente na página")
        

        try:
            
            date1_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ecm_widget_search_SearchForm_0_ecm.widget.SearchCriterian_0']")))
            date1_field.clear()
            date1_field.send_keys(date1)

            date2_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='ecm_widget_search_SearchForm_0_ecm.widget.SearchCriterian_0_2']")))
            date2_field.clear()
            date2_field.send_keys(date2)

            #str_ag = '00'+str(ag)
            ag_field = self.driver.find_elements(By.XPATH, "//input[@title='Agência']")
            select_ag_field = ag_field[0]
            select_ag_field.send_keys(ag)

            
            str_ag = '00'+str(ag)
            new_cc = cc[:-2]
            new_cc = str(new_cc).zfill(7)

            
            ag_field = self.driver.find_elements(By.XPATH, "//input[@title='Conta']" )
            select_ag_field = ag_field[0]
            select_ag_field.send_keys(new_cc)
            
            
            btn_search = driver.find_element(By.XPATH, "//span[@widgetid='dijit_form_Button_2']")
            btn_search.click()
            time.sleep(3)

                        
        except:
            print("Erro no preenchimento das informacoes do forumulario para busca de arquivos 'Francesinha - 79166' ")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.error("Tirando print e salvando ultima interacao...")
            logging.error("Erro no preenchimento das informacoes do forumulario para busca de arquivos 'Francesinha - 79166' ")

        
        return task_path, list_of_subdir
    
    def list_foward(self, numbar):

        try:
            
            prox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Próxima página')]")))            
            prox_par = prox.find_element(By.XPATH, " ..")
            prox_par.click()
            time.sleep(3)
            
            print(f"Mudando para proxima tabela de lista..., rodada de busca de numero: {numbar}")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.info("Tirando print e salvando ultima interacao...")
            return logging.info(f"Mudando para proxima tabela de lista..., rodada de busca de numero: {numbar}")
            
        except:

            print(f"Nao e possivel avancar na lista de itens disponiveis, rodada de busca de numero: {numbar}")
            logging.info(f"Nao e possivel avancar na lista de itens disponiveis, rodada de busca de numero: {numbar}")
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.info("Tirando print e salvando ultima interacao...")
            return False

    def move_foward(self):

        try:        
            original_window_handle = self.driver.current_window_handle
            all_window_handles = self.driver.window_handles
            new_window_handle = [handle for handle in all_window_handles if handle != original_window_handle][0]
            self.driver.switch_to.window(new_window_handle)
            self.driver.switch_to.window(original_window_handle)
            arrow_foward = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@title='Visualizar o próximo documento na lista']")))
            arrow_foward.click()
            time.sleep(3)

            return None
        except:
            print("Algo esta errado ao clicar no proximo item da lista processada para download")
            logging.warning("Algo esta errado ao clicar no proximo item da lista processada para download")

            return False

        
    def download_files(self, wanted_element):    

        
                
        
        time.sleep(2)   
        
        iframe = self.driver.find_element(By.XPATH, "//iframe[@title='IframeDocViewer']")
        self.driver.switch_to.frame(iframe)
        #copy_download = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//button[@class = 'toolbarButtons ui-button ui-corner-all ui-widget ui-button-icon-only']")))
        copy_download = self.driver.find_elements(By.XPATH, "//div[@id='toolbar']//child::button")
        
       
        if len(copy_download) != 19:
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.error("Tirando print e salvando ultima interacao...")
            logging.error("A quantidade de botoes mudou, revisar a quantidade de botoes e identificar o elemento responsavel pelo download dos itens")
            return print("A quantidade de botoes mudou, revisar a quantidade de botoes e identificar o elemento responsavel pelo download dos itens")
        
        else:

            
            copy_download[14].click()
            time.sleep(3)
            btn_ok = self.driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
            btn_ok.click()
        

        
        '''status = self.data_man.verify_item_existence(self.download_dir, 'controle', wanted_element)
        if status == True:
            print(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
            logging.warning(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
        else:
            self.data_man.update_row(self.download_dir, 'controle', wanted_element)
            print(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")
            logging.warning(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")'''

    def select_element(self, wanted_element):
        actions = ActionChains(self.driver)
        selected_item = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='gridxBody gridxBodyRowHoverEffect']//div/table//child::*[contains(text(), '{wanted_element}')]")))
        actions.double_click(selected_item).perform()


    def search_element(self, wanted_element):
        

        numbar = 0
        actions = ActionChains(self.driver) 
        #O loop abaixo é responsável pela procura de um elemento em específico
        while True:            
            time.sleep(2)
            try:                           
                
                #0982250000b003 
                selected_item = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='gridxBody gridxBodyRowHoverEffect']//div/table//child::*[contains(text(), '{wanted_element}')]")))
                actions.double_click(selected_item).perform()
                original_window_handle = self.driver.current_window_handle
                all_window_handles = self.driver.window_handles
                new_window_handle = [handle for handle in all_window_handles if handle != original_window_handle][0]
                self.driver.switch_to.window(new_window_handle)
                
                time.sleep(2)
                print(f"Item {wanted_element} encontrado com sucesso! '\U0001F609' ")
                break

                
            except:
                arrow_status = self.list_foward(numbar)
                if arrow_status == False:
                    return print(f"Item {wanted_element} não encontrado ")                    

                else:                                        
                    numbar = numbar+1
                    time.sleep(2)
        
        return print("Funcao 'search_element' rodada com sucesso! ")
        

    def organize_by_date(self):
        try:                
            time.sleep(5)  
            organize_files_box = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(text(), 'Data')]")))
            organized_file = organize_files_box[0]
            organized_file.click() 

            
            
        except:
            
            inpu = 'S'
            #inpu = input("A página está demorando mais do que o normal para carregar, deseja continuar esperando ou reiniciar o robô? ('S' para sim e 'N' para não)")
            if inpu == 'S':                
                
                while True:
                    try:
                        self.driver.find_element(By.XPATH, "//div[contains(text(), 'Pesquisando')]")
                        print("Aguardando o carregamento da pagina ...")
                        time.sleep(2)
                    except:
                        print("A pagina demorada finalmente carregou os itens! ;) ")
                        break

                organize_files_box = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(text(), 'Data')]")))
                organized_file = organize_files_box[0]
                organized_file.click() 
                print(" os itens por data na tentativa de numero 2 devido a demora de carregamento da pagina; é recomendado que se reinicie o robo. ")
                
                self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
                logging.error("Tirando print e salvando ultima interacao...")
                return logging.error("Houve um erro ao organizar os itens por data na tentativa 1 e o carregamento ocorreu na tentativa de numero 2 devido a demora de carregamento da pagina;")
            
            else:                
                print("Houve um erro ao organizar os itens por data devido a demora de carregamento da pagina; é recomendado que se reinicie o robo. ")
                
                self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
                logging.error("Tirando print e salvando ultima interacao...")
                return logging.error("Houve um erro ao organizar os itens por data devido a demora de carregamento da pagina; é recomendado reiniciar o robo.")
    
    def rename_it(self, file_path, date_emissao):
        
        
        formatted_date = date_emissao.replace('/', '.')
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, formatted_date+'.pdf')

        if os.path.exists(new_file_path):
            ino = 0
            while os.path.exists(new_file_path):
                ino = ino + 1
                print("valor de ino controle de quantidade de arquivos com mesma data de emissao: ", ino)
                new_file_path = os.path.join(directory, formatted_date+f' {ino}.pdf')
        try:
            os.rename(file_path, new_file_path)
            print(f"Um arquivo foi renomeado de {file_path} para {new_file_path}")
            return formatted_date
        
        except FileNotFoundError:
            print(f"Arquivo {file_path} nao encontrado no diretorio {directory}")
            logging.error(f"Arquivo {file_path} nao encontrado no diretorio {directory}")
        except Exception as e:
            print(f"Ocorreu um erro enquanto renomeava o arquivo {e}")
            logging.error(f"Ocorreu um erro enquanto renomeava o arquivo {e}")


    def find_element_position(self, lst, target):
        for i, element in enumerate(lst):
            if element == target:
                return i



    def loop_manager(self, wanted_elements):        
        
        input_string = wanted_elements[-1]
        
        try:
            match = re.search(r'\((\d+)\)', input_string)
            if match:
                result = match.group(1)
                print(result)
                print("A definicao do elemento a ser procurado na lista inicia no ULTIMO elemento da lista em arquivo diretorio raiz '.txt' ")
                logging.info("A definicao do elemento a ser procurado na lista inicia no ULTIMO elemento da lista em arquivo diretorio raiz '.txt' ")

                if len(wanted_elements) >= 200:                    
                    divs = len(wanted_elements)%200
                    for yui in range(math.floor(len(wanted_elements)/200)):
                        self.list_foward(99999999999)
                else:
                    divs = len(wanted_elements)                  


                wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
                wanted_element = wanted_elements[divs]
                wanted_element = wanted_element.get_attribute("textContent")
            
            
            else:
                print("O ultimo elemento da lista do diretorio raiz nao pode ser definido")
                return logging.error("O ultimo elemento da lista do diretorio raiz nao pode ser definido")
        except:
            
            wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
            wanted_element = wanted_elements[0]
            wanted_element = wanted_element.get_attribute("textContent")
            print("A definicao do elemento a ser procurado na lista inicia no primeiro elemento da lista em CMOD")
            logging.info("A definicao do elemento a ser procurado na lista inicia no primeiro elemento da lista em CMOD")
            divs = 0 
            #self.driver.switch_to.window(new_window_handle)
        
        
        

        self.search_element(wanted_element)
        
        original_window_handle = self.driver.current_window_handle
        all_window_handles = self.driver.window_handles
        new_window_handle = [handle for handle in all_window_handles if handle != original_window_handle][0]
        
        control = ''
        countng = 0
        while True:
                
                for uol in range(200):
                                        
                    uoll = divs+uol
                    self.driver.switch_to.window(new_window_handle)
                    wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
                    
                    wanted_element = wanted_elements[uoll]
                    wanted_element = wanted_element.get_attribute("textContent")
                    
                    #Formatar wanted_element
                    if wanted_element == None:  
                        wanted_element = wanted_elements[uoll]                     
                        wanted_element = wanted_element.text 
                        if wanted_element == '0000000000000' or wanted_element == '':
                            print ("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                            return logging.error("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                    
                    #wanted_element = wanted_element.text
                    
                    wanted_element = str(wanted_element).zfill(13)
                    time.sleep(2)
                   
                    #self.select_element(wanted_element)
                    
                    '''if control == 'search':
                        #self.driver.close()
                        self.driver.switch_to.window(new_window_handle)
                        self.search_element(wanted_element)
                        original_window_handle = self.driver.current_window_handle
                        all_window_handles = self.driver.window_handles
                        new_window_handle = [handle for handle in all_window_handles if handle != original_window_handle][0]
                        
                    '''
                    self.driver.switch_to.window(original_window_handle)
                    print(f"Mudanca de controle de pagina para a segunda janela com informacoes do item selecionado em andamento - item n° {countng}")
                    
                    status = self.data_man.verify_item_existence(self.download_dir, 'controle', int(wanted_element))
                                  
                    if status == True:
                        print(f"O elemento {wanted_element} existe na lista de controle dos itens processados e nao sera baixado")
                        logging.warning(f"O elemento {wanted_element} existe na lista de controle dos itens processados e nao sera baixado")
                    else:
                        
                        self.download_files(wanted_element)
                    
                    if uoll >= 199:
                         
                        #Antes de dar quit na janela verificar em qual página o robô está para quitar a "original"
                        
                        #self.driver.close()
                        self.driver.switch_to.window(new_window_handle)
                        try:
                            self.list_foward(99999999999)
                            control = 'search'
                        except:
                            print(f"Esta é a última rodada do loop na última lista de itens disponíveis, com {countng} elementos processados")
                            logging.info(f"Esta e a ultima rodada do loop na ultima lista de itens disponiveis, com {countng} elementos processados")
                            
                            #CONTROL AQUI DEVE SER = 'loop'
                            continue
                        
                        '''original_window_handle = self.driver.current_window_handle
                        #all_window_handles = self.driver.window_handles
                        #new_window_handle = [handle for handle in all_window_handles if handle != original_window_handle][0]
                        self.driver.switch_to.window(original_window_handle)
                        time.sleep(3)
                        wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
                        wanted_element = wanted_elements[0]      
                        wanted_element = wanted_element.get_attribute("TextContent")

                        if wanted_element == None:
                            wanted_element = wanted_elements[0]
                            wanted_element = wanted_element.text                             
                            if wanted_element == '0000000000000' or wanted_element == '':
                                print ("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                                return logging.error("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                        
                        wanted_element = str(wanted_element).zfill(13)
                        self.search_element(wanted_element)
                        status = self.data_man.verify_item_existence(self.download_dir, 'controle', wanted_element)
                        
                        if status == True:
                            print(f"O elemento {wanted_element} existe na lista de controle dos itens processados e nao sera baixado")
                            logging.warning(f"O elemento {wanted_element} existe na lista de controle dos itens processados e nao sera baixado")
                        else:
                            self.download_files(wanted_element)'''
                        
                        print(f"Processados 200 elementos - limite total da pagina -> Elemento {wanted_element}")
                        logging.info(f"Processados 200 elementos - limite total da pagina -> Elemento {wanted_element}")
                        self.move_foward()
                        break

                    else:
                        
                        seting = self.move_foward()  
                        if seting == False:
                            control = 'loop'
                            print("Existe um problema ao clicar no item seguinte funcao 'move_foward'")
                            logging.info(("Existe um problema ao clicar no item seguinte funcao 'move_foward'"))
                            break
                                                          
                        control = 'loop'
                        time.sleep(2)

                    countng = countng + 1
                    
                    
                    
                
                if control == 'loop':
                    print("Fim do processamento dos itens das listas CMOD")
                    logging.info(("Fim do processamento dos itens das listas CMOD"))
                    break

                else:
                    divs = 0                     
                    continue


    def get_item_list(self, itens_path):

        
        network_directory = itens_path        
        all_files = os.listdir(network_directory)
        name_file = itens_path+'\\'+'controle.xlsx'
        
        

        time.sleep(3)
        self.organize_by_date()
        
        
        #O trecho abaixo verifica a existencia do arquivo de controle em excel e cria um, caso não exista
        if os.path.isfile(name_file):
            values = self.data_man.get_item_list(itens_path, 'controle')
             
            print("O arquivo de controle ja existe")
            if values != None and values != '':
                try:
                    #Se o primeiro da lista for equivalente ao 'wanted_element' então a regra de download funcionará
                    wanted_element = values[0]
                    print(f"O arquivo de controle ja existe com {len(values)} elementos")
                except:
                    print("problema na definicao dos elementos internos do arquivo de controle")
                    logging.error("problema na definicao dos elementos internos do arquivo de controle")
                
            time.sleep(1)          

        else:
            
            self.data_man.create_file(itens_path, 'controle')
            print("Arquivo controle criado")
            time.sleep(5)
       
            print("Arquivo controle nao pode contar elementos/itens, arquivo 'controle' sera populado")
            logging.error("Arquivo controle nao pode contar elementos/itens, arquivo 'controle' sera populado")
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
           
            time.sleep(3)
            wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
            wanted_element = wanted_elements[0]
            #wanted_element = wanted_element.text
            wanted_element = wanted_element.get_attribute("TextContent")
            if wanted_element == None:
                wanted_element = wanted_elements[0]
                wanted_element = wanted_element.text 
                if wanted_element == '0000000000000' or wanted_element == '':
                    print ("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                    return logging.error("O processamento de texto do elemento está retornando vazio ou 0000000000000")
            
            wanted_element = str(wanted_element).zfill(13)
            #self.search_element(wanted_element)
            
            print("vindo do controle vazio")
            self.loop_manager(wanted_elements)            
                                                
        #O trecho abaixo procura por todos os arquivos '.lin' existentes no diretorio
        #O trecho abaixo e responsavel por baixar tudão e rodar até parar, depois, caso pare, vai rodar uma condicional para acionar ou nao a funcao que vai encapsular tudo abaixo
        
        try:        
            network_directory = itens_path        
            all_files = os.listdir(network_directory)
            
            lin_files = [file for file in all_files if file.endswith('.lin')]                
            txt_files = [file for file in all_files if file.endswith('.txt')] 
            tmp_files = [file for file in all_files if file.endswith('.tmp')]
                            
            #VERIFICACAO 1 - A quantidade de arquivos '.lin'+'.txt' encontrada deve ser igual a quantidade encontrada no arquivo controle
            #if len(values) == (len(lin_files)+ len(txt_files)):     
            #Fazer um loop deste abaixo para '.tmp_files'           
            if (len(lin_files)+ len(txt_files)+len(tmp_files)) > 0:       
                 
                for i in range(len(lin_files)):
                    
                    file_path = network_directory+'\\'+lin_files[i]
                    
                    new_path, n_numero = self.rename_it(file_path)
                    
                    
                    status = self.data_man.verify_item_existence(self.download_dir, 'controle', n_numero)
                    if status == True:
                        print(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
                        logging.warning(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
                    else:
                        self.data_man.update_row(self.download_dir, 'controle', n_numero)

                    print(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")
                    logging.warning(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")
                    print("A quantidade de arquivos lida é compatível com a quantidade encontrada no diretorio raiz")
                    time.sleep(1)
                
                for i in range(len(tmp_files)):
                    
                    file_path = network_directory+'\\'+tmp_files[i]
                    
                    new_path, n_numero = self.rename_it(file_path)
                    
                    
                    status = self.data_man.verify_item_existence(self.download_dir, 'controle', n_numero)
                    if status == True:
                        print(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
                        logging.warning(f"O elemento {wanted_element} existe na lista de controle dos itens processados")
                    else:
                        self.data_man.update_row(self.download_dir, 'controle', n_numero)

                    print(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")
                    logging.warning(f"O elemento {wanted_element} foi inserido na lista de controle dos itens processados")
                    print("A quantidade de arquivos lida é compatível com a quantidade encontrada no diretorio raiz")
                    time.sleep(1)

    
                wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")

                wanted_element = str(wanted_element).zfill(13)
                #self.search_element(wanted_element)   
                #self.move_foward()              
                #self.download_files(wanted_element)
                
                print("vindo do controle cheio")
                self.loop_manager(txt_files)
            else:
                wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-6']")
                wanted_element = wanted_elements[0]
                #wanted_element = wanted_element.text
                wanted_element = wanted_element.get_attribute("TextContent")
                if wanted_element == None:
                    wanted_element = wanted_elements[0]
                    wanted_element = wanted_element.text 
                    if wanted_element == '0000000000000' or wanted_element == '':
                        print ("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                        return logging.error("O processamento de texto do elemento está retornando vazio ou 0000000000000")
                
                wanted_element = str(wanted_element).zfill(13)
                #self.search_element(wanted_element)
                
                print("vindo do controle vazio")
                self.loop_manager(wanted_elements)

                self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
                logging.warning("Tirando print e salvando ultima interacao...")
                return logging.warning("Quantidade de arquivos e registros no diretorio raiz zerada, porem, arquivo controle existe tambem vazio, arquivos processados desde o inicio")
        
        except:
            
            self.take_screenshot(r'C:\Users\jordan.santos\Documents\CMOD Lanbacen\CMOD-Manager\error_print\error_screen_shot.png')
            logging.error("Tirando print e salvando ultima interacao...")
            return logging.error("Codigo interrompido na selecao e gerenciamento dos itens; possivel queda de conexao")


    def selecting_element(self, ene): 

        wanted_elements = self.driver.find_elements(By.XPATH, "//table[@class = 'gridxRowTable']//child::td[@aria-describedby='gridx_Grid_2-7']")
        wanted_element = wanted_elements[ene]

        return wanted_element
        
    
    def add_card(self):
        
        self.organize_by_date()
        
        for i in range(200):

            wanted_element = self.selecting_element(i)  
            self.driver.execute_script("arguments[0].scrollIntoView(true);", wanted_element)
            wanted_element.click()
            time.sleep(5)

            try:       
                
                time.sleep(5)
                actions = ActionChains(self.driver)      
                #organize_files_box = WebDriverWait(self.drive
                # r, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'dijitReset dijitInline dijitButtonNode') and @data-dojo-attach-event='ondijitclick:__onClick']")))
                organize_files_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@id = 'ADDTOSUNRISECARTACTION_dijit_form_Button_0']")))
                organize_files_box.click()
                
                time.sleep(10)
                
                if i == 0:
                    time.sleep(5)
                
                '''if i == 1:
                    try:
                        tras = self.driver.find_element(By. XPATH, "//span[@class='align-right ui-icon ui-icon-trash']")
                        tras.click()
                        self.driver.execute_script("arguments[0].click();", btn_tras)

                    except:
                        print("A funcao funcionou normalmente sem interrupcoes")'''
                #script = "document.getElementById('ecm_widget_Button_41').click()"
                #self.driver.execute_script(script)]

                if i == 0:
                    btn_preview = self.driver.find_element(By.XPATH, "(//span[contains(text(), 'Preview')])")
                    btn_tras = self.driver.find_element(By.XPATH, "(//span[contains(text(), 'Close')])//parent::span[1]")
                    
                else:
                    btn_preview = self.driver.find_element(By.XPATH, "(//span[contains(text(), 'Preview')])[2]")
                    btn_tras = self.driver.find_element(By.XPATH,f"(//span[contains(text(), 'Close')])[{i+1}]//parent::span[1]")
                 
                time.sleep(5)
                parent_span = btn_preview.find_element(By.XPATH, "(./parent::span)[1]")
                self.driver.execute_script("arguments[0].click();", parent_span)
                time.sleep(5)
                
                #actions.move_to_element(parent_span).perform()
                
                try:
                    
                    tras = self.driver.find_element(By. XPATH, "//span[@class='align-right ui-icon ui-icon-trash']")
                    tras.click()
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", btn_tras)

                except:
                    print("A funcao funcionou normalmente sem interrupcoes")

                                                         
                '''btn_preview = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Preview')]")
                parent_span = btn_preview.find_element(By.XPATH, "./parent::span")



                bar_element_preview = self.driver.find_elements(By.XPATH, "(//div[@class='dijitDialogPaneActionBar ecmDialogPaneActionBar']")
                bar_element = bar_element_preview[-2]
                button_bars = bar_element.find_element(By.XPATH, "(//span)")
                button_bar = button_bars[7]


                #Elemnteare de java script
                self.driver.execute_script("arguments[0].click();", button_bar)

                preview_elements = self.driver.find_elements(By.XPATH, "(//span[@class = 'dijit dijitReset dijitInline idxButtonDerived dijitButton'])")
                preview = preview_elements[-1]
                actions.move_to_element(preview).perform()
                preview.click()
                
                time.sleep(4)'''
                
                

            except Exception as e:
                print("Elemento nao encontrado, verificar a existencia e posicao de identificador:", e)
                logging.error("Elemento nao encontrado, verificar a existencia e posicao de identificador:")

    
    def rename_n_save(self, file_path_outros):

        name_file = file_path_outros+'\\'+'controle.xlsx'

        if os.path.isfile(name_file):
            
            print("O arquivo de controle ja existe")  
            '''try:                    
                values = self.data_man.get_item_list(name_file, 'controle')                                          
                time.sleep(1)   
                

            except:
                print("Não foram encontrados valores dentro do arquivo de controle.xlsx no diretório controle")
                logging.warning("Nao foram encontrados valores dentro do arquivo de controle.xlsx no diretorio controle")       '''

        else:            
            self.data_man.create_file(name_file, 'controle')
        
        pdf_files = self.data_man.pdf_quantity(file_path_outros)
                
        pattern2 = r'^\d{2}\.\d{2}\.\d{4}\.pdf$'       
        pattern3 = r'^\d{2}\.\d{2}\.\d{4} \d+\.pdf$'
        new_file_handle = [file for file in pdf_files if not re.match(pattern2, file) and not re.match(pattern3, file)]
  
        if new_file_handle:
            for i in range(len(new_file_handle)):
                
                breakpoint()
                pdf_file = os.path.join(file_path_outros, new_file_handle[i])
                #text = self.data_man.read_pdf(pdf_file)
                df = self.data_man.extract_text_from_pdf(pdf_file)
                date_emissao = self.data_man.get_date_from_df(df)
                cl_info_dict, indices, status = self.data_man.get_linhas_cl(df, file_path_outros)
                if status == False:
                    formatted_date = self.rename_it(pdf_file, date_emissao)
                    
                    time.sleep(1)
                    if formatted_date:

                        dir = os.path.dirname(file_path_outros)
                        old_dir = dir + f'\\Controle\\{formatted_date}.pdf'

                        if 2 in indices:
                            new_dir = dir + f'\\CL - 2\\{formatted_date}.pdf'
                        else:
                            new_dir = dir + f'\\CL - OUTROS\\{formatted_date}.pdf'
                        self.data_man.send_file(old_dir,new_dir)
                    else:
                        print("Nao foi possivel fazer mudanca de diretorio")
                else:
                    print(f"O arquivo {pdf_file} já foi renomeado e inserido no devido diretorio de destino")

        else:
            print("The list is empty.")
        
        return print("itens renomeados e movidos com sucesso")
    

            




        
       
 
    
'''if __name__ == "__main__":    
    chrome_driver_manager = ChromeDriverMan()
    
    chrome_driver_manager.get_page(chrome_driver_manager.url)
    chrome_driver_manager.login()
'''
    
    
