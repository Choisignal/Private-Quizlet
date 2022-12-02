import pandas as pd
import random


def 엑셀파일구분하기(data_direct, filename):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    return_list1 = []
    return_list2 = []
    try:
        날짜목록 = list(set(data["날짜"]))
        for 날짜 in 날짜목록:
            save_filename1 = f"{data_direct}{filename}_{날짜}.xlsx"
            data1 = data[data["날짜"] == 날짜]
            data1.to_excel(save_filename1, index=False)
            return_list1 += [f"{filename}_{날짜}"]
            print(save_filename1)
    except:
        print("날짜 없음!")

    try:
        구분목록 = list(set(data["구분"]))
        for 구분 in 구분목록:
            save_filename2 = f"{data_direct}{filename}_{구분}.xlsx"
            data2 = data[data["구분"] == 구분]
            data2.to_excel(save_filename2, index=False)
            return_list2 += [f"{filename}_{구분}"]
            print(save_filename2)
    except:
        print("구분 없음!")
    return return_list1, return_list2


def 객관식_만들기(파일명, data_direct, 단답형=True):
    data = pd.read_excel(data_direct+파일명+".xlsx")

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답}"
        for j in [1, 2]:
            선지목록[선지번호[j]-1] = f"{선지번호[j]}. {대답목록[j]}"
        출력_질문 = f"{질문}\n{선지목록[0]}\n{선지목록[1]}\n{선지목록[2]}"
        출력_질문목록 += [출력_질문]
        출력_대답목록 += [f"{선지번호[0]}, {대답}"]

    save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
    save_filename = data_direct+"객관식_"+파일명+".xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)

    # 여기 아래는 단답형
    if 단답형 == True:
        출력_질문목록 = list(data["질문"]) + 출력_질문목록
        출력_대답목록 = list(data["대답"]) + 출력_대답목록

        save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
        save_filename = data_direct+"객관식+단답형_"+파일명+".xlsx"
        print(save_filename)
        save_data.to_excel(save_filename, index=False)


def 특정구분제거(data_direct, filename, 구분목록):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    제거요소 = ""
    for 구분 in 구분목록:
        data = data[data["구분"] != 구분]
        제거요소 += f"{구분}_"
    save_filename = f"{data_direct}{filename}_{제거요소[:-1]}제거.xlsx"
    data.to_excel(save_filename, index=False)
    print(save_filename)


data_direct = "./학습자료/단답형/"
filename = "영어_유의어"
if filename == "국어_기출의지혜":
    엑셀파일구분하기(data_direct, filename)
    객관식_만들기("국어_기출의지혜_속담", data_direct, 단답형=False)
    특정구분제거(data_direct, filename, 구분목록=["속담"])

if filename == "영어_유의어":
    return_list1, return_list2 = 엑셀파일구분하기(data_direct, filename)
    for filename in return_list1:
        객관식_만들기(filename, data_direct, 단답형=True)
