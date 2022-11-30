from pandas import read_excel
import numpy as np
df = read_excel("책_저자_내용.xlsx")
책 = np.array(df["책"])
저자 = np.array(df["저자"])
내용 = np.array(df["내용"])

def 책_저자():
    책_저자있음 = 책[np.where(저자 != ".")]
    저자_저자있음 = 저자[np.where(저자 != ".")]

    for i in range(책_저자있음.size):
        print(f"{책_저자있음[i]}/{저자_저자있음[i]}")

def 책_내용():
    책_내용있음 = 책[np.where(내용 != ".")]
    내용_내용있음 = 내용[np.where(내용 != ".")]

    for i in range(책_내용있음.size):
        print(f"{책_내용있음[i]}/{내용_내용있음[i]}")

책_저자()