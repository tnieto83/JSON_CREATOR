import pandas as pd
import re
import json
import sys
import shlex
from subprocess import call
import io
import csv



def json_creator(input, lang):
    file = input.rsplit('.', 1)[0]+ ".json"
    out_file = open(file, "w+", encoding='latin-1')




    #########OPERANDOS
    # cargo el primer txt y lo convierto en dataframe
    df = pd.read_csv('REFS_operands_'+ lang +'.txt', header = None, encoding='latin-1')


    # sustituyo : por / para unificar
    df2 = df.replace('\:','/', regex= True)
    # print(df2)

    # divido los datos por / y creo una columna para cada uno
    df3 =df2[0].str.split('/',expand=True)


    #creo un data frame con las 4 ultimas columnas
    df4 = df3.iloc[:, [-4, -3,-2,-1]]
    #print(df4)


    #elimino columnas con valores none
    df5 = df4.dropna()
    # print(df5)


    #asigno nombre a las columnas

    df5.columns = ['grammar_type', 'grammar_type_2', 'file_name' , 'text']
    print(df5)


    ############TRANSCRIPCIONES
    # cargo el primer txt y lo convierto en dataframe
    df = pd.read_csv('REFS_transcriptions_'+ lang +'.txt', header = None, encoding='latin-1')


    # sustituyo : por / para unificar
    df2 = df.replace('\:','/', regex= True)
    # print(df2)

    # divido los datos por / y creo una columna para cada uno
    df3 =df2[0].str.split('/',expand=True)


    #creo un data frame con las 4 ultimas columnas
    df4 = df3.iloc[:, [-4, -3,-2,-1]]
    # print(df4)

    #elimino columnas con valores none
    final_transciptions = df4.dropna()
    # print(df5)


    #asigno nombre a las columnas
    final_transciptions.columns = ['grammar_type', 'grammar_type_2', 'file_name' , 'text']
    print(final_transciptions)


    ######MERGEO LOS DOS DATAFRAME

    df_final = pd.merge(df5, final_transciptions, on='file_name', how='left')
    print(df_final)
    final_data = df_final[["text_y", "text_x",]]
    print(final_data)

    final_data.columns = ['text', 'tags']
    print(final_data)


    #####LO GUARDO EN UN JSON
    js = final_data.to_json(orient = 'records', force_ascii=False)
    out_file.write(js)


def grammar_tk_launcher(input, lang):       
       
        file = input.rsplit('.', 1)[0]+ ".json"
        call(shlex.split('/opt/verbio/bin/grammar-tk' + ' -a ' + 'builtin_' + input + '_' + lang + '-asr3.bnf' + ' -r ' + file + ' -o  ' + input.rsplit('.', 1)[0] + '_results.json'))

def results_parser(input, lang):
            
            js_input = str(input.rsplit('.', 1)[0] + '_results.json')
            x = io.open(js_input, encoding='latin-1')  
            data = json.load(x)       
        
            
        
            f = csv.writer(open(input.rsplit('.', 1)[0] + ".csv", "w+", encoding="latin-1"), delimiter=';')
            
            # Write CSV Header, If you dont need that, remove this line
            f.writerow(["text","success", "reference", "tags"])
        
            for d in data:
                f.writerow([
                            d["reference"]["text"],
                            d["success"],
                            d["reference"]["tags"],          
                            d["tags"]])


def main():
        print("Creating your json!")
        json_creator(sys.argv[1], sys.argv[2])
        print("Launching grammar-tk!")
        grammar_tk_launcher(sys.argv[1], sys.argv[2])
        print('Parsing results to csv!')
        results_parser(sys.argv[1], sys.argv[2])
main()    
