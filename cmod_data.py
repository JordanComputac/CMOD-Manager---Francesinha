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
import PyPDF2
from PyPDF2 import PdfReader
import fitz
import shutil


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
            #name_file = root+'\\'+new_file_name+'.xlsx'
            name_file = root
            try:
                df.to_excel(name_file, index=False)
                column_names = ['gen_infos', 'cl_number']
                df = pd.DataFrame(columns=column_names)
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
            excel_file = root
            column_name = 'Nosso numero'
            df = pd.read_excel(excel_file)            
            files = [file for file in df[column_name].values]                        
            return files
        except:
            print(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            logging.error(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            return ''
        
    def verify_item_existence(self, root, file_name, row):
        
        try:
            #excel_file = root+'\\'+file_name+'.xlsx'
            excel_file = root
            column_name = 'gen_infos'
            df = pd.read_excel(excel_file)
            row = str(row)
            item_exists = row in df[column_name].values
            #files = [file for file in df[column_name].values ]  
            
            return item_exists
        except:
            print(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            return logging.error(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
    


    def get_data_one(self, row):

        rows = self.connect.main()
        

        columns = ['TASK', 'PERIODO_INICIAL', 'PERIODO_FINAL', 'BANCO', 'AGENCIA', 'CONTA', 'DIGITO', 'RAZAO', 'NOME', 'NUM_DOCUMENTOS', 'NUM_PAGINAS', 'CURR_PAGE', 'CURR_LINE', 'STATUS', 'HOST', 'PROCESSO', 'CURR_DOC', 'GUID']
        
        row_data = list(rows[0])
        new_row = [row_data]
        df = pd.DataFrame(new_row, columns=columns)

        try:

            network_directory = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS FRANCESINHA"
            #network_directory = self.xlsx_dir            
            all_files = os.listdir(network_directory)
            xlsx_files = [file for file in all_files if file.endswith('.xlsx')]


           
            

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

            child_dir3_name = "CL - 2"
            child_dir3 = os.path.join(main_dir_task, child_dir3_name)
            path_to3 = main_dir_task+"\\"+child_dir3_name
            
            list_of_subdir = [path_to1, path_to2, path_to3]

            if os.path.exists(main_dir_task):
                print(f"O arquivo {task_name} já foi criado")

                if os.path.exists(path_to1):
                    print(f"O arquivo {path_to1} já existe no diretorio")                            
                elif os.path.exists(path_to2):
                    print(f"O arquivo {path_to2} já existe no diretorio")
                elif os.path.exists(path_to3):
                    print(f"O arquivo {path_to3} já existe no diretorio")
                else:
                    
                    try:                        
                        self.create_folder(main_dir_task, child_dir1_name)
                        time.sleep(1)
                        self.create_folder(main_dir_task, child_dir2_name)
                        time.sleep(1)
                        self.create_folder(main_dir_task, child_dir3_name)
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
                    time.sleep(1)
                    self.create_folder(main_dir_task, child_dir3_name)
                except:
                    logging.error(f"ERRROR ao criar pasta {task_name} ou subpastas dentro da pasta {task_name}")

        except:
            return logging.error(f"Alguma coisa errada não está certa na criação do diretório para a task {task_name}, verificar se os nomes estão corretos no arquivo '.xlsx' ")
        
        
        return date_string1, date_string2, ag, cc, network_directory, list_of_subdir
    

    def read_pdf(self, file_path):

        try:
            
            with open(file_path, 'rb') as file:
                
                pdf = PdfReader(file)
                
                information = pdf.metadata
                number_of_pages = len(pdf.pages)                

                #reader = PyPDF2.PdfReader(file)
                
                if pdf.is_encrypted:
                    pdf.decrypt('')
                                
                text = ''
                
                for page_num in range(number_of_pages):
                    #page = pdf.getPage(page_num)
                    page = pdf.pages[page_num]
                    text += page.extract_text()
                
                return text
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error("Ocorreu um erro na leitura do conteúdo do pdf na lista")
            return None


    def pdf_quantity(self, files_path):

        network_directory = files_path        
        all_files = os.listdir(network_directory)

        pdf_files = [file for file in all_files if file.lower().endswith('.pdf')]
        
        '''lin_files = [file for file in all_files if file.endswith('.lin')]                
        txt_files = [file for file in all_files if file.endswith('.txt')] 
        tmp_files = [file for file in all_files if file.endswith('.tmp')]'''

        return pdf_files
           

    def extract_text_from_pdf(self, file_path):
        try:
            document = fitz.open(file_path)
            text = ''
            for page_num in range(document.page_count):
                
                page = document.load_page(page_num)
                text += page.get_text()
                lines = text.strip().split('\n')
                lines = [line for line in lines if line.strip()]
                max_columns = 0
                for line in lines:
                    columns = line.split(',')
                    if len(columns) > max_columns:
                        max_columns = len(columns)
                data = []
                for line in lines:
                    columns = line.split(',')
                    while len(columns) < max_columns:
                        columns.append('')
                    data.append(columns)

                df = pd.DataFrame(data)
            return df
        
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error("Ocorreu um erro na leitura do conteúdo do pdf na lista")
            return None

    def get_date_from_df(self, df):
        matches = re.findall(r'\d{2}/\d{2}/\d{4}', df[0][1])
        if len(matches) >= 2:
            second_date = matches[1]
            print(second_date)
        else:
            print("Second date not found")
        return second_date
        
    
    def update_excel_with_new_row(self, file_name, data_dict):
      
        try:            
            existing_df = pd.read_excel(file_name)
        except FileNotFoundError:                        
            #existing_df = pd.DataFrame(columns=data_dict[0].keys())
            existing_df = pd.DataFrame(columns = data_dict.keys())
            print(f"{file_name} nao existia e precisou ser criado")
            logging.warning(f"{file_name} nao existia e precisou ser criado")
        
        try:
            new_data_list = [value for key, value in data_dict.items()]
            new_row_df = pd.DataFrame([data_dict])
            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)        
            updated_df.to_excel(file_name, index=False)
            return print("dados atualizados na lista de controle com sucesso! ")
        except:
            print("Atualizacao de dados de controle .xlsx nao ocorreu conforme planejado, há algum impeditivo")
            logging.warning("Atualizacao de dados de controle .xlsx nao ocorreu conforme planejado, ha algum impeditivo")
            
    
            
    def get_linhas_cl(self, df, file_path_outros):

        file_name = file_path_outros+'\\controle.xlsx'
        pattern = r'09/\d{2}/\d{3}\.\d{3}\.\d{3}'

        indices = []
        gen_infos = []
        cl_numbers = []
        info_pack = {'gen_infos': '', 'cl_number': ''}

        for index, row in df.iterrows():
            for col in df.columns:
                if re.search(pattern, str(row[col])):
                    indices.append(index)                   
                    first_string = df.iloc[index,0]
                    splitie =  first_string.split()
                    nosso_numero = splitie[0]
                    gen_infos.append(first_string)

                    if nosso_numero != str(row[col]).split()[0]:
                        print(f"Codigo regex {str(row[col])[0]} diferente do valor encontrado em 'Nosso Numero' {str(nosso_numero)} ")
                        #logging.warning("Codigo regex diferente do valor encontrado em 'Nosso Numero' ")
                                        
                    dirty_string = df.iloc[index, -3]
                    cleaned_string = ' '.join(dirty_string.split())
                    cleaned = cleaned_string.split()
                    cl_number = cleaned[1]
                    cl_numbers.append(cl_number)    
                    
                    
                    info_pack1 = {'gen_infos': f'{first_string}', 'cl_number': f'{cl_number}'}   
                    status = self.verify_item_existence(file_name, 'controle', f'{first_string}')

                    if status == False:
                        self.update_excel_with_new_row(file_name, info_pack1)
                    else:        
                        break    
                    time.sleep(1)                    
                    
        if status == False:
            info_pack = {'gen_infos': 'Lista de CLs ---> ', 'cl_number': f'{cl_numbers}'}
            self.update_excel_with_new_row(file_name, info_pack)
        else:
            print(f"O elemento {first_string} já existe e será pulado")
            
        return info_pack, indices, status
    



    
    def send_file(self, file_path, new_file_path):
        try:
            shutil.move(file_path, new_file_path)
            print(f"File moved from {file_path} to {new_file_path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

