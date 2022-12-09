from datetime import datetime
from pandas import read_excel, DataFrame
from numpy import round
from tkinter import END, Tk, Button, Label, Radiobutton, Text, StringVar, Entry, filedialog, IntVar, E, W, N, S, Menu
from os.path import exists, isfile, basename
from os import makedirs
import random
import re
import shutil
try:
    import winsound as sd

    def beepsound():
        fr = 1000    # range : 37 ~ 32767
        du = 1000     # 1000 ms ==1second
        sd.Beep(fr, du)  # winsound.Beep(frequency, duration)
except:
    pass


def make_list(right_answer):
    right_answer = re.sub('\([^)]+\)','',right_answer)
    try:
        right_answer_list = right_answer.split(",")
    except:
        right_answer_list = [str(right_answer)]

    lang = button8.cget("text")
    if lang == "연표":
        right_answer_list += [str(right_answer)[2:]]
    return right_answer_list


def createDirectory(directory):
    try:
        if not exists(directory):
            makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def tkinter_eng_word_test(data_direct, filename):
    try:
        text.delete("1.0", "end")
        button2.configure(state="disable")
        button3.configure(state="disable")
        button4.configure(state="disable")
        button5.configure(state="disable")
        button6.configure(state="disable")
        button7.configure(state="disable")
        button8.configure(state="disable")
        entry.delete(0, END)
        from time import sleep
        df = read_excel("{0}{1}.xlsx".format(data_direct, filename))
        df = df.drop_duplicates()
        lang = button8.cget("text")
        filename = lang.replace(" ", "_")+"_"+filename
        df = df.sample(frac=1).reset_index(drop=True)  # 데이터 프레임의 행을 랜덤으로 뒤섞는다.
        wrong_log = "{0}오답노트/오답노트_테스트_{1}.xlsx".format(
            data_direct, filename)
        wrong_log_direct = "{0}오답노트/".format(data_direct)
        createDirectory(wrong_log_direct)
        num_total = df.shape[0]
        count_right = 0
        count = 0
        stop_check = False
        while stop_check == False:
            range_list = list(range(num_total))
            random.shuffle(range_list)
            num_test = button_test.cget("text")
            qusetion_num = int(num_test.split("문항")[0])
            if qusetion_num > num_total:
                qusetion_num = num_total
            # print(qusetion_num)
            for i in range_list[0:qusetion_num]:
                count += 1
                if lang == "연표":
                    ask = df["사건"][i]
                    right_answer = df["연도"][i]
                elif lang == "단답형":
                    ask = df["질문"][i]
                    right_answer = df["대답"][i]
                    try:
                        if ask != right_answer:
                            ask = ask.replace(right_answer, "[   ]")
                    except:
                        pass
                else:
                    ask = df["Text 1"][i]
                    right_answer = df["Text 2"][i]

                ############################
                ############################
                ############################
                window.update()
                answer = ""
                for i in range(400):
                    text.insert(
                        "1.0", " ( {0}/{1} : {2})\n".format(count, qusetion_num, int(0.05*(399-i))))
                    text.insert("1.0", ask, "emphasis")
                    window.update()
                    sleep(0.05)
                    text.delete("1.0", END)
                    #text.delete("1.0", "2.0")
                    answer = entry.get()
                    if answer == "s.":
                        answer = "ㄴ."
                    elif answer == "d.":
                        answer = "ㅇ."
                    if len(answer) != 0 and answer[-1] == ".":
                        answer = answer[0:-1]
                        break
                if len(answer) != 0 and (answer.lower() == "stop" or answer == "종료" or answer == "끝" or answer == "중지"):
                    entry.delete(0, END)
                    stop_check = True
                    break
                text.insert("1.0", f"{'%-15s' % ask} -> {answer}\n")
                window.update()
                ############################
                ############################
                ############################
                right_answer2 = str(right_answer)
                right_answer = str(right_answer).replace(" ", "")
                answer2 = str(answer)
                answer = str(answer).replace(" ", "")
                if lang == "연표" and len(answer) == 2 and len(right_answer) > 2:
                    answer = right_answer[:2]+answer
                right_answer_list = make_list(right_answer)

                if answer != "" and answer in right_answer_list:
                    count_right += 1

                else:
                    # Answer - wrong
                    now = datetime.now()
                    day = now.strftime("%Y%m%d")
                    hour = now.strftime("%H")
                    if isfile(wrong_log):
                        df_wrong = read_excel(wrong_log)
                    else:
                        df_wrong = DataFrame(
                            {'질문': [], '대답': [], '정답': [], '날짜': [], '시간': []})
                    df_wrong.loc[-1] = [ask, answer2, right_answer2, day, hour]
                    df_wrong.to_excel(wrong_log, index=False)
                stop_check = True
                entry.delete(0, END)
                text.delete("1.0", END)
                window.update()
            enter_in_text("총점 : {0}/{1} = {2}점".format(count_right,
                                                       qusetion_num, round(count_right/qusetion_num*100)))

            button2.configure(state="normal")
            button3.configure(state="normal")
            button4.configure(state="normal")
            button5.configure(state="normal")
            button6.configure(state="normal")
            button7.configure(state="normal")
            button8.configure(state="normal")
    except:
        button2.configure(state="normal")
        button3.configure(state="normal")
        button4.configure(state="normal")
        button5.configure(state="normal")
        button6.configure(state="normal")
        button7.configure(state="normal")
        button8.configure(state="normal")


def tkinter_eng_word_roof(data_direct, filename):
    entry.delete(0, END)
    text.delete("1.0", "end")
    from time import sleep
    df = read_excel("{0}{1}.xlsx".format(data_direct, filename))
    df = df.drop_duplicates()
    lang = button8.cget("text")
    filename = lang.replace(" ", "_")+"_"+filename
    df = df.sample(frac=1).reset_index(drop=True)  # 데이터 프레임의 행을 랜덤으로 뒤섞는다.
    wrong_log = "{0}오답노트/오답노트_무한반복_{1}.xlsx".format(
        data_direct, filename)
    wrong_log_direct = "{0}오답노트/".format(data_direct)
    createDirectory(wrong_log_direct)
    num_total = df.shape[0]
    count_right = 0
    count = 0
    stop_check = False
    while stop_check == False:
        range_list = list(range(0, num_total-1))
        random.shuffle(range_list)
        for i in range_list:
            if stop_check != False:
                break
            count += 1
            lang = button8.cget("text")
            if lang == "연표":
                ask = df["사건"][i]
                right_answer = df["연도"][i]
            elif lang == "단답형":
                ask = df["질문"][i]
                right_answer = df["대답"][i]
            else:
                ask = df["Text 1"][i]
                right_answer = df["Text 2"][i]
                exp = df["Text 3"][i]
            text.insert(
                "1.0", " ( {0}/{1} )\n\n\n".format(count, num_total))
            if lang != "순서배열":
                try:
                    text.insert("1.0", ask.replace(
                        right_answer, "[   ]"), "emphasis")
                except:
                    text.insert("1.0", ask, "emphasis")
            else:
                text.insert("1.0", f"{ask}\n", "emphasis")
            ############################
            ############################
            ############################
            #answer = sh.typing_yourself()
            window.update()
            answer = ""
            check_ans = False
            while check_ans == False:
                sleep(0.05)
                window.update()
                answer = entry.get()
                if len(answer) != 0 and answer[-1] == "+":
                    text.delete("1.0", "end")
                    click_open_btn()
                    entry.delete(0, END)
                    text.insert(
                        "1.0", " ( {0}/{1} )".format(count, num_total))
                    if lang != "순서배열":
                        try:
                            text.insert("1.0", ask.replace(
                                right_answer, "[   ]"), "emphasis")
                        except:
                            text.insert("1.0", ask, "emphasis")
                    else:
                        text.insert("1.0", f"{ask}\n", "emphasis")
                if answer == "s.":
                    answer = "ㄴ."
                elif answer == "d.":
                    answer = "ㅇ."
                if len(answer) != 0 and answer[-1] == ".":
                    answer = answer[0:-1]
                    check_ans = True
                if len(answer) != 0 and (answer.lower() == "stop" or answer == "종료" or answer == "끝"):
                    stop_check = True
            if stop_check != True:
                text.insert("1.0", "\n")
                window.update()
                ############################
                ############################
                ############################
                if lang == "순서배열":
                    answer = answer.replace("r", "ㄱ")
                    answer = answer.replace("s", "ㄴ")
                    answer = answer.replace("e", "ㄷ")
                    answer = answer.replace("f", "ㄹ")
                    answer = answer.replace("1", "ㄱ")
                    answer = answer.replace("2", "ㄴ")
                    answer = answer.replace("3", "ㄷ")
                    answer = answer.replace("4", "ㄹ")
                right_answer2 = str(right_answer)
                right_answer = str(right_answer).replace(" ", "")
                answer2 = str(answer)
                answer = str(answer).replace(" ", "")
                if lang == "연표" and len(answer) == 2 and len(right_answer) > 2:
                    answer = right_answer[:2]+answer

                right_answer_list = make_list(right_answer)

                if answer != "" and answer in right_answer_list:
                    if lang == "O X 퀴즈":
                        if answer == "ㅇ":
                            enter_in_text(
                                f"정답! {ask.split('=')[0]} 은(는) '{exp}' 입니다.\n")
                        else:
                            enter_in_text(
                                f"정답! {ask.split('=')[0]} 은(는)'{ask.split('=')[1][:-1]}' 이(가) 아니라 '{exp}' 입니다.\n")
                    elif lang == "연표":
                        enter_in_text(
                            f"정답! {answer}년:")
                        era = ask.count("\n")+1
                    elif lang == "단답형":
                        enter_in_text(
                            f"정답! '{right_answer2}':")
                        era = ask.count("\n")+1
                    else:
                        enter_in_text(
                            f"정답! \n{exp}\n")
                    count_right += 1

                else:
                    try:
                        beep_check = button5.cget("text")
                        if beep_check == "소리ON" and answer != "":
                            beepsound()
                    except:
                        print("Beep!")
                    if lang == "O X 퀴즈":
                        # Answer - wrong
                        if answer == "ㅇ":
                            text.insert("1.0", f" 입니다.\n")
                            text.insert("1.0", exp, "emphasis")
                            text.insert(
                                "1.0", f" 은(는)  '{ask.split('=')[1][1:-1]}' 이(가) 아니라 ")
                            text.insert("1.0", "\n"+f"오답~,{ask.split('=')[0]}")
                        else:
                            text.insert("1.0", f"이(가) 맞습니다.\n")
                            text.insert("1.0", f"'{exp}'", "emphasis")
                            text.insert("1.0", f" 은(는) ")
                            text.insert("1.0", "\n"+f"오답~,{ask.split('=')[0]}")
                    elif lang == "연표":
                        text.insert("1.0", f"년 입니다.\n")
                        text.insert("1.0", right_answer2, "emphasis")
                        if answer != '':
                            text.insert("1.0", f"{answer}년이 아니고 ")
                            text.insert("1.0", "\n")
                        else:
                            text.insert("1.0", "\n"+f"정답은 ")
                        era = ask.count("\n")+1
                    elif lang == "단답형":
                        text.insert("1.0", f" 입니다.\n")
                        text.insert("1.0", right_answer2, "emphasis")
                        if answer != '':
                            text.insert("1.0", f"'{answer2}'이(가) 아니고 ")
                            text.insert("1.0", "\n")
                        else:
                            text.insert("1.0", "\n"+f"정답은 ")
                        era = ask.count("\n")+1
                    else:
                        text.insert("1.0", f"{exp}\n\n")
                        text.insert("1.0", f" 입니다.\n")
                        text.insert("1.0", right_answer2, "emphasis")
                        if answer != '':
                            text.insert("1.0", f"'{answer}'이 아니라 ")
                        text.insert("1.0", "\n"+f"오답~,")
                    now = datetime.now()
                    day = now.strftime("%Y%m%d")
                    hour = now.strftime("%H")
                    if isfile(wrong_log):
                        df_wrong = read_excel(wrong_log)
                    else:
                        df_wrong = DataFrame(
                            {'질문': [], '대답': [], '정답': [], '날짜': [], '시간': []})
                    df_wrong.loc[-1] = [ask, answer2, right_answer2, day, hour]
                    df_wrong.to_excel(wrong_log, index=False)
                entry.delete(0, END)
                if lang == "O X 퀴즈":
                    text.delete("4.0", "end")
                elif lang == "순서배열":
                    text.delete("7.0", "end")
                enter_in_text("\n"+"총점 : {0}/{1} = {2}점\n".format(count_right,
                                                                  count, round(count_right/count*100)))
                window.update()
    enter_in_text("종료\n")
    entry.delete(0, END)
    text.delete("1.0", "end")
    window.update()

#########################################################################################


def enter_in_text(enter):
    text.insert("1.0", enter + "\n")


def get_file_direct():
    try:
        files = filedialog.askopenfilenames(initialdir="./",
                                            title="파일을 선택 해 주세요",
                                            filetypes=(("*.xlsx", "*xlsx"), ("*.xls", "*xls")))
        file = files[0]
        try:
            filename = file.split("/")[-1]
            오답노트 = file.replace(filename,"")+"오답노트"
            shutil.rmtree(오답노트)
        except:
            print(오답노트)
            pass
        label.config(text=file)
    except:
        pass


def click_start_btn():
    name = label.cget("text")
    if isfile(name):
        name2 = name.split("/")
        data_direct = (name[0:-len(name2[-1])])
        filename = (name2[-1].split(".")[0])
        if RadioVariety_1.get() == 2:
            tkinter_eng_word_test(data_direct, filename)
        elif RadioVariety_1.get() == 1:
            tkinter_eng_word_roof(data_direct, filename)
        else:
            enter_in_text("원하는 작업을 선택해주세요.")
    else:
        enter_in_text("실행할 수 없습니다. 파일을 선택했는지, 자료가 있는지 확인해주세요.")


def check():
    pass


def enter_in_entry(event):
    entry.insert(END, ".")
    #entry.delete(0, END)


def click_stop_btn():
    entry.insert(END, "종료.")


def click_open_btn():
    name = label.cget("text")
    lang = button8.cget("text")
    name = name.replace("/객관식+단답형_","/")
    name = name.replace("/객관식_","/")
    name = name.replace("_연도별모음","")
    name = name.replace("_문제","")
    name = name.replace("순서배열","연표")
    name = name.replace("_번역","")
    name = name.replace("_구분통합","")
    for i in [1,2,3,4]:
        name = name.replace(f"{i}글자.",".")
    if isfile(name):
        df = read_excel(name)
        lang = button8.cget("text")
        if lang == "O X 퀴즈":
            df = df.sort_values(by="Text 1", ascending=True)
            df = df.drop_duplicates()
            key_word = df["Text 1"].tolist()
            content_to_print = df["Text 2"].tolist()
        elif lang == "연표" or lang == "순서배열":
            df = df.drop_duplicates()
            df = df.drop_duplicates(["사건"])
            key_word = df["연도"].tolist()
            content_to_print = df["사건"].tolist()
        elif lang == "단답형":
            df = df.drop_duplicates()
            #df = df.sort_values(by="대답", ascending=True)
            key_word = df["대답"].tolist()
            content_to_print = df["질문"].tolist()
        line = button7.cget("text")
        if line == "줄바꿈 1":
            a = " "
            b = ""
        elif line == "줄바꿈 2":
            a = ""
            b = "\n"
        elif line == "줄바꿈 3":
            a = "\n"
            b = "\n"
        else:
            a = " "
            b = ""

        search = entry.get()
        search = search.replace(".", "")
        search = search.replace("+", "")
        search = search.replace("종료", "")
        if lang == "O X 퀴즈":
            k = 1
            for i in range(len(key_word)):
                if content_to_print[len(key_word)-i-1] == "ㅇ":
                    k += 1
            j = 1
            text.insert("1.0", f"\n")
            for i in range(len(key_word)):
                if content_to_print[len(key_word)-i-1] == "ㅇ":

                    if search == "여기 입력하세요!" or search == "":
                        print_check = True
                    else:
                        if search in str(key_word[len(key_word)-i-1].split('=')[0]) or search in str(key_word[len(key_word)-i-1].split('=')[1][:-1]):
                            print_check = True
                        else:
                            print_check = False
                    if print_check == True:
                        if k-j >= 100:
                            zfil = 1
                            if int((k-j) % 100) == 0:
                                text.insert(
                                    "1.0", f"{k-j}----------------------------------------------------------", "emphasis")
                        else:
                            zfil = 0

                        text.insert(
                            "1.0", f"{'%-5s' % key_word[len(key_word)-i-1].split('=')[0]}\n{b}")
                        text.insert(
                            "1.0", f"{'%-5s' % key_word[len(key_word)-i-1].split('=')[1][:-1]}{a}", "emphasis")
                        text.insert(
                            "1.0", f"{str(k-j).zfill(2)[zfil:]}.")
                        j += 1
                '''
                text.insert(
                    "1.0", f"{str(len(key_word)-i).zfill(2)}. {'%-5s' % key_word[len(key_word)-i-1]}  {content_to_print[len(key_word)-i-1]} \n", "emphasis")
                '''
            text.insert("1.0", "\n\n")
        else:
            text.insert("1.0", f"\n")
            for i in range(len(key_word)):
                if search == "여기 입력하세요!" or search == "":
                    print_check = True
                    search_check = False
                else:
                    if search in str(content_to_print[len(key_word)-i-1]) or search in str(key_word[len(key_word)-i-1]):
                        print_check = True
                        search_check = True
                    else:
                        print_check = False
                ##print(search, print_check)
                if print_check == True:
                    if search_check == True:
                        text.insert(
                            "1.0", f"{'%-5s' % content_to_print[len(key_word)-i-1]}\n{b}")
                    elif line == "줄바꿈 0" and ((i != 0 and (str(key_word[len(key_word)-i-1]).replace(" ", "") != str(key_word[len(key_word)-i]).replace(" ", "")))):
                        text.insert(
                            "1.0", f"{'%-5s' % content_to_print[len(key_word)-i-1]}\n\n{b}")
                    else:
                        text.insert(
                            "1.0", f"{'%-5s' % content_to_print[len(key_word)-i-1]}\n{b}")
                    text.insert(
                        "1.0", f"{'%-5s' % key_word[len(key_word)-i-1]}{a}", "emphasis")
                    text.insert(
                        "1.0", f"{str(len(key_word)-i).zfill(len(str(len(key_word))))}.")
            text.insert("1.0", "\n\n")
    else:
        enter_in_text("실행할 수 없습니다. 파일을 선택했는지, 자료가 있는지 확인해주세요.")


def click_wrong_btn():
    name = label.cget("text")
    if isfile(name):
        name2 = name.split("/")
        data_direct = name[0:-len(name2[-1])]
        filename = name2[-1].split(".")[0]
        lang = button8.cget("text")
        filename = lang.replace(" ", "_")+"_"+filename
        wrong_log = "{0}오답노트/오답노트_테스트_{1}.xlsx".format(
            data_direct, filename)

        if RadioVariety_1.get() == 2:
            wrong_log = "{0}오답노트/오답노트_테스트_{1}.xlsx".format(
                data_direct, filename)
        elif RadioVariety_1.get() == 1:
            wrong_log = "{0}오답노트/오답노트_무한반복_{1}.xlsx".format(
                data_direct, filename)
        df = read_excel(wrong_log)
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        df = df[df['날짜'] == int(date)]
        ask = df["질문"].tolist()
        ans = df["대답"].tolist()
        cor = df["정답"].tolist()
        times = df["시간"].tolist()
        lang = button8.cget("text")
        if lang == "O X 퀴즈" or lang == "연표":
            for i in range(len(ask)):
                text.insert(
                    "1.0",
                    f"{str(len(ask) - i).zfill(2)}   ({str(times[i]).zfill(2)}시)   {'%-15s' % ask[i]}      {ans[i]} / {cor[i]}\n")

            text.insert(
                "1.0", f"\n(시험 본 시각)     {'%-3s' % '질문'}          대답 / 정답\n")
            text.insert("1.0", f"{date}")
        else:
            for i in range(len(ask)):
                text.insert(
                    "1.0", f"{str(len(ask)-i).zfill(2)}   ({str(times[i]).zfill(2)}시)   \n{'%-15s' % ask[i]}      \n{ans[i]} / {cor[i]}\n\n")

            text.insert(
                "1.0", f"\n(시험 본 시각)     {'%-3s' % '질문'}          대답 / 정답\n")
            text.insert("1.0", f"{date}")
    else:
        enter_in_text("실행할 수 없습니다. 파일을 선택했는지, 자료가 있는지 확인해주세요.")


def click_erase_btn():
    text.delete("1.0", "end")


def click_kor_eng_btn():
    lang = button8.cget("text")
    if lang == "순서배열":
        button8.config(text="O X 퀴즈")
    elif lang == "O X 퀴즈":
        button8.config(text="연표")
    elif lang == "연표":
        button8.config(text="단답형")
    elif lang == "단답형":
        button8.config(text="순서배열")


def click_test_number_btn():
    num_test = button_test.cget("text")
    if num_test == "5문항":
        button_test.config(text="10문항")
    elif num_test == "10문항":
        button_test.config(text="15문항")
    elif num_test == "15문항":
        button_test.config(text="20문항")
    elif num_test == "20문항":
        button_test.config(text="25문항")
    elif num_test == "25문항":
        button_test.config(text="30문항")
    elif num_test == "30문항":
        button_test.config(text="5문항")


def click_line_btn():
    line = button7.cget("text")
    if line == "줄바꿈 0":
        button7.config(text="줄바꿈 1")
    elif line == "줄바꿈 1":
        button7.config(text="줄바꿈 2")
    elif line == "줄바꿈 2":
        button7.config(text="줄바꿈 3")
    elif line == "줄바꿈 3":
        button7.config(text="줄바꿈 0")


def click_beep_btn():
    lang = button5.cget("text")
    if lang == "소리ON":
        button5.config(text="소리OFF")
    else:
        button5.config(text="소리ON")


def on_click(event):
    event.widget.delete(0, END)


def on_click2(event):
    event.widget.delete(1.0, END)


def click_close_btn():
    window.destroy()


def click_double_esc_btn(self):
    window.destroy()


def click_esc_btn(self):
    window.attributes('-fullscreen', False)


def click_f11_btn(self):
    window.attributes('-fullscreen', True)


def click_memo_btn():
    es = ""

    def saveFile(event):
        ts = str(ta.get(1.0, END))
        try:
            f = open("idea.txt", "w")
        except:
            f = open("idea.txt", "w", encoding="utf-8")
        f.write(ts)
        f.close()

    top = Tk()
    top.title("memo")
    top.geometry("400x750+0+100")

    ta = Text(top)
    ta.configure(bg=_from_rgb((11, 58, 19)), foreground="white", highlightthickness=0, insertbackground="yellow", selectbackground="yellow", selectforeground=_from_rgb((11, 58, 19)),
                 font=('Courier', 15))
    top.grid_rowconfigure(0, weight=1)
    top.grid_columnconfigure(0, weight=1)
    ta.grid(sticky=N + E + S + W)
    top.bind_all('<Control-Key-s>', saveFile)

    mb = Menu(top, background=_from_rgb((11, 58, 19)),
              foreground="yellow", activebackground="yellow", activeforeground=_from_rgb((11, 58, 19)), font=('Courier', 10))

    top.config(menu=mb)

    file = "idea.txt"
    ##print(file, type(file))
    top.title(basename(file) + " - 메모장")
    ta.delete(1.0, END)
    try:
        f = open(file, "r")
    except:
        f = open(file, "r", encoding="utf-8")
    ta.insert(1.0, f.read())
    f.close()

    top.mainloop()

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 
##############################################################################################################
window = Tk()

window.title("나만의 퀴즐렛")
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
window.columnconfigure(7, weight=1)
window.rowconfigure(4, weight=1)

#window.geometry('%dx%d+0+0' % (width,height))
window.geometry("1245x770+400+100")
window.resizable(True, True)
window.configure(bg=_from_rgb((11, 58, 19)))

window.bind_all('<Return>', enter_in_entry)
window.bind_all('<F11>', click_f11_btn)
window.bind_all('<Escape>', click_esc_btn)
window.bind_all('<Double-Escape>', click_double_esc_btn)
##############################################################################################################


button = Button(window, relief="flat", overrelief="flat", width=8, height=2, text="파일 선택", font=('Courier', 20),
                command=get_file_direct)
button.grid(column=0, row=0, rowspan=3, ipadx=2, ipady=2)
button.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                 activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", highlightthickness=0)

label = Label(
    window, text="<- 버튼을 눌러 파일을 선택하세요 :)", font=('Courier', 20), width=80, height=3, wraplength=1000)
label.grid(column=1, row=0, rowspan=3, columnspan=7)
label.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                highlightthickness=0)

RadioVariety_1 = IntVar()

radio1 = Radiobutton(
    window, text="무한반복", value=1, variable=RadioVariety_1, command=check, width=8, font=('Courier', 20), anchor="w")
radio1.grid(column=8, row=0)
radio1.select()
radio1.configure(bg=_from_rgb((11, 58, 19)), foreground="white", selectcolor=_from_rgb((11, 58, 19)),
                 activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", relief="flat", highlightthickness=0)

radio2 = Radiobutton(
    window, text="테스트", value=2, variable=RadioVariety_1, command=check, width=8, font=('Courier', 20), anchor="w")
radio2.grid(column=8, row=1)
radio2.configure(bg=_from_rgb((11, 58, 19)), foreground="white", selectcolor=_from_rgb((11, 58, 19)),
                 activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", highlightthickness=0)

button_test = Button(window, relief="flat", overrelief="flat", width=8, height=1, text="5문항", font=('Courier', 20),
                     command=click_test_number_btn)
button_test.grid(column=8, row=2)
button_test.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                      activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", highlightthickness=0)
##############################################################################################################


text = Text(window, font=('Courier', int(round(width*0.02))),
            relief="raised",  borderwidth=0)
text.grid(column=0, row=4, columnspan=9, rowspan=1,
          ipadx=20, ipady=0, sticky=W+E+N+S)
text.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
               highlightthickness=0, insertbackground="yellow", selectbackground=_from_rgb((11, 58, 19)), selectforeground="yellow")

textEntry = StringVar()
textEntry.set("여기 입력하세요!")

#text.tag_config("emphasis", foreground="yellow")
text.tag_config("emphasis", foreground="yellow")

entry = Entry(window, font=('Courier', 25),
              relief="flat", justify="center", textvariable=textEntry)

entry.bind("<Button-1>", on_click)
entry.grid(column=0, row=5, columnspan=9,
           rowspan=1, ipadx=20, ipady=2, sticky=W+E)
entry.configure(bg=_from_rgb((11, 58, 19)), foreground="white", insertbackground="yellow", borderwidth=0,
                highlightthickness=1, highlightcolor="yellow")

##############################################################################################################

button2 = Button(window, relief="flat", width=10, height=1, text="시작", font=('Courier', 18),
                 command=click_start_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button2.grid(column=0, row=6, rowspan=1, ipadx=2, ipady=7)
button2.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)

button3 = Button(window, relief="flat", width=10, height=1, text="파일 열기", font=('Courier', 18),
                 command=click_open_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button3.grid(column=1, row=6, rowspan=1, ipadx=0, ipady=7)
button3.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)


button7 = Button(window, relief="flat", width=12, height=1, text="줄바꿈 0", font=(
    'Courier', 18), activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", command=click_line_btn)
button7.grid(column=2, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
button7.configure(bg=_from_rgb((11, 58, 19)), foreground="white", highlightthickness=0)

button4 = Button(window, relief="flat", width=10, height=1, text="오답노트", font=('Courier', 18),
                 command=click_wrong_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button4.grid(column=3, row=6, rowspan=1, ipadx=0, ipady=7)
button4.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)

button5 = Button(window, relief="flat", width=10, height=1, text="소리ON", font=('Courier', 18),
                 command=click_beep_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button5.grid(column=4, row=6, rowspan=1, ipadx=0, ipady=7)
button5.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)


button6 = Button(window, relief="flat", width=10, height=1, text="지우기", font=('Courier', 18),
                 command=click_erase_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button6.grid(column=5, row=6, rowspan=1, ipadx=0, ipady=7)
button6.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)


button8 = Button(window, relief="flat", width=10, height=1, text="단답형", font=('Courier', 18),
                 command=click_kor_eng_btn, activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow")
button8.grid(column=6, row=6, rowspan=1, ipadx=0, ipady=7, stick=W)
button8.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)

button9 = Button(window, relief="flat", width=10, height=1, text="중지", font=(
    'Courier', 18), activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", command=click_stop_btn)
button9.grid(column=7, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
button9.configure(bg=_from_rgb((11, 58, 19)), foreground="white",
                  highlightthickness=0)

button10 = Button(window, relief="flat", width=12, height=1, text="프로그램 종료", font=(
    'Courier', 18), activebackground=_from_rgb((11, 58, 19)), activeforeground="yellow", command=click_close_btn)
button10.grid(column=8, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
button10.configure(bg=_from_rgb((11, 58, 19)), foreground="white", highlightthickness=0)

window.attributes('-fullscreen', True)
window.mainloop()
