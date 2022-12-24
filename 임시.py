from pathlib import Path
from pandas import read_excel, DataFrame
from datetime import datetime


def 학습시간(모드, study_hour=0):
    now = datetime.now()
    day = now.strftime("%Y%m%d")
    my_file = Path("학습시간.xlsx")
    if my_file.is_file():
        df = read_excel("학습시간.xlsx")
    else:
        df = DataFrame({'날짜': [day], '학습시간': [0]})
        df.to_excel("학습시간.xlsx", index=False)

    if 모드 == '읽기':
        날짜목록 = list(df['날짜'])
        if int(day) in 날짜목록:
            study_hour = int(df[df['날짜'] == int(day)]['학습시간'])
        else:
            df['날짜'][-1] = day
            df['학습시간'][-1] = 0
            study_hour = 0
    elif 모드 == '쓰기':
        날짜목록 = list(df['날짜'])
        last_study_time = int(df[df['날짜'] == int(day)]['학습시간'])
        if int(day) in 날짜목록:
            df.loc[df['날짜'] == int(day), '학습시간'] = last_study_time + study_hour
        else:
            df['날짜'][-1] = day
            df['학습시간'][-1] = study_hour
        df.to_excel("학습시간.xlsx", index=False)
        study_hour = int(df[df['날짜'] == int(day)]['학습시간'])
    return study_hour


study_hour = 학습시간(모드="읽기", study_hour=0)
print(type(study_hour), study_hour)
study_hour = 학습시간(모드="쓰기", study_hour=1)
print(type(study_hour), study_hour)
