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
    df = pd.read_csv('REFS_operands_'+ lang +'.txt', header = None, encoding='latin-1').replace('\:','/', regex= True)
    df2 =df[0].str.split('/',expand=True).iloc[:, [-4, -3,-2,-1]].dropna()
    df2.columns = ['grammar_type', 'grammar_type_2', 'file_name' , 'text']

    ############TRANSCRIPCIONES
    
    df3 = pd.read_csv('REFS_transcriptions_'+ lang +'.txt', header = None, encoding='latin-1').replace('\:','/', regex= True)
    df4 =df3[0].str.split('/',expand=True).iloc[:, [-4, -3,-2,-1]].dropna()
    df4.columns = ['grammar_type', 'grammar_type_2', 'file_name' , 'text']
    
   
    ######MERGEO LOS DOS DATAFRAME

    df_final = pd.merge(df2, df4, on='file_name', how='left')
    final_data = df_final[["text_y", "text_x",]]
    
    # planets_2008 = planets[planets['grammar_type_x'] == input]
    final_data.columns = ['text', 'tags',]
    
    
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
