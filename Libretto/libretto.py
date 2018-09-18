'''
Created on Feb 20, 2018

@author: Odelin Charron
'''
import Queue
from ScrolledText import ScrolledText
from Tkconstants import END
from Tkinter import Text, Tk, IntVar
import sys
from tkFileDialog import askopenfilename
import tkFont
import ttk


FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

DefaultFileNameMRIImage = "X_"
DefaultFileNameMRIMasks = "Y_"
DefaultFileNameOther = "Z_"
DefaultFileNameMatrix = "T_"
DefaultDirectory = "D_"
DefaultName = "n_"
DefaultWarning = "!!"
DefaultTitle = "="
DefaultSubTitle = "~"
DefaultSubSubTitle = "*"
DefaultComment = "#"
DefaultValidate = ">"
DefaultParameter = "p_"


def DeleteTabulation(str0):
    ''' Handle the tabulation '''
    if str0[0] == " ":
        while str0[0] == " ":
            str0 = str0[1:]
    return str0


class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''

    def __init__(self, text_area):
        self.text_area = text_area


class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''

    def write(self, str0):
        '''  '''
        try:
            # Handle the tabulation
            try:
                str1 = DeleteTabulation(str0)
            except:
                str1 = str0

            global DefaultFileNameMRIImage
            global DefaultFileNameMRIMasks
            global DefaultFileNameOther
            global DefaultFileNameMatrix
            global DefaultDirectory
            global DefaultName
            global DefaultWarning
            global DefaultTitle
            global DefaultSubTitle
            global DefaultSubSubTitle
            global DefaultComment
            global DefaultValidate
            global DefaultParameter

            if str1[0:len(DefaultSubTitle)] == DefaultSubTitle:
                self.text_area.insert("end", str0, 'subTitle')
            elif str1[0:len(DefaultSubSubTitle)] == DefaultSubSubTitle:
                self.text_area.insert("end", str0, 'subsubTitle')
            elif str1[0:len(DefaultParameter)] == DefaultParameter:
                self.text_area.insert("end", str0, 'param')
            elif str1[0:len(DefaultTitle)] == DefaultTitle:
                self.text_area.insert(END, "\n")
                self.text_area.insert("end", str0, 'Title')
            elif str1[0:len(DefaultComment)] == DefaultComment:
                self.text_area.insert("end", str0, 'comment')
            elif str1[0:len(DefaultFileNameMRIImage)] == DefaultFileNameMRIImage:
                self.text_area.insert("end", "   " + str0, 'File')
            elif str1[0:len(DefaultFileNameMRIMasks)] == DefaultFileNameMRIMasks:
                self.text_area.insert("end", "   " + str0, 'File')
            elif str1[0:len(DefaultFileNameOther)] == DefaultFileNameOther:
                self.text_area.insert("end", "   " + str0, 'FileOther')
            elif str1[0:len(DefaultFileNameMatrix)] == DefaultFileNameMatrix:
                self.text_area.insert("end", "   " + str0, 'File')
            elif str1[0:len(DefaultDirectory)] == DefaultDirectory:
                self.text_area.insert("end", "   " + str0, 'Directory')
            elif str1[0:len(DefaultWarning)] == DefaultWarning:
                self.text_area.insert("end", str0, 'warn')
            elif str1[0:len(DefaultValidate)] == DefaultValidate:
                self.text_area.insert("end", str0, 'validate')
            else:
                self.text_area.insert("end", str0)
            self.text_area.yview(END)
        except:
            self.text_area.insert("end", str0)


class ThreadSafeText(Text):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.queue = Queue.Queue()
        self.update_me()

    def write(self, line):
        self.queue.put(line)

    def update_me(self):
        while not self.queue.empty():
            line = self.queue.get_nowait()
            self.insert(END, line)
            self.see(END)
            self.update_idletasks()
        self.after(10, self.update_me)


class LogReader(object):

    def __init__(self, root, **kwargs):
        self.root = root
        self.filenameLog = kwargs.get('filenameLog', None)

        self.ClearDisplay = kwargs.get('ClearDisplay', False)
        ''' By default don't display Filenames and directory '''

        mainstyle = ttk.Style()
#         mainstyle.theme_use(mainstyle.theme_names()[0])
        mainstyle.configure('My.TFrame',
                            background='gray50',
                            foreground='gray97',
                            font="Monospace 12")

        Btnstyle = ttk.Style()
        Btnstyle.configure('My.TButton',
                           background='gray50',
                           foreground='gray97',
                           font="Monospace 12")
        root.title("Log reader v0.1")

        Chkstyle = ttk.Style()
        Chkstyle.configure('My.TCheckbutton',
                           background='gray50',
                           foreground='gray97',
                           font="Monospace 12")

        Chkstyle = ttk.Style()
        Chkstyle.configure('My.TLabel',
                           background='gray50',
                           foreground='gray97',
                           font="Monospace 12")

        root.title("Libretto v0.1")

        self.initParam()

        #======================================================================
        # Main Frame
        #======================================================================
        self.f0 = ttk.Frame(self.root, style='My.TFrame')
        self.f0.pack(expand=True, fill='both')
        LabelUP = ttk.Label(
            self.f0, text="Please select the log file then click on read",
            style='My.TLabel')
        LabelUP.pack(side="top")

        self.fDisp = ttk.Frame(self.f0, style='My.TFrame')
        self.fDisp.pack(expand=True, fill='both', side="right")

        self.fParam = ttk.Frame(self.f0, style='My.TFrame')
        self.fParam.pack(side="left")

        #======================================================================
        # Frame fDisp
        #======================================================================
        # Display stdout
        self.customFont = tkFont.Font(
            family="Helvetica", size=12)
        self.text_area = ScrolledText(
            self.fDisp, font=self.customFont, undo=True, background='gray20', foreground="gray92")
        self.text_area.pack(expand=True, fill='both')
        self.text_area.configure(state='normal')
        self.text_area.yview(END)
        self.text_area.after(0)

        self.text_area.tag_configure("comment",
                                     font="Helvetica 12",
                                     foreground="gray60")
        self.text_area.tag_configure("subsubTitle",
                                     font="Helvetica 12 bold")
        self.text_area.tag_configure("subTitle",
                                     font="Helvetica 14 bold")
        self.text_area.tag_configure("Title",
                                     font="Helvetica 16 bold")
        self.text_area.tag_configure("warn",
                                     font="Helvetica 12 bold",
                                     foreground="red")
        self.text_area.tag_configure("File",
                                     font="Helvetica 10",
                                     foreground="DarkSlateGray1")
        self.text_area.tag_configure("FileOther",
                                     font="Helvetica 10",
                                     foreground="plum")
        self.text_area.tag_configure("Directory",
                                     font="Helvetica 10",
                                     foreground="goldenrod1")
        self.text_area.tag_configure("validate",
                                     font="Helvetica 12 bold",
                                     foreground="OliveDrab1")
        self.text_area.tag_configure("param",
                                     font="Helvetica 12",
                                     foreground="wheat")

        # stdout redirection
        sys.stdout = StdoutRedirector(self.text_area)

        #======================================================================
        # Parameters
        #======================================================================

        # File Selection button
        SelectLogFileBtn = ttk.Button(
            self.fParam, text="Select the log file", style='My.TButton')
        SelectLogFileBtn.grid(row=0, column=0)
        SelectLogFileBtn.configure(command=lambda: self.set_LogFile())
        Label = ttk.Label(self.fParam, text="", style='My.TLabel')
        Label.grid(row=1, column=0)

        # Refresh button
        SelectLogFileBtn = ttk.Button(
            self.fParam, text="Refresh", style='My.TButton')
        SelectLogFileBtn.grid(row=2, column=0)
        SelectLogFileBtn.configure(command=lambda: self.RefreshLog())

        Label = ttk.Label(self.fParam, text="", style='My.TLabel')
        Label.grid(row=9, column=0)

        # Display Files button
        ChkBtnDispFilenames = ttk.Checkbutton(
            self.fParam, text="Display the filenames", style='My.TCheckbutton')
        ChkBtnDispFilenames.grid(row=10, column=0)
        ChkBtnDispFilenames.configure(variable=self.Entry_DispFilenames,
                                      command=lambda: self.set_DispFilenames())

        # Display Comments button
        ChkBtnDispCom = ttk.Checkbutton(
            self.fParam, text="Display the comments", style='My.TCheckbutton')
        ChkBtnDispCom.grid(row=11, column=0)
        ChkBtnDispCom.configure(variable=self.Entry_DispComment,
                                command=lambda: self.set_DispComment())

        # Display Directories button
        ChkBtnDispDir = ttk.Checkbutton(
            self.fParam, text="Display the directories", style='My.TCheckbutton')
        ChkBtnDispDir.grid(row=12, column=0)
        ChkBtnDispDir.configure(variable=self.Entry_DispDir,
                                command=lambda: self.set_DispDir())

        # Display Warnings button
        ChkBtnDispWarn = ttk.Checkbutton(
            self.fParam, text="Display the warnings", style='My.TCheckbutton')
        ChkBtnDispWarn.grid(row=13, column=0)
        ChkBtnDispWarn.configure(variable=self.Entry_DispWarn,
                                 command=lambda: self.set_DispWarn())

        # Display Warnings button
        ChkBtnDispParam = ttk.Checkbutton(
            self.fParam, text="Display the parameters", style='My.TCheckbutton')
        ChkBtnDispParam.grid(row=14, column=0)
        ChkBtnDispParam.configure(variable=self.Entry_DispParam,
                                  command=lambda: self.set_DispParam())

        self.RefreshLog()
        if self.ClearDisplay:
            self.UpdateAllDisp()

    def printExample(self):
        return ["=========================================",
                "= Welcome in the Log Reader        ",
                "=========================================",
                "", "=== This is a big title ! ===",
                "    ~ A little bit different of this sub-Title",
                "        *  And guess what, now a sub-sub-Title ! ",
                "            # right now I am commenting my example",
                "            p_Dodo is a parameter",
                "            BlablablaAudyIsTheBestBlablabla...",
                "            X_something is a most of the time the filename of " +
                " an MRI image or created",
                "            Z_something is the filename of a file which is not an " +
                "mri image (it can be some stats or a matrix)",
                "            D_anotherthing is a directory",
                "    > Well this task seems to be a success",
                "    !! But this is a message you should read"]

    def initParam(self):
        self.logExtension = ("*.txt", "*.log")

        self.LogMessage = None
        self.listHideBal = []
        global DefaultFileNameMRIImage
        global DefaultFileNameMRIMasks
        global DefaultFileNameOther
        global DefaultFileNameMatrix
        global DefaultDirectory
        global DefaultName
        global DefaultWarning
        global DefaultTitle
        global DefaultSubTitle
        global DefaultSubSubTitle
        global DefaultComment
        global DefaultValidate
        global DefaultParameter

        self.DefaultFileNameMRIImage = DefaultFileNameMRIImage
        self.DefaultFileNameMRIMasks = DefaultFileNameMRIMasks
        self.DefaultFileNameOther = DefaultFileNameOther
        self.DefaultFileNameMatrix = DefaultFileNameMatrix
        self.DefaultDirectory = DefaultDirectory
        self.DefaultName = DefaultName
        self.DefaultWarning = DefaultWarning
        self.DefaultTitle = DefaultTitle
        self.DefaultSubTitle = DefaultSubTitle
        self.DefaultSubSubTitle = DefaultSubSubTitle
        self.DefaultComment = DefaultComment
        self.DefaultValidate = DefaultValidate
        self.DefaultParameter = DefaultParameter

        self.DispWarn = True
        self.Entry_DispWarn = IntVar(value=1)
        self.DispParam = True
        self.Entry_DispParam = IntVar(value=1)

        if self.ClearDisplay:
            self.DispFilenames = False
            self.Entry_DispFilenames = IntVar(value=0)
            self.DispComment = False
            self.Entry_DispComment = IntVar(value=0)
            self.DispDir = False
            self.Entry_DispDir = IntVar(value=0)
        else:
            self.DispFilenames = True
            self.Entry_DispFilenames = IntVar(value=1)
            self.DispComment = True
            self.Entry_DispComment = IntVar(value=1)
            self.DispDir = True
            self.Entry_DispDir = IntVar(value=1)

    def DispOrHide(self, DispSomething, listHideBal):
        if DispSomething:
            # update the balise to hide list
            listHideBal = [e for e in self.listHideBal if e not in listHideBal]
        else:
            listHideBal = listHideBal + self.listHideBal
        self.listHideBal = listHideBal
        self.resetDisp()
        self.watchLog(bal=self.listHideBal)

    def set_DispFilenames(self):
        self.DispFilenames = self.Entry_DispFilenames.get()
        listbal0 = [self.DefaultFileNameMRIImage,
                    self.DefaultFileNameMatrix,
                    self.DefaultFileNameMRIMasks,
                    self.DefaultFileNameOther]
        self.DispOrHide(self.DispFilenames, listbal0)

    def set_DispDir(self):
        self.DispDir = self.Entry_DispDir.get()
        listbal0 = [self.DefaultDirectory]
        self.DispOrHide(self.DispDir, listbal0)

    def set_DispComment(self):
        self.DispComment = self.Entry_DispComment.get()
        listbal0 = [self.DefaultComment]
        self.DispOrHide(self.DispComment, listbal0)

    def set_DispWarn(self):
        self.DispWarn = self.Entry_DispWarn.get()
        listbal0 = [self.DefaultWarning]
        self.DispOrHide(self.DispWarn, listbal0)

    def set_DispParam(self):
        self.DispParam = self.Entry_DispParam.get()
        listbal0 = [self.DefaultParameter]
        self.DispOrHide(self.DispParam, listbal0)

    def UpdateAllDisp(self):
        self.set_DispComment()
        self.set_DispDir()
        self.set_DispFilenames()

    def set_LogFile(self):
        self.filenameLog = self.OpenFile(
            self.OriginalDirectory, self.logExtension)
        self.RefreshLog()

    def filterLog(self, str0, bal):
        ''' delete the lines which contain a specific balise '''
        if type(bal) != list:
            if type(bal) != str:
                if not bal:
                    return str0
            else:
                bal = [bal]
        try:
            str1 = DeleteTabulation(str0)
        except:
            str1 = str0

        for e in bal:
            if str1[0:len(e)] == e:
                return None
        return str0

    def loadLog(self):
        ''' load a log '''
        if self.filenameLog:
            with open(self.filenameLog) as f:
                self.LogMessage = f.read().splitlines()
        else:
            self.LogMessage = self.printExample()

    def watchLog(self, bal=None):
        ''' display the log '''
        for line in self.LogMessage:
            l = self.filterLog(line, bal)
            if l:
                print l

    def resetDisp(self):
        ''' '''
        self.text_area.delete('1.0', END)

    def RefreshLog(self):
        self.loadLog()
        self.resetDisp()
        self.watchLog(bal=self.listHideBal)

    def OpenFile(self, initialdir0="", filetype='*.*'):
        if filetype != '*.*':
            filetypes0 = (("Files", filetype),
                          ("All Files", "*.*"))
            name = askopenfilename(initialdir=initialdir0,
                                   filetypes=filetypes0,
                                   title="Choose a file.")
        else:
            name = askopenfilename(initialdir=initialdir0,
                                   title="Choose a file.")
        return name

    def close(self):
        print "close"
        exit()


def Call_Reader(fileLog=None, fullscreen=False, ClearDisplay=False):
    root = Tk()
    if fullscreen:
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
    my_gui = LogReader(root, filenameLog=fileLog, ClearDisplay=ClearDisplay)
    root.protocol("WM_DELETE_WINDOW", my_gui.close)
    root.mainloop()


if __name__ == '__main__':
    Call_Reader(fileLog=None, fullscreen=False, ClearDisplay=False)
