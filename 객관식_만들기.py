import pandas as pd
import random
import googletrans
from tqdm import tqdm
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

def 객관식_만들기_한자어(파일명, data_direct, 단답형=True,설명=True,글자수=2,번역=False):
    translator = googletrans.Translator()
    data = pd.read_excel(data_direct+파일명+".xlsx")
    한자 = []
    한글 = []
    for i in tqdm(range(data["대답"].size)):
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        if len(질문.split('/')[0]) == 글자수:
            if 번역 ==True:
                한자번역 = translator.translate(질문, dest='en')
                한자번역 = 한자번역.text
                if len(한자번역.split(" ")) == 1 and 한자번역 != "no":
                    대답 = f"{대답}({한자번역})"
            한자 += [질문]
            한글 += [대답]
    data = pd.DataFrame({"질문":한자,"대답":한글})

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        질문 = 질문.replace(대답, "[   ]")

        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        if 설명 == True:
            선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {대답}"
            for j in [1, 2]:
                선지목록[선지번호[j] - 1] = f"{선지번호[j]}. {대답목록[j]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        else:
            선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
            for j in [1, 2]:
                선지목록[선지번호[j] - 1] = f"{선지번호[j]}. {str(대답목록[j]).split(',')[0]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

        출력_질문목록 += [출력_질문]
        출력_대답목록 += [f"{선지번호[0]}, {대답}"]

    save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
    if 번역==True:
        번역="_번역"
    else:
        번역 =""
    save_filename = data_direct + "객관식_" + 파일명 + f"{글자수}글자{번역}.xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)

def 객관식_만들기(파일명, data_direct, 단답형=True,설명=True):
    data = pd.read_excel(data_direct+파일명+".xlsx")

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        질문 = 질문.replace(대답,"[   ]")

        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        if 설명 == True:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답}"
            for j in [1, 2]:
                선지목록[선지번호[j]-1] = f"{선지번호[j]}. {대답목록[j]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        else:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
            for j in [1, 2]:
                선지목록[선지번호[j]-1] = f"{선지번호[j]}. {str(대답목록[j]).split(',')[0]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

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
if filename == "국어_복습":
    엑셀파일구분하기(data_direct, filename)
    객관식_만들기("국어_복습_속담", data_direct, 단답형=False)
    객관식_만들기("국어_복습_사자성어", data_direct, 단답형=False,설명=False)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=1,번역=False)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=2,번역=True)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=3,번역=True)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=4,번역=False)
    특정구분제거(data_direct, filename, 구분목록=["속담"])
elif filename == "영어_유의어":
    return_list1, return_list2 = 엑셀파일구분하기(data_direct, filename)
    객관식_만들기(filename, data_direct, 단답형=False,설명=True)
    for filename in return_list1:
        객관식_만들기(filename, data_direct, 단답형=False,설명=True)
elif filename == "영어_복습":
    엑셀파일구분하기(data_direct, filename)
    객관식_만들기("영어_복습_암기표현", data_direct, 단답형=False)
else:
    객관식_만들기(filename, data_direct, 단답형=False,설명=False)
