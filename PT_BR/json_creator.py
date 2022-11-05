import pandas as pd
import re
import sys
import shlex
from subprocess import call
import io
import json
import csv

def json_creator(input):
    with open('REFS_operands_pt-br.txt', encoding='latin-1') as operands:
        lst_operands = []
        file = input.rsplit('.', 1)[0]+ ".json"
        out_file = open(file, "w+", encoding='latin-1') 
       
        # if input in 'boolean' or input in 'time' or input in 'creditcard' or input in 'number':       
        
        for l in operands:
                       if '/' + input in l and 'TEXT REFERENCES' not in l:
                            
                            # data = re.sub('TEXT REFERENCES FOR spell/spell_digits FOLDER', " ", l)
                            # print(data)
                            data = re.sub("[\/\:]", ",", l) 
                            file = data.rsplit(',')
                            file_name = file[-2].strip()
                            # print(file_name)
                            gram_type =  file[-3].strip()
                            # print(gram_type)
                            text = file[-1].strip()
                            # print(text)

                            lst_operands.append({'GRAMMAR':gram_type, 'FILE_NAME':file_name, 'tags':text})


        df = pd.DataFrame(lst_operands)
        # print(df)




        with open('REFS_transcriptions_pt-br.txt', encoding='latin-1') as transcriptions:
            lst_transcriptions = []
            
            for l in transcriptions:
                                                             
                       if '/' + input in l and 'TEXT REFERENCES' not in l:
                            

                            data = re.sub("[\/\:]", ",", l) 
                            file = data.rsplit(',')
                            # print(file)
                            file_name = file[-2].strip()
                            # print(file_name)
                            gram_type =  file[-3].strip()
                            # print(gram_type)
                            text = file[-1].strip()
                            # print(text)

                            lst_transcriptions.append({'GRAMMAR':gram_type, 'FILE_NAME':file_name, 'text':text})


            df_2 = pd.DataFrame(lst_transcriptions)



        df_final = pd.merge(df, df_2, on='FILE_NAME', how='left')
        final_data = df_final[["text", "tags",]]


        # print(final_data)

        # # # Guardamos en un json
        js = final_data.to_json(orient = 'records', force_ascii=False) 
        # print(js)
        out_file.write(js)


def grammar_tk_launcher(input):       
       
        file = input.rsplit('.', 1)[0]+ ".json"
        call(shlex.split('/opt/verbio/bin/grammar-tk' + ' -a ' + 'builtin_' + input + '_pt-br-asr3.bnf' + ' -r ' + file + ' -o  ' + input.rsplit('.', 1)[0] + '_results.json'))

def results_parser(input):
            
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
        json_creator(sys.argv[1])
        print("Launching grammar-tk!")
        grammar_tk_launcher(sys.argv[1])
        print('Parsing results to csv!')
        results_parser(sys.argv[1])
main()    
