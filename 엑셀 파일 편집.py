import pandas as pd

file = "./학습자료/단답형/영어_복습.xlsx"
data = pd.read_excel(file)
data.to_excel(file.replace(".xlsx","_백업.xlsx"))
ask_list = list(data["질문"])
ans_list = list(data["대답"])
cat_list = list(data["구분"])

for i in range(len(ask_list)):
    ask = ask_list[i]
    ans = ans_list[i]
    cat = cat_list[i]
    ask = str(ask).strip()
    ans = str(ans).strip()
    cat = str(cat).strip()
    ask = ask.replace("\n","")
    ask = ask.replace(":","\n:")
    '''
    ask = ask.replace("보빙사 파견 1883)","보빙사 파견 1883 ")
    ask = ask.replace(" ,",",")
    ans = ans.replace(" ,",",")
    ans = ans.replace("갑신정변 1884","갑신정변")
    ans = ans.replace("임오군란 1882","임오군란")
    ans = ans.replace("  →","→ ")
    ans = ans.replace("경작)","경작)")

    if cat == "성리학 인물":
        cat = f"{cat} {len(ans.split(','))}명"
        print(cat)
    ''' 
    data.loc[i,"질문"] = ask
    data.loc[i,"대답"] = ans
    data.loc[i,"구분"] = cat

data.to_excel(file)