import pandas as pd

file = "./학습자료/단답형/영어_단어.xlsx"
data = pd.read_excel(file)
data.to_excel(file,index=False)
data_중목항목제거 = data.drop_duplicates(['대답'], keep = False)
ans_list = list(data_중목항목제거["대답"])
for ans in ans_list:
    mask = data['대답'].isin([ans])
    data = data[~mask]
data_기출 = data.drop_duplicates(['대답'], keep = 'first')
data_기출.to_excel(file.replace(".xlsx","_기출.xlsx"),index=False)

data_유의어 = data.copy()
ans_list = list(data_기출["질문"])
for ans in ans_list:
    mask = data_유의어['질문'].isin([ans])
    data_유의어 = data_유의어[~mask]
data = data_유의어.copy()

ask_list1 = list(data_기출["질문"])
ans_list1 = list(data_기출["대답"])
cat_list1 = list(data_기출["구분"])
dic = {}
for i in range(len(ans_list1)):
    dic[ans_list1[i]] = ask_list1[i]

ask_list2 = list(data_유의어["질문"])
ans_list2 = list(data_유의어["대답"])
cat_list2 = list(data_유의어["구분"])

for i in range(len(ans_list2)):
    ask_list2[i] = f"{ask_list2[i]} : {ans_list2[i]}"
    ans_list2[i] = f"{dic[ans_list2[i]]}"
    
dic = {"질문":ask_list2,"대답":ans_list2,"구분":cat_list2}
df = pd.DataFrame(dic)
df.to_excel(file.replace(".xlsx","_유의어.xlsx"),index=False)