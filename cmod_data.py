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
from datetime import datetime


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
            
    def create_file2(self, root, new_file_name):
                                
            df = pd.DataFrame()            
            #name_file = root+'\\'+new_file_name+'.xlsx'
            name_file = root
            try:
                df.to_excel(name_file, index=False)
                #column_names = ['gen_infos', 'cl_number']
                df = pd.DataFrame()
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
            #files = [file for file in df[column_name].values 
            
            return item_exists
        except:
            print(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
            return logging.error(f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}")
    
    def verify_item_existence2(self, root, file_name, row):
        try:
            # Define the full path to the Excel file
            excel_file = root  # If the full path is already provided, no need to concatenate file_name
            df = pd.read_excel(excel_file)
            
            # Convert the row to a DataFrame for comparison
            row_df = pd.DataFrame([row], columns=df.columns)
            
            # Check if the row exists in the DataFrame
            item_exists = any(df.eq(row_df.iloc[0]).all(axis=1))
            
            return item_exists
        except Exception as e:
            error_message = f"Nao foi possivel verificar a existencia do arquivo, tente novamente ou verifique o nome e local do arquivo {excel_file}: {e}"
            print(error_message)
            return logging.error(error_message)
        
    def get_data_one(self, row):

        try:
            
            network_directory = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS FRANCESINHA"
            #network_directory = self.xlsx_dir            
            all_files = os.listdir(network_directory)
            xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
            
            

            if len(xlsx_files) == 1:
                file_path = network_directory+'\\'+xlsx_files[0]
                df = pd.read_excel(file_path)

            else:
                print("ERRO! Verifique a pasta 'DOCUMENTOS FRANCESINHA' e certifique-se de haver apenas um arquivo '.xlsx' na raiz")
                return logging.error("ERRO! Verifique a pasta 'DOCUMENTOS FRANCESINHA' e certifique-se de haver apenas um arquivo '.xlsx' na raiz")

            num_rows, num_columns = df.shape

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
            
            list_of_subdir_original = []          

            for i in range(num_rows):
                child_dir1_name = str(task_name)+'-'+str(df.iloc[i,5])                    
                list_of_subdir_original.append(main_dir_task+"\\"+child_dir1_name)
                
        except:
            return logging.error(f"Alguma coisa errada não está certa na criação do diretório para a task {task_name}, verificar se os nomes estão corretos no arquivo '.xlsx' ")
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
        
        
        return date_string1, date_string2, ag, cc, network_directory,list_of_subdir_original, list_of_subdir



    def get_data_two(self, row):

        rows = self.connect.main()
        network_directory = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS FRANCESINHA"
        dataw = r"\\192.168.24.17\Carga\Bradesco\CPI\LANBACEM-TI\DOCUMENTOS FRANCESINHA\Controle_de_dados"
        new_file_controle = os.path.join(dataw, 'controle_dados.xlsx')
        dask_name = 'Controle_de_dados'
        columns = ['TASK_ID', 'START_DATE', 'END_DATE', 'FIELD1', 'FIELD2', 'FIELD3', 'FIELD4', 'CODE', 'NAME', 'FIELD5', 'FIELD6', 'FIELD7', 'FIELD8', 'STATUS', 'FIELD9', 'DESCRIPTION', 'FIELD10', 'UNIQUE_ID']
        

        '''if os.path.exists(dataw):
                print(f"O arquivo Controle_de_dados  já foi criado")

                if os.path.exists(new_file_controle):
                    print("O arquivo de controle_dados já existe")
                    for row in rows:
                        
                        eacth = str(row)
                        stats = self.verify_item_existence2(new_file_controle,'nenhum',eacth)
                        if stats == False:
                            existing_df = pd.read_excel(new_file_controle)  
                            eacth = eval(eacth)                  
                            pd.concat([existing_df, pd.DataFrame([eacth], columns=columns)], ignore_index=True).to_excel(new_file_controle, index=False)    
                            new_row_df = pd.DataFrame(eacth)
                            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)        
                            updated_df.to_excel(new_file_controle, index=False)
                            
                else:                
                    self.create_file2(new_file_controle, 'nthing')
                    print("O arquivo de controle_dados está sendo criado")
                    for row in rows:
                        eacth = str(row)
                        stats = self.verify_item_existence(new_file_controle,'nenhum',eacth)
                        if stats == False:                        
                            existing_df = pd.read_excel(new_file_controle)                        
                            new_row_df = pd.DataFrame(eacth)
                            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)        
                            updated_df.to_excel(new_file_controle, index=False)
                
            else:
                print("Criando o arquivo diretorio para salvar dados de controle")
                self.create_folder(network_directory,dask_name)            

                if os.path.exists(new_file_controle):
                    print("O arquivo de controle_dados já existe")
                    for row in rows:
                        
                        eacth = str(row)
                        stats = self.verify_item_existence(new_file_controle,'nenhum',eacth)
                        if stats == False:
                            existing_df = pd.read_excel(new_file_controle)                        
                            new_row_df = pd.DataFrame(eacth)
                            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)        
                            updated_df.to_excel(new_file_controle, index=False)
                            
                else:                
                    self.create_file(new_file_controle, 'nthing')
                    print("O arquivo de controle_dados está sendo criado")
                    for row in rows:
                        eacth = str(row)
                        stats = self.verify_item_existence(new_file_controle,'nenhum', eacth)
                        if stats == False:                        
                            existing_df = pd.read_excel(new_file_controle)                        
                            new_row_df = pd.DataFrame(eacth)
                            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)        
                            updated_df.to_excel(new_file_controle, index=False)
                                '''

        columns = ['TASK', 'PERIODO_INICIAL', 'PERIODO_FINAL', 'BANCO', 'AGENCIA', 'CONTA', 'DIGITO', 'RAZAO', 'NOME', 'NUM_DOCUMENTOS', 'NUM_PAGINAS', 'CURR_PAGE', 'CURR_LINE', 'STATUS', 'HOST', 'PROCESSO', 'CURR_DOC', 'GUID']
        
        row_data = list(rows[-1])
        new_row = [row_data]
        df = pd.DataFrame(new_row, columns=columns)

        try:

            
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
        
        
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_dict['date_time'] = current_datetime

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
        #pattern = r'\d{2}/\d{2}/\d{3}\.\d{3}\.\d{3}'
        #pattern = r'\d{2}/\d{2,5}/(\d{3}\.\d{3}\.\d{3}|\d+)'
        #pattern = r'(\d{2}/\d{2}/\d{3}\.\d{3}\.\d{3})\s+(\d+)\s+([\w\s&]+?)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(\d+)'
        pattern = r'(\d{2}/\d{2}/\d{3}\.\d{3}\.\d{3})\s+(\d+/\d+|\d+)\s+([\w\s&]+?)\s+(\d{2}/\d{2}/\d{4})\s+([\d,]+)'
        #pattern = r"(\d{2}/\d{2}/\d{3}\.\d{3})\s+(\d+)\s+([A-Z\s]+)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2},\d{2})"
        indices = []
        gen_infos = []
        cl_numbers = []
        info_pack = {'gen_infos': '', 'cl_number': ''} 
        colls = []
        
        for index, row in df.iterrows():            
            
            for col in df.columns:
                
                if re.search(pattern, str(row[col])):                                       
                    time.sleep(1)
                    indices.append(index)              
                    first_string = df.iloc[index,0]
                    colls.append(first_string)
                    print(f"Dados identificados e encontrado {first_string}")
                    
                    '''elif len(colls) == 0:
                    print("Regex nao está identificando os dados do pdf")
                    logging.error("Regex nao esta identificando os dados do pdf")
                    return [],[], "Não foi encontrado o padrão regex para este documento"'''
                else:
                    #return [],[], "alguma diferenca do estado antigo para atual"
                    pass
                    
        if len(colls)>0:
            for i in range(len(colls)):
                
                last_nosso_numero = colls[-1].split()
                last_nosso_numero = last_nosso_numero[0]
                
                splitie =  colls[i].split()
                nosso_numero = splitie[0]
                first_string = colls[i] 
                gen_infos.append(first_string)            
                
                if nosso_numero != str(colls[i]).split()[0]:
                    print(f"Codigo regex {str(row[col])[0]} diferente do valor encontrado em 'Nosso Numero' {str(nosso_numero)} ")
                elif len(indices) != len(colls):
                    print("O numero de registros de indices é diferente dos valores encontrados de nosso número na lista de CLs")
                elif first_string not in gen_infos:
                    gen_infos.append(first_string)
                
                            
                dirty_string = df.iloc[indices[i], -3]
                cleaned_string = ' '.join(dirty_string.split())
                cleaned = cleaned_string.split()

                
                
                if len(cleaned)==0:
                    print("CL number is a little fcd :) ")
                    logging.warning("CL number is a little fcd :) ")
                    try:
                        dirty_string = df.iloc[indices[i], 1]
                        cleaned_string = ' '.join(dirty_string.split())
                        cleaned = cleaned_string.split()
                        cl_number = cleaned[-1]
                        print("Tentativa de abordagem diferente para obtencao do CL pois  apresenta formatacao diferente")
                        logging.warning("Tentativa de abordagem diferente para obtencao do CL pois  apresenta formatacao diferente")
                        print(f'gen_info = {colls[i]}, e suposto CL = {cl_number}')
                        logging.warning(f'gen_info = {colls[i]}, e suposto CL = {cl_number}')
                        
                        print(f'Novo gen_info = {colls[i]}, e suposto CL = {cl_number}')
                        logging.warning(f'Novo gen_info = {colls[i]}, e suposto CL = {cl_number}')
                    except:
                        print("A definicao do elemento CL esta com problemas")
                        logging.warning("A definicao do elemento CL esta com problemas")
                    
                    cl_numbers.append(cl_number)     
                    info_pack1 = {'gen_infos': f'{first_string}', 'cl_number': f'{cl_number}'}
                    
                    status = self.verify_item_existence(file_name, 'controle', f'{first_string}')
                    
                    #False means "do not exist" ---then--> update/insert in the file
                    if status == False:
                        self.update_excel_with_new_row(file_name, info_pack1)
                        time.sleep(1)
                        print(f"Realizando atualizacao da lista controle com elemento n°: {i}")
                        if nosso_numero == last_nosso_numero:
                            info_pack = {'gen_infos': 'Lista de CLs ---> ', 'cl_number': f'{cl_numbers}'}
                            self.update_excel_with_new_row(file_name, info_pack)
                            (f"Realizando atualizacao do elemento separador final da lista controle com elemento n°: {i}")
                    else:
                        print(f"O elemento ja existe na lista de controle ---> volta de número: {i}")                        
                        return [],[], True
                else:   
                    print("CL number is not as fcd as before :) ")
                    logging.warning("CL number is not as fcd as before :) ")
                    
                    if cleaned[-1] == '.':
                        cl_number = cleaned[-2]
                    else:
                        cl_number = cleaned[-1]
                        '''try:
                            print("Tentativa de abordagem diferente para obtencao do CL pois  apresenta formatacao diferente")
                            logging.warning("Tentativa de abordagem diferente para obtencao do CL pois  apresenta formatacao diferente")
                            print(f'gen_info = {colls[i]}, e suposto CL = {cl_number}')
                            logging.warning(f'gen_info = {colls[i]}, e suposto CL = {cl_number}')
                            dirty_string = df.iloc[indices[i], 1]
                            cleaned_string = ' '.join(dirty_string.split())
                            cleaned = cleaned_string.split()
                            cl_number = cleaned[-1]
                            print(f'Novo gen_info = {colls[i]}, e suposto CL = {cl_number}')
                            logging.warning(f'Novo gen_info = {colls[i]}, e suposto CL = {cl_number}')
                        except:
                            print("A definicao do elemento CL esta com problemas")
                            logging.warning("A definicao do elemento CL esta com problemas")'''
                        

                    cl_numbers.append(cl_number)     
                    info_pack1 = {'gen_infos': f'{first_string}', 'cl_number': f'{cl_number}'}
                    
                    status = self.verify_item_existence(file_name, 'controle', f'{first_string}')
                    
                    #False means "do not exist" ---then--> update/insert in the file
                    if status == False:
                        self.update_excel_with_new_row(file_name, info_pack1)
                        time.sleep(1)
                        print(f"Realizando atualizacao da lista controle com elemento n°: {i}")
                        if nosso_numero == last_nosso_numero:
                            info_pack = {'gen_infos': 'Lista de CLs ---> ', 'cl_number': f'{cl_numbers}'}
                            self.update_excel_with_new_row(file_name, info_pack)
                            (f"Realizando atualizacao do elemento separador final da lista controle com elemento n°: {i}")
                    else:

                        print(f"O elemento ja existe na lista de controle ---> volta de número: {i}")                        
                        return [],[], True

                time.sleep(1)
            else:
                print("Todas as colunas analisadas nao retornaram padrao de reconhecimento do regex")
                logging.warning("Todas as colunas analisadas nao retornaram padrao de reconhecimento do regex")
                
        
        return info_pack1, cl_numbers, status
    



    
    def send_file(self, file_path, new_file_path):
        try:
            shutil.move(file_path, new_file_path)
            print(f"File moved from {file_path} to {new_file_path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

