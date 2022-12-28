import pandas as pd

def 엑셀파일구분하기(data_direct, filename):
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    return_list = []
    try:
        날짜목록 = list(set(data["날짜"]))
        for 날짜 in 날짜목록:
            save_filename1 = f"{data_direct}{filename}_{날짜}.xlsx"
            data1 = data[data["날짜"] == 날짜]
            data1.to_excel(save_filename1, index=False)
            return_list += [f"{filename}_{날짜}"]
            print(save_filename1)
    except:
        print("날짜 없음!")

    try:
        구분목록 = list(set(data["구분"]))
        for 구분 in 구분목록:
            print(구분)
            save_filename2 = f"{data_direct}{filename}_{구분}.xlsx"
            data2 = data[data["구분"] == 구분]
            data2.to_excel(save_filename2, index=False)
            return_list += [f"{filename}_{구분}"]
            print(save_filename2)
    except:
        print("구분 없음!")
    return return_list

def 국어_복습():
    data_direct = "./학습자료/단답형/"
    filename = "국어_복습"
    단답형_목록 = ["단답형"]
    객관식_목록 = []
    #엑셀파일구분하기(data_direct, filename)
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    체언 = ["명사","대명사","수사","의존명사"]
    수식언 = ["관형사","부사"]
    관계언 = ["조사","격조사","접속조사","보조사"]
    독립언 = ["독립어"]
    용언 = ["동사","형용사"]
    # 품사 구분하기
    index_list = list(data[data["구분"]=="품사"]["구분"].index)
    for i in index_list:
        if data["대답"][i] in 체언+관계언+독립언:
            data.loc[i, '구분'] = "품사_체언_관계언_독립언"
        elif data["대답"][i] in 수식언+용언:
            data.loc[i, '구분'] = "품사_수식언_용언"
        else:
            data.loc[i, '구분'] = "품사_품사없음"

    구분목록 = list(set(data["구분"]))
    for 구분 in 구분목록:
        if 구분 not in 단답형_목록:
            if 구분 != "한자어":
                객관식_목록 += [구분]
            
    # 단답형 추출
    if len(단답형_목록) > 0:
        data_단답형1 = data[data["구분"] == 단답형_목록[0]]
        if len(단답형_목록) > 1:
            for 단답형 in 단답형_목록[1:]:
                data_단답형2 = data[data["구분"] == 단답형]
                data_단답형1 = pd.concat([data_단답형1,data_단답형2],ignore_index=True)
        try:
            data_단답형1.replace({'대답': {',': ' |'}}, inplace = True)
            data_단답형1_original = pd.read_excel(f"{data_direct}{filename}_단답형.xlsx")
            data_단답형1_original.replace({'대답': {',': ' |'}}, inplace = True)
            data_단답형1 = pd.concat([data_단답형1_original, data_단답형1], ignore_index=True)
            data_단답형1 = data_단답형1.drop_duplicates(['질문','대답'])
        except:
            print(f"기존 파일 없음 : {data_direct}{filename}_단답형.xlsx")
        data_단답형1.replace({'대답': {',': ' |'}}, inplace = True)
        data_단답형1.to_excel(f"{data_direct}{filename}_단답형.xlsx")

    if len(객관식_목록) > 0:

        # 객관식 추출
        data_객관식1 = data[data["구분"] == 객관식_목록[0]]
        if len(객관식_목록) > 1:
            for 객관식 in 객관식_목록[1:]:
                data_객관식2 = data[data["구분"] == 객관식]
                data_객관식1 = pd.concat([data_객관식1,data_객관식2],ignore_index=True)


        try:
            data_객관식1_original = pd.read_excel(f"{data_direct}{filename}_객관식.xlsx")
            data_객관식1 = pd.concat([data_객관식1_original, data_객관식1], ignore_index=True)
            data_객관식1 = data_객관식1.drop_duplicates(['질문','대답'])
        except:
            print(f"기존 파일 없음 : {data_direct}{filename}_객관식.xlsx")
        data_객관식1.to_excel(f"{data_direct}{filename}_객관식.xlsx")

    data_한자어1 = data[data["구분"] == "한자어"]

    try:
        data_한자어1_original = pd.read_excel(f"{data_direct}{filename}_한자어.xlsx")
        data_한자어1 = pd.concat([data_한자어1_original, data_한자어1], ignore_index=True)
        data_한자어1 = data_한자어1.drop_duplicates(['질문', '대답'])
    except:
        print(f"기존 파일 없음 : {data_direct}{filename}_한자어.xlsx")
    data_한자어1.to_excel(f"{data_direct}{filename}_한자어.xlsx")