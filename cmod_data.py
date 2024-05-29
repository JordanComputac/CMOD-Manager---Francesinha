from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import csv
import re
import pandas as pd
from datetime import datetime
import logging
import time
from request import Connect

logging.basicConfig(filename='warning.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


class DataManager:

    def __init__(self):

        self.connect = Connect()
        
        current_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(current_dir, '.env')              
        load_dotenv(dotenv_path)

        
        self.xlsx_dir = os.getenv("XLSX_DIR")


    def create_folder(self, root, new_folder_name):
        
        try:
                
            dir_task = new_folder_name
            destination_folder = root
            new_folder_path = os.path.join(destination_folder, dir_task)
            
            os.mkdir(new_folder_path)

            return print(f"O diretório {new_folder_name} foi criado com sucesso no caminho {root}")
        except:

            print(f"Ocorreu um erro na criação da pasta {new_folder_name}, verificar diretório {root} ou acesso com VPN")
            return logging.error(f"Ocorreu um erro na criação da pasta {new_folder_name}, verificar diretório {root} ou acesso com VPN")




    def create_file(self, root, new_file_name):
                    
            df = pd.DataFrame()            
            name_file = root+'\\'+new_file_name+'.xlsx'
            try:
                df.to_excel(name_file, index=False)
                print("Arquivo de controle de processados criado com sucesso! ('\U0001F603')")
            except:
                print(f"Houve um problema ao criar o arquivo {new_file_name} no diretorio fornecido {root}")
                logging.error(f"Houve um problema ao criar o arquivo {new_file_name} no diretorio fornecido {root}")


    def update_row(self, root, file_name, nosso_numero):

        excel_file = root+'\\'+file_name+'.xlsx'
        df = pd.read_excel(excel_file)
        new_row = {'Nosso numero': f'{nosso_numero}', 'Nome arquivo': file_name}
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)

        try:
            df.to_excel(excel_file, index=False)
            return print(f"Nova linha {new_row} inserida com sucessso! '\U0001F609'" )
        except:
            print(f"Problema ao salvar nome do arquivo processado - arquivo {file_name} que esta na raiz como {excel_file}")
            return logging.error(f"Problema ao salvar nome do arquivo processado - arquivo {file_name} que esta na raiz {excel_file}")
      
        
    
    def get_item_list(self, root, file_name):
        
        try:
            excel_file = root+'\\'+file_name+'.xlsx'
            column_name = 'Nosso numero'
            df = pd.read_excel(excel_file)
            #row = int(row)
            #item_exists = row in df[column_name].values 
            files = [file for file in df[column_name].values ]                        
            return files
        except:
            print(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            logging.error(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            return ''
        
    def verify_item_existence(self, root, file_name, row):
        
        try:
            excel_file = root+'\\'+file_name+'.xlsx'
            column_name = 'Nosso numero'
            df = pd.read_excel(excel_file)
            row = int(row)
            item_exists = row in df[column_name].values 
            #files = [file for file in df[column_name].values ]            
            return item_exists
        except:
            print(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            return logging.error(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
    


    def get_data_one(self, row):

        rows = self.connect.main()
        

        columns = ['TASK', 'PERIODO_INICIAL', 'PERIODO_FINAL', 'BANCO', 'AGENCIA', 'CONTA', 'DIGITO', 'RAZAO', 'NOME', 'NUM_DOCUMENTOS', 'NUM_PAGINAS', 'CURR_PAGE', 'CURR_LINE', 'STATUS', 'HOST', 'PROCESSO', 'CURR_DOC', 'GUID']
        row_data = list(rows[-1])
        new_row = [row_data]
        df = pd.DataFrame(new_row, columns=columns)

        try:

            network_directory = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS FRANCESINHA"
            #network_directory = self.xlsx_dir            
            all_files = os.listdir(network_directory)
            xlsx_files = [file for file in all_files if file.endswith('.xlsx')]


            '''if len(xlsx_files) == 1:
                file_path = network_directory+'\\'+xlsx_files[0]
                df = pd.read_excel(file_path)

            else:
                print("ERRO! Verifique a pasta 'DOCUMENTOS BAIXA' e certifique-se de haver apenas um arquivo '.xlsx' na raiz")
                return logging.error("ERRO! Verifique a pasta 'DOCUMENTOS BAIXA' e certifique-se de haver apenas um arquivo '.xlsx' na raiz")

            num_rows, num_columns = df.shape'''

            

            task_name = df.iloc[row,0]
            date1 = df.iloc[row,1]
            date2 = df.iloc[row,2]

            timestamp = pd.to_datetime(date1)
            date_string1 = timestamp.strftime('%d-%m-%Y')           
            date_string1 = date_string1.replace('-','/')
            timestamp2 = pd.to_datetime(date2)
            date_string2 = timestamp2.strftime('%d-%m-%Y')
            date_string2 = date_string2.replace('-','/')
            
            ag = df.iloc[row,4]
            
            ag = str(ag).zfill(5)
            c1 = df.iloc[row, 5]
            c2 = df.iloc[row,6]
            cc = str(c1)+'-'+str(c2)         
            nome = df.iloc[row,8]
            


        except:
           print("Algum problema com a aquisicao de dados, verifique o seu arquivo se está no formato e com campos alocados corretamente")
           return logging.error("Algum problema com a aquisicao de dados, verifique o seu arquivo se esta no formato e com campos alocados corretamente")
        
        try:

            main_dir_task = os.path.join(network_directory, task_name)
            #child_dir1_name = "CL - 2"
            child_dir1_name = "Controle"
            child_dir1 = os.path.join(main_dir_task, child_dir1_name)
            path_to1 = main_dir_task+"\\"+child_dir1_name

            child_dir2_name = "CL - OUTROS"
            child_dir2 = os.path.join(main_dir_task, child_dir2_name)
            path_to2 = main_dir_task+"\\"+child_dir2_name
            
            list_of_subdir = [path_to1, path_to2]

            if os.path.exists(main_dir_task):
                print(f"O arquivo {task_name} já foi criado")

                if os.path.exists(path_to1):
                    print(f"O arquivo {path_to1} já existe no diretorio")                            
                elif os.path.exists(path_to2):
                    print(f"O arquivo {path_to2} já existe no diretorio")
                else:
                    
                    try:                        
                        self.create_folder(main_dir_task, child_dir1_name)
                        time.sleep(1)
                        self.create_folder(main_dir_task, child_dir2_name)
                    except:
                        logging.error(f"ERRROR ao criar as subpastas dentro da pasta {task_name}")

                
            else:
                #Criacao do diretorio principal que guardará o{s subdiretórios de contas diferentes
                try:
                    self.create_folder(network_directory,task_name)
                    time.sleep(3)
                    self.create_folder(main_dir_task, child_dir1_name)
                    time.sleep(1)
                    self.create_folder(main_dir_task, child_dir2_name)
                except:
                    logging.error(f"ERRROR ao criar pasta {task_name} ou subpastas dentro da pasta {task_name}")

        except:
            return logging.error(f"Alguma coisa errada não está certa na criação do diretório para a task {task_name}, verificar se os nomes estão corretos no arquivo '.xlsx' ")
        
        
        return date_string1, date_string2, ag, cc, network_directory, list_of_subdir
    
    


    
    