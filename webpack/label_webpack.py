import pandas as pd
import urllib.request

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
            print(error)
            lab_scripts.update({script:0})
    return lab_scripts

def updating_features_excel(lab_scripts,original_features_file_path):
    original_features_file = pd.read_excel(original_features_file_path)
    labelled_features_file = original_features_file.copy()
    labelled_features_file['is_bundled'] = None 
    for index, row in labelled_features_file.iterrows():
        labelled_features_file.loc[index, 'is_bundled'] = lab_scripts[row['script_name']]

    labelled_features_file.to_excel("labelled_features_file.xlsx", index=False)



if __name__ == "__main__":
    #reading the excel file of features
    original_features_file_path="D:/Research/WebCheck/WebCheck/server/output/infowars.com/features.xlsx"
    scripts=read_script_names(original_features_file_path)
    #labelling the scripts 
    labelled_scripts=mark_scripts_bundled(scripts)
    #print (labelled_scripts)
    updating_features_excel(labelled_scripts,original_features_file_path)
    
    ##################################################################################

    # req = urllib.request.Request(
    #     url='https://www.infowars.com/', 
    #     headers={'User-Agent': 'Mozilla/5.0'}
    # )

    # with urllib.request.urlopen(req) as response:
    #             html = response.read().decode("utf-8")
    #             print(html)
    #             is_bundled=check_webpack_keyword(html)
    #             print(is_bundled)

