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
    df2 =df[0].str.split('/',expand=True).iloc[:, [-3,-2,-1]].dropna()
    df2.columns = ['grammar_type_2', 'file_name' , 'text']
    # print(df2)

    ############TRANSCRIPCIONES
    
    df3 = pd.read_csv('REFS_transcriptions_'+ lang +'.txt', header = None, encoding='latin-1').replace('\:','/', regex= True)
    df4 =df3[0].str.split('/',expand=True).iloc[:, [-3,-2,-1]].dropna()
    df4.columns = ['grammar_type_2_x', 'file_name' , 'text']
    # print(df4.columns)
   
    ######MERGEO LOS DOS DATAFRAME

    df_final = pd.merge(df2, df4, on='file_name', how='left')
    print(df_final)
    time_bar = df_final['grammar_type_2'] == input 
    all = df_final[time_bar]
    # print(all)
    # 
    final_data = df_final[["text_y", "text_x",]]
    print(final_data)
    
    
    final_data.columns = ['text', 'tags',]
    
    
    ###LO GUARDO EN UN JSON
    js = final_data.to_json(orient = 'records', force_ascii=False)
    out_file.write(js)
# 


def main():
        print("Creating your json!")
        json_creator(sys.argv[1], sys.argv[2])
        # print("Launching grammar-tk!")
        # grammar_tk_launcher(sys.argv[1], sys.argv[2])
        # print('Parsing results to csv!')
        # results_parser(sys.argv[1], sys.argv[2])
main()    
