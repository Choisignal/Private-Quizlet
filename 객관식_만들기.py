import pandas as pd
import random
import googletrans
from tqdm import tqdm
import numpy as np
import os


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


def 객관식_만들기_한자어(파일명, data_direct, 단답형=True, 설명=True, 글자수=2, 번역=False):
    translator = googletrans.Translator()
    data = pd.read_excel(data_direct+파일명+".xlsx")
    한자 = []
    한글 = []
    for i in tqdm(range(data["대답"].size)):
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        if len(질문.split('/')[0]) == 글자수:
            if 번역 == True:
                한자번역 = translator.translate(질문, dest='en')
                한자번역 = 한자번역.text
                if len(한자번역.split(" ")) == 1 and 한자번역 != "no":
                    대답 = f"{대답}({한자번역})"
            한자 += [질문]
            한글 += [대답]
    data = pd.DataFrame({"질문": 한자, "대답": 한글})

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
    if 번역 == True:
        번역 = "_번역"
    else:
        번역 = ""
    save_filename = data_direct + "객관식_" + 파일명 + f"{글자수}글자{번역}.xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)


def 객관식_만들기(파일명, data_direct, 단답형=True, 설명=True):
    data = pd.read_excel(data_direct+파일명+".xlsx")

    출력_질문목록 = []
    출력_대답목록 = []
    for i in range(data["대답"].size):
        대답목록 = list(set(data["대답"]))
        질문 = data["질문"][i]
        대답 = data["대답"][i]
        try:
            질문 = 질문.replace(대답, "[   ]")
        except:
            pass
        대답목록.remove(대답)
        선지번호 = [1, 2, 3]
        random.shuffle(선지번호)
        random.shuffle(대답목록)
        선지목록 = [1, 2, 3]
        if 설명 == True:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답}"
            선지목록[선지번호[1]-1] = f"{선지번호[1]}. {대답목록[0]}"
            선지목록[선지번호[2]-1] = f"{선지번호[2]}. {대답목록[1]}"
            출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        else:
            선지목록[선지번호[0]-1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
            선지목록[선지번호[1]-1] = f"{선지번호[1]}. {str(대답목록[0]).split(',')[0]}"
            선지목록[선지번호[2]-1] = f"{선지번호[2]}. {str(대답목록[1]).split(',')[0]}"
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


def 객관식_만들기_구분통합(filename, data_direct, 단답형=True, 설명=True):
    최종저장파일명 = data_direct + "객관식_" + filename + "_구분통합.xlsx"
    return_list1, 파일명_목록 = 엑셀파일구분하기(data_direct, filename)
    for filename in return_list1:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    저장파일명목록 = []
    for 파일명 in 파일명_목록:
        data = pd.read_excel(data_direct+파일명+".xlsx")
        os.remove(data_direct+파일명+".xlsx")
        출력_질문목록 = []
        출력_대답목록 = []
        for i in range(data["대답"].size):
            대답목록 = list(set(data["대답"]))
            질문 = data["질문"][i]
            대답 = data["대답"][i]
            try:
                질문 = 질문.replace(대답, "[   ]")
            except:
                pass

            if len(대답목록) > 2:
                대답목록.remove(대답)
                선지번호 = [1, 2, 3]
                random.shuffle(선지번호)
                random.shuffle(대답목록)
                선지목록 = [1, 2, 3]
                대답목록 = [대답] + 대답목록
                if 설명 == True:
                    선지목록[선지번호[0]-1] = f"{선지번호[0]}. {대답목록[0]}"
                    선지목록[선지번호[1]-1] = f"{선지번호[1]}. {대답목록[1]}"
                    선지목록[선지번호[2]-1] = f"{선지번호[2]}. {대답목록[2]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                else:
                    선지목록[선지번호[0] -
                         1] = f"{선지번호[0]}. {str(대답목록[0]).split(',')[0]}"
                    선지목록[선지번호[1] -
                         1] = f"{선지번호[1]}. {str(대답목록[1]).split(',')[0]}"
                    선지목록[선지번호[2] -
                         1] = f"{선지번호[2]}. {str(대답목록[2]).split(',')[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"

                출력_질문목록 += [출력_질문]
                출력_대답목록 += [f"{선지번호[0]}, {대답}"]
            elif len(대답목록) == 2:
                선지번호 = [1, 2]
                선지목록 = [1, 2]
                대답목록.remove(대답)
                if 설명 == True:
                    선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {대답}"
                    선지목록[선지번호[1] - 1] = f"{선지번호[1]}. {대답목록[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"
                else:
                    선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {str(대답).split(',')[0]}"
                    선지목록[선지번호[1] -
                         1] = f"{선지번호[1]}. {str(대답목록[0]).split(',')[0]}"
                    출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"

                출력_질문목록 += [출력_질문]
                출력_대답목록 += [f"{선지번호[0]}, {대답}"]

        save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
        save_filename = data_direct+"객관식_"+파일명+".xlsx"

        # 여기 아래는 단답형
        if 단답형 == True:
            출력_질문목록 = list(data["질문"]) + 출력_질문목록
            출력_대답목록 = list(data["대답"]) + 출력_대답목록

            save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
            save_filename = data_direct+"객관식+단답형_"+파일명+".xlsx"
            print(save_filename)
            save_data.to_excel(save_filename, index=False)
        else:
            print(save_filename)
            save_data.to_excel(save_filename, index=False)
        저장파일명목록 += [save_filename]
    save_df = pd.read_excel(저장파일명목록[0])
    os.remove(저장파일명목록[0])
    for 저장파일명 in 저장파일명목록[1:]:
        df = pd.read_excel(저장파일명)
        save_df = pd.concat([save_df, df])
        os.remove(저장파일명)
    print(최종저장파일명)
    save_df.to_excel(최종저장파일명)


def 특정구분제거(data_direct, filename, 구분목록):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    제거요소 = ""
    for 구분 in 구분목록:
        data = data[data["구분"] != 구분]
        제거요소 += f"{구분}_"
    save_filename = f"{data_direct}{filename}_{제거요소[:-1]}제거.xlsx"
    data.to_excel(save_filename, index=False)
    print(save_filename)


def OX퀴즈만들기(data_direct, filename):
    translator = googletrans.Translator()
    text1 = []
    text2 = []
    text3 = []

    df = pd.read_excel(f"{data_direct}{filename}.xlsx")
    df = df.drop_duplicates(['질문'])
    df = df.reset_index()
    kor = df["대답"]
    chi = df["질문"]
    pri = df["구분"]
    two_list = []
    for i in range(len(chi)):
        if len(chi[i]) == 2:
            two_list += [i]

    kor = kor[two_list]
    chi = chi[two_list]
    pri = pri[two_list]
    kor = np.array(kor)
    chi = np.array(chi)
    pri = np.array(pri)
    딕셔너리 = {}
    for i in range(kor.size):
        단어 = str(kor[i])
        if 단어 not in 딕셔너리.keys():
            딕셔너리[단어] = ""
        if chi[i] not in 딕셔너리[단어]:
            딕셔너리[단어] = 딕셔너리[단어] + chi[i] + ", "

    print_list = []
    for i in range(kor.size):
        pri1 = str(pri[i])
        if pri1 == "한자어":
            kor1 = str(kor[i])
            chi1 = str(chi[i])
            trans = translator.translate(chi1, dest='en')
            trans = trans.text
            if len(trans.split(" ")) == 1:
                trans = f"({trans})".lower()
            else:
                trans = ""
            for j in range(kor.size):
                kor2 = str(kor[j])
                chi2 = str(chi[j])
                if kor1 == kor2 and chi1 == chi2:
                    print_word = f"'{kor1}{trans}' = {chi2}?/o , ㅇ , {chi2}"
                    if print_word not in print_list:
                        print(print_word)
                        text1 += [f"'{kor1}{trans}' = {chi2}?"]
                        text2 += [f"ㅇ"]
                        text3 += [f"{chi2}"]
                    print_list += [print_word]
                elif kor1[0] == kor2[0] and chi1[0] != chi2[0]:
                    chi3 = chi2[0]+chi1[1]
                    print_word = f"'{kor1}{trans}' = {chi3}?/x , ㄴ, {chi1}"
                    if print_word not in print_list:
                        print(print_word)
                        text1 += [f"'{kor1}{trans}' = {chi3}?"]
                        text2 += [f"ㄴ"]
                        text3 += [f"{chi1}"]
                    print_list += [print_word]

    print_list = []
    for i in range(kor.size):
        pri1 = str(pri[i])
        if pri1 == "o":
            kor1 = str(kor[i])
            chi1 = str(chi[i])
            trans = translator.translate(chi1, dest='en')
            trans = trans.text
            if len(trans.split(" ")) == 1:
                trans = f"({trans})".lower()
            else:
                trans = ""
            for j in range(kor.size):
                kor2 = str(kor[j])
                chi2 = str(chi[j])
                if kor1 == kor2 and chi1 == chi2:
                    pass
                elif kor1[1] == kor2[1] and chi1[1] != chi2[1]:
                    chi3 = chi1[0]+chi2[1]
                    print_word = f"'{kor1}{trans}' = {chi3}?/x , ㄴ, {chi1}"
                    if print_word not in print_list:
                        print(print_word)
                        text1 += [f"'{kor1}{trans}' = {chi3}?"]
                        text2 += [f"ㄴ"]
                        text3 += [f"{chi1}"]
                    print_list += [print_word]

    data = {"Text 1": text1, "Text 2": text2, "Text 3": text3}
    data = pd.DataFrame(data)
    data.to_excel(
        f"{data_direct}{filename}.xlsx".replace("단답형", "O X 퀴즈"))


data_direct = "./학습자료/단답형/"
filename = "영어_단어"
if filename == "국어_복습":
    엑셀파일구분하기(data_direct, filename)
    객관식_만들기("국어_복습_속담", data_direct, 단답형=False)
    객관식_만들기("국어_복습_의미", data_direct, 단답형=False, 설명=False)
    특정구분제거(data_direct, filename, 구분목록=["속담"])
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=4,번역=False)
    '''
    OX퀴즈만들기(data_direct, "국어_복습_한자어")
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=1,번역=False)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=2,번역=True)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=3,번역=False)
    객관식_만들기_한자어("국어_복습_한자어", data_direct, 단답형=False,설명=False,글자수=4,번역=False)
    '''
elif filename == "국어_암기자료":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "국어_57항":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "영어_단어":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
    '''
    return_list1, return_list2 = 엑셀파일구분하기(data_direct, filename)
    객관식_만들기(filename, data_direct, 단답형=False,설명=True)
    for filename in return_list1:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    for filename in return_list2:
        객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    day_list = []
    for day in return_list1:
        day_list += [int(day.split("Day")[-1])]
    filename = f"영어_단어_Day{str(max(day_list)).zfill(2)}"
    객관식_만들기(filename, data_direct, 단답형=False,설명=True)
    try:
        객관식_만들기(filename+"_유의어", data_direct, 단답형=False,설명=True)
    except:
        print("유의어")
    try:
        객관식_만들기(filename+"_관용어", data_direct, 단답형=False,설명=True)
    except:
        print("관용어")
    '''
elif filename == "영어_복습":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "삼국통합":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "삼국통합":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "불교":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "한국사_대조":
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
elif filename == "한자의지혜":
    #OX퀴즈만들기(data_direct, "한자의지혜")
    객관식_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=1,번역=False)
    객관식_만들기_한자어(filename, data_direct, 단답형=False, 설명=False, 글자수=2, 번역=True)
    객관식_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=3,번역=False)
    객관식_만들기_한자어(filename, data_direct, 단답형=False,설명=False,글자수=4,번역=False)
else:
    객관식_만들기(filename, data_direct, 단답형=False, 설명=True)
    객관식_만들기_구분통합(filename, data_direct, 단답형=False, 설명=True)
