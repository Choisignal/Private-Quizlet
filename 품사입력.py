import pandas as pd
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import nltk
import googletrans
from tqdm import tqdm

file = "./학습자료/단답형/영어_기초단어.xlsx"
data = pd.read_excel(file)
data.to_excel(file.replace(".xlsx","_백업.xlsx"))
ask_list = list(data["질문"])
ans_list = list(data["대답"])
cat_list = list(data["구분"])
translator = googletrans.Translator()
명사 = ["NN","NNS"]
동사 = ["VBG","VBN","VB"]
부사 = ["RB"]
전치사 = ["IN"]
형용사 = ["JJS","JJ"]

for i in tqdm(range(len(ask_list))):
    ask = ask_list[i]
    ans = ans_list[i]
    cat = cat_list[i]
    ask = str(ask).strip()
    ans = str(ans).strip()
    cat = str(cat).strip()
    tagged_list = pos_tag(word_tokenize(ask))
    번역 = translator.translate(ask, dest='ko')
    번역 = 번역.text
    ans = f"({번역}) {ans}"
    품사 = tagged_list[0][1]

    if 품사 in 명사:
        cat = "명사"
    elif 품사 in 동사:
        cat = "동사"
    elif 품사 in 부사:
        cat = "부사"
    elif 품사 in 전치사:
        cat = "전치사"
    elif 품사 in 형용사:
        cat = "형용사"
    if ans[-1] =="다":
        cat = "동사"
    if ans[-1] in ["한","는","진","난","인"]:
        cat = "형용사"
    data.loc[i,"질문"] = ask
    data.loc[i,"대답"] = ans
    data.loc[i,"구분"] = cat
data.to_excel(file,index=False)