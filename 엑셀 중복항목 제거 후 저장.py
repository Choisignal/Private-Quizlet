import pandas as pd

direct = "./학습자료/단답형/"
filename = "한자의지혜"

file = f"{direct}{filename}.xlsx"
savefile = f"{direct}{filename}_중복제거.xlsx"
data = pd.read_excel(file)
data = data.drop_duplicates(["질문"])
data.to_excel(savefile)