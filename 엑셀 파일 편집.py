import pandas as pd

def 수정(단어,이전,이후):
    if 이전 in 단어:
        print("수정 전 : ",단어)
        단어 = 단어.replace(이전,이후)
        print("수정 후 : ",단어,"\n")
    return 단어
    
def 파일수정(file = "./학습자료/단답형/국어_복습_객관식.xlsx"):
    data = pd.read_excel(file)
    data.to_excel(file.replace(".xlsx","_백업.xlsx"),index=False)
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

        질문 = 수정(질문,"to부정사/동사원형",
                "to부정사/동사원형")
        data.loc[i,"질문"] = 질문
        data.loc[i,"대답"] = 대답
        data.loc[i,"구분"] = 구분
    data.to_excel(file,index=False)

파일수정(file = "./학습자료/단답형/국어_복습_객관식.xlsx")
파일수정(file = "./학습자료/단답형/국어_복습.xlsx")