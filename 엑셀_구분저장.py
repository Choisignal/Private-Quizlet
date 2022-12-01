import pandas as pd

data_direct = "./학습자료/"
filename = "단답형_국어기출암기"
data = pd.read_excel(f"{data_direct}{filename}.xlsx")

구분목록 = list(set(data["구분"]))
날짜목록 = list(set(data["날짜"]))

for 날짜 in 날짜목록:
    save_filename1 = f"{data_direct}{filename}_{날짜}.xlsx"
    data1 = data[data["날짜"]==날짜]
    data1.to_excel(save_filename1,index=False)
    print(save_filename1)

for 구분 in 구분목록:
    save_filename2 = f"{data_direct}{filename}_{구분}.xlsx"
    data2 = data[data["구분"]==구분]
    data2.to_excel(save_filename2,index=False)
    print(save_filename2)