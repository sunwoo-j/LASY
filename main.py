#Import modules from Python library
import tkinter as tk
import time, random
from PIL import ImageTk, Image
from shutil import copyfile

bg_colour = "#ffffff"

class main:
    #Code for GUI
    def __init__(self, root):
        #Tab key
        def focus_next_widget(widget):
            widget.tk_focusNext().focus()
            return "break"
        self.root = root
        self.root.resizable(False, False)
        self.root.title("LASY: Assistant for Latin Poetry Scansion")
        self.root.configure(background = bg_colour)
        self.canvas = tk.Canvas(root, width = 800, height = 500, background = bg_colour)
        self.canvas.pack()
        #Load images
        column = Image.open("Resource/column.png")
        column = column.resize((93, 302), Image.ANTIALIAS)
        self.column = ImageTk.PhotoImage(column)
        self.canvas.create_image(20, 30, anchor = "nw",image = self.column)
        self.canvas.create_image(685, 30, anchor= "nw",image = self.column)
        logo = Image.open("Resource/logo.png")
        logo = logo.resize((225, 125), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(logo)
        self.canvas.create_image(288, 20, anchor= "nw", image = self.logo)
        #Sets
        global bt_clear, bt_hexa, bt_penta
        bt_clear = tk.Button(width = 21, height = 0, text = "Clear", command = algorithm.clear_text)
        bt_hexa = tk.Button(relief = "ridge", bd = 1, activebackground = "#92daf7", activeforeground = "white", bg = "#76c0de", fg = "white", height = 1, width = 15, font = ("malgun gothic", 11), text = "Hexameter", state = "disabled", command = algorithm.hexameter)
        bt_penta = tk.Button(relief = "ridge", bd = 1, activebackground = "#92daf7", activeforeground = "white", bg = "#76c0de", fg = "white", height = 1, width = 15, font = ("malgun gothic", 11), text = "Pentameter", state = "disabled", command = algorithm.pentameter)
        global lb_syllable, lb_scansion, lb_alert
        lb_syllable = tk.Label(width = 58, bg = bg_colour, text = "", anchor = "w", font = ("times", 13))
        lb_scansion = tk.Label(width = 58, bg = bg_colour, text = "", anchor = "w", font = ("arial", 13))
        lb_info = tk.Label(width = 100, bg = bg_colour, justify = "left", text = "WARNING: Please use this program as a secondary source of help, primary source being your Latin teachers and peers. \nThis program does not cover the entirety of Latin language's complexity, and may not be accurate in scanning every text. \nAlso, it must only be used to scan a pre-existing line of poetry and not to check the validity of your own. \nWhere possible, please change consonantal 'i's to 'j' and distinguish 'u' and 'v' for better accuracy.", anchor = "w", font = ("calibri", 10))
        lb_alert = tk.Label(width = 60, text = "", anchor = "w", bg = bg_colour, font = ("arial", 11), fg = "red")
        global bt_table, bt_dictionary, bt_quiz, bt_setting
        bt_table = tk.Button(relief = "flat", bd = 1, activebackground = bg_colour, activeforeground = "black", bg = bg_colour, fg = "black", height = 1, width = 15, font = ("malgun gothic", 11, "underline"), text = "Noun Endings", command = lambda: self.new_window(tables))
        bt_dictionary = tk.Button(relief = "flat", bd = 1, activebackground = bg_colour, activeforeground = "black", bg = bg_colour, fg = "black", height = 1, width = 15, font = ("malgun gothic", 11, "underline"), text = "Dictionary", command = lambda: self.new_window(dictionary))
        bt_quiz = tk.Button(relief = "flat", bd = 1, activebackground = bg_colour, activeforeground = "black", bg = bg_colour, fg = "black", height = 1, width = 15, font = ("malgun gothic", 11, "underline"), text = "Quiz", command = lambda: self.new_window(quiz))
        bt_setting = tk.Button(relief = "flat", bd = 1, activebackground = bg_colour, activeforeground = "black", bg = bg_colour, fg = "black", height = 1, width = 15, font = ("malgun gothic", 11, "underline"), text = "Settings", command = lambda: self.new_window(setting))
        global entry
        entry = tk.Text(root, relief = "flat", xscrollcommand = True, highlightthickness = 2, height = 0, width = 58, pady = 6, font = ("times", 13))
        entry.insert(tk.END, "Arma virumque cano Troiae qui primus ab oris")
        entry.bind('<Return>', lambda event: self.pressed_enter())
        entry.bind("<Tab>", lambda event: focus_next_widget(entry))
        bt_syllable = tk.Button(relief = "ridge", bd = 1, activebackground = "#92daf7", activeforeground = "white", bg = "#76c0de", fg = "white", width = 30, height = 1, text = "Separate Syllables", font = ("malgun gothic", 11), command = algorithm.syllable_sequence)
        #Startup loading screen
        img = Image.open("Resource/logo_white.png")
        self.photoImg = ImageTk.PhotoImage(img)
        startLogo = self.canvas.create_image(0, 0, anchor='nw',image=self.photoImg)
        #Buttons, labels and entry box GUI
        self.root.after(1000, lambda: self.canvas.delete(startLogo))
        self.root.after(1000, lambda: bt_syllable.place(relx = 0.5, rely = 0.4, anchor = "center"))
        self.root.after(1000, lambda: bt_hexa.place(relx = 0.410, rely = 0.62, anchor = "center"))
        self.root.after(1000, lambda: bt_penta.place(relx = 0.590, rely = 0.62, anchor = "center"))
        self.root.after(1000, lambda: entry.place(x = 130, y = 140))
        self.root.after(1000, lambda: lb_syllable.place(x = 130, y = 230))
        self.root.after(1000, lambda: lb_scansion.place(x = 130, y = 260))
        self.root.after(1000, lambda: lb_info.place(relx = 0.515, rely = 0.9, anchor = "center"))
        self.root.after(1000, lambda: lb_alert.place(x = 130, y = 115))
        self.root.after(1000, lambda: bt_table.place(relx = 0.2, rely = 0.75, anchor = "center"))
        self.root.after(1000, lambda: bt_dictionary.place(relx = 0.4, rely = 0.75, anchor = "center"))
        self.root.after(1000, lambda: bt_quiz.place(relx = 0.6, rely = 0.75, anchor = "center"))
        self.root.after(1000, lambda: bt_setting.place(relx = 0.8, rely = 0.75, anchor = "center"))
        #Load settings
        global showtip, his_include
        with open("Text/settings.txt", 'r') as fp:
            first_line = fp.readline()
        a, b = [int(x) for x in first_line.strip().split()]
        #with open("Text/settings.txt", "r") as f:
        showtip = tk.StringVar()
        showtip.set(str(a))
        his_include = tk.StringVar()
        his_include.set(str(b))
    #Bind enter key to command, disable new line
    def pressed_enter(self):
        algorithm.syllable_sequence()
        return "break"
    #Open new window
    def new_window(self, _class):
        #Disable duplicate windows
        if str(_class) == "<class '__main__.dictionary'>":
            bt_dictionary.config(state = "disabled")
        elif str(_class) == "<class '__main__.tables'>":
           bt_table.config(state = "disabled")
        elif str(_class) == "<class '__main__.quiz'>":
            bt_quiz.config(state = "disabled")
        elif str(_class) == "<class '__main__.setting'>":
            bt_setting.config(state = "disabled")

        self.new = tk.Toplevel(self.root)
        _class(self.new)
#Setting window
class setting:
    def __init__(self, root):
        self.root = root
        self.root.focus()
        self.root.geometry("200x150")
        self.root.resizable(False, False)
        self.root.title("LASY: Settings")
        self.root.configure(background = bg_colour)
        lb_inst = tk.Label(self.root, bg = bg_colour, fg = "red", font = ("calibri", 10), text = "Settings are applied after \nreopening respective windows.")
        lb_inst.place(relx = 0.5, rely = 0.8, anchor = "center")
        quiztoggle = tk.Checkbutton(self.root, text = "Include history in quiz", variable = his_include, onvalue = True, offvalue = False, bg = bg_colour, activebackground = bg_colour, command = lambda: self.save())
        quiztoggle.place(relx = 0.5, rely = 0.6, anchor = "center")
        tiptoggle = tk.Checkbutton(self.root, text = "Show tips", variable = showtip, onvalue = True, offvalue = False, bg = bg_colour, activebackground = bg_colour, command = lambda: self.save())
        tiptoggle.place(relx = 0.337, rely = 0.4, anchor = "center")
        bt_clearhistory = tk.Button(self.root, width = 20, text = "Clear search history", bg = bg_colour, bd = 0, activebackground = bg_colour, relief = "flat", font = ("calibri", 10, "underline"), command = lambda: self.clear())
        bt_clearhistory.place(relx = 0.5, rely = 0.17, anchor = "center")
        self.root.iconbitmap('Resource/favicon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.onclose)
    #Clear search_history.txt
    def clear(self):
        f = open("Text/search_history.txt", 'r+')
        f.truncate(0)
    #Save setting on file
    def save(self):
        with open("Text/settings.txt", "w") as f:
            f.write(str(showtip.get())+" "+str(his_include.get()))
    #Activate Setting window button when closed
    def onclose(self):
        bt_setting.config(state = "active")
        self.root.destroy()
#Tables window
class tables:
    def __init__(self, root):
        self.root = root
        self.root.focus()
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.title("LASY: Noun Endings")
        self.root.configure(background = bg_colour)        
        noun = Image.open("Resource/noun.jpg")
        noun = noun.resize((760, 434), Image.ANTIALIAS)
        self.root.canvas = tk.Canvas(root, width = 890, height = 525, background = bg_colour)
        self.root.canvas.pack()
        self.root.noun = ImageTk.PhotoImage(noun)
        self.root.canvas.create_image(20, 25, anchor= "nw", image = self.root.noun)
        
        self.root.iconbitmap('Resource/favicon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.onclose)
    #Activate Table window button when closed
    def onclose(self):
        bt_table.config(state = "active")
        self.root.destroy()
#Quiz window
class quiz:
    def __init__(self, root):
        def quiz_setup():
            file = open("Text/quiz.txt", "r")
            global questions
            #2D array for words: definition
            questions = {}
            for line in file:
                x = line.split("@")
                a = x[0].strip()
                b = x[1].strip()
                questions[a] = b
            try:
                if his_include.get() == "1":
                    file2 = open("Text/search_history.txt", "r")
                    for line in file2:
                        x = line.split("@")
                        if x[0].strip() == "hexa":
                            a = x[1].strip()
                            b = x[2].strip()
                            if a not in questions:
                                questions[a] = b
            except NameError:
                return None
        #Load new question
        def new_question(d):
            global ans
            q, ans = random.choice(list(d.items()))
            lb_question.config(text = q)
            lb_mark.config(image = "")
        #Change response
        def changeoption(n):
            global ans1, ans2, ans3, ans4, ans5
            global bt_ans1, bt_ans2, bt_ans3, bt_ans4, bt_ans5
            if n == 1:
                if ans1 == "s":
                    bt_ans1.config(image = self.root.dactyl)
                    ans1 = "d"
                else:
                    bt_ans1.config(image = self.root.spondee)
                    ans1 = "s"
            elif n == 2:
                if ans2 == "s":
                    bt_ans2.config(image = self.root.dactyl)
                    ans2 = "d"
                else:
                    bt_ans2.config(image = self.root.spondee)
                    ans2 = "s"
            elif n == 3:
                if ans3 == "s":
                    bt_ans3.config(image = self.root.dactyl)
                    ans3 = "d"
                else:
                    bt_ans3.config(image = self.root.spondee)
                    ans3 = "s"
            elif n == 4:
                if ans4 == "s":
                    bt_ans4.config(image = self.root.dactyl)
                    ans4 = "d"
                else:
                    bt_ans4.config(image = self.root.spondee)
                    ans4 = "s"
            elif n == 5:
                if ans5 == "s":
                    bt_ans5.config(image = self.root.dactyl)
                    ans5 = "d"
                else:
                    bt_ans5.config(image = self.root.spondee)
                    ans5 = "s"
        #Check answer    
        def checkans():
            answer = ans + "d"
            ans_str = ans1 + ans2 + ans3 + ans4 + ans5
            if answer == ans_str:
                lb_mark.config(image = self.root.check)
            else:
                lb_mark.config(image = self.root.cross)
                
        self.root = root
        self.root.focus()
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.title("LASY: Quiz")
        self.root.configure(background = bg_colour)
        #Load images
        check = Image.open("Resource/check.png")
        check = check.resize((17, 10), Image.ANTIALIAS)
        self.root.check = ImageTk.PhotoImage(check)
        cross = Image.open("Resource/cross.png")
        cross = cross.resize((16, 14), Image.ANTIALIAS)
        self.root.cross = ImageTk.PhotoImage(cross)
        dactyl = Image.open("Resource/dactyl.jpg")
        dactyl = dactyl.resize((76, 40), Image.ANTIALIAS)
        self.root.dactyl = ImageTk.PhotoImage(dactyl)
        spondee = Image.open("Resource/spondee.jpg")
        spondee = spondee.resize((76, 40), Image.ANTIALIAS)
        self.root.spondee = ImageTk.PhotoImage(spondee)
        end = Image.open("Resource/end.jpg")
        end = end.resize((76, 40), Image.ANTIALIAS)
        self.root.end = ImageTk.PhotoImage(end)
        self.root.iconbitmap('Resource/favicon.ico')

        lb_question = tk.Label(self.root, width = 60, text = "", height = 15, anchor = "center", justify = "center", bg = bg_colour, font = ("times", 18), fg = "black")
        lb_question.pack()
        lb_mark = tk.Label(self.root, anchor = "e", bg = bg_colour)
        lb_mark.pack()
        #Set widgets
        a = 165
        b = 240
        c = 80
        global ans1, ans2, ans3, ans4, ans5
        ans1 = "s"
        ans2 = "s"
        ans3 = "s"
        ans4 = "s"
        ans5 = "s"
        global bt_ans1, bt_ans2, bt_ans3, bt_ans4, bt_ans5
        bt_newq = tk.Button(self.root, text = "Try another", relief = "flat", bg = bg_colour, activebackground = bg_colour, bd = 0, anchor = "center", font = ("malgun gothic", 12), width = 15, height = 2, command= lambda: new_question(questions)).place(relx = 0.5, rely = 0.7, anchor = "center")
        bt_checkans = tk.Button(self.root, text = "Submit", relief = "flat", bg = bg_colour, activebackground = bg_colour, bd = 0, anchor = "center", font = ("malgun gothic", 12), width = 15, height = 2, command= lambda: checkans()).place(relx = 0.5, rely = 0.63, anchor = "center")
        lb_end = tk.Label(self.root, image = self.root.end, bg = bg_colour)
        lb_end.place(x = a+c*5, y = b)
        bt_ans1 = tk.Button(self.root, bd = 0, image = self.root.spondee, activebackground = bg_colour, bg = bg_colour, relief = "flat", command = lambda: changeoption(1))
        bt_ans1.place(x = a+c*0, y = b)
        bt_ans2 = tk.Button(self.root, bd = 0, image = self.root.spondee, activebackground = bg_colour, bg = bg_colour, relief = "flat", command = lambda: changeoption(2))
        bt_ans2.place(x = a+c*1, y = b)        
        bt_ans3 = tk.Button(self.root, bd = 0, image = self.root.spondee, activebackground = bg_colour, bg = bg_colour, relief = "flat", command = lambda: changeoption(3))
        bt_ans3.place(x = a+c*2, y = b)
        bt_ans4 = tk.Button(self.root, bd = 0, image = self.root.spondee, activebackground = bg_colour, bg = bg_colour, relief = "flat", command = lambda: changeoption(4))
        bt_ans4.place(x = a+c*3, y = b)
        bt_ans5 = tk.Button(self.root, bd = 0, image = self.root.spondee, activebackground = bg_colour, bg = bg_colour, relief = "flat", command = lambda: changeoption(5))
        bt_ans5.place(x = a+c*4, y = b)
        #Backup quiz file
        quiz_setup()
        copyfile("Text/quiz.txt", "Text/quiz_backup.txt")
        new_question(questions)
        
        self.root.protocol("WM_DELETE_WINDOW", self.onclose)
    #Activate Quiz window button when closed
    def onclose(self):
        bt_quiz.config(state = "active")
        self.root.destroy()
#Dictionary window  
class dictionary:
    def __init__(self, root):
        #Generate dictionary page
        def dic_generate(pg, pgst, load, mxpg, mxln, mxpgst, firstLoad):
            global page, pageset
            page = pg
            pageset = pgst
            if firstLoad:
                for i in range(10):
                    if page < mxpg or (page == mxpg and i < mxpg):
                        var_holder["self.lb_word" + str(i)] = tk.Label(root, width = 20, bg = bg_colour, anchor = "nw", font = ("times", ft_size), fg = "black", text = load[i+pg*10][0])
                        var_holder["self.lb_word" + str(i)].place(x = a, y = b+c*i)
                        var_holder["self.lb_altform" + str(i)] = tk.Label(root, width = 20, bg = bg_colour, anchor = "nw", font = ("times", ft_size), fg = "black", text = load[i+pg*10][1])
                        var_holder["self.lb_altform" + str(i)].place(x = a+d, y = b+c*i)
                        var_holder["self.lb_class" + str(i)] = tk.Label(root, width = 20, bg = bg_colour, anchor = "nw", font = ("times", ft_size-1, "italic"), fg = "black", text = load[i+pg*10][3])
                        var_holder["self.lb_class" + str(i)].place(x = a+e, y = b+c*i)
                        var_holder["self.lb_def" + str(i)] = tk.Label(root, width = 40, bg = bg_colour, anchor = "nw", font = ("times", ft_size), fg = "black", text = load[i+pg*10][2])
                        var_holder["self.lb_def" + str(i)].place(x = a+f, y = b+c*i)
            else:
                for i in range(10):
                    if page < mxpg or (page == mxpg and i < mxln):
                        var_holder["self.lb_word" + str(i)].config(text = load[i+pg*10][0])
                        var_holder["self.lb_altform" + str(i)].config(text = load[i+pg*10][1])
                        var_holder["self.lb_class" + str(i)].config(text = load[i+pg*10][3])
                        var_holder["self.lb_def" + str(i)].config(text = load[i+pg*10][2])
                    else:
                        var_holder["self.lb_word" + str(i)].config(text = "")
                        var_holder["self.lb_altform" + str(i)].config(text = "")
                        var_holder["self.lb_class" + str(i)].config(text = "")
                        var_holder["self.lb_def" + str(i)].config(text = "")

            for i in range(1, 6):
                try:
                    if (i-1+pageset*5) == page:
                        var_holder["bt_page" + str(i)].config(fg = "black", font = ("arial", 10, "underline"))
                    else:
                        var_holder["bt_page" + str(i)].config(fg = "#525252", font = ("arial", 10, ""))
                except KeyError:
                    return None
            locals().update(var_holder)

            self.root.bind('<Up>', lambda event: pressed_left(pg, pgst, load, mxpg, mxln, mxpgst, False))
            self.root.bind('<Down>', lambda event: pressed_right(pg, pgst, load, mxpg, mxln, mxpgst, False))
        #Shift dictionary page by 5
        def shift_set(pgst, load, mxpg, mxln, mxpgst, firstLoad):
            global pageset
            pageset = pgst
            global bt_page1, bt_page2, bt_page3, bt_page4, bt_page5
            if firstLoad == True:
                if pageset < mxpgst:
                    bt_nextpage = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, text = ">", bg = bg_colour, command = lambda:[shift_set((pageset + 1), load, mxpg, mxln, mxpgst, False), dic_generate(pageset*5, pageset, load, mxpg, mxln, mxpgst, False)])
                    bt_nextpage.place(x = bta+btc*6, y = btb)
                    for i in range(1, 6):
                        moveto = i-1+pageset*5
                        if i == 1:
                            var_holder["bt_page" + str(i)] = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, font = ("arial", 10, "underline"), fg = "#525252", bg = bg_colour, text = i+pageset*5, command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False)) #Store current value of moveto
                            var_holder["bt_page" + str(i)].place(x = bta+btc*i, y = btb)
                        else:
                            var_holder["bt_page" + str(i)] = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, font = ("arial", 10), fg = "#525252", bg = bg_colour, text = i+pageset*5, command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False)) #Store current value of moveto
                            var_holder["bt_page" + str(i)].place(x = bta+btc*i, y = btb)
                else:
                    bt_nextpage = tk.Button(self.root, relief = "flat", width = 2, activebackground = bg_colour, state = "disabled", text = "", bg = bg_colour)
                    bt_nextpage.place(x = bta+btc*6, y = btb)
                    leftpages = mxpg + 1 - mxpgst*5
                    for i in range(1, leftpages+1):
                        moveto = i-1+pageset*5
                        if i == 1:
                            var_holder["bt_page" + str(i)] = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, font = ("arial", 10, "underline"), fg = "#525252", bg = bg_colour, text = i+pageset*5, command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False)) #Store current value of moveto
                            var_holder["bt_page" + str(i)].place(x = bta+btc*i, y = btb)
                        else:
                            var_holder["bt_page" + str(i)] = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, fg = "#525252", font = ("arial", 10), bg = bg_colour, text = i+pageset*5, command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False)) #Store current value of moveto
                            var_holder["bt_page" + str(i)].place(x = bta+btc*i, y = btb)
                    for i in range(leftpages+1, 6):
                        var_holder["bt_page" + str(i)] = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, fg = "#525252", font = ("arial", 10), bg = bg_colour, text = "•", state = "disabled") #Store current value of moveto
                        var_holder["bt_page" + str(i)].place(x = bta+btc*i, y = btb)
            else:
                if pageset < mxpgst:
                    bt_nextpage = tk.Button(self.root, relief = "flat", bd = 0, activebackground = bg_colour, width = 3, height = 3, text = ">", bg = bg_colour, command = lambda pageset = pageset:[shift_set((pageset+1), load, mxpg, mxln, mxpgst, False), dic_generate((pageset+1)*5, pageset+1, load, mxpg, mxln, mxpgst, False)])
                    bt_nextpage.place(x = bta+btc*6, y = btb)
                    for i in range(1, 6):
                        moveto = i-1+pageset*5
                        var_holder["bt_page" + str(i)].config(text = i+pageset*5, state = "active", command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False))
                else:
                    bt_nextpage = tk.Button(self.root, relief = "flat", bd = 0, width = 3, height = 3, activebackground = bg_colour, state = "disabled", text = "", bg = bg_colour)
                    bt_nextpage.place(x = bta+btc*6, y = btb)
                    leftpages = mxpg + 1 - mxpgst*5
                    for i in range(1, leftpages+1):
                        moveto = i-1+pageset*5
                        if i == 1:
                            var_holder["bt_page" + str(i)].config(text = i+pageset*5, fg = "#525252", bg = bg_colour, font = ("arial", 10, "underline"), state = "active", command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False))
                        else:
                            var_holder["bt_page" + str(i)].config(text = i+pageset*5, fg = "#525252", bg = bg_colour, font = ("arial", 10), state = "active", command = lambda moveto = moveto: dic_generate(moveto, pageset, load, mxpg, mxln, mxpgst, False))#Store current value of moveto
                    for i in range(leftpages+1, 6):
                        var_holder["bt_page" + str(i)].config(text = "•", fg = "#525252", bg = bg_colour, state = "disabled")

                if pageset > 0:
                    bt_prevpage = tk.Button(self.root, relief = "flat", bd = 0, width = 3, height = 3, text = "<", activebackground = bg_colour, bg = bg_colour, command = lambda pageset = pageset:[shift_set((pageset-1), load, mxpg, mxln, mxpgst, False), dic_generate(((pageset-1)*5+4), pageset-1, load, mxpg, mxln, mxpgst, False)])
                    bt_prevpage.place(x = bta+btc*0, y = btb)
                else:
                    bt_prevpage = tk.Button(self.root, relief = "flat", bd = 0, width = 3, height = 3, activebackground = bg_colour, state = "disabled", text = "", bg = bg_colour)
                    bt_prevpage.place(x = bta+btc*0, y = btb)

            locals().update(var_holder)
        #Show search result
        def showsearch(result):
            mx_page = int(len(result)/10)
            mx_line = len(result)%10
            mx_pageset = int(mx_page/5)

            page = 0
            pageset = 0

            dic_generate(page, pageset, result, mx_page, mx_line, mx_pageset, False)
            
            bta = 235
            btb = 450
            btc = 50
            
            shift_set(pageset, result, mx_page, mx_line, mx_pageset, False)
        #Sort dictionary.txt in alphabetical order
        def sort_file():
            f = open("Text/dictionary.txt")
            lines = open("Text/dictionary.txt").readlines()
            lines.sort()
            #for i in range(len(lines)):
            #    print(lines[i])
            f.close()
            writeFile = open("Text/dictionary.txt", "w+")
            for i in range(len(lines)):
                writeFile.write(lines[i])
        #Dictionary search function
        def search(keyword):
            lb_alrtsearch.config(text = "")
            keyword = keyword.strip()
            keyword = keyword.replace(" ", "")
            repeat = True
            repeat_counter = 0
            repeat_limit = len(keyword)
            while repeat == True:
                try:
                    ch = keyword[repeat_counter].lower()
                    if (ch not in alphabet) and (ch not in accented[0]) and (ch not in accented[1]) and (ch not in accented[2]) and (ch not in accented[3]) and (ch not in accented[4]):
                        if (ch not in signs):
                            lb_alrtsearch.config(text = "Invalid character detected")
                        keyword = keyword[:repeat_counter] + "" + keyword[repeat_counter+1:]
                        repeat_limit -= 1
                        repeat_counter -= 1
                    else:
                        for j in range(0, len(accented)):
                            if keyword[repeat_counter].lower() in accented[j]:
                                keyword = keyword[:repeat_counter] + vowel[j] + keyword[repeat_counter+1:]
                    repeat_counter += 1
                    if repeat_counter >= repeat_limit:
                        repeat = False
                except IndexError:
                    break
            matched = []
            global searchdic
            searchdic = []
            for i in range(0, len(syncdic)):
                if len(keyword) <= len(syncdic[i][0]):
                    if keyword == syncdic[i][0][:len(keyword)]:
                        exist = False
                        for j in range(0, len(matched)):
                            if syncdic[i][1] == matched[j]:
                                exist = True
                                break
                        if exist == False:
                            matched.append(syncdic[i][1])
                    
            for i in range(0, len(matched)):
                searchdic.append(dic[matched[i]])
                
            showsearch(searchdic)
        #Basic setup, link words with definitions
        def dictionary_setup():
            file = open("Text/dictionary.txt", "r")

            linecount = 0
            with open("Text/dictionary.txt", "r") as f:
                for line in f:
                    linecount += 1
            global dic
            #2D array for words: definition
            dic = []
            global syncdic
            #2D array for keeping track of words with same definition
            syncdic = []
            sync_count = 0

            for line in file:
                x = line.split("@")
                dic.append((x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip()))
                y = x[1].split(",")
                a = x[0].strip()
                syncdic.append((a, sync_count))
                for i in range(0, len(y)):
                    b = y[i].strip()
                    syncdic.append((b, sync_count))
                sync_count += 1
        #Key binding settings
        def pressed_left(pg, pgst, load, mxpg, mxln, mxpgst, firstLoad):
            if pg%5 == 0:
                if pgst > 0:
                    shift_set(pgst-1, load, mxpg, mxln, mxpgst, False)
                    dic_generate(pg-1, pgst-1, load, mxpg, mxln, mxpgst, False)
            else:
                dic_generate(pg-1, pgst, load, mxpg, mxln, mxpgst, False)               
        def pressed_right(pg, pgst, load, mxpg, mxln, mxpgst, firstLoad):
            if pg%5 == 4 and pgst != mxpgst:
                shift_set(pgst+1, load, mxpg, mxln, mxpgst, False)
                dic_generate(pg+1, pgst+1, load, mxpg, mxln, mxpgst, False)
            else:
                if pg != mxpg:
                    dic_generate(pg+1, pgst, load, mxpg, mxln, mxpgst, False)        
        def pressed_enter():
            search(self._searchbar.get("1.0", "end").lower())
            return "break"
        def focus_next_widget(widget):
            widget.tk_focusNext().focus()
            return "break"
        
        dic_tip = ["Tip: Use ↑ and ↓ keys to navigate through pages", "Tip: Search blank to view all words", "Tip: Check README to add words to the dictionary"]

        sort_file()
        dictionary_setup()
        #Create backup file
        copyfile("Text/dictionary.txt", "Text/dictionary_backup.txt")

        self.root = root
        self.root.focus()
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.title("LASY: Dictionary")
        self.root.configure(background = bg_colour)
        #Set widgets
        img_search = Image.open("Resource/search.png")
        self.root.img_search = ImageTk.PhotoImage(img_search)
        
        self._searchbar = tk.Text(root, highlightthickness = 2, height = 0, width = 50, padx = 2, pady = 6, font = ("times", 11))
        self._searchbar.place(x = 200, y = 24)
        self._searchbar.bind('<Return>', lambda event: pressed_enter())
        self._searchbar.bind("<Tab>", lambda event: focus_next_widget(self._searchbar))

        self.bt_search = tk.Button(root, relief = "flat", width = 29, height = 29, image = self.root.img_search, bg = "#76c0de", command = lambda: search(self._searchbar.get("1.0", "end").lower()))
        self.bt_search.place(x = 560, y = 24)
        
        global lb_alrtsearch
        lb_alrtsearch = tk.Label(self.root, width = 60, text = "", anchor = "w", bg = bg_colour, font = ("arial", 10), fg = "red")
        lb_alrtsearch.place(x = 200, y = 0)
        
        a = 60 #x start position
        b = 85 #y start position
        c = 35 #y space1
        d = 130 #y space2
        e = 330 #y space3
        f = 440 #y space4
        ft_size = 11
        page = 0
        pageset = 0

        max_page = int(len(dic)/10)
        max_line = len(dic)%10
        max_pageset = int(max_page/5)
        var_holder = {}

        dic_generate(page, pageset, dic, max_page, max_line, max_pageset, True)
        
        bta = 235
        btb = 430
        btc = 50
        
        shift_set(pageset, dic, max_page, max_line, max_pageset, True)

        #Show tip for 10 seconds
        try:
            if showtip.get() == "1":
                self.lb_dictips = tk.Label(root, width = 50, bg = bg_colour, anchor = "nw", font = ("arial", 10, "bold"), fg = "black", text = dic_tip[(random.randint(0,3)-1)])
                self.lb_dictips.place(x = 58, y = 60)
                self.root.after(10000, lambda: self.lb_dictips.destroy())
        except NameError:
            return None

        self.root.bind('<Up>', lambda event: pressed_left(page, pageset, dic, max_page, max_line, max_pageset, False))
        self.root.bind('<Down>', lambda event: pressed_right(page, pageset, dic, max_page, max_line, max_pageset, False))
        global bt_addword
        bt_addword = tk.Button(self.root, relief = "flat", bd = 1, activebackground = bg_colour, activeforeground = "black", bg = bg_colour, fg = "black", height = 1, width = 15, font = ("calibri", 10), text = "+ Add new word", command = lambda: self.new_window(addword))
        bt_addword.place(relx = 0.89, rely = 0.91, anchor = "center")
        self.root.iconbitmap('Resource/favicon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.onclose)

    #Activate Dictionary window button when closed
    def onclose(self):
        self.root.destroy()
        bt_dictionary.config(state = "active")
    #Open new window
    def new_window(self, _class):
        #Disable duplicate windows
        if str(_class) == "<class '__main__.addword'>":
            bt_addword.config(state = "disabled")
        self.new = tk.Toplevel(self.root)
        _class(self.new)
#Addword window
class addword:
    def __init__(self, root):
        def new_word():
            word = tt_word.get("1.0", "end")
            word = word.strip()
            form = tt_form.get("1.0", "end")
            form = form.strip()
            pofs = tt_pofs.get("1.0", "end")
            pofs = pofs.strip()
            _def = tt_def.get("1.0", "end")
            _def = _def.strip()
            if word == "" or form == "" or pofs == "" or _def == "":
                lb_alrt.config(text = "Missing input")
            else:
                writable = True
                nwrd = word+"@"+form+"@"+_def+"@"+pofs
                with open("Text/dictionary.txt", 'r') as f:
                    if nwrd in f.read():
                        writable = False
                if writable == True:
                    writeFile = open("Text/dictionary.txt", "a+")
                    writeFile.write("\n"+word+"@"+form+"@"+_def+"@"+pofs)
                    lb_alrt.config(text = "")
                    tt_word.delete('1.0', "end")
                    tt_form.delete('1.0', "end")
                    tt_pofs.delete('1.0', "end")
                    tt_def.delete('1.0', "end")
                else:
                    lb_alrt.config(text = "Existing word")
        self.root = root
        self.root.focus()
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.title("LASY: Dictionary")
        self.root.configure(background = bg_colour)
        lb_word = tk.Label(self.root, width = 20, bg = bg_colour, font = ("arial", 10, "bold"), fg = "black", text = "Word")
        lb_word.place(relx = 0.2, rely = 0.1, anchor = "center")
        lb_form = tk.Label(self.root, width = 20, bg = bg_colour, font = ("arial", 10, "bold"), fg = "black", text = "Alternate forms")
        lb_form.place(relx = 0.2, rely = 0.3, anchor = "center")
        lb_pofs = tk.Label(self.root, width = 20, bg = bg_colour, font = ("arial", 10, "bold"), fg = "black", text = "Part of speech")
        lb_pofs.place(relx = 0.2, rely = 0.5, anchor = "center")
        lb_def = tk.Label(self.root, width = 20, bg = bg_colour, font = ("arial", 10, "bold"), fg = "black", text = "Definition")
        lb_def.place(relx = 0.2, rely = 0.7, anchor = "center")

        tt_word = tk.Text(self.root, bd = 4, relief = "flat", xscrollcommand = True, highlightthickness = 2, height = 0, width = 30, font = ("times", 11))
        tt_word.bind('<Return>', lambda event: pressed_enter())
        tt_word.bind("<Tab>", lambda event: focus_next_widget(tt_word))
        tt_word.place(relx = 0.66, rely = 0.1, anchor = "center")
        tt_form = tk.Text(self.root, bd = 4, relief = "flat", xscrollcommand = True, highlightthickness = 2, height = 0, width = 30, font = ("times", 11))
        tt_form.bind('<Return>', lambda event: pressed_enter())
        tt_form.bind("<Tab>", lambda event: focus_next_widget(tt_form))
        tt_form.place(relx = 0.66, rely = 0.3, anchor = "center")
        tt_pofs = tk.Text(self.root, bd = 4, relief = "flat", xscrollcommand = True, highlightthickness = 2, height = 0, width = 30, font = ("times", 11))
        tt_pofs.bind('<Return>', lambda event: pressed_enter())
        tt_pofs.bind("<Tab>", lambda event: focus_next_widget(tt_pofs))
        tt_pofs.place(relx = 0.66, rely = 0.5, anchor = "center")
        tt_def = tk.Text(self.root, bd = 4, relief = "flat", xscrollcommand = True, highlightthickness = 2, height = 0, width = 30, font = ("times", 11))
        tt_def.bind('<Return>', lambda event: pressed_enter())
        tt_def.bind("<Tab>", lambda event: focus_next_widget(tt_def))
        tt_def.place(relx = 0.66, rely = 0.7, anchor = "center")

        bt_enter = tk.Button(self.root, text = "Submit", relief = "flat", bg = bg_colour, activebackground = bg_colour, bd = 0, anchor = "center", font = ("malgun gothic", 12, "underline"), width = 15, height = 2, command= lambda: new_word())
        bt_enter.place(relx = 0.5, rely = 0.89, anchor = "center")

        lb_alrt = tk.Label(self.root, width = 20, bg = bg_colour, font = ("arial", 10), fg = "red", text = "")
        lb_alrt.place(relx = 0.5, rely = 0.8, anchor = "center")
        
        self.root.iconbitmap('Resource/favicon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.onclose)
        def focus_next_widget(widget):
            widget.tk_focusNext().focus()
            return "break"
        def pressed_enter():
            new_word()
            return "break"
    #Activate Dictionary window button when closed
    def onclose(self):
        self.root.destroy()
        bt_addword.config(state = "active")
#Main algorithms
class algorithm:
    def clear_text():
        entry.insert(tk.END, "")
    #Make public lists to be used across classes
    #These lists contain basic alphabets for validation and bits(prefix, postfix etc.) to be used in further algorithms
    global signs, alphabet, vowel, accented, liquids, stop, m_ending, h_start, diphthong, all_diphthongs, q_diphthong, i_to_j, ui_exception, eu_exception, ei_exception, oi_exception, i_to_j_exception, sets_front, sets_middle, sets_back
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    vowel = ["a", "e", "i", "o", "u", "y"]
    accented = [["ã", "á", "à", "ä", "ă", "ā"], ["è", "é", "ë", "ě", "ē"], ["ì", "í", "ï", "ĭ", "ī"], ["ò", "ó", "ö", "ŏ", "ō"], ["ù", "ú", "ü", "ŭ", "ū"],["ȳ"]]
    signs = [".", ",", ";", ":", '"', "'", "!", "?"]
    liquids = ["l", "r"]
    stop = ["b", "c", "d", "g", "p", "t"]
    m_ending = ["am", "em", "im", "om", "um"]
    h_start = ["ha", "he", "hi", "ho", "hu", "hy"]
    diphthong = ["ae", "ai", "au", "oe"]
    all_diphthongs = ["ae", "ai", "au", "oe", "ui", "eu", "ei", "oi"]
    q_diphthong = ["ua", "ui", "ue", "uo"]
    i_to_j = ["ia", "ie", "io", "iu"]
    sets_front = ["ch", "th", "st", "sc", "sp", "gn", "ph"]
    sets_middle = ["ch", "ph", "sp", "st", "sc", "th"]
    sets_back = ["mp", "ns"]
    #List of exceptions that does not follow the normal rule of the Latin language. Must be updated if new exceptions are reported by users.
    ui_exception = ["cui", "hui"]
    eu_exception = ["ceu", "seu", "heu", "neu", "teu"]
    ei_exception = ["dein", "hei", "eia", "viei"]
    oi_exception = ["proin"]
    i_to_j_exception = ["troia", "coniunx", "coniug", "deie"]
    @staticmethod
    #Function separating syllables
    def syllable_sequence():
        sentence = entry.get("1.0", "end")
        sentence = sentence.strip()
        sentence = sentence.replace("  ", " ")
        sentence = sentence.replace("   ", " ")
        
        global words
        words = sentence.split(" ")
        words = [x for x in words if x != " "]

        no_value = True
        for i in range(len(words)):
            if len(words[i]) > 0:
                no_value = False
                break

        #Alert for no input value
        if no_value == True:
            lb_alert.config(text = "Please enter your sentence")
        else:
            lb_alert.config(text = "")

        algorithm.format_check()
        algorithm.consonantal_i()
        algorithm.diphthong_exceptions()
        algorithm.elision()

        global output_sentence
        output_sentence = "@@@@@@@" + " ".join(output) + "@@@"

        repeater = len(output_sentence) - 1
        #Check for two same consonants
        for i in range(repeater):
            if output_sentence[i] == output_sentence[i+1] and output_sentence[i] not in vowel:
                output_sentence = output_sentence[:i+1] + "/" + output_sentence[i+1:]
                repeater = repeater + 1
        repeater = len(output_sentence) - 1
        skip = -1
        repeater = len(output_sentence)-1
        #Algorithm for dividing words into syllables
        for i in range(repeater):
            if i <= skip:
                continue
            try:
                if output_sentence[repeater-i].lower() in vowel:
                    if output_sentence[repeater-i-1:repeater-i+1].lower() in diphthong:
                        if output_sentence[repeater-i-2:repeater-i].lower() in q_diphthong and (output_sentence[repeater-i-3].lower() == "q"):
                            if output_sentence[repeater-i-4] == " ":
                                output_sentence = output_sentence[:repeater-i-4] + "/" + output_sentence[repeater-i-4:]
                                skip = i + 5
                                repeater = repeater + 1
                            elif output_sentence[repeater-i-4] not in ["/"," ", "(", ")"]:
                                output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                skip = i + 4
                                repeater = repeater + 1
                        else:
                            if output_sentence[repeater-i-2].lower() in liquids:
                                if output_sentence[repeater-i-2] == output_sentence[repeater-i-3]:
                                    output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                    skip = i + 2
                                elif (output_sentence[repeater-i-3].lower() not in vowel) and (output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]):
                                    if (output_sentence[repeater-i-4:repeater-i-2].lower() in sets_front) and (output_sentence[repeater-i-5] in [" ", "@"]):
                                        output_sentence = output_sentence[:repeater-i-5] + "/" + output_sentence[repeater-i-5:]
                                        skip = i + 5
                                    else:
                                        if output_sentence[repeater-i-4] not in ["/"," ", "(", ")"]:
                                            output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                            skip = i + 3
                                else:
                                    if output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]:
                                        output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                        skip = i + 3
                                    elif output_sentence[repeater-i-3] == " " and output_sentence[repeater-i-4] not in ["/"," ", "(", ")"]:
                                        output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                        skip = i + 4
                                    else:
                                        skip = i + 3
                            else:
                                if (output_sentence[repeater-i-3:repeater-i-1].lower() in sets_front) and (output_sentence[repeater-i-4] not in ["/"," ", "(", ")"]):
                                    output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                    skip = i + 3
                                elif output_sentence[repeater-i-2].lower() in vowel:
                                    output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                    skip = i + 1
                                else:
                                    if output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]:
                                        output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                        skip = i + 2
                    else:
                        if (output_sentence[repeater-i-1:repeater-i+1].lower() in q_diphthong) and (output_sentence[repeater-i-2].lower() == "q"):
                            if output_sentence[repeater-i-3] == " ":
                                output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                skip = i + 4
                                repeater = repeater + 1
                            elif output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]:
                                output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                skip = i + 3
                                repeater = repeater + 1
                        else:
                            if output_sentence[repeater-i-1].lower() in vowel:
                                if output_sentence[repeater-i-1:repeater-i+1].lower() == "ui":
                                    for j in range(len(ui_exception)):
                                        if ui_exception[j] == output_sentence[repeater-i-2:repeater-i+1].lower():
                                            if output_sentence[repeater-i-3] == " ":
                                                output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                                skip = i + 4
                                            else:
                                                output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                                skip = i + 3
                                            break
                                        if j == len(ui_exception)-1:
                                            output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                                elif output_sentence[repeater-i-1:repeater-i+1].lower() == "eu":
                                    for j in range(len(eu_exception)):
                                        if eu_exception[j] == output_sentence[repeater-i-2:repeater-i+1].lower():
                                            if output_sentence[repeater-i-3] == " ":
                                                output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                                skip = i + 4
                                            else:
                                                output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                                skip = i + 3
                                            break
                                        if j == len(eu_exception)-1:
                                            output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                                else:
                                    output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                            elif output_sentence[repeater-i-1:repeater-i+1].lower() == "$i":
                                skip = i + 1
                            elif output_sentence[repeater-i-1].lower() in liquids:
                                #print(output_sentence[repeater-i-3:repeater-i-1])
                                if (output_sentence[repeater-i-2].lower() not in vowel) and (output_sentence[repeater-i-3:repeater-i-1].lower() not in sets_front) and (output_sentence[repeater-i-2] not in ["/"," ", "(", ")"]) and (output_sentence[repeater-i-2].lower() != output_sentence[repeater-i-1].lower()):
                                    if (output_sentence[repeater-i-3:repeater-i-1].lower() in sets_front) and (output_sentence[repeater-i-4] not in ["/"," ", "(", ")"]):
                                        output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                        skip = i + 3
                                        repeater = repeater + 1
                                    else:
                                        if output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]:
                                            output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                            skip = i + 2
                                            repeater = repeater + 1
                                else:
                                    if output_sentence[repeater-i-3:repeater-i-1].lower() in sets_front and output_sentence[repeater-i-4] == " ":
                                            output_sentence = output_sentence[:repeater-i-4] + "/" + output_sentence[repeater-i-4:]
                                            skip = i + 4
                                            repeater = repeater + 1
                                    else:
                                        if output_sentence[repeater-i-2] not in ["/"," ", "(", ")"]:
                                            output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                            skip = i + 2
                                            repeater = repeater + 1
                                        elif (output_sentence[repeater-i-2] == " ") and (output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]):
                                            output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                            skip = i + 2
                                        else:
                                            skip = i + 2
                            #elif output_sentence[repeater-i-1].lower() == "h":
                             #   print("C5")
                              #  if (
                            else:
                                if (output_sentence[repeater-i-2:repeater-i].lower() in sets_front) and (output_sentence[repeater-i-3] in [" ", "@"]):
                                    output_sentence = output_sentence[:repeater-i-3] + "/" + output_sentence[repeater-i-3:]
                                    skip = i + 4
                                    repeater = repeater + 1
                                elif (output_sentence[repeater-i-2:repeater-i].lower() in sets_middle) and (output_sentence[repeater-i-3] != " "):
                                    if output_sentence[repeater-i-3] not in ["/"," ", "(", ")"]:
                                        output_sentence = output_sentence[:repeater-i-2] + "/" + output_sentence[repeater-i-2:]
                                        skip = i + 3
                                        repeater = repeater + 1
                                    else:
                                        skip = i + 3
                                elif output_sentence[repeater-i-1] == " ":
                                    if output_sentence[repeater-i-2] != ")":
                                        output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                        skip = i + 2
                                    else:
                                        skip = i
                                elif output_sentence[repeater-i-2] not in ["/"," ", "(", ")"]:
                                    if (output_sentence[repeater-i-1].lower() == "x") and (output_sentence[repeater-i-2].lower() in vowel):
                                        output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                                    else:
                                        output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                        skip = i + 2
                                        repeater = repeater + 1
                #If not vowel
                elif output_sentence[repeater-i] == ")":
                    if output_sentence[repeater-i-2] == "(":
                        skip = i + 2
                    elif output_sentence[repeater-i-3] == "(":
                        skip = i + 3
                else:
                    if output_sentence[repeater-i-1] == " ":
                        if output_sentence[repeater-i-2] == ")":
                            if output_sentence[repeater-i-4] == "(":
                                skip = i + 2
                            elif output_sentence[repeater-i-5] == "(":
                                skip = i + 3
                        else:
                            output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                            repeater = repeater + 1
                    elif output_sentence[repeater-i+1] == "(" and output_sentence[repeater-i] != "/":
                        if (output_sentence[repeater-i].lower() in liquids):
                            if (output_sentence[repeater-i-1].lower() not in vowel) and (output_sentence[repeater-i-1] not in ["/"," ", "(", ")"]):
                                if(output_sentence[repeater-i-2].lower() in vowel):
                                    output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                    repeater = repeater + 1
                                elif (output_sentence[repeater-i-2] not in ["/"," ", "(", ")"]) and (output_sentence[repeater-i-3].lower() in vowel):
                                    output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                                    skip = i + 3
                            elif (output_sentence[repeater-i-1].lower() in vowel):
                                output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                        elif (output_sentence[repeater-i-1:repeater-i+1].lower() in sets_front) and (output_sentence[repeater-i-2].lower() in vowel):
                            output_sentence = output_sentence[:repeater-i-1] + "/" + output_sentence[repeater-i-1:]
                            skip = i + 1
                            repeater = repeater + 1
                        elif output_sentence[repeater-i-1].lower() in vowel:
                            output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]
                        elif (output_sentence[repeater-i-1].lower() not in vowel) and (output_sentence[repeater-i-1] not in ["/"," ", "(", ")"]) and (output_sentence[repeater-i-1:repeater-i+1] not in sets_front):
                            output_sentence = output_sentence[:repeater-i] + "/" + output_sentence[repeater-i:]           
            except IndexError:
                i = repeater

        output_sentence = output_sentence.replace("@//", "")
        output_sentence = output_sentence.replace("@/", "")
        output_sentence = output_sentence.replace("@", "")
        output_sentence = output_sentence.replace("$", "")
        #check_syllable_number
        global syllable
        syllable = 0
        for i in range(len(output_sentence)):
            if output_sentence[i] == "/":
                syllable = syllable + 1
        if syllable != 0:
            syllable = syllable + 1
        else:
            for i in range(len(vowel)):
                if vowel[i] in output_sentence:
                    syllable = syllable + 1
                    break
        #Display separated syllables
        lb_syllable.config(text = output_sentence)
        lb_scansion.config(text = "", font = ("arial", 13))
        #Check if scansion is valid, activate button of possible meter, output error if both are impossible
        if 13 <= syllable <= 14:
            lb_scansion.config(fg = "black", font = ("arial", 13))
            bt_penta.config(state = "active")
            bt_hexa.config(state = "active")
        elif 12 == syllable:
            lb_scansion.config(fg = "black", font = ("arial", 13))
            bt_hexa.config(state = "disabled")
            bt_penta.config(state = "active")
        elif 15 <= syllable <= 17:
            lb_scansion.config(fg = "black", font = ("arial", 13))
            bt_hexa.config(state = "active")
            bt_penta.config(state = "disabled")
        elif syllable > 17:
            lb_scansion.config(fg = "red", text = "Too many syllables for both scansion", font = ("arial", 11))
            bt_hexa.config(state = "disabled")
            bt_penta.config(state = "disabled")
        else:
            bt_hexa.config(state = "disabled")
            bt_penta.config(state = "disabled")
            if len(output_sentence) == 0:
                lb_scansion.config(text = "", font = ("arial", 13))
            else:
                lb_scansion.config(fg = "red", text = "Insufficient syllables for both scansion", font = ("arial", 11))
    #Check input validity       
    def format_check():
        for i in range(len(words)):
            repeat_counter = 0
            repeat_limit = len(words[i])
            repeat = True
            while repeat == True:
                try:
                    ch = words[i][repeat_counter].lower()
                    if (ch not in alphabet) and (ch not in accented[0]) and (ch not in accented[1]) and (ch not in accented[2]) and (ch not in accented[3]) and (ch not in accented[4]):
                        if (ch not in signs):
                            lb_alert.config(text = "Invalid character detected")
                        words[i] = words[i][:repeat_counter] + "" + words[i][repeat_counter+1:]
                        repeat_limit = repeat_limit - 1
                        repeat_counter = repeat_counter - 1
                    else:
                        for j in range(len(accented)):
                            if (words[i][repeat_counter].lower() in accented[j]) == True:
                                words[i] = words[i][:repeat_counter] + vowel[j] + words[i][repeat_counter+1:]
                    repeat_counter = repeat_counter + 1
                    if repeat_counter >= repeat_limit:
                        repeat = False
                except IndexError:
                    return None
        global save_history
        save_history = ""
        for i in range(len(words)):
            save_history = save_history + words[i] + " "
        save_history = save_history.strip()
    #Change consonantal i's to j
    def consonantal_i():
        for i in range(len(words)):
                if words[i][:2].lower() in i_to_j:
                    if words[i][0] == "I":
                        words[i] = "J" + words[i][1:]
                    else:
                        words[i] = "j" + words[i][1:]

        global output
        output = words[:]
        
        for i in range(len(i_to_j_exception)):
            for j in range(len(output)):
                if i_to_j_exception[i] in output[j].lower():
                    output[j] = output[j][:len(i_to_j_exception[i])].replace("i", "j") + output[j][len(i_to_j_exception[i]):]
    #Distinguish diphthongs out of two consecutive vowels
    def diphthong_exceptions():
        for i in range(len(ei_exception)):
            for j in range(len(output)):
                if ei_exception[i] in output[j].lower():
                    output[j] = output[j].replace("ei", "e$i")
        for i in range(len(oi_exception)):
            for j in range(len(output)):
                if oi_exception[i] in output[j].lower():
                    output[j] = output[j].replace("oi", "o$i")
    #Add parentheses around syllable that is being silenced due to elision
    def elision():
        for i in range(len(words)-1):
            if (words[i][-1:].lower() in vowel or words[i][-2:].lower() in m_ending) and (words[i+1][:1].lower() in vowel or words[i+1][:2].lower() in h_start):
                if words[i][-1:].lower() in vowel:
                    if words[i][-2:].lower() in diphthong:
                        if words[i][-3:-2] in vowel:
                            if words[i][-4:-3].lower() == "q":
                                output[i] = output[i][:len(output[i])-2]+ '('+ output[i][len(output[i])-2:] + ')'
                                words[i] = words[i][:-2]
                            else:
                                output[i] = output[i][:len(output[i])-2]+ '/(' + output[i][len(output[i])-2:] + ')'
                                words[i] = words[i][:-2]
                        else:
                            output[i] = output[i][:len(output[i])-2]+ '(' + output[i][len(output[i])-2:] + ')'
                            words[i] = words[i][:-2]
                    else:
                        if words[i][-2:-1] in vowel:
                            if words[i][-3:-2].lower() == "q":
                                output[i] = output[i][:len(output[i])-1] + '(' + output[i][len(output[i])-1:] + ')'
                                words[i] = words[i][:-1]
                            else:
                                output[i] = output[i][:len(output[i])-1] + '/(' + output[i][len(output[i])-1:] + ')'
                                words[i] = words[i][:-1]
                        else:
                            output[i] = output[i][:len(output[i])-1] + '(' + output[i][len(output[i])-1:] + ')'
                            words[i] = words[i][:-1]
                else:
                    output[i] = output[i][:len(output[i])-2]+ '(' + output[i][len(output[i])-2:] + ')'
                    words[i] = words[i][:-2]
    #Function for scanning in hexameter
    def hexameter():
        lb_scansion.config(text = "")
        w_space = output_sentence.split("/")
        syllables = [None] * len(w_space)
        for i in range(len(w_space)):
            syllables[i] = w_space[i]
        delete = False
        for i in range(syllable-1):
            syllables[i] = syllables[i].replace(" ", "").lower()
            w_space[i] = w_space[i].lower()
            a = -1
            b = -1
            for j in range(len(syllables[i])):
                if syllables[i][j] == "(":
                    a = j
                elif syllables[i][j] == ")":
                    b = j + 1
            syllables[i] = syllables[i][:a] + syllables[i][b:]

        feet = [None] * syllable

        feet[syllable-1] = "x"
        feet[syllable-2] = "–"
        feet[syllable-3] = "⏑"
        feet[syllable-4] = "⏑"
        feet[syllable-5] = "–"

        filled = False

        left = syllable - 5
        dactyl = left - 8
        spondee = 12 - left
        #left_set = 4
        repeated = 0
        skip = -1
        z = ""
        for i in range(left):
            #print(i)
            if i <= skip:
                continue
            try:
                if feet[1] == "–":
                    feet[0] = "–"
                #If only one set is left
                if spondee == 0 and syllable-6-i != 0 and syllable-7-i != 0:
                    #print("A")
                    dactyl = dactyl - 1
                    feet[syllable-6-i] = "⏑"
                    feet[syllable-7-i] = "⏑"
                    feet[syllable-8-i] = "–"
                    skip = i + 2
                    z = z + "d"
                elif dactyl == 0:
                    #print("B")
                    spondee = spondee - 1
                    feet[syllable-6-i] = "–"
                    feet[syllable-7-i] = "–"
                    skip = i + 1
                    z = z + "s"
                else:
                    #Check for q
                    if "q" not in syllables[syllable-6-i] or "q" not in syllables[syllable-7-i]:
                        #print("C")
                        #Long if diphthong
                        for j in range(len(all_diphthongs)):
                            if all_diphthongs[j] in syllables[syllable-6-i] or all_diphthongs[j] in syllables[syllable-7-i]:
                                #print("D")
                                spondee = spondee - 1
                                feet[syllable-6-i] = "–"
                                feet[syllable-7-i] = "–"
                                skip = i + 1
                                z = z + "s"
                                break
                            else:
                                #Short if two vowels are adjacent and not diphthong
                                #print("D1")
                                if j == len(all_diphthongs)-1:
                                    if (syllables[syllable-6-i][-1] in vowel and syllables[syllable-5-i][0] in vowel) or (syllables[syllable-7-i][-1] in vowel and syllables[syllable-6-i][0] in vowel):
                                        #print("E")
                                        dactyl = dactyl - 1
                                        feet[syllable-6-i] = "⏑"
                                        feet[syllable-7-i] = "⏑"
                                        feet[syllable-8-i] = "–"
                                        skip = i + 2
                                        z = z + "d"
                                        break
                    else:
                        #Short if que
                        #print("C1")
                        if "que" in syllables[syllable-6-i] or "que" in syllables[syllable-7-i]:
                            #print("C2")
                            dactyl = dactyl - 1
                            feet[syllable-6-i] = "⏑"
                            feet[syllable-7-i] = "⏑"
                            feet[syllable-8-i] = "–"
                            skip = i + 2
                            z = z + "d"
                            break
                    if feet[syllable-6-i] == None:
                        #print("F")
                        _5i0 = syllables[syllable-5-i][0]
                        _5i1 = syllables[syllable-5-i][1]
                        _5i_1 = syllables[syllable-5-i][-1]
                        _5i_2 = syllables[syllable-5-i][-2]
                        _6i0 = syllables[syllable-6-i][0]
                        _6i1 = syllables[syllable-6-i][1]
                        _6i_1 = syllables[syllable-6-i][-1]
                        _6i_2 = syllables[syllable-6-i][-2]
                        _7i0 = syllables[syllable-7-i][0]
                        _7i1 = syllables[syllable-7-i][1]
                        _7i_1 = syllables[syllable-7-i][-1]
                        _7i_2 = syllables[syllable-7-i][-2]
                        #Long if two consonants are adjacent and not liquids
                        if ((_6i0 not in vowel and _6i0 not in liquids and _7i_1 not in vowel) or (_6i0 not in vowel and _6i1 not in vowel and _6i1 not in liquids)) or (_7i_1 not in vowel and _7i_1 not in liquids and _7i_2 not in vowel) or (_5i0 not in vowel and _5i1 not in vowel and _5i1 not in liquids) or (_6i_1 not in vowel and _5i0 not in vowel and _5i0 not in liquids) or (_6i_1 not in vowel and _6i_1 not in liquids and _6i_2 not in vowel):
                            #print("G")
                            spondee = spondee - 1
                            feet[syllable-6-i] = "–"
                            feet[syllable-7-i] = "–"
                            skip = i + 1
                            z = z + "s"
                        else:
                            #Assume long if o present withought liquid consonant
                            if (_7i_1 in ["o", "u", "i"] and w_space[syllable-6-i][0] == " ") or (_6i_1 in ["o", "u", "i"] and w_space[syllable-5-i][0] == " "): #and w_space[syllable-6-i][1] not in vowel and w_space[syllable-6-i][1] not in liquids and w_space[syllable-6-i][1] != "v"):
                                spondee = spondee - 1
                                feet[syllable-6-i] = "–"
                                feet[syllable-7-i] = "–"
                                skip = i + 1
                                z = z + "s"
                            else:
                                #print("H")
                                dactyl = dactyl - 1
                                feet[syllable-6-i] = "⏑"
                                feet[syllable-7-i] = "⏑"
                                feet[syllable-8-i] = "–"
                                skip = i + 2
                                z = z + "d"
            except IndexError:
                i = left
        if dactyl == 1:
            for i in range(len(feet)):
                if feet[i] == None:
                    feet[i] = "⏑"
        elif spondee == 1:
            for i in range(len(feet)):
                if feet[i] == None:
                    feet[i] = "–"
        scansion_output = ""
        d_counter = 0
        s_counter = 0
        for i in range(len(feet)):
            if feet[i] == "–":
                s_counter = s_counter + 1
            if feet[i] == "⏑":
                d_counter = d_counter + 1
                s_counter = 0
            if d_counter == 2 or s_counter == 2:
                scansion_output = scansion_output + " " + feet[i] + " |"
                d_counter = 0
                s_counter = 0
            else:
                scansion_output = scansion_output + " " + feet[i]

        writable = True
        hstry = "hexa@"+save_history+"@"+z+"\n"
        with open("Text/search_history.txt", 'r') as fx:
            if hstry in fx.read():
                writable = False
        if writable == True:
            writeFile = open("Text/search_history.txt", "a+")
            writeFile.write("hexa@"+save_history+"@"+z+"\n")
        #Display scansion
        lb_scansion.config(text = scansion_output)

    #Function for scanning in pentameter
    def pentameter():
        z = ""
        lb_scansion.config(text = "")
        syllables = output_sentence.split("/")
        delete = False
        for i in range(syllable-1):
            syllables[i] = syllables[i].replace(" ", "").lower()
            a = -1
            b = -1
            for j in range(len(syllables[i])):
                if syllables[i][j] == "(":
                    a = j
                elif syllables[i][j] == ")":
                    b = j + 1
            syllables[i] = syllables[i][:a] + syllables[i][b:]

        feet = [None] * syllable

        feet[syllable-1] = "–"
        feet[syllable-2] = "⏑"
        feet[syllable-3] = "⏑"
        feet[syllable-4] = "–"
        feet[syllable-5] = "⏑"
        feet[syllable-6] = "⏑"
        feet[syllable-7] = "-"
        feet[syllable-8] = "-"

        filled = False

        left = syllable - 8
        dactyl = left - 4
        spondee = 6 - left
        repeated = 0
        skip = -1
        for i in range(left):
            if i <= skip:
                continue
            try:
                #If only one set is left
                if spondee == 0:
                    dactyl = dactyl - 1
                    feet[syllable-9-i] = "⏑"
                    feet[syllable-10-i] = "⏑"
                    feet[syllable-11-i] = "–"
                    skip = i + 2
                    z = z + "d"
                elif dactyl == 0:
                    spondee = spondee - 1
                    feet[syllable-9-i] = "–"
                    feet[syllable-10-i] = "–"
                    skip = i + 1
                    z = z + "s"
                else:
                    #Check for q
                    if "q" not in syllables[syllable-9-i] or "q" not in syllables[syllable-10-i]:
                        for j in range(len(all_diphthongs)):
                            #Long if diphthong
                            if all_diphthongs[j] in syllables[syllable-9-i] or all_diphthongs[j] in syllables[syllable-10-i]:
                                spondee = spondee - 1
                                feet[syllable-9-i] = "–"
                                feet[syllable-10-i] = "–"
                                skip = i + 1
                                z = z + "s"
                                break
                            else:
                                #Short if two vowels are adjacent and not diphthong
                                if j == len(all_diphthongs)-1:
                                    if (syllables[syllable-9-i][-1] in vowel and syllables[syllable-8-i][0] in vowel) or (syllables[syllable-10-i][-1] in vowel and syllables[syllable-9-i][0] in vowel):
                                        dactyl = dactyl - 1
                                        feet[syllable-9-i] = "⏑"
                                        feet[syllable-10-i] = "⏑"
                                        feet[syllable-11-i] = "–"
                                        skip = i + 2
                                        z = z + "d"
                                        break
                    else:
                        #Short if que
                        if "que" in syllables[syllable-9-i] or "que" in syllables[syllable-10-i]:
                            dactyl = dactyl - 1
                            feet[syllable-9-i] = "⏑"
                            feet[syllable-10-i] = "⏑"
                            feet[syllable-11-i] = "–"
                            skip = i + 2
                            z = z + "d"
                            break
                    if feet[syllable-9-i] == None:
                        _5i0 = syllables[syllable-8-i][0]
                        _5i1 = syllables[syllable-8-i][1]
                        _5i_1 = syllables[syllable-8-i][-1]
                        _5i_2 = syllables[syllable-8-i][-2]
                        _6i0 = syllables[syllable-9-i][0]
                        _6i1 = syllables[syllable-9-i][1]
                        _6i_1 = syllables[syllable-9-i][-1]
                        _6i_2 = syllables[syllable-9-i][-2]
                        _7i0 = syllables[syllable-10-i][0]
                        _7i1 = syllables[syllable-10-i][1]
                        _7i_1 = syllables[syllable-10-i][-1]
                        _7i_2 = syllables[syllable-10-i][-2]
                        #Long if two consonants are adjacent and not liquids 
                        if ((_6i0 not in vowel and _6i0 not in liquids and _7i_1 not in vowel) or (_6i0 not in vowel and _6i1 not in vowel and _6i1 not in liquids)) or (_7i_1 not in vowel and _7i_1 not in liquids and _7i_2 not in vowel) or (_5i0 not in vowel and _5i1 not in vowel and _5i1 not in liquids) or (_6i_1 not in vowel and _5i0 not in vowel and _5i0 not in liquids) or (_6i_1 not in vowel and _6i_1 not in liquids and _6i_2 not in vowel):
                            spondee = spondee - 1
                            feet[syllable-9-i] = "–"
                            feet[syllable-10-i] = "–"
                            skip = i + 1
                            z = z + "s"
                        else:
                            #Assume long if o present withought liquid consonant                            
                            if (_6i_1 == "o" and _5i0 not in vowel and _5i0 not in liquids) or (_5i_1 == "o" and _6i0 not in vowel and _6i0 not in liquids):
                                spondee = spondee - 1
                                feet[syllable-9-i] = "–"
                                feet[syllable-10-i] = "–"
                                skip = i + 1
                                z = z + "s"
                            else:
                                dactyl = dactyl - 1
                                feet[syllable-9-i] = "⏑"
                                feet[syllable-10-i] = "⏑"
                                feet[syllable-11-i] = "–"
                                skip = i + 2
                                z = z + "d"
            except IndexError:
                i = left

        scansion_output = ""
        d_counter = 0
        s_counter = 0
        for i in range(len(feet)-8):
            if feet[i] == "–":
                s_counter = s_counter + 1
            elif feet[i] == "⏑":
                d_counter = d_counter + 1
                s_counter = 0
            if d_counter == 2 or s_counter == 2:
                scansion_output = scansion_output + " " + feet[i] + " |"
                d_counter = 0
                s_counter = 0
            else:
                scansion_output = scansion_output + " " + feet[i]
        scansion_output = scansion_output+ " - || - ⏑ ⏑ | - ⏑ ⏑ | -"

        writable = True
        hstry = "penta@"+save_history+"@"+z+"\n"
        with open("Text/search_history.txt", 'r') as fx:
            if hstry in fx.read():
                writable = False
        if writable == True:
            writeFile = open("Text/search_history.txt", "a+")
            writeFile.write("penta@"+save_history+"@"+z+"\n")
            
        #Display scansion
        lb_scansion.config(text = scansion_output)
#Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = main(root)
    root.iconbitmap('Resource/favicon.ico')
    root.mainloop()
