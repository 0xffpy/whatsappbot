import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from fileFilterer import FileFilterer
from whatzBot import WhatzBot


class MyBoard1(tk.Tk):
    __textToSend = ''
    __photos = []
    __document = []
    __backgroundColor = '#36454f'
    __textColor = '#ffffff'
    __file_number = ''
    __is_there_text = False
    __is_there_file = False
    __file_filter_object = FileFilterer()
    __whatsapp_object = WhatzBot()

    def __init__(self):
        super().__init__()
        self.title("whatsapp Bot ")
        self.geometry('1600x1080')
        self.config(background=self.__backgroundColor)
        Label(self,
              text='Welcome to Whatsapp Bot',
              bg=self.__backgroundColor,
              font=('Helvetica', 50, 'bold italic'),
              fg=self.__textColor
              ).pack(side=TOP)
        self.warning_1_label = Label(self,
                                     text="",
                                     bg='#36454f',
                                     font=('Helvetica', 18, 'bold italic'),
                                     fg='#363131'
                                     )
        self.warning_1_label.pack(side=TOP)
        self.textFields()
        self.buttonsForPhoto()
        self.buttonsForFile()
        self.startbutton()
        self.buttons_for_documents()


    def buttonsForPhoto(self):
        self.labelForPhoto = Label(self,
                                   text='Click on the Button so you can chose the photos',
                                   font=('Helvetica', 20, 'bold italic'),
                                   bg=self.__backgroundColor,
                                   fg=self.__textColor)
        self.labelForPhoto.pack()
        self.labelForPhoto.place(y=300, x=730)

        self.photobt = Button(self,
                              text='Click me to load pictures loooool',
                              width=40,
                              command=self.photoDialoges
                              ,bg = self.__backgroundColor,
                              fg = self.__textColor)
        self.photobt.pack()
        self.photobt.place(x=1000, y=400)


    def buttonsForFile(self):
        self.labelForNum = Label(self,
                                 text='Click on the Button so you can chose the number file ',
                                 font=('Helvetica', 20, 'bold italic'),
                                 bg=self.__backgroundColor,
                                 fg=self.__textColor)
        self.labelForNum.pack()
        self.labelForNum.place(y=570, x=0)

        self.num_bt = Button(self,
                             text='Click me to load number file ',
                             width=40,
                             command=self.fileDialoges)
        self.num_bt.pack()
        self.num_bt.place(x=30, y=620)


    def startbutton(self):
        self.__start_button = Button(self,
                                     text='Start The Program',
                                     command=self.start)
        self.__start_button.pack()
        self.__start_button.place(x=1080, y=750)


    def buttons_for_documents(self):
        self.labelForPhoto = Label(self,
                                   text='Click on the Button so you can upload document',
                                   font=('Helvetica', 20, 'bold italic'),
                                   bg=self.__backgroundColor,
                                   fg=self.__textColor)
        self.labelForPhoto.pack()
        self.labelForPhoto.place(y=900, x=1000)

        self.photobt = Button(self,
                              text='Click me for document',
                              width=40,
                              command=self.document_dialog
                              , bg=self.__backgroundColor,
                              fg=self.__textColor)
        self.photobt.pack()
        self.photobt.place(x=1000, y=1000)

    def textFields(self):
        self.labelForEnrty = Label(self,
                                   text='Enter the message you want to send',
                                   font=('Helvetica', 20, 'bold italic'),
                                   bg=self.__backgroundColor,
                                   fg=self.__textColor)
        self.labelForEnrty.pack()
        self.labelForEnrty.place(x=5, y=370)
        self.entry = Entry(self,
                           fg=self.__textColor,
                           bg=self.__backgroundColor,
                           relief=RAISED,
                           width=70, )

        self.entry.pack()
        self.entry.place(x=10, y=500)
        self.bt1 = Button(self, text='Click to submit', command=self.submit, height=1, width=15,
                          bg=self.__textColor)
        self.bt1.pack(side=LEFT)
        self.bt1.place(x=30, y=430)
        self.entry_2 = Entry(self,
                           fg=self.__textColor,
                           bg=self.__backgroundColor,
                           relief=RAISED,
                           width=10, )
        self.entry_2.pack()
        self.entry_2.place(x=30,y=800)
        self.bt2 = Button(self,text = 'Number column',command = self.submit_2,height = 1,width = 15)
        self.bt2.pack(side = LEFT)
        self.bt2.place(x = 30,y = 850)

    # event handlers
    def submit(self):
        try:
            x = self.entry.get()
            self.__textToSend = x
            self.__is_there_text = True
        except:
            print("hello none lol")


    def submit_2(self):
        try:
            y = self.entry_2.get()
            self.__file_filter_object.set_number_of_columns(y)
        except:
            print("hello none lol")


    def photoDialoges(self):
        name = fd.askopenfilename()
        if name:
            self.__photos.append(name)


    def document_dialog(self):
        name = fd.askopenfilename()
        if name:
            self.__document.append(name)


    def fileDialoges(self):
        file_num_path = fd.askopenfilename()
        if file_num_path:
            self.__file_number = file_num_path
            self.__is_there_file = True
            texttry = Label(self,
                            text=self.__file_number,
                            font=('Helvetica', 20, 'bold italic'),
                            bg=self.__backgroundColor,
                            fg=self.__textColor
                            )
            texttry.pack()
            texttry.place(y=650, x=0)

    def start(self):
        count = 0
        if self.__is_there_text:
            if self.__is_there_file:
                self.__start_button['state'] = DISABLED
                self.__whatsapp_object.set_photo_list(self.__photos)
                self.__whatsapp_object.set_text_message(self.__textToSend)
                self.__whatsapp_object.set_document_list(self.__document)
                self.__file_filter_object.set_file_path(self.__file_number)
                self.destroy()
                self.__file_filter_object.excute_program()
                print(len(self.__file_filter_object.getlistofnums()))
                self.__whatsapp_object.startingWhats()
                print(len(self.__file_filter_object.getlistofnums()))
                #self.__file_filter_object.generate(1000)
                for i in self.__file_filter_object.getlistofnums():
                    count+=1
                    print(count)
                    while True:
                        try:
                            y = self.__whatsapp_object.contactingNumbers(i,count)
                            if not y:
                                while True:
                                    if self.__whatsapp_object.contactingNumbers(i,count):
                                        break
                                    else:
                                        continue
                            break
                        except:
                            continue


            else:
                self.warning_1_label['text'] = "please enter a file"
        else:
            self.warning_1_label['text'] = 'please enter a text'
