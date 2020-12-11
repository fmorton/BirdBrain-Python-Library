#https://realpython.com/python-gui-tkinter/
#https://docs.python.org/3/library/tkinter.html


from BirdBrain import Finch
import time
import tkinter as tk
 

myFinch = Finch('A')

fontName = "Arial"
btnFontSize = 30 
lblFontSize = 18


def start_test(event):
    lbl_results.pack_forget()
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
    print("checking for more tests")
    if len(test_list) <= current_test:
        display_results()
        return

    print("about to run test " + str(current_test) + " (" + test_label_list[current_test] + ")")
    test_list[current_test]()


def results(success):
    global current_test
    test_results[current_test] = success
    current_test += 1
    next_test()
    

def test_buzzer():
    myFinch.playNote(60, 1)
    question.configure(text="Buzzer ok? \n(Did you hear a tone at the normal volume?)")
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
    question.configure(text="LEDs ok? \n(Did all 5 LEDs turn red, green, and blue?)")
    pack_response()
    
def test_motors():
    myFinch.setMove('F', 15.9, 50)
    myFinch.setMove('B', 15.9, 50)
    myFinch.setTurn('R', 90, 50)
    question.configure(text="Motors ok? \n(Did the finch drive straight forward, then backward, then turn?)")
    pack_response()


def test_max_sensors():
    lbl_instructions.configure(text="Hold the finch up in the air with the beak pointed into the distance (check for missing screws?).")
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
    maxSensorResults = "MAX Sensor Results:\n\tDistance: " + str(distance) + \
        "\n\tLeft Light: " + str(light_left) + "\n\tRight Light: " + str(light_right) + \
        "\n\tLeft Line: " + str(line_left) + "\n\tRight Line: " + str(line_right) + \
        "\nMax Sensors Total"
    test_label_list[current_test] = maxSensorResults
    success = (light_left > 5 and light_right > 5 and line_left < 50 and line_right < 50 and distance > 100)
    btn_ok.bind("<Button-1>", lambda event: results(success))
    btn_recheck.bind("<Button-1>", lambda event: check_max_sensors())
    lbl_sensor_results.configure(text=(maxSensorResults + ": " + ("PASS" if success else "FAIL")))
    frm_sensor_results.pack()


def test_min_sensors():
    lbl_instructions.configure(text="Place the finch in a dark box with the lid closed")
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
    minSensorResults = "MIN Sensor Results:\n\tDistance: " + str(distance) + \
        "\n\tLeft Light: " + str(light_left) + "\n\tRight Light: " + str(light_right) + \
        "\n\tLeft Line: " + str(line_left) + "\n\tRight Line: " + str(line_right) + \
        "\nMax Sensors Total"
    test_label_list[current_test] = minSensorResults
    success = (light_left < 5 and light_right < 5 and line_left > 90 and line_right > 90 and distance < 20)
    btn_ok.bind("<Button-1>", lambda event: results(success))
    btn_recheck.bind("<Button-1>", lambda event: check_min_sensors())
    lbl_sensor_results.configure(text=(minSensorResults + ": " + ("PASS" if success else "FAIL")))
    frm_sensor_results.pack()
          

def display_results():
    resultsString = "Test Results:"
    finchDidPass = True
    for i in range(0, len(test_list)):
        finchDidPass = (finchDidPass and test_results[i])
        thisResult = "Pass" if test_results[i] else "Fail"
        resultsString = resultsString + "\n" + test_label_list[i] + ": " + thisResult

    resultsString = resultsString + "\n\nTOTAL: " + ("PASS" if finchDidPass else "FAIL")
    color = "#f57c73"
    if finchDidPass:
        color = "#9afa82"
    lbl_results.configure(text=resultsString, bg=color)
    lbl_results.pack()


test_list = [test_buzzer, test_leds, test_motors, test_max_sensors, test_min_sensors]
test_label_list = ["Buzzer", "LEDs", "Motors", "Max Sensors", "Min Sensors"]
test_results = [True, True, True, True, True]
current_test = 0

#Configure the main window
window = tk.Tk()
#https://stackoverflow.com/questions/36575890/how-to-set-a-tkinter-window-to-a-constant-size
window.title('Finch Quality Control')
window.geometry("500x700")
window.resizable(0,0)

#Configure the static area at the top of the window
frm_static = tk.Frame()
btn_start = tk.Button(
    master=frm_static,
    text="Start",
    width=5,
    height=2,
    fg="green",
    font=(fontName, btnFontSize + 10)
)
btn_start.bind("<Button-1>", start_test)
btn_start.pack(padx=25, pady=25)
frm_static.pack()

#Configure the response frame for tests that require user input
frm_response = tk.Frame()
question = tk.Label(master=frm_response, font=(fontName, lblFontSize), wraplength=350, justify="center")
question.pack(pady=25)
frm_buttons = tk.Frame(master=frm_response)
btn_yes = tk.Button(master=frm_buttons, text="✓", fg="green", highlightbackground="green", font=(fontName, btnFontSize))
btn_yes.bind("<Button-1>", lambda event, s=True: results(s))
btn_yes.grid(padx=25, row=0, column=0)
btn_no = tk.Button(master=frm_buttons, text="X", fg="red", highlightbackground="red", font=(fontName, btnFontSize))
btn_no.bind("<Button-1>", lambda event, s=False: results(s))
btn_no.grid(padx=25, row=0, column=1)
btn_retry = tk.Button(master=frm_buttons, text="↺ ↩ \U0001f501", font=(fontName, btnFontSize - 10)) #https://charbase.com/block/arrows
btn_retry.bind("<Button-1>", lambda event: next_test())
btn_retry.grid(padx=25, row=0, column=3)
frm_buttons.pack()

#Configure an instructions area for test that require setup
frm_instructions = tk.Frame()
lbl_instructions = tk.Label(master=frm_instructions, font=(fontName, lblFontSize), wraplength=350, justify="center")
lbl_instructions.pack(pady=25)
btn_done = tk.Button(master=frm_instructions, text="✓", fg="green", highlightbackground="green", font=(fontName, btnFontSize))
btn_done.pack()

#Configure sensor only results area for sensor tests
frm_sensor_results = tk.Frame()
lbl_sensor_results = tk.Label(master=frm_sensor_results, font=(fontName, lblFontSize), wraplength=350, justify="left")
lbl_sensor_results.grid(pady=25, row=0, column=0, columnspan=2)
btn_ok = tk.Button(master=frm_sensor_results, text="✓", fg="green", font=(fontName, btnFontSize))
btn_ok.grid(row=1, column=0)
btn_recheck = tk.Button(master=frm_sensor_results, text="↺", font=(fontName, btnFontSize))
btn_recheck.grid(row=1, column=1)

#Configure a results area to display results when all tests are complete
lbl_results = tk.Label(font=(fontName, lblFontSize), justify="left", width=30)
lbl_error = tk.Label(text="Finch Not Connected", font=(fontName, lblFontSize), justify="center")

window.mainloop()
