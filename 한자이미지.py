import glob
import numpy as np
from pandas import read_excel
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import hanja
from hanja import hangul
import re
import pandas as pd
import googletrans
import pandas as pd
import os


def make_image(chi, png_filename):
    W = 1920
    H = 1080
    bg_color = 'rgb(0, 0, 0)'
    if len(chi) == 1:
        size_chi = 500
        x_text = 750
        y_text = 250
    elif len(chi) == 2:
        size_chi = 500
        x_text = 500
        y_text = 250
    elif len(chi) == 3:
        size_chi = 450
        x_text = 300
        y_text = 250
    elif len(chi) == 4:
        size_chi = 400
        x_text = 200
        y_text = 300
    else:
        size_chi = 350
        x_text = 250
        y_text = 350

    font = ImageFont.truetype('NanumBarunGothic.ttf', size=size_chi)

    image = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(image)

    lines = wrap(f"{chi}", width=20)

    for line in lines:
        width, height = font.getsize(line)
        draw.text((x_text, y_text), line, font=font, fill='rgb(255, 255, 255)')
        y_text += height

    image.save(png_filename)


def makeImg(start_num):
    df = read_excel("한자이미지.xlsx")
    chis = df["chi"]
    kors = df["kor"]
    for i in range(len(chis)):
        chi = chis[i]
        kor = kors[i].split(",")[0]
        make_image(chi.replace(
            " ", ""), f"./한자이미지/{str(start_num + i).zfill(2)}_{str(kor).replace('/','')}.png")


def translate():
    df = read_excel("한자이미지.xlsx")
    chis = df["chi"]
    kors = df["kor"]
    regex = '\([^)]+\)'

    print_list = []

    for i in range(len(chis)):
        chi = chis[i]
        chi_trans = hanja.translate(chi, 'substitution')
        kor = kors[i]
        if type(kor) == type("a"):
            kor = re.sub(regex, '', kor)
            kor = kor.replace("\n", "")
            kor = kor.replace("a.", "")
            kor = kor.replace("b.", "")
        else:
            kor = ""
        for j in chi_trans:
            if hangul.is_hangul(j) == False:
                if kor != "":
                    print(f"{chi_trans} / {kor}")
                else:
                    print(f"{chi_trans}")
                chi_trans = input("위 한자를 번역해주세요! : ")
                print("-----------")
                break
        if kor != "":
            kor = f"{chi_trans.replace(' ','')}, {kor}"
        else:
            kor = f"{chi_trans.replace(' ','')}"
        print_list += [f"{kor} / {chi}"]

    for i in print_list:
        print(i)


def 한자의지혜():
    df = read_excel("한자의지혜.xlsx")
    datas = df["data"]
    for data in datas:
        data = data.split(" ")
        chi = data[0]
        kor = ""
        kors = data[1:]
        for korp in kors:
            kor += korp + " "
        kor = kor[0:-1]
        print(f"{kor}/{chi}".replace(",", " ,"))


def 한자_동음어(복습=1):
    복습 = f"복습{복습}"
    df = read_excel("한자의지혜_문제.xlsx")
    df = df.drop_duplicates(['chi'])
    df = df.reset_index()
    kor = df["kor"]
    chi = df["chi"]
    pri = df["pri"]
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
    for i in range(chi.size):
        단어 = str(chi[i])
        if 단어 not in 딕셔너리.keys():
            딕셔너리[단어] = ""
        if kor[i] not in 딕셔너리[단어]:
            딕셔너리[단어] = 딕셔너리[단어] + kor[i] + ", "

    print_list = []
    for i in range(chi.size):
        pri1 = str(pri[i])
        if pri1 == 복습:
            chi1 = str(chi[i])
            kor1 = str(kor[i])
            for j in range(chi.size):
                chi2 = str(chi[j])
                kor2 = str(kor[j])
                if chi1 == chi2 and kor1 == kor2:
                    print_word = f"'{chi1}' = {kor2}?/o , ㅇ , {kor2}"
                    if print_word not in print_list:
                        print(print_word)
                    print_list += [print_word]
                elif chi1[0] == chi2[0] and kor1[0] != kor2[0]:
                    kor3 = kor2[0] + kor1[1]
                    print_word = f"'{chi1}' = {kor3}?/x , ㄴ , {딕셔너리[chi1][0:-2]}"
                    if print_word not in print_list:
                        print(print_word)
                    print_list += [print_word]
                elif chi1[0] == chi2[0] and chi1[1] != chi2[1] and kor1 != kor2:
                    print_word = f"'{chi1}' = {kor2}?/x , ㄴ, {딕셔너리[chi1][0:-2]}"
                    if print_word not in print_list:
                        print(print_word)
                    print_list += [print_word]

    print_list = []
    for i in range(chi.size):
        pri1 = str(pri[i])
        if pri1 == "o":
            chi1 = str(chi[i])
            kor1 = str(kor[i])
            for j in range(chi.size):
                chi2 = str(chi[j])
                kor2 = str(kor[j])
                if chi1 == chi2 and kor1 == kor2:
                    pass
                elif chi1[1] == chi2[1] and kor1[1] != kor2[1]:
                    kor3 = kor1[0] + kor2[1]
                    print_word = f"'{chi1}' = {kor3}?/x , ㄴ , {딕셔너리[chi1][0:-2]}"
                    if print_word not in print_list:
                        print(print_word)
                    print_list += [print_word]
                elif chi1[1] == chi2[1] and chi1[0] != chi2[0] and kor1 != kor2:
                    print_word = f"'{chi1}' = {kor2}?/x , ㄴ , {딕셔너리[chi1][0:-2]}"
                    if print_word not in print_list:
                        print(print_word)
                    print_list += [print_word]


def 한글_동음어(복습=1):
    translator = googletrans.Translator()
    text1 = []
    text2 = []
    text3 = []

    복습 = f"복습{복습}"
    df = read_excel("한자의지혜_문제.xlsx")
    df = df.drop_duplicates(['chi'])
    df = df.reset_index()
    kor = df["kor"]
    chi = df["chi"]
    pri = df["pri"]
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
        if pri1 == 복습:
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
        f"./학습자료/O X 퀴즈_한자의지혜_복습{복습[2:]}.xlsx")


def 한자의지혜통합(file_path, file_format, 복습목록, save_format, columns=None):
    merge_df = pd.DataFrame()
    save_path = f"./학습자료/O X 퀴즈_한자의지혜_복습_통합_{min(복습목록)}_{max(복습목록)}.xlsx"
    file_list = []
    for 복습 in 복습목록:
        file_list += [f"{file_path}/{file}" for file in os.listdir(
            file_path) if f"{복습}{file_format}" in file]
    for file in file_list:
        if file_format == ".xlsx":
            file_df = pd.read_excel(file)
        else:
            file_df = pd.read_csv(file)

        if columns is None:
            columns = file_df.columns

        temp_df = pd.DataFrame(file_df, columns=columns)

        merge_df = merge_df.append(temp_df)

    if save_format == ".xlsx":
        merge_df.to_excel(save_path, index=False)
    else:
        merge_df.to_csv(save_path, index=False)


def 한자의지혜_복습자료만들기():
    '''
    복습목록 = []
    check = True
    while check == True:
        복습 = input("정수 입력 (0 = 종료): ")
        if 복습 == "0":
            check = False
        else:
            try:
                복습목록 += [int(복습)]
                복습목록.sort()
                print(f"복습목록 : {복습목록}")
            except:
                pass
    '''
    복습목록 = [36]
    for 복습 in 복습목록:
        # 한자_동음어(복습=복습)
        한글_동음어(복습=복습)
    '''

    한자의지혜통합(file_path="./학습자료/", file_format=".xlsx",
            복습목록=복습목록, save_format=".xlsx")
    '''


if __name__ == '__main__':
    # 한자의지혜()
    # translate()
    # makeImg(start_num=449)
    # 한글_동음어()
    # makeImg(start_num=449)
    한자의지혜_복습자료만들기()
