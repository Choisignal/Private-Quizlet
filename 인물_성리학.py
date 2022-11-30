import numpy as np
from pandas import read_excel
import pandas as pd
import random

df = read_excel("성리학_순서.xlsx")
자료 = df["내용"]
인물목록 = ["서경덕","조식","이언적","윤휴","박세당","한원진","권상하","성혼","이간","홍대용"]

for i in range(자료.size):
    설명들 = 자료[i].split("\n")
    for 설명 in 설명들:
        설명인물 = ""
        for 인물 in 인물목록:
            if 인물 in 설명:
                설명 = 설명.replace(인물,"[ _____ ]")
                설명인물 = 설명인물 + f", {인물}"
        설명인물 = 설명인물[2:]
        설명 += f"/{설명인물}"
        if 설명인물 != "":
            설명 = 설명.replace("[ _____ ]이 ","[ _____ ]이(가) ")
            설명 = 설명.replace("[ _____ ]가 ","[ _____ ]이(가) ")
            설명 = 설명.replace("[ _____ ]와 ","[ _____ ]와(과) ")
            설명 = 설명.replace("[ _____ ]과 ","[ _____ ]와(과) ")
            print(설명)