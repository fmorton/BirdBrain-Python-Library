# -*- coding: utf-8 -*-
#https://realpython.com/python-gui-tkinter/
#https://docs.python.org/3/library/tkinter.html
#This gui requires python3.


from BirdBrain import Finch
import time
import tkinter as tk
 

myFinch = Finch('A')

fontName = "Courier" #"Arial"
btnFontSize = 30 
lblFontSize = 18
backgroundColor="#62BCC7" #fountain blue

#Translatable text
english = {
    'NotConnected': "Finch Not Connected",
    'BuzzerOK': "Buzzer ok? \n(Did you hear a tone at the normal volume?)",
    'LEDsOK': "LEDs ok? \n(Did all 5 LEDs turn red, green, and blue?)",
    'MotorsOK': "Motors ok? \n(Did the finch drive straight forward, then backward, then turn?)",
    'MaxSensorsInstr': "Hold the finch up in the air with the beak pointed into the distance.",
    'MinSensorsInstr': "Place the finch in a dark box with the lid closed.",

    'Max': "MAX Sensor Results",
    'Distance': "Distance",
    'LightL': "Left Light",
    'LightR': "Right Light",
    'LineL': "Left Line",
    'LineR': "Right Line",
    'MaxTot': "Max Sensors Total",
    'Min': "MIN Sensor Results",
    'MinTot': "Min Sensors Total",

    'Pass': "PASS",
    'Fail': "FAIL",

    'Results': "Final Results",
    'Tot': "TOTAL",

    'Buzzer': "Buzzer",
    'Motors': "Motors",
    'LEDs': "LEDs",
    'MaxSensors': "Max Sensors",
    'MinSensors': "Min Sensors",
    'Title': "Finch Quality Control",
    'Start': "Start"
    }

chinese = {
    'NotConnected':  "Finch 没有连接",
    'BuzzerOK': "蜂鸣器正常？\n你能听到一个正常音量的声响吗？",
    'LEDsOK': "LED 正常？\n5个LED 显示红 绿 和兰色 吗？",
    'MotorsOK': "马达正常？\nFinch能向前，然后向后，然后转弯？",
    'MaxSensorsInstr': "阻挡Finch ,它的嘴应对着没有障碍物的方向",
    'MinSensorsInstr': "把Finch 放入不透光的盒子里，盖上盖子",

    'Max': "最大感应结果",
    'Distance': "距离",
    'LightL': "左灯",
    'LightR': "右灯",
    'LineL': "左线",
    'LineR': "右线",
    'MaxTot': "总的最大感应",
    'Min': "最小感应结果",
    'MinTot': "总的最小感应",

    'Pass': "通过",
    'Fail': "不合格",

    'Results': "最后结果",
    'Tot': "总计",

    'Buzzer': "蜂鸣器",
    'Motors': "马达",
    'LEDs': "LED灯",
    'MaxSensors': "最大感应器",
    'MinSensors': "最小感应器",
    'Title': "Finch 质量控制",
    'Start': "开始"
    }

strings = english


def start_test(event):
    frm_results.pack_forget()
    lbl_error.pack_forget()
    frm_response.pack_forget()
    window.update()
    if not myFinch.isConnectionValid():
        lbl_error.pack()
        return
    global current_test
    current_test = 0
    next_test()


def pack_response():
    frm_response.pack()


def unpack_response():
    frm_response.pack_forget()
    frm_sensor_results.pack_forget()
    window.update()


def next_test():
    unpack_response()
    if len(test_list) <= current_test:
        display_results()
        return

    #print("about to run test " + str(current_test) + " (" + test_label_list[current_test] + ")")
    test_list[current_test]()


def results(success):
    global current_test
    test_results[current_test] = success
    current_test += 1
    next_test()
    

def test_buzzer():
    myFinch.playNote(60, 1)
    question.configure(text=strings['BuzzerOK'])
    pack_response()


def test_leds():
    pauseTime = 0.2
    myFinch.setBeak(100, 0, 0)
    myFinch.setTail("all", 100, 0, 0)
    time.sleep(pauseTime)
    myFinch.setBeak(0, 100, 0)
    myFinch.setTail("all", 0, 100, 0)
    time.sleep(pauseTime)
    myFinch.setBeak(0, 0, 100)
    myFinch.setTail("all", 0, 0, 100)
    time.sleep(pauseTime)
    myFinch.stopAll()
    question.configure(text=strings['LEDsOK'])
    pack_response()
    
    
def test_motors():
    myFinch.setMove('F', 15.9, 50)
    myFinch.setMove('B', 15.9, 50)
    myFinch.setTurn('R', 90, 50)
    question.configure(text=strings['MotorsOK'])
    pack_response()


def test_max_sensors():
    lbl_instructions.configure(text=strings['MaxSensorsInstr'])
    btn_done.bind("<Button-1>", lambda event: check_max_sensors())
    frm_instructions.pack()


def check_max_sensors():
    btn_recheck.bind("<Button-1>", lambda event: check_max_sensors())
    sensors_check(
        strings['Max'],
        strings['MaxTot'],
        [60, 5, 5, 60, 60],
        False
    )


def test_min_sensors():
    lbl_instructions.configure(text=strings['MinSensorsInstr'])
    btn_done.bind("<Button-1>", lambda event: check_min_sensors())
    frm_instructions.pack()


def check_min_sensors():
    btn_recheck.bind("<Button-1>", lambda event: check_min_sensors())
    sensors_check(
        strings['Min'],
        strings['MinTot'],
        [20, 5, 5, 10, 10],
        True
    )


def sensors_check(title, total, thresholds, minimum):
    frm_instructions.pack_forget()
    window.update()

    names = [strings['Distance'], strings['LightL'], strings['LightR'], strings['LineL'], strings['LineR']]

    values = []
    values.append(myFinch.getDistance())
    values.append(myFinch.getLight("L"))
    values.append(myFinch.getLight("R"))
    values.append(myFinch.getLine("L"))
    values.append(myFinch.getLine("R"))
    
    success = True
    resultsText = title + ":"
    for i in range(0, len(names)):
        resultsText = resultsText + "\n    " + names[i] + ": " + str(values[i])
        thisSuccess = (values[i] < thresholds[i]) if (minimum ^ (i>2)) else (values[i] > thresholds[i])
        success = success and thisSuccess
        if not thisSuccess:
            resultsText = resultsText + " (" + strings['Fail'] + ")"
    
    resultsText = resultsText + "\n" + total
    test_label_list[current_test] = resultsText
    btn_ok.bind("<Button-1>", lambda event: results(success))
    lbl_sensor_results.configure(text=(resultsText + ": " + (strings['Pass'] if success else strings['Fail'])))
    frm_sensor_results.pack()
          

def display_results():
    resultsString = strings['Results'] + ":"
    finchDidPass = True
    for i in range(0, len(test_list)):
        finchDidPass = (finchDidPass and test_results[i])
        thisResult = strings['Pass'] if test_results[i] else strings['Fail']
        resultsString = resultsString + "\n" + test_label_list[i] + ": " + thisResult

    resultsString = resultsString + "\n\n" + strings['Tot'] + ": " + (strings['Pass'] if finchDidPass else strings['Fail'])
    color = "#f57c73"
    if finchDidPass:
        color = "#9afa82"
    lbl_results.configure(text=resultsString, bg=color)
    frm_results.pack()


test_list = [test_buzzer, test_motors, test_leds,  test_max_sensors, test_min_sensors]
test_label_list = [strings['Buzzer'], strings['Motors'], strings['LEDs'], strings['MaxSensors'], strings['MinSensors']]
test_results = [True, True, True, True, True]
current_test = 0

#Configure the main window
window = tk.Tk()
#https://stackoverflow.com/questions/36575890/how-to-set-a-tkinter-window-to-a-constant-size
window.title(strings['Title'])
window.geometry("500x700")
#window.resizable(0,0)
window.configure(bg=backgroundColor)

#Configure the static area at the top of the window
frm_static = tk.Frame(bg=backgroundColor)
btn_start = tk.Button(
    master=frm_static,
    text=strings['Start'],
#    width=5,
#    height=2,
    fg="green",
    font=(fontName, btnFontSize + 10),
    highlightbackground=backgroundColor
)
btn_start.bind("<Button-1>", start_test)
btn_start.pack(padx=25, pady=25)
frm_static.pack()

#Configure the response frame for tests that require user input
frm_response = tk.Frame(bg=backgroundColor)
question = tk.Label(master=frm_response, font=(fontName, lblFontSize), wraplength=350, justify="center", bg=backgroundColor)
question.pack(pady=25)
frm_buttons = tk.Frame(master=frm_response, bg=backgroundColor)
btn_yes = tk.Button(master=frm_buttons, text="✓", fg="green", highlightbackground="green", font=(fontName, btnFontSize))
btn_yes.bind("<Button-1>", lambda event, s=True: results(s))
btn_yes.grid(padx=25, row=0, column=0)
btn_no = tk.Button(master=frm_buttons, text="X", fg="red", highlightbackground="red", font=(fontName, btnFontSize))
btn_no.bind("<Button-1>", lambda event, s=False: results(s))
btn_no.grid(padx=25, row=0, column=1)
btn_retry = tk.Button(master=frm_buttons, text="↺", highlightbackground=backgroundColor, font=(fontName, btnFontSize - 10)) #https://charbase.com/block/arrows
btn_retry.bind("<Button-1>", lambda event: next_test())
btn_retry.grid(padx=25, row=0, column=3)
frm_buttons.pack()

#Configure an instructions area for test that require setup
frm_instructions = tk.Frame(bg=backgroundColor)
lbl_instructions = tk.Label(master=frm_instructions, font=(fontName, lblFontSize), wraplength=350, justify="center", bg=backgroundColor)
lbl_instructions.pack(pady=25)
btn_done = tk.Button(master=frm_instructions, text="✓", fg="green", highlightbackground="green", font=(fontName, btnFontSize))
btn_done.pack()

#Configure sensor only results area for sensor tests
frm_sensor_results = tk.Frame(bg=backgroundColor)
lbl_sensor_results = tk.Label(master=frm_sensor_results, font=(fontName, lblFontSize), wraplength=350, justify="left", bg=backgroundColor)
lbl_sensor_results.grid(pady=25, row=0, column=0, columnspan=2)
btn_ok = tk.Button(master=frm_sensor_results, text="✓", fg="green", highlightbackground=backgroundColor, font=(fontName, btnFontSize))
btn_ok.grid(row=1, column=0)
btn_recheck = tk.Button(master=frm_sensor_results, text="↺", highlightbackground=backgroundColor, font=(fontName, btnFontSize))
btn_recheck.grid(row=1, column=1)

#Configure a results area to display results when all tests are complete
frm_results = tk.Frame(relief=tk.RIDGE, borderwidth=5)
lbl_results = tk.Label(master=frm_results, font=(fontName, lblFontSize), justify="left", width=30)
lbl_results.pack()

#Configure an error message for when no finch is connected
lbl_error = tk.Label(text=strings['NotConnected'], font=(fontName, lblFontSize), justify="center", bg=backgroundColor)

window.mainloop()
