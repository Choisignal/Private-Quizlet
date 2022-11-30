from pandas import read_excel

df = read_excel("구전치사.xlsx")
engs = df["eng"]
kors = df["kor"]

for i in range(engs.size):
    eng = engs[i]
    eng = eng.replace("["," [ ")
    eng = eng.replace("]"," ] ")
    eng = eng.split(" ")
    kor = kors[i]
    question = ""
    answer = ""
    for j in range(len(eng)):
        if eng[j] in ["at", "out","of", "in","with","as","on","to","for","by"]:
            answer += f", {eng[j]}"
            eng[j] = "___"
        question += f"{eng[j]} "
    question = question[:-1]
    answer = answer[2:]
    print(f"{question} ({kor}) / {answer}")

print("\n=======================================\n")
for i in range(engs.size):
    eng = engs[i]
    kor = kors[i]
    print(f"{eng} / {kor}")