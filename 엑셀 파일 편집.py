import pandas as pd

file = "./학습자료/단답형/한국사 종합.xlsx"
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
    '''
    length = len("③ 역할 : 농민의 불만과 개혁 요구를 반영하기 위해 정치·경제·사회 등")
    if ":" in ask:
        print(ask)
        ask_list2 = ask.split("\n")
        ask = ""
        for asks in ask_list2:
            if len(asks) >= length:
                asks = asks.replace(":",":\n")
            ans += asks + "\n"
        ask = ask[:-1]
    '''
    ask = ask.replace(".",",")
    if ask[-1] == ",":
        ask = ask[:-1]
    data.loc[i,"질문"] = ask
    data.loc[i,"대답"] = ans
    data.loc[i,"구분"] = cat

    if ":" in ask:
        print(ask)
data.to_excel(file)