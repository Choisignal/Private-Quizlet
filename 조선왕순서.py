import numpy as np
from numpy import random
#data1 = np.array(["태조","혜종","정종1","광종","경종","성종","목종","현종","덕종","정종2","문종","순종","선종","헌종","숙종","예종","인종","의종","명종","고종","원종","충렬왕","충선왕","충숙왕","충혜왕","충목왕","충정왕","공민왕","우왕","창왕","공양왕"])
data1 = np.array(["태조","정종","태종","세종","문종","단종","세조","예종","성종","연산군","중종","인종","명종","선조","광해군","인조","효종","현종","숙종","경종","영조","정조","순조","헌종","철종"])
data2 = np.array(range(len(data1)-2))

question = ""
answer = ""
count = 1
for name in data1:
    question = question + f"{name} ({count}) ,"
    count += 1
question = question[0:-1]
print(question)

for i in range(100):
    index = random.choice(data2, size=1, replace=False)
    names = [data1[index][0],data1[index+1][0],data1[index+2][0]]

    question = f"{names[0]} - _____ - {names[2]}"
    answer = f"{names[1]}"

    print(f"{question} / {answer}")