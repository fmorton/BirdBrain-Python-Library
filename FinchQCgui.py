# -*- coding: utf-8 -*-
#https://realpython.com/python-gui-tkinter/
#https://docs.python.org/3/library/tkinter.html
#This gui requires python3.


from BirdBrain import Finch
import time
import tkinter as tk
 

myFinch = Finch('A')

fontName = "Arial"
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
    frm_instructions.pack_forget()
    window.update()
    light_left = myFinch.getLight("L")
    light_right = myFinch.getLight("R")
    line_left = myFinch.getLine("L")
    line_right = myFinch.getLine("R")
    distance = myFinch.getDistance()
    maxSensorResults = strings['Max'] + ":\n\t" + strings['Distance'] + ": " + str(distance) + \
        "\n\t" + strings['LightL'] + ": " + str(light_left) + "\n\t" + strings['LightR'] + ": " + str(light_right) + \
        "\n\t" + strings['LineL'] + ": " + str(line_left) + "\n\t" + strings['LineR'] + ": " + str(line_right) + \
        "\n" + strings['MaxTot']
    test_label_list[current_test] = maxSensorResults
    success = (light_left > 5 and light_right > 5 and line_left < 60 and line_right < 60 and distance > 60)
    btn_ok.bind("<Button-1>", lambda event: results(success))
    btn_recheck.bind("<Button-1>", lambda event: check_max_sensors())
    lbl_sensor_results.configure(text=(maxSensorResults + ": " + (strings['Pass'] if success else strings['Fail'])))
    frm_sensor_results.pack()


def test_min_sensors():
    lbl_instructions.configure(text=strings['MinSensorsInstr'])
    btn_done.bind("<Button-1>", lambda event: check_min_sensors())
    frm_instructions.pack()


def check_min_sensors():
    frm_instructions.pack_forget()
    window.update()
    light_left = myFinch.getLight("L")
    light_right = myFinch.getLight("R")
    line_left = myFinch.getLine("L")
    line_right = myFinch.getLine("R")
    distance = myFinch.getDistance()
    minSensorResults = strings['Min'] + ":\n\t" + strings['Distance'] + ": " + str(distance) + \
        "\n\t" + strings['LightL'] + ": " + str(light_left) + "\n\t" + strings['LightR'] + ": " + str(light_right) + \
        "\n\t" + strings['LineL'] + ": " + str(line_left) + "\n\t" + strings['LineR'] + ": " + str(line_right) + \
        "\n" + strings['MinTot']
    test_label_list[current_test] = minSensorResults
    success = (light_left < 5 and light_right < 5 and line_left > 90 and line_right > 90 and distance < 20)
    btn_ok.bind("<Button-1>", lambda event: results(success))
    btn_recheck.bind("<Button-1>", lambda event: check_min_sensors())
    lbl_sensor_results.configure(text=(minSensorResults + ": " + (strings['Pass'] if success else strings['Fail'])))
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
