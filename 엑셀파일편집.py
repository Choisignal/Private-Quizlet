import pandas as pd
import re

def 수정(단어,이전,이후):
    if 이전 in 단어:
        print("수정 전 : ",단어)
        단어 = 단어.replace(이전,이후)
        print("수정 후 : ",단어,"\n")
    return 단어

def 확인(질문,대답,구분,검색):
    if 검색 in 질문:
        print(f"{질문.replace(검색,f'[{검색}]'):20} : {대답.replace(검색,f'[{검색}]'):20} : {구분:20}")
    elif 검색 in 대답:
        print(f"{질문.replace(검색,f'[{검색}]'):20} : {대답.replace(검색,f'[{검색}]'):20} : {구분:20}")

### 국어 한자
'''
        if 구분 == "국한":
            질문 = re.findall('\(([^)]+)', 대답)[0]
            대답 = re.sub('\([^)]+\)', '', 대답)
            구분 = f"한자 {len(질문)}글자"

        if 구분 == "한국":
            if "|" in 대답:
                질문 = re.sub('\([^)]+\)', '', 대답).split("|")[0]
                대답 = re.findall('\(([^)]+)', 대답)[0] + " |"+re.sub('\([^)]+\)', '', 대답).split("|")[1]
            else:
                질문 = re.sub('\([^)]+\)', '', 대답)
                대답 = re.findall('\(([^)]+)', 대답)[0]
            구분 = f"한자 {len(질문)}글자"
            #print(f"{질문}\n{대답}\n{구분}\n\n")
        if 구분 == "한자 2글자":
            if 대답[0] == 대답[1]:
                구분 = "한자 2글자 동음"
                print(f"{질문}\n{대답}\n{구분}\n\n")
'''
def 파일수정(file = "./학습자료/단답형/국어_복습_객관식.xlsx"):
    data = pd.read_excel(file)
    data.to_excel(file.replace(".xlsx","_백업.xlsx"),index=False)
    data.to_excel(file,index=False)
    data = pd.read_excel(file)
    질문_list = list(data["질문"])
    대답_list = list(data["대답"])
    구분_list = list(data["구분"])

    for i in range(len(질문_list)):
        질문 = 질문_list[i]
        대답 = 대답_list[i]
        구분 = 구분_list[i]
        질문 = str(질문).strip()
        대답 = str(대답).strip()
        구분 = str(구분).strip()

        질문 = re.sub('\([^)]+\)', '', 질문)
    #    print(f"{질문}\n{대답}\n{구분}\n\n")
        if 대답 == 'nan':
            if "[" in 질문:
                대답 = 질문[질문.find("]")+1:]
                질문 = 질문[0:질문.find("[")]
                대답 = re.sub('\([^)]+\)', '', 대답)
            elif "：" in 질문:
                대답 = 질문.split("：")[1]
                질문 = 질문.split("：")[0]
                대답 = re.sub('\([^)]+\)', '', 대답)
            else:
                print(f"{질문} | {대답} | {구분}")
                대답 = 질문.split(" ")[1]
                질문 = 질문.split(" ")[0]
                대답 = re.sub('\([^)]+\)', '', 대답)
            if "□ " in 질문:
                질문 = 질문[질문.find("□ ")+1:]

            질문 = str(질문).strip()
            대답 = str(대답).strip()
            구분 = str(구분).strip()
            print(f"{질문} | {대답} | {구분}")

        data.loc[i,"질문"] = 질문
        data.loc[i,"대답"] = 대답
        data.loc[i,"구분"] = 구분
    data.to_excel(file,index=False)

#파일수정(file = "./학습자료/단답형/국어_복습_객관식.xlsx")
#파일수정(file = "./학습자료/단답형/영어_복습.xlsx")
파일수정(file = "./학습자료/단답형/영단어 기초.xlsx")