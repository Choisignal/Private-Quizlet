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


if __name__ == "__main__":
    data_direct = "./학습자료/단답형/"
    filename = "국어_복습"
    단답형_목록 = ["발음","고쳐쓰기"]
    객관식_목록 = []
    #엑셀파일구분하기(data_direct, filename)
    data = pd.read_excel(f"{data_direct}{filename}.xlsx")
    구분목록 = list(set(data["구분"]))
    for 구분 in 구분목록:
        if 구분 not in 단답형_목록:
            객관식_목록 += [구분]
    # 단답형 추출
    if len(단답형_목록) > 0:
        data_단답형1 = data[data["구분"] == 단답형_목록[0]]
        if len(단답형_목록) > 1:
            for 단답형 in 단답형_목록[1:]:
                data_단답형2 = data[data["구분"] == 단답형]
                data_단답형1 = pd.concat([data_단답형1,data_단답형2],ignore_index=True)
        data_단답형1.to_excel(f"{data_direct}{filename}_단답형.xlsx")

    if len(객관식_목록) > 0:
        # 객관식 추출
        data_객관식1 = data[data["구분"] == 객관식_목록[0]]
        if len(객관식_목록) > 1:
            for 객관식 in 객관식_목록[1:]:
                data_객관식2 = data[data["구분"] == 객관식]
                data_객관식1 = pd.concat([data_객관식1,data_객관식2],ignore_index=True)
        data_객관식1.to_excel(f"{data_direct}{filename}_객관식.xlsx")