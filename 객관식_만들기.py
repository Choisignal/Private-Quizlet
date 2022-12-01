import pandas as pd
import random
data_direct = "./학습자료/"
filename = "단답형_영어_유의어"
data = pd.read_excel(f"{data_direct}{filename}.xlsx")

출력_질문목록 = []
출력_대답목록 = []
for i in range(data["대답"].size):
    대답목록 = list(set(data["대답"]))
    질문 = data["질문"][i]
    대답 = data["대답"][i]
    대답목록.remove(대답)
    선지번호 = [1,2,3,4]
    random.shuffle(선지번호)
    random.shuffle(대답목록)
    선지목록 = [1,2,3,4]
    선지목록[선지번호[0]-1]=f"{선지번호[0]}. {대답}"
    for j in [1,2,3]:
        선지목록[선지번호[j]-1]=f"{선지번호[j]}. {대답목록[j]}"
    출력_질문 = f"{질문}\n{선지목록[0]}\n{선지목록[1]}\n{선지목록[2]}\n{선지목록[3]}"
    출력_질문목록 += [출력_질문]
    출력_대답목록 += [f"{선지번호[0]}, {대답}"]

save_data = pd.DataFrame({"질문":출력_질문목록,"대답":출력_대답목록})
save_filename = f"{data_direct}단답형_객관식_{filename.replace('단답형','')}.xlsx".replace("__","_")
save_data.to_excel(save_filename,index=False)

# 여기 아래는 단답형
출력_질문목록 += list(data["질문"])
출력_대답목록 += list(data["대답"])

save_data = pd.DataFrame({"질문":출력_질문목록,"대답":출력_대답목록})
save_filename = f"{data_direct}단답형_객관식+단답형_{filename.replace('단답형','')}.xlsx".replace("__","_")
save_data.to_excel(save_filename,index=False)