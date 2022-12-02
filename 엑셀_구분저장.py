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
    filename = "단답형_영어_유의어"
    엑셀파일구분하기(data_direct, filename)
