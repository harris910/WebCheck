import pandas as pd
import urllib.request
import os
from openpyxl import load_workbook

notloaded_scripts=[]

def read_script_names(features_file_name):
    df = pd.read_excel(features_file_name)
    scripts = df["script_name"].unique().tolist()
    return scripts 
    #print(scripts)

def check_webpack_keyword(string):
    is_bundled=0
    keywords=["webpackChunk","webpackJsonp"]
    for keyword in keywords:
        if keyword in string:
            is_bundled = 1
    return is_bundled

def mark_scripts_bundled(scripts):
    lab_scripts={}
    for script in scripts:
        req = urllib.request.Request(
            url=script, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        try:
            with urllib.request.urlopen(req) as response:
                html = response.read().decode("utf-8")
                #print(html)
                is_bundled=check_webpack_keyword(html)
                lab_scripts.update({script:is_bundled})
                #print(is_bundled)
        except Exception as error:
            #print(error)
            notloaded_scripts.append((script,error))
            lab_scripts.update({script:0})
    return lab_scripts

def updating_features_excel(input_features_file_path,output_folder_path,lab_scripts):
    original_features_file = pd.read_excel(input_features_file_path)
    labelled_features_file = original_features_file.copy()
    labelled_features_file['is_bundled'] = None 
    for index, row in labelled_features_file.iterrows():
        labelled_features_file.loc[index, 'is_bundled'] = lab_scripts[row['script_name']]

    output_folder_path_plus_file=output_folder_path+"labelled_features.xlsx"
    if os.path.exists(output_folder_path):
        os.remove(output_folder_path_plus_file)
    labelled_features_file.to_excel(output_folder_path_plus_file, index=False)



if __name__ == "__main__":
    # #reading the excel file of features
    # original_features_file_path="D:/Research/WebCheck/WebCheck/server/output/infowars.com/features.xlsx"
    # scripts=read_script_names(original_features_file_path)
    # #labelling the scripts 
    # labelled_scripts=mark_scripts_bundled(scripts)
    # #print (labelled_scripts)
    # updating_features_excel(labelled_scripts,original_features_file_path)
    folder_path="/Research/WebCheck/WebCheck/server/output/"
    file_name="features.xlsx"
    notloaded_scripts_filename="/Research/WebCheck/WebCheck/not_loaded_scripts.xlsx"
    folder = os.listdir(folder_path)

    
    
    count=0
    for f in folder:
        count=count+1
        sub_folder_path=folder_path+f+"/"
        excel_file_path = os.path.join(sub_folder_path, file_name)
        if os.path.isfile(excel_file_path):
            #print("bundling_labelled: "+ f)
            scripts=read_script_names(excel_file_path)
            labelled_scripts=mark_scripts_bundled(scripts)
            updating_features_excel(excel_file_path,sub_folder_path,labelled_scripts)
        else:
            print("bundling_not_labelled: "+ f)
    print("total_folders_labelled:" + str(count))

    #creating a file for not accessed scripts for analysis
    notloaded_scripts_df = pd.DataFrame(notloaded_scripts, columns=['Script', 'Error'])
    if os.path.exists(notloaded_scripts_filename):
        os.remove(notloaded_scripts_filename)
    notloaded_scripts_df.to_excel(notloaded_scripts_filename, index=False)


        


        
    
 

