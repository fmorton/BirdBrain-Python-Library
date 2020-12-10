#https://realpython.com/python-gui-tkinter/
#https://docs.python.org/3/library/tkinter.html


from BirdBrain import Finch
import time
import tkinter as tk
 

myFinch = Finch('A')



def start_test(event):
    results_label.pack_forget()
    global current_test
    current_test = 0
    next_test()


def pack_response():
    frm_response.pack()
    #question.pack()
    #btn_yes.pack()
    #btn_no.pack()


def unpack_response():
    print("unpack response")
    frm_response.pack_forget()
    #question.pack_forget()
    #btn_yes.pack_forget()
    #btn_no.pack_forget()
    window.update()


def next_test():
    unpack_response()
    print("checking for more tests")
    if len(test_list) <= current_test:
        display_results()
        return

    print("about to run test " + str(current_test) + " (" + test_label_list[current_test] + ")")
    test_list[current_test]()
    pack_response()


def results(success):
    global current_test
    test_results[current_test] = success
    current_test += 1
    next_test()
    

def test_buzzer():
    myFinch.playNote(60, 1)
    question.configure(text="Buzzer ok? (Did you hear a tone at the normal volume?)")

    
def test_motors():
    myFinch.setMove('F', 10, 50)
    myFinch.setMove('B', 10, 50)
    myFinch.setTurn('R', 90, 50)
    question.configure(text="Motors ok? (Did the finch drive straight forward, then backward, then turn?)")


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
    results_label.configure(text=resultsString, bg=color)
    results_label.pack()


test_list = [test_buzzer, test_motors]
test_label_list = ["Buzzer", "Motors"]
test_results = [True, True]
current_test = 0

window = tk.Tk()
#https://stackoverflow.com/questions/36575890/how-to-set-a-tkinter-window-to-a-constant-size
window.title('Finch Quality Control')
window.geometry("500x500")
window.resizable(0,0)


#greeting = tk.Label(text="Finch Quality Control")
#greeting.configure(bg='blue')
#greeting.pack()

frm_static = tk.Frame()
btn_start = tk.Button(
    master=frm_static,
    text="Start",
    width=25,
    height=5,
    background="red",
    highlightbackground="yellow",
    fg="blue",
)
btn_start.bind("<Button-1>", start_test)
btn_start.pack()
frm_static.pack()

frm_response = tk.Frame()
question = tk.Label(master=frm_response)
question.pack()
btn_yes = tk.Button(master=frm_response, text="Yes", bg="green", highlightbackground="green")
btn_yes.bind("<Button-1>", lambda event, s=True: results(s))
btn_yes.pack()
btn_no = tk.Button(master=frm_response, text="No", bg="red", highlightbackground="red")
btn_no.bind("<Button-1>", lambda event, s=False: results(s))
btn_no.pack()

results_label = tk.Label()

window.mainloop()
