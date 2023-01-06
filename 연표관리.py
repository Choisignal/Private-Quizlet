
import numpy as np
from pandas import read_excel
import pandas as pd
import random
import os


def 엑셀파일구분하기(data_direct, filename):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    return_list = []

    try:
        구분목록 = list(set(data["구분"]))
        for 구분 in 구분목록:
            save_filename2 = f"{data_direct}{filename}_{구분}.xlsx"
            data2 = data[data["구분"] == 구분]
            data2.to_excel(save_filename2, index=False)
            return_list += [f"{filename}_{구분}"]
            print(save_filename2)
    except:
        print("구분 없음!")
    return return_list


def 연도_객관식(data_direct, filename):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    data["질문"] = data["사건"]
    data["대답"] = data["연도"]
    data_direct = data_direct.replace('연표', '단답형')
    new_file = f"{data_direct}{filename}.xlsx"
    data.to_excel(new_file)
    data = pd.read_excel(new_file)

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
        선지목록[선지번호[0] - 1] = f"{선지번호[0]}. {대답}"
        for j in [1, 2]:
            선지목록[선지번호[j] - 1] = f"{선지번호[j]}. {대답목록[j]}"
        출력_질문 = f"{질문}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
        출력_질문목록 += [출력_질문]
        출력_대답목록 += [f"{선지번호[0]}, {대답}"]

    save_data = pd.DataFrame({"질문": 출력_질문목록, "대답": 출력_대답목록})
    save_filename = data_direct + "객관식_" + filename + ".xlsx"
    print(save_filename)
    save_data.to_excel(save_filename, index=False)
    return


def 연표_통합(data_direct, file):
    파일명 = data_direct + file
    df = read_excel(f"{파일명}.xlsx")
    df = df.dropna()
    연도 = np.array(df["연도"])
    사건 = np.array(df["사건"])
    새연표 = {}
    for i in range(연도.size):
        try:
            해 = int(연도[i])
        except:
            해 = str(연도[i])
        if 해 not in 새연표.keys():
            새연표[해] = []
        새연표[해] = 새연표[해] + [사건[i]]

    연도 = list(새연표)
    사건목록 = []
    for 해 in 연도:
        저장사건 = ""
        for 사건 in 새연표[해]:
            저장사건 = 저장사건 + f"{사건}\n"
        저장사건 = 저장사건[0:-1]
        사건목록 = 사건목록 + [저장사건]

    새연표 = {"연도": 연도, "사건": 사건목록}
    새연표 = pd.DataFrame(새연표)
    새연표 = 새연표.drop_duplicates(["사건"])
    저장파일명 = f"{file}_연도별모음"
    새연표.to_excel(f"{data_direct+저장파일명}.xlsx", index=False)
    print(저장파일명)
    return 저장파일명  # filename+"_연도별모음"


def 순서배열(data_direct, 파일명):
    df = read_excel(f"{data_direct+파일명}.xlsx")

    엑셀용_리스트_문제 = []
    엑셀용_리스트_정답 = []
    엑셀용_리스트_해설 = []

    for i in range(100):
        리스트_문제 = []
        리스트_원래 = []
        리스트_연도 = []
        리스트_원래_연도용 = []
        리스트_연도_해설용 = []
        리스트_원래_해설용 = []
        for i in range(df["사건"].size):
            contents = df["사건"][i].split("\n")
            content = np.random.choice(contents, size=1)[0]
            리스트_문제 += [content]
            리스트_원래 += [content]
            리스트_원래_연도용 += [content]
            year = df["연도"][i]
            리스트_연도 += [year]

        random.shuffle(리스트_문제)
        리스트_문제 = 리스트_문제[0:3]
        #리스트_원래 = [x for i in 리스트_원래 for x in 리스트_문제 if i in x]
        리스트_원래2 = []
        for x in 리스트_원래:
            if x in 리스트_문제:
                리스트_원래2 += [x]
        리스트_원래 = 리스트_원래2

        for i in range(len(리스트_원래_연도용)):
            if 리스트_원래_연도용[i] in 리스트_원래:
                리스트_원래_해설용 += [리스트_원래_연도용[i]]
                리스트_연도_해설용 += [리스트_연도[i]]

        dic = {'label': ['ㄱ', 'ㄴ', 'ㄷ'],
               'original': 리스트_원래, 'new': 리스트_문제}
        new_df = pd.DataFrame(dic)

        정답 = ""
        문제 = ""
        for i in 리스트_원래:
            정답 += list(new_df["label"][new_df["new"] == i])[0] + ""

        for i in range(3):
            문제 += f"{new_df['label'][i]}. {리스트_문제[i]} \n"
        문제 = 문제[0:-2]
        정답 = 정답
        해설 = ""
        for i in range(3):
            해설 += f"{정답[i]}. {리스트_연도_해설용[i]} - {리스트_원래_해설용[i]}\n"
        엑셀용_리스트_문제 += [문제]
        엑셀용_리스트_정답 += [정답]
        엑셀용_리스트_해설 += [해설]

    저장용 = {'Text 1': 엑셀용_리스트_문제, 'Text 2': 엑셀용_리스트_정답, 'Text 3': 엑셀용_리스트_해설}
    저장용 = pd.DataFrame(저장용)
    final_filename = f"{data_direct+파일명}_문제.xlsx".replace("연표", "순서배열")
    print(final_filename)
    저장용.to_excel(final_filename, index=False)


def 순서배열_구분통합(data_direct, filename,객관식 = False):
    최종_통합파일명목록 = []
    최종저장파일명 = f"{data_direct}{filename}_문제_구분통합.xlsx".replace("연표", "순서배열")
    file_list = 엑셀파일구분하기(data_direct, filename)
    경로_통합파일명목록 = []
    for file in file_list:
        if 객관식 == True:
            연도_객관식(data_direct, file)
        파일명 = 연표_통합(data_direct, file)  # 사건을 연도별로 모아준다
        print(data_direct+파일명)
        경로_통합파일명목록 += [data_direct+파일명]
    for 경로_통합파일명 in 경로_통합파일명목록:
        df = read_excel(f"{경로_통합파일명}.xlsx")

        엑셀용_리스트_문제 = []
        엑셀용_리스트_정답 = []
        엑셀용_리스트_해설 = []

        for i in range(10):
            리스트_문제 = []
            리스트_원래 = []
            리스트_연도 = []
            리스트_원래_연도용 = []
            리스트_연도_해설용 = []
            리스트_원래_해설용 = []
            for i in range(df["사건"].size):
                contents = df["사건"][i].split("\n")
                content = np.random.choice(contents, size=1)[0]
                리스트_문제 += [content]
                리스트_원래 += [content]
                리스트_원래_연도용 += [content]
                year = df["연도"][i]
                리스트_연도 += [year]

            random.shuffle(리스트_문제)
            리스트_문제 = 리스트_문제[0:3]
            #리스트_원래 = [x for i in 리스트_원래 for x in 리스트_문제 if i in x]
            리스트_원래2 = []
            for x in 리스트_원래:
                if x in 리스트_문제:
                    리스트_원래2 += [x]
            리스트_원래 = 리스트_원래2

            for i in range(len(리스트_원래_연도용)):
                if 리스트_원래_연도용[i] in 리스트_원래:
                    리스트_원래_해설용 += [리스트_원래_연도용[i]]
                    리스트_연도_해설용 += [리스트_연도[i]]

            dic = {'label': ['ㄱ', 'ㄴ', 'ㄷ'],
                   'original': 리스트_원래, 'new': 리스트_문제}
            new_df = pd.DataFrame(dic)

            정답 = ""
            문제 = ""
            for i in 리스트_원래:
                정답 += list(new_df["label"][new_df["new"] == i])[0] + ""

            for i in range(3):
                문제 += f"{new_df['label'][i]}. {리스트_문제[i]} \n"
            문제 = 문제[0:-2]
            정답 = 정답
            해설 = ""
            for i in range(3):
                해설 += f"{정답[i]}. {리스트_연도_해설용[i]} - {리스트_원래_해설용[i]}\n"
            엑셀용_리스트_문제 += [문제]
            엑셀용_리스트_정답 += [정답]
            엑셀용_리스트_해설 += [해설]

        저장용 = {'Text 1': 엑셀용_리스트_문제, 'Text 2': 엑셀용_리스트_정답, 'Text 3': 엑셀용_리스트_해설}
        저장용 = pd.DataFrame(저장용)
        final_filename = f"{경로_통합파일명}_문제.xlsx".replace("연표", "순서배열")
        print(final_filename, "***************")
        저장용.to_excel(final_filename, index=False)
        최종_통합파일명목록 += [final_filename]
    save_df = pd.read_excel(최종_통합파일명목록[0])
    os.remove(최종_통합파일명목록[0])
    for 저장파일명 in 최종_통합파일명목록[1:]:
        df = pd.read_excel(저장파일명)
        save_df = pd.concat([save_df, df])
        os.remove(저장파일명)
    print(최종저장파일명)
    save_df.to_excel(최종저장파일명)


data_direct = "./학습자료/연표/"
filename = "무신정권"
if filename == "사건 순서":
    파일명 = 연표_통합(data_direct, filename)  # 사건을 연도별로 모아준다
    순서배열_구분통합(data_direct, filename,객관식 = False)  # ㄱㄴㄷㄹ 순서 배열 문제 만든다
elif filename =="조선":
    파일명 = 연표_통합(data_direct, filename)  # 사건을 연도별로 모아준다
    순서배열_구분통합(data_direct, filename,객관식 = True)  # ㄱㄴㄷㄹ 순서 배열 문제 만든다
elif filename =="국어 순서배열":
    순서배열_구분통합(data_direct, filename,객관식 = False)  # ㄱㄴㄷㄹ 순서 배열 문제 만든다
elif filename =="무신정권":
    순서배열_구분통합(data_direct, filename,객관식 = False)  # ㄱㄴㄷㄹ 순서 배열 문제 만든다
'''
연도_객관식(data_direct, file)  # 객관식 문제 만든다
try:
    순서배열(data_direct, 파일명)  # ㄱㄴㄷㄹ 순서 배열 문제 만든다
except:
    print(f"Error! 문제만들기 {파일명}")
try:
    연도_객관식(data_direct, 파일명)  # 객관식 문제 만든다
except:
    print(f"Error! 객관식 {파일명}")
'''
