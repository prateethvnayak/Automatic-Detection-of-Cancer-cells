from tkinter import *
import tkFileDialog
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import benchmark_main
from segment import main_call
import call

path = ''
ans = 0
frame_1 = 0
status = 0

class MenuFormat:
    def __init__(self, root):
        menu = Menu(root, tearoff=False)  # Creates menu object
        root.config(menu=menu, bg="alice blue")  # Configuring menu object to be a menu

        submenu = Menu(menu, tearoff=False)  # Creating a sub-menu inside a menu

        menu.add_cascade(label="File",
                         menu=submenu)  # Creates file button with drop-down, sub menu is the drop

        submenu.add_command(label="Choose an image...",
                            command=self.doThis)
        submenu.add_command(label="New...",
                            command=self.doThis)  # 2 commands in the sub menu now

        submenu.add_separator()  # Creates seperator in the drop

        submenu.add_command(label="Exit",
                            command=root.quit)  # Another sub menu item

        editmenu = Menu(menu, tearoff=False)  # Create another item in main menu

        menu.add_cascade(label="Edit",
                         menu=editmenu)

        editmenu.add_command(label="Undo",
                             command=self.doThis)
        editmenu.add_separator()

        editmenu.add_command(label="Cut",
                             command=self.doThis)

        editmenu.add_command(label="Copy",
                             command=self.doThis)

        editmenu.add_command(label="Paste",
                             command=self.doThis)

    def doThis(self):
        print("Sorry!\nI can only do this displaying thing right now!")


welcome = Tk()
m = welcome.attributes('-fullscreen', True)
# welcome.geometry('{}x{}+0+0'.format(*m))
welcome.title('Welcome to the Automated Cancer Screening Application')
w = MenuFormat(welcome)
frame8 = Frame(welcome, bg='white')
frame8.pack(side=TOP, fill=X)
hi = Label(frame8, bd=30, text='VISVESVARAYA TECHNOLOGICAL UNIVERSITY', font='italic, 20', bg='white')
hi.pack(side=TOP)
image1 = Image.open('download.jpg')
image2 = Image.open('BIT.jpg')
image3 = Image.open('AIndra.png')
# image = image.resize((200, 100), Image.ANTIALIAS)
photo1 = ImageTk.PhotoImage(image1)
photo2 = ImageTk.PhotoImage(image2)
photo3 = ImageTk.PhotoImage(image3)
ht1 = photo1.height()
wi1 = photo1.width()
ht2 = photo2.height()
wi2 = photo2.width()
ht3 = photo3.height()
wi3 = photo3.width()
spacer = Label(welcome, bg='white', height=ht1)
spacer.pack(side=TOP, fill=X)
pane = Label(spacer, width=40, bg='white')
pane.pack(side=LEFT)
panel1 = Label(spacer, image=photo1, width=wi1, height=ht1)
panel1.image = photo1
panel1.pack(side=LEFT, padx=40)
panel2 = Label(spacer, image=photo2, width=wi1, height=ht1, bg='white')
panel2.image = photo1
panel2.pack(side=LEFT, padx=40, pady=40)
panel3 = Label(spacer, image=photo3, width=wi3, height=ht3, anchor=NE)
panel3.image = photo1
panel3.pack(side=LEFT, padx=40)
frame = Frame(welcome, bg='white')
frame.pack(side=BOTTOM, fill=X)
space = Label(welcome, bg='white', text='Cancer screening application presented in association'
                                        ' with Aindra systems\n and the Department of Electronics and '
                                        'Communication Engineering\n at Bangalore Institute of Technology.\n\n\n'
                                        'To get started, please click on begin.', font=5)
space.pack(side=TOP, fill=X)
begin = Button(frame, text="BEGIN!", bg='white', bd=8, fg='black', command=frame.master.destroy, width=13, height=1)
space8 = Label(frame, height=2, bg='white')
space8.pack(side=BOTTOM)
begin.pack()
welcome.mainloop()


def open_image():
    filename = tkFileDialog.askopenfilename(title='Choose an image', defaultextension=".bmp",
                                            filetypes=(('Bitmap Images', '*.bmp'), ('Herlev Images', '*.BMP'), ('JPEG Images', '*.jpg'),
                                                       ('PNG Images', '*.png')))
    copyPath.set(filename)
    global path
    path = filename
    image = Image.open(filename)
    image = image.resize((350, 300), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    ht = photo.height()
    wi = photo.width()
    spacer = Label(blank, width=8, bg='alice blue')
    panel = Label(blank, image=photo, width=wi, height=ht)
    panel.image = photo
    spacer.pack(side=LEFT)
    panel.pack(side=LEFT)
    global status
    status = Frame(blank, width=8, bg='azure')
    status.pack(side=BOTTOM, fill=X)
    frame_n = Frame(blank, width=20, height=6, bg='alice blue')
    frame_n.pack(side=BOTTOM, fill=X, padx=20, pady=20)
    b2 = Button(frame_n, text='Evaluate', bg='white', bd=8, fg='black', command=evaluate, width=13, height=1)
    b2.pack(side=LEFT, padx=10)
    b3 = Button(frame_n, text='Segment', bg='white', bd=8, fg='black', command=segment, width=13, height=1)
    b3.pack(side=LEFT, padx=10)
    b1 = Button(frame_n, text="Predict", bg='white', bd=8, fg='black', command=predict, width=13, height=1)
    b1.pack(side=LEFT, padx=10)


def evaluate():
    ev = Label(status, text='Evaluating...', bg='alice blue', font=8)
    ev.pack(side=LEFT)
    global ans
    ans = messagebox.askquestion("Choose Dataset Name", "Is the image from the Kidwai data-set?")
    if ans == 'yes':
        prec, reca = benchmark_main.segment(path, 1)
    else:
        prec, reca = benchmark_main.segment(path, 2)
    ev.pack_forget()
    global frame_1
    frame_1 = Frame(blank, bd=18, bg='alice blue')
    frame_1.pack(side=RIGHT, fill=Y)
    frame0 = Frame(frame_1, bd=18, bg='alice blue')
    frame0.pack(side=TOP, fill=X)
    head1 = Label(frame0, width=40, bd=2, text='Evaluation Result', bg='yellow', font=4)
    head1.pack(side=TOP)
    space_1 = Label(frame_1, width=2, bg='alice blue')
    space_1.pack(side=LEFT, fill=Y)
    frame_2 = Frame(frame_1, bd=18, bg='alice blue')
    frame_2.pack(side=TOP, fill=X)
    precision = Label(frame_2, text='Precision      :', font=3, fg='black', bg='alice blue')
    precision.pack(side=LEFT)
    pre = Label(frame_2, width=18, bg='azure', text=prec)
    pre.pack(side=LEFT)
    frame_3 = Frame(frame_1, bd=18, bg='alice blue')
    frame_3.pack(side=TOP, fill=X)
    # space3 = Label(frame_3, width=4, bg='alice blue')
    recall = Label(frame_3, text='Recall           :', font=3, fg='black', bg='alice blue')
    rec = Label(frame_3, width=18, bg='azure', text=reca)
    # space3.pack(side=LEFT)
    recall.pack(side=LEFT)
    rec.pack(side=LEFT)


def predict():
    pr = Label(status, text='Predicting...', bg='alice blue', font=8)
    pr.pack(side=LEFT)
    global ans
    if ans == 'yes':
        a, n = call.predict('ROOT DIRECTORY NAME/cropped/kidwai_crop')
    else:
        a, n = call.predict('ROOT DIRECTORY NAME/cropped/herlev_crop')
    pr.pack_forget()

    frame4 = Frame(frame_1, bd=18, bg='alice blue')
    frame4.pack(side=TOP, fill=X)
    head2 = Label(frame4, width=40, bd=2, text='Classifier Output', bg='yellow', font=4)
    head2.pack(side=TOP)
    frame5 = Frame(frame_1, bd=18, bg='alice blue')
    frame5.pack(side=TOP, fill=X)
    # space5 = Label(frame5, width=4, bg='alice blue')
    normal = Label(frame5, text='Normal Count     :', font=3, fg='black', bg='alice blue')
    normal.pack(side=LEFT)
    nor = Label(frame5, width=14, bg='azure', text=n)
    nor.pack(side=LEFT)
    frame6 = Frame(frame_1, bd=18, bg='alice blue')
    frame6.pack(side=TOP, fill=X)
    # space6 = Label(frame6, width=4, bg='alice blue')
    abnormal = Label(frame6, text='Abnormal Count :', font=3, fg='black', bg='alice blue')
    abnormal.pack(side=LEFT)
    abn = Label(frame6, width=14, bg='azure', text=a)
    abn.pack(side=LEFT)


def segment():
    se = Label(status, text='Segmenting...', bg='alice blue', font=8)
    se.pack(side=LEFT)
    global ans
    ans = messagebox.askquestion("Choose Dataset Name", "Is the image from the Kidwai data-set?")
    if ans == 'yes':
        main_call(path, 1)
    else:
        main_call(path, 2)
    se.pack_forget()


blank = Tk()
blank.title('Automated Cancer Screening')
blank.geometry('900x600')
copyPath = StringVar(None)
g = MenuFormat(blank)

frame1 = Frame(blank, bd=18, bg='alice blue')
frame1.pack(side=TOP, fill=X)
space1 = Label(frame1, width=2, bg='alice blue')
image_path = Entry(frame1, width=60, bd=2, textvariable=copyPath)
image_path.update()
image_path.focus_set()
space2 = Label(frame1, width=8, bg='alice blue')
choose_image = Button(frame1, text='Choose Image', bd=8, command=open_image)
space1.pack(side=LEFT)
image_path.pack(side=LEFT)
space2.pack(side=LEFT)
choose_image.pack(side=LEFT)

blank.mainloop()
