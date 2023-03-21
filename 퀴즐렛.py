from datetime import datetime
from pandas import read_excel, DataFrame
from numpy import round
from tkinter import END, Tk, Button, Label, Radiobutton, Text, StringVar, Entry, filedialog, IntVar, E, W, N, S, Menu
from os.path import exists, isfile, basename
from os import makedirs
import random
import re
import shutil
from copy import copy
from pathlib import Path
import pandas as pd
import os
import psutil

def 매인함수(text_size2=0):
    def 학습시간(모드, study_hour=0):
        now = datetime.now()
        day = now.strftime("%Y%m%d")
        quizlet = os.path.abspath(__file__).split("\\")[-1]
        file = os.path.abspath(__file__).replace(quizlet,"학습시간.xlsx")
        my_file = Path(file)
        if my_file.is_file():
            df = read_excel(file)
            날짜목록 = list(df['날짜'])
            if int(day) not in 날짜목록:
                new_df = DataFrame({'날짜': [day], '학습시간': [0]})
                df = pd.concat([df, new_df])
                df.to_excel(file, index=False)
        else:
            df = DataFrame({'날짜': [day], '학습시간': [0]})
            df.to_excel(file, index=False)

        if 모드 == '읽기':
            날짜목록 = list(df['날짜'])
            try:
                study_hour = int(df[df['날짜'] == int(day)]['학습시간'])
            except:
                study_hour = 0
        elif 모드 == '쓰기':
            날짜목록 = list(df['날짜'])
            last_study_time = int(df[df['날짜'] == int(day)]['학습시간'])
            df.loc[df['날짜'] == int(day), '학습시간'] = last_study_time + study_hour
            df.to_excel(file, index=False)
            study_hour = int(df[df['날짜'] == int(day)]['학습시간'])
        return study_hour


    try:
        import winsound as sd

        def beepsound():
            fr = 750    # range : 37 ~ 32767
            du = 500     # 1000 ms ==1second
            sd.Beep(fr, du)  # winsound.Beep(frequency, duration)
    except:
        pass


    def make_list(right_answer):
        lang = button8.cget("text")
        right_answer_original = right_answer
        right_answer_list = []

        try:
            right_answer_list += right_answer.split("|")
        except:
            right_answer_list += [str(right_answer)]           
            
        if lang != "객관식":
            right_answer = re.sub('\([^)]+\)', '', right_answer) 
            
            try:
                right_answer_list += right_answer.split(',')
            except:
                right_answer_list += [str(right_answer)]

        if lang == "연표":
            right_answer_list += [str(right_answer)[2:]]
        right_answer_list += [right_answer_original]
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
                # #print(qusetion_num)
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
                    elif lang == "객관식":
                        ask = df["질문"][i]
                        ask = ask.replace(" \n","")
                        right_answer = df["대답"][i]
                        category = df["구분"][i]
                        df2 = df[df["구분"] == category]
                        answer_list = list(set(df2["대답"]))
                        print_ask = df["질문"][i]
                        try:
                            print_ask = print_ask.replace(right_answer, "[   ]")
                        except:
                            pass
                        if len(answer_list) > 3:
                            len_answer_list = 3
                            선지번호 = [1, 2, 3]
                            선지목록 = [1, 2, 3]
                            선지목록_체크용 = [1, 2, 3]
                            random.shuffle(선지번호)

                            answer_list.remove(right_answer)
                            random.shuffle(answer_list)
                            answer_list = [right_answer] + answer_list

                            선지목록_체크용[선지번호[0] -
                                    1] = f"{str(answer_list[0]).split('|')[0]}"
                            선지목록_체크용[선지번호[1] -
                                    1] = f"{str(answer_list[1]).split('|')[0]}"
                            선지목록_체크용[선지번호[2] -
                                    1] = f"{str(answer_list[2]).split('|')[0]}"

                            선지목록[선지번호[0] -
                                1] = f"{선지번호[0]}. {str(answer_list[0]).split('|')[0]}"
                            선지목록[선지번호[1] -
                                1] = f"{선지번호[1]}. {str(answer_list[1]).split('|')[0]}"
                            선지목록[선지번호[2] -
                                1] = f"{선지번호[2]}. {str(answer_list[2]).split('|')[0]}"
                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                        elif len(answer_list) == 3:
                            len_answer_list = 3
                            선지번호 = [1, 2, 3]
                            선지목록 = [1, 2, 3]
                            선지목록_체크용 = [1, 2, 3]
                            random.shuffle(선지번호)

                            선지목록_체크용[선지번호[0] -
                                    1] = f"{str(answer_list[0]).split('|')[0]}"
                            선지목록_체크용[선지번호[1] -
                                    1] = f"{str(answer_list[1]).split('|')[0]}"
                            선지목록_체크용[선지번호[2] -
                                    1] = f"{str(answer_list[2]).split('|')[0]}"

                            선지목록[선지번호[0] -
                                1] = f"{선지번호[0]}. {str(answer_list[0]).split('|')[0]}"
                            선지목록[선지번호[1] -
                                1] = f"{선지번호[1]}. {str(answer_list[1]).split('|')[0]}"
                            선지목록[선지번호[2] -
                                1] = f"{선지번호[2]}. {str(answer_list[2]).split('|')[0]}"
                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                        elif len(answer_list) == 2:
                            len_answer_list = 2
                            선지번호 = [1, 2]
                            선지목록 = [1, 2]
                            선지목록_체크용 = [1, 2]
                            random.shuffle(선지번호)
                            '''
                            answer_list.remove(right_answer)
                            random.shuffle(answer_list)
                            answer_list = [right_answer] + answer_list
                            '''
                            선지목록_체크용[선지번호[0] -
                                    1] = f"{str(answer_list[0]).split('|')[0]}"
                            선지목록_체크용[선지번호[1] -
                                    1] = f"{str(answer_list[1]).split('|')[0]}"

                            선지목록[선지번호[0] -
                                1] = f"{선지번호[0]}. {str(answer_list[0]).split('|')[0]}"
                            선지목록[선지번호[1] -
                                1] = f"{선지번호[1]}. {str(answer_list[1]).split('|')[0]}"

                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"
                        else:
                            len_answer_list = 1
                            선지번호 = [1]
                            선지목록 = [1]
                            선지목록_체크용 = [1]

                            answer_list = [right_answer]

                            선지목록_체크용[선지번호[0] -
                                    1] = f"{str(answer_list[0]).split('|')[0]}"

                            선지목록[선지번호[0] -
                                1] = f"{선지번호[0]}. {str(answer_list[0]).split('|')[0]}"

                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n\n"
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
                        if lang == "객관식":
                            text.insert("1.0", print_ask, "emphasis")
                        else:
                            text.insert("1.0", ask, "emphasis")

                        window.update()
                        sleep(0.05)
                        text.delete("1.0", END)
                        # text.delete("1.0", "2.0")
                        answer = entry.get()
                        if lang == "순서배열":
                            answer = answer.replace("r", "ㄱ")
                            answer = answer.replace("s", "ㄴ")
                            answer = answer.replace("e", "ㄷ")
                            answer = answer.replace("f", "ㄹ")
                            answer = answer.replace("1", "ㄱ")
                            answer = answer.replace("2", "ㄴ")
                            answer = answer.replace("3", "ㄷ")
                            answer = answer.replace("4", "ㄹ")
                        if len(answer) != 0:
                            if answer[-1] == ".":
                                answer = answer[0:-1]
                                break
                            elif (lang == "객관식"):
                                try:
                                    if int(answer) in list(range(1, len_answer_list+1)):
                                        answer = 선지목록_체크용[int(
                                            answer)-1].split('|')[0]
                                        break
                                except:
                                    pass
                            elif (lang == "O X 퀴즈" and answer in ["ㄴ", "s", "1", "ㅇ", "d", "2"]):
                                if answer in ["s", "1"]:
                                    answer = "ㄴ"
                                elif answer in ["d", "2"]:
                                    answer = "ㅇ"
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
                        minute = now.strftime("%M")
                        if isfile(wrong_log):
                            df_wrong = read_excel(wrong_log)
                        else:
                            df_wrong = DataFrame(
                                {'질문': [], '대답': [], '정답': [], '날짜': [], '시간': []})
                        df_wrong.loc[-1] = [ask, answer2,
                                            right_answer2, day, f"{hour}시 {minute}분"]
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


    def tkinter_eng_word_roof(data_direct, filename,text_size2):
        entry.delete(0, END)
        text.delete("1.0", "end")
        from time import sleep
        original_filename = "{0}{1}.xlsx".format(data_direct, filename)
        df = read_excel(original_filename)
        df = df.drop_duplicates()
        if '오답가산점' not in list(df.keys()):
            df['오답가산점'] = [0 for i in range(len(df))]
        df['오답가산점'] = df['오답가산점'].fillna(1)
        if '구분' not in list(df.keys()):
            df['구분'] = ['기본' for i in range(len(df))]
        df['구분'] = df['구분'].fillna('기본')
        if '질문' not in list(df.keys()):
            df['질문'] = ['옳은 것은?' for i in range(len(df))]
        df['질문'] = df['질문'].fillna('옳은 것은?')

        for key in list(df.keys()):
            if 'Unnamed' in key:
                df = df.drop(columns=key)
        df.to_excel(original_filename, index=False)
        lang = button8.cget("text")
        filename = lang.replace(" ", "_")+"_"+filename
        # df = df.sample(frac=1).reset_index(drop=True)  # 데이터 프레임의 행을 랜덤으로 뒤섞는다.
        wrong_log = "{0}오답노트/오답노트_무한반복_{1}.xlsx".format(
            data_direct, filename)
        wrong_log_direct = "{0}오답노트/".format(data_direct)
        createDirectory(wrong_log_direct)
        num_total = df.shape[0]
        count_right = 0
        count = 0
        count2 = 0
        stop_check = False
        while stop_check == False:
            sum_check = df['오답가산점'].sum()
            if sum_check == 0:
                range_list = list(range(0, num_total-1))
                range_list.sort(reverse=True)
            else:
                newdf = copy(df)
                # newdf = newdf.sample(frac=1).reset_index(drop=True)
                newdf = newdf.sort_values('오답가산점', ascending=False)
                틀린목록 = list(newdf[newdf["오답가산점"] > 0].index)
                random.shuffle(틀린목록)
                틀릭적없는목록 = list(newdf[newdf["오답가산점"] == 0].index)
                random.shuffle(틀릭적없는목록)
                맞은목록 = list(newdf[newdf["오답가산점"] < 0].index)
                random.shuffle(맞은목록)
                range_list = 틀린목록 + 틀릭적없는목록 + 맞은목록
                text.insert(
                    "1.0", f"오답 체크 : {len(틀린목록)}개 ({newdf['오답가산점'].max()}점)")
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
                elif lang == "객관식":
                    ask = str(df["질문"][i])
                    ask = ask.replace(" \n","")
                    right_answer = df["대답"][i]
                    category = df["구분"][i]
                    df2 = df[df["구분"] == category]
                    answer_list = list(set(df2["대답"]))
                    print_ask = df["질문"][i]

                    if "//" in str(right_answer):
                        answer_list_print = right_answer.split("//")
                        for num in range(len(answer_list_print)):
                            answer_list_print[num] = str(answer_list_print[num].split("|")[0]).strip()
                        '''
                        if len(answer_list_print) == 2 and (("둘 다 맞음" not in answer_list_print) or ("둘 다 아님" not in answer_list_print)):
                            answer_list_print += [random.choice(["둘 다 맞음","둘 다 아님"])]
                        '''
                        answer_list_print = list(sorted(answer_list_print))
                        if "//" not in str(right_answer).split('|')[-1]:
                            right_answer = f"{str(right_answer.split('//')[0]).strip()}|{str(right_answer.split('|')[-1])}"
                        else:
                            right_answer = f"{str(right_answer.split('//')[0]).strip()}"
                    else:
                        answer_list_print = []
                        for answer_list_word in answer_list:
                            answer_list_print += [str(answer_list_word).split('|')[0]]
                        answer_list_print = list(set(answer_list_print.copy()))
                    answer_list_print = sorted(answer_list_print)

                    try:
                        if print_ask.replace(right_answer.split("|")[0], "[   ]").strip() != "[   ]":
                            print_ask = print_ask.replace(str(right_answer.split("|")[0]).strip(), "[   ]")
                    except:
                        pass
                    right_answer = str(right_answer)
                    word_list = []
                    for word1 in answer_list_print:
                        word_list += [str(word1)]
                    word_list.sort(key=len)
                    answer_list_print = word_list

                    if len(answer_list_print) > 3:
                        len_answer_list = 3
                        선지번호 = [1, 2, 3]
                        선지목록 = [1, 2, 3]
                        선지목록_체크용 = [1, 2, 3]
                        random.shuffle(선지번호)
                        answer_list_print.remove(str(right_answer).split("|")[0])
                        random.shuffle(answer_list_print)
                        answer_list_print = [str(right_answer).split("|")[0]] + answer_list_print
                        선지목록_체크용[선지번호[0] -
                                1] = f"{str(answer_list_print[0])}"
                        선지목록_체크용[선지번호[1] -
                                1] = f"{str(answer_list_print[1])}"
                        선지목록_체크용[선지번호[2] -
                                1] = f"{str(answer_list_print[2])}"

                        선지목록[선지번호[0] -
                            1] = f"{선지번호[0]}. {str(answer_list_print[0])}"
                        선지목록[선지번호[1] -
                            1] = f"{선지번호[1]}. {str(answer_list_print[1])}"
                        선지목록[선지번호[2] -
                            1] = f"{선지번호[2]}. {str(answer_list_print[2])}"
                        if text_size2 < 10:
                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                        else:
                            print_ask = f"{print_ask}\n{선지목록[0]}\n{선지목록[1]}\n{선지목록[2]}"
                    elif len(answer_list_print) == 3:
                        len_answer_list = 3
                        선지번호 = [1, 2, 3]
                        선지목록 = [1, 2, 3]
                        선지목록_체크용 = [1, 2, 3]
                        선지목록_체크용[선지번호[0] -
                                1] = f"{str(answer_list_print[0])}"
                        선지목록_체크용[선지번호[1] -
                                1] = f"{str(answer_list_print[1])}"
                        선지목록_체크용[선지번호[2] -
                                1] = f"{str(answer_list_print[2])}"

                        선지목록[선지번호[0] -
                            1] = f"{선지번호[0]}. {str(answer_list_print[0])}"
                        선지목록[선지번호[1] -
                            1] = f"{선지번호[1]}. {str(answer_list_print[1])}"
                        선지목록[선지번호[2] -
                            1] = f"{선지번호[2]}. {str(answer_list_print[2])}"
                        #print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                        
                        if text_size2 < 10:
                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n{선지목록[2]}"
                        else:
                            print_ask = f"{print_ask}\n{선지목록[0]}\n{선지목록[1]}\n{선지목록[2]}"
                    elif len(answer_list_print) == 2:
                        len_answer_list = 2
                        선지번호 = [1, 2]
                        선지목록 = [1, 2]
                        선지목록_체크용 = [1, 2]
                        '''
                        random.shuffle(선지번호)
                        answer_list.remove(right_answer)
                        random.shuffle(answer_list)
                        answer_list = [right_answer] + answer_list
                        '''
                        선지목록_체크용[선지번호[0] -
                                1] = f"{str(answer_list_print[0])}"
                        선지목록_체크용[선지번호[1] -
                                1] = f"{str(answer_list_print[1])}"

                        선지목록[선지번호[0] -
                            1] = f"{선지번호[0]}. {str(answer_list_print[0])}"
                        선지목록[선지번호[1] -
                            1] = f"{선지번호[1]}. {str(answer_list_print[1])}"

                        #print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"
                        
                        if text_size2 < 10:
                            print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n{선지목록[1]}\n\n"
                        else:
                            print_ask = f"{print_ask}\n{선지목록[0]}\n{선지목록[1]}\n"
                    else:
                        len_answer_list = 1
                        선지번호 = [1]
                        선지목록 = [1]
                        선지목록_체크용 = [1]

                        answer_list = [right_answer]

                        선지목록_체크용[선지번호[0] -
                                1] = f"{str(answer_list_print[0])}"

                        선지목록[선지번호[0] -
                            1] = f"직접 입력하세요!"

                        print_ask = f"{print_ask}\n\n{선지목록[0]}\n\n\n"
                else:
                    ask = df["Text 1"][i]
                    right_answer = df["Text 2"][i]
                    exp = df["Text 3"][i]
                text.insert(
                    "1.0", "({0}/{1})\n".format(count, num_total))
                count2 += 1
                if count2 == num_total:
                    count2 = -1
                if sum_check != 0 and count2 == len(틀린목록)+1:
                    text.insert("1.0", "\n\n오답 체크 완료!")
                    try:
                        beep_check = button5.cget("text")
                        if answer != "":
                            if beep_check == "소리ON":
                                beepsound()
                                beepsound()
                            else:
                                sleep(1)
                    except:
                        sleep(1)
                if lang == "객관식":
                    text.insert("1.0", f"{print_ask}\n", "emphasis")
                elif lang != "순서배열":
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
                # answer = sh.typing_yourself()
                window.update()
                answer = ""
                check_ans = False
                now = ""
                '''
                study_time_pre = int(
                    (datetime.now() - start_time).total_seconds()/60)
                '''
                while check_ans == False:
                    lang = button8.cget("text")
                    '''
                    clock_check = button_test.cget("text")
                    now = datetime.now()
                    study_time = int((now - start_time).total_seconds()/60)
                    if study_time == 0:
                        study_time_sec = int(
                            (now - start_time).total_seconds())
                        new = f"{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}({study_time_sec}:{total_study_hour}"
                    elif study_time > 0:
                        new = f"{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}({int((now - start_time).total_seconds()/60)}:{total_study_hour}"
                        if study_time_pre != int((now - start_time).total_seconds()/60):
                            학습시간(모드="쓰기", study_hour=1)
                            total_study_hour = 학습시간(모드="읽기")
                            study_time_pre = copy(
                                int((now - start_time).total_seconds()/60))

                    if clock_check == "시계ON":
                        battery = psutil.sensors_battery()
                        try:
                            if battery.power_plugged == True:
                                용량 = f" {battery.percent}% 충전중"
                            else:
                                용량 = f" {battery.percent}%"
                        except:
                            용량 = ""
                        new = f"{new}{용량})\n\n"
                        if now != new:
                            now = copy(new)
                            text.insert("1.0", now)
                    '''
                    sleep(0.05)
                    window.update()
                    '''
                    if clock_check == "시계ON":
                        text.delete("1.0", f"3.0")
                    '''
                    answer = entry.get()
                    if len(answer) != 0 and (answer[-1] in ["+", "-", "*", "=", "]","[","/"]):
                        text.delete("1.0", "end")
                        click_open_btn()
                        entry.delete(0, END)
                        text.insert(
                            "1.0", " ( {0}/{1} )".format(count, num_total))
                        if lang == "단답형":
                            if answer[-1] in ["*", "]"]:
                                button8.config(text="객관식")
                                text.insert("1.0", print_ask, "emphasis")
                            elif answer[-1] == "-":
                                try:
                                    text.insert("1.0", print_ask, "emphasis")
                                except:
                                    try:
                                        text.insert("1.0", ask.replace(
                                            right_answer, "[   ]"), "emphasis")
                                    except:
                                        text.insert("1.0", ask, "emphasis")
                            elif answer[-1] in ["[","/"]:
                                click_wrong_btn()
                            else:
                                try:
                                    text.insert("1.0", ask.replace(
                                        right_answer, "[   ]"), "emphasis")
                                except:
                                    text.insert("1.0", ask, "emphasis")
                        elif lang == "객관식":
                            if answer[-1] in ["*", "]"]:
                                button8.config(text="단답형")
                                text.insert("1.0", print_ask, "emphasis")
                            elif answer[-1] == "-":
                                text.insert("1.0", print_ask, "emphasis")
                            elif answer[-1] in ["[","/"]:
                                click_wrong_btn()
                        else:
                            text.insert("1.0", f"{ask}\n", "emphasis")
                    if lang == "순서배열":
                        answer = answer.replace("r", "ㄱ")
                        answer = answer.replace("s", "ㄴ")
                        answer = answer.replace("e", "ㄷ")
                        answer = answer.replace("f", "ㄹ")
                        answer = answer.replace("1", "ㄱ")
                        answer = answer.replace("2", "ㄴ")
                        answer = answer.replace("3", "ㄷ")
                        answer = answer.replace("4", "ㄹ")
                    if len(answer) != 0:
                        if answer[-1] == ".":
                            answer = answer[0:-1]
                            check_ans = True
                        elif (lang == "객관식"):
                            try:
                                if int(answer) in list(range(1+6, len_answer_list+1+6)):
                                    answer = str(int(answer)-6)
                                if int(answer) in list(range(1, len_answer_list+1)):
                                    answer = 선지목록_체크용[int(answer)-1].split('|')[0]
                                    check_ans = True
                            except:
                                pass
                        elif (lang == "O X 퀴즈" and answer in ["ㄴ", "s", "1", "ㅇ", "d", "2"]):
                            check_ans = True
                            if answer in ["s", "1"]:
                                answer = "ㄴ"
                            elif answer in ["d", "2"]:
                                answer = "ㅇ"
                    if len(answer) != 0 and (answer.lower() == "stop" or answer == "종료" or answer == "끝"):
                        stop_check = True
                if stop_check != True:
                    text.insert("1.0", "\n")
                    window.update()
                    ############################
                    ############################
                    ############################
                    right_answer2 = str(right_answer)
                    right_answer2 = right_answer2.replace("\n \n","\n")
                    right_answer2 = right_answer2.replace("\n\n","\n")
                    right_answer2 = right_answer2.replace("」\n ","」\n")
                    right_answer2 = right_answer2.replace(") ",")")
                    if right_answer2.count("|") == 1:
                        right_answer2 = right_answer2.replace("|",":")
                    if right_answer2.count("|") > 1:
                        right_answer2 = right_answer2.replace("|",",")
                    right_answer = str(right_answer).replace(" ", "")
                    answer2 = str(answer)
                    answer = str(answer).replace(" ", "")
                    if lang == "연표" and len(answer) == 2 and len(right_answer) > 2:
                        answer = right_answer[:2]+answer
                        answer = right_answer[:2]+answer

                    right_answer_list = make_list(right_answer)
                    #print("answer : ",answer)
                    #print("right_answer_list : ",right_answer_list)
                    if answer != "" and answer in right_answer_list:
                        df["오답가산점"][i] = df["오답가산점"][i] - 1
                        keys = list(df.keys())
                        for key in keys:
                            if 'Unnamed' in key:
                                df = df.drop(columns=key)
                        df.to_excel(original_filename, index=False)
                        if lang == "O X 퀴즈":
                            if answer == "ㅇ":
                                enter_in_text(
                                    f"정답! {ask.split('=')[0]}은(는) '{exp}' 입니다.\n")
                            else:
                                enter_in_text(
                                    f"정답! {ask.split('=')[0]}은(는) '{str(ask.split('=')[1][:-1]).strip()}' 이(가) 아니라 '{exp}' 입니다.\n")
                        elif lang == "연표":
                            enter_in_text(
                                f"정답! {answer}년:")
                            era = ask.count("\n")+1
                        elif lang == "단답형":
                            if len(right_answer2)>=33 and len(ask)<=5:
                                enter_in_text(
                                    f"\n정답! {ask} : {right_answer2}")
                            else:
                                right_answer2 = right_answer2.replace("|",",")
                                enter_in_text(
                                    f"\n정답! '{right_answer2}':")
                            era = ask.count("\n")+1
                        elif lang == "객관식":
                            if (len(right_answer2)>=33 and len(ask)<=5) or text_size2>10:
                                enter_in_text(
                                    f"정답! {ask} : {right_answer2}")
                            else:
                                right_answer2 = right_answer2.replace("|",",")
                                enter_in_text(
                                    f"정답! '{right_answer2}':")
                            era = ask.count("\n")+1
                            if text_size2 >= 10:
                                entry.delete(0, END)
                                pass_check = True
                                while pass_check == True:
                                    window.update()
                                    sleep(0.05)
                                    pass_enter = entry.get()
                                    if pass_enter != "":
                                        pass_check = False

                        else:
                            enter_in_text(
                                f"정답! \n{exp}\n")
                        count_right += 1

                    else:
                        df["오답가산점"][i] = df["오답가산점"][i] + 1
                        keys = list(df.keys())
                        for key in keys:
                            if 'Unnamed' in key:
                                df = df.drop(columns=key)
                        df.to_excel(original_filename, index=False)
                        try:
                            beep_check = button5.cget("text")
                            if answer != "":
                                if beep_check == "소리ON":
                                    beepsound()
                                elif text_size2<10:
                                    sleep(2)
                        except:
                            sleep(1)
                        if lang == "O X 퀴즈":
                            # Answer - wrong
                            if answer == "ㅇ":
                                text.insert("1.0", f" 입니다.\n")
                                text.insert("1.0", exp, "emphasis")
                                text.insert(
                                    "1.0", f"은(는) '{str(ask.split('=')[1][1:-1]).strip()}' 이(가) 아니라 ")
                                text.insert("1.0", "\n"+f"오답~,{ask.split('=')[0]}")
                            else:
                                text.insert("1.0", f"이(가) 맞습니다.\n")
                                text.insert("1.0", f"'{exp}'", "emphasis")
                                text.insert("1.0", f"은(는) ")
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
                                # text.insert("1.0", "\n")
                            else:
                                text.insert("1.0", "\n"+f"정답은 ")
                            era = ask.count("\n")+1
                        elif lang == "객관식":
                            text.insert("1.0", f" 입니다.\n")                            
                            text.insert("1.0", right_answer2, "emphasis")
                            text.insert("1.0", f"정답은 ")
                            era = ask.count("\n")+1
                            if text_size2 >= 10:
                                entry.delete(0, END)
                                pass_check = True
                                while pass_check == True:
                                    window.update()
                                    sleep(0.05)
                                    pass_enter = entry.get()
                                    if pass_enter != "":
                                        pass_check = False
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
                        minute = now.strftime("%M")
                        if isfile(wrong_log):
                            df_wrong = read_excel(wrong_log)
                        else:
                            df_wrong = DataFrame(
                                {'질문': [], '대답': [], '정답': [], '날짜': [], '시간': []})
                        df_wrong.loc[-1] = [ask, answer2,
                                            right_answer2, day, f"{hour}시 {minute}분"]
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
            quizlet = os.path.abspath(__file__).split("\\")[-1]
            file = os.path.abspath(__file__).replace(quizlet,"")
            files = filedialog.askopenfilenames(initialdir=file,
                                                title="파일을 선택 해 주세요",
                                                filetypes=(("*.xlsx", "*xlsx"), ("*.xls", "*xls")))
            file = files[0]
            try:
                filename = file.split("/")[-1]
                오답노트 = file.replace(filename, "")+"오답노트"
                # shutil.rmtree(오답노트)
            except:
                #print(오답노트)
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
                tkinter_eng_word_roof(data_direct, filename,text_size2)
            else:
                enter_in_text("원하는 작업을 선택해주세요.")
        else:
            enter_in_text("실행할 수 없습니다. 파일을 선택했는지, 자료가 있는지 확인해주세요.")


    def check():
        pass


    def enter_in_entry(event):
        entry.insert(END, ".")
        # entry.delete(0, END)


    def click_stop_btn():
        entry.insert(END, "종료.")


    def click_open_btn():
        name = label.cget("text")
        lang = button8.cget("text")
        name = name.replace("/객관식+단답형_", "/")
        name = name.replace("/객관식_", "/")
        name = name.replace("_연도별모음", "")
        name = name.replace("_문제", "")
        name = name.replace("순서배열", "연표")
        name = name.replace("_번역", "")
        name = name.replace("_구분통합", "")
        name = name.replace("_전기", "")
        name = name.replace("_중기", "")
        name = name.replace("_후기", "")
        for i in [1, 2, 3, 4]:
            name = name.replace(f"{i}글자.", ".")
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
            elif lang == "단답형" or lang == "객관식":
                df = df.drop_duplicates()
                # df = df.sort_values(by="대답", ascending=True)
                key_word = df["대답"].tolist()
                for i1 in range(len(key_word)):
                    key_word[i1] = str(key_word[i1]).split("//")[0]
                    key_word[i1] = str(key_word[i1]).split("|")[0]
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
            search = search.replace("=", "")
            search = search.replace("-", "!@")
            search = search.replace("종료", "")
            if search == "]":
                search = search.replace("]", "!@")

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
                    # #print(search, print_check)
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
            # df = df[df['날짜'] == int(date)]
            ask = df["질문"].tolist()
            ans = df["대답"].tolist()
            cor = df["정답"].tolist()
            times = df["시간"].tolist()
            lang = button8.cget("text")
            if lang == "O X 퀴즈" or lang == "연표":
                for i in range(len(ask)):
                    text.insert(
                        "1.0",
                        f"{str(len(ask) - i).zfill(2)}   ({str(times[i]).zfill(2)}). 질문 | {'%-15s' % ask[i]}\n대답 | {ans[i]}\n정답 | {cor[i]}\n\n")

                #text.insert("1.0", f"\n\n")
            else:
                for i in range(len(ask)):
                    text.insert(
                        "1.0", f"{str(len(ask)-i).zfill(2)}   ({str(times[i]).zfill(2)})\n질문 | {'%-15s' % ask[i]}\n대답 | {ans[i]}\n정답 | {cor[i]}\n\n")

                #text.insert("1.0", f"\n\n")
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
            button8.config(text="객관식")
        elif lang == "객관식":
            button8.config(text="단답형")
        elif lang == "단답형":
            button8.config(text="순서배열")


    def click_test_number_btn():
        num_test = button_test.cget("text")

        #if RadioVariety_1.get() == 2:
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
        else:
            button_test.config(text="5문항")
        '''
        if RadioVariety_1.get() == 1:
            if num_test == "시계ON":
                button_test.config(text="시계OFF")
            elif num_test == "시계OFF":
                button_test.config(text="시계ON")
            else:
                button_test.config(text="시계ON")
        '''


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
        ta.configure(bg=background_color, foreground="white", highlightthickness=0, insertbackground="yellow", selectbackground="yellow", selectforeground=background_color,
                    font=('Courier', 15))
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)
        ta.grid(sticky=N + E + S + W)
        top.bind_all('<Control-Key-s>', saveFile)

        mb = Menu(top, background=background_color,
                foreground="yellow", activebackground="yellow", activeforeground=background_color, font=('Courier', 10))

        top.config(menu=mb)

        file = "idea.txt"
        # #print(file, type(file))
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
    # 글자 크기 조절 변수. Dell xps 13 (9370) = -3
    # text_size2 = 0
    # 배경색
    now_hour = datetime.now().hour
    if now_hour > 18 or now_hour <= 7:
        background_color = _from_rgb((0, 0, 0))  # 검은색
    else:
        background_color = _from_rgb((11, 58, 19))  # 칠판 초록색

    window = Tk()

    window.title("나만의 퀴즐렛")
    width, height = window.winfo_screenwidth(), window.winfo_screenheight()

    # 글자 크기 조절 변수. Dell xps 13 (9370) = -3
    if width >= 1920:
        text_size = 0
    else:
        text_size = -3
    # 배경색
    now_hour = datetime.now().hour
    if now_hour > 18 or now_hour <= 7:
        background_color = _from_rgb((0, 0, 0))  # 검은색
    else:
        background_color = _from_rgb((11, 58, 19))  # 칠판 초록색

    #print(os.path.abspath(__file__),width)
    window.columnconfigure(7, weight=1)
    window.rowconfigure(4, weight=1)

    window.geometry('%dx%d+0+0' % (width, height))
    # window.geometry("1245x770+400+100")
    window.resizable(True, True)
    window.configure(bg=background_color)

    window.bind_all('<Return>', enter_in_entry)
    window.bind_all('<F11>', click_f11_btn)
    window.bind_all('<Escape>', click_esc_btn)
    window.bind_all('<Double-Escape>', click_double_esc_btn)
    ##############################################################################################################


    button = Button(window, relief="flat", overrelief="flat", width=8, height=2, text="파일 선택", font=('Courier', 20+text_size),
                    command=get_file_direct)
    button.grid(column=0, row=0, rowspan=3, ipadx=2, ipady=2)
    button.configure(bg=background_color, foreground="white",
                    activebackground=background_color, activeforeground="yellow", highlightthickness=0)

    label = Label(
        window, text="<- 버튼을 눌러 파일을 선택하세요 :)", font=('Courier', 20+text_size), width=80, height=3, wraplength=800)
    label.grid(column=1, row=0, rowspan=3, columnspan=7)
    label.configure(bg=background_color, foreground="white",
                    highlightthickness=0)

    RadioVariety_1 = IntVar()

    radio1 = Radiobutton(
        window, text="무한반복", value=1, variable=RadioVariety_1, command=check, width=8, font=('Courier', 20+text_size), anchor="w")
    radio1.grid(column=8, row=0)
    radio1.select()
    radio1.configure(bg=background_color, foreground="white", selectcolor=background_color,
                    activebackground=background_color, activeforeground="yellow", relief="flat", highlightthickness=0)

    radio2 = Radiobutton(
        window, text="테스트", value=2, variable=RadioVariety_1, command=check, width=8, font=('Courier', 20+text_size), anchor="w")
    radio2.grid(column=8, row=1)
    radio2.configure(bg=background_color, foreground="white", selectcolor=background_color,
                    activebackground=background_color, activeforeground="yellow", highlightthickness=0)

    button_test = Button(window, relief="flat", overrelief="flat", width=8, height=1, text="5문항", font=('Courier', 20+text_size),
                        command=click_test_number_btn)
    button_test.grid(column=8, row=2)
    button_test.configure(bg=background_color, foreground="white",
                        activebackground=background_color, activeforeground="yellow", highlightthickness=0)
    ##############################################################################################################


    text = Text(window, font=('Courier', int(round(width*0.02))+text_size+text_size2),
                relief="raised",  borderwidth=0)
    text.grid(column=0, row=4, columnspan=9, rowspan=1,
            ipadx=20, ipady=0, sticky=W+E+N+S)
    text.configure(bg=background_color, foreground="white",
                highlightthickness=0, insertbackground="yellow", selectbackground=background_color, selectforeground="yellow")

    textEntry = StringVar()
    textEntry.set("여기 입력하세요!")

    # text.tag_config("emphasis", foreground="yellow")
    text.tag_config("emphasis", foreground="yellow")

    entry = Entry(window, font=('Courier', 25+text_size),
                relief="flat", justify="center", textvariable=textEntry)

    entry.bind("<Button-1>", on_click)
    entry.grid(column=0, row=5, columnspan=9,
            rowspan=1, ipadx=20, ipady=2, sticky=W+E)
    entry.configure(bg=background_color, foreground="white", insertbackground="yellow", borderwidth=0,
                    highlightthickness=1, highlightcolor="yellow")

    ##############################################################################################################

    button2 = Button(window, relief="flat", width=10, height=1, text="시작", font=('Courier', 18+text_size),
                    command=click_start_btn, activebackground=background_color, activeforeground="yellow")
    button2.grid(column=0, row=6, rowspan=1, ipadx=2, ipady=7)
    button2.configure(bg=background_color, foreground="white",
                    highlightthickness=0)

    button3 = Button(window, relief="flat", width=10, height=1, text="파일 열기", font=('Courier', 18+text_size),
                    command=click_open_btn, activebackground=background_color, activeforeground="yellow")
    button3.grid(column=1, row=6, rowspan=1, ipadx=0, ipady=7)
    button3.configure(bg=background_color, foreground="white",
                    highlightthickness=0)


    button7 = Button(window, relief="flat", width=12, height=1, text="줄바꿈 0", font=(
        'Courier', 18+text_size), activebackground=background_color, activeforeground="yellow", command=click_line_btn)
    button7.grid(column=2, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
    button7.configure(bg=background_color,
                    foreground="white", highlightthickness=0)

    button4 = Button(window, relief="flat", width=10, height=1, text="오답노트", font=('Courier', 18+text_size),
                    command=click_wrong_btn, activebackground=background_color, activeforeground="yellow")
    button4.grid(column=3, row=6, rowspan=1, ipadx=0, ipady=7)
    button4.configure(bg=background_color, foreground="white",
                    highlightthickness=0)

    button5 = Button(window, relief="flat", width=10, height=1, text="소리ON", font=('Courier', 18+text_size),
                    command=click_beep_btn, activebackground=background_color, activeforeground="yellow")
    button5.grid(column=4, row=6, rowspan=1, ipadx=0, ipady=7)
    button5.configure(bg=background_color, foreground="white",
                    highlightthickness=0)


    button6 = Button(window, relief="flat", width=8, height=1, text="지우기", font=('Courier', 18+text_size),
                    command=click_erase_btn, activebackground=background_color, activeforeground="yellow")
    button6.grid(column=5, row=6, rowspan=1, ipadx=0, ipady=7)
    button6.configure(bg=background_color, foreground="white",
                    highlightthickness=0)


    button8 = Button(window, relief="flat", width=8, height=1, text="객관식", font=('Courier', 18+text_size),
                    command=click_kor_eng_btn, activebackground=background_color, activeforeground="yellow")
    button8.grid(column=6, row=6, rowspan=1, ipadx=0, ipady=7, stick=W)
    button8.configure(bg=background_color, foreground="white",
                    highlightthickness=0)

    button9 = Button(window, relief="flat", width=8, height=1, text="중지", font=(
        'Courier', 18+text_size), activebackground=background_color, activeforeground="yellow", command=click_stop_btn)
    button9.grid(column=7, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
    button9.configure(bg=background_color, foreground="white",
                    highlightthickness=0)

    button10 = Button(window, relief="flat", width=11, height=1, text="프로그램 종료", font=(
        'Courier', 18+text_size), activebackground=background_color, activeforeground="yellow", command=click_close_btn)
    button10.grid(column=8, row=6, rowspan=1, ipadx=0, ipady=7, stick=E)
    button10.configure(bg=background_color,
                    foreground="white", highlightthickness=0)

    window.attributes('-fullscreen', True)
    window.mainloop()
if __name__ == "__main__":
    매인함수(text_size2=0)