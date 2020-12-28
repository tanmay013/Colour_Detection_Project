# importing libraries
import cv2
import numpy as np
import pandas as pd
from tkinter import *

# declaring global variables
click = False
r = g = b = xpos = ypos = 0


# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, click
        click = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# function to perform Pixel Color Detection
def pixel_det(img_path):
    ipath = str(img_path)
    csv_path = 'colors.csv'
    global img
    # reading csv file
    index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
    global df
    df = pd.read_csv(csv_path, names=index, header=None)

    # reading image
    img = cv2.imread(ipath)
    img = cv2.resize(img, (800, 600))

    # creating window
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)
    while True:
        cv2.imshow('image', img)
        if click:
            # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
            cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

            # Creating text string to display( Color name and RGB values )
            text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # For very light colours we will display text in black colour
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


# Function for Color Filtering

def Filter(img_path, rcolor):
    # getting hsv range of color from file
    index = ['color_name', 'L1', 'L2', 'L3', 'U1', 'U2', 'U3']
    fdf = pd.read_csv("Colors_HSV.csv", names=index, header=None)
    c = fdf[fdf["color_name"] == rcolor]
    l1 = [int(c['L1']), int(c['L2']), int(c['L3'])]
    u1 = [int(c['U1']), int(c['U2']), int(c['U3'])]
    # importing image in bgr format
    ipath = str(img_path)
    img = cv2.imread(ipath)
    # converting bgr to rbg
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # converting image to hsv format
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

    # lower color range and upper color range
    lower = np.array(l1)
    upper = np.array(u1)
    # creating a mask of detected color
    mask = cv2.inRange(grid_HSV, lower, upper)
    # removing mask and viweing image
    res = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask)
    res = cv2.resize(res, (1100, 700))
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    cv2.imshow('filtered image', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Button Function of Main Menu
def Pixel_Button_Function():
    img_path = TextPX.get()
    win.destroy()
    pixel_det(img_path)


def Filter_Button_Function():
    img_path = TextPX.get()
    color = TextPY.get()
    win.destroy()
    Filter(img_path, color)


# Main Of the Program

# Window Creation.
win = Tk()
win.geometry("1165x800")
win.title("COLOUR DETECTION PROGRAM")
win.configure(background="cyan")

# Frames

TopFrame = Frame(win, bg="cyan", pady=2, width=1150, height=100, relief=RIDGE)
TopFrame.grid(row=0, column=0)

Gtitle = Label(TopFrame, font=("Times", 50, "bold"), text="COLOUR DETECTION PROGRAM", bd=21, bg="cyan", fg="black",
               justify=CENTER)
Gtitle.grid(row=0, column=0)

ImageFrame = Frame(win, bd=10, bg="lemon chiffon", pady=2, width=1150, height=150, padx=2, relief=RIDGE)
ImageFrame.grid(row=1, column=0)

MainFrame = Frame(win, bd=10, bg="lemon chiffon", pady=2, width=1155, height=300, padx=2, relief=RIDGE)
MainFrame.grid(row=2, column=0)

LeftFrame = Frame(MainFrame, bd=10, width=562, height=300, pady=2, padx=2, bg="lemon chiffon", relief=RIDGE)
LeftFrame.pack(side=LEFT)

RightFrame = Frame(MainFrame, bd=10, width=562, height=300, pady=2, padx=2, bg="lemon chiffon", relief=RIDGE)
RightFrame.pack(side=RIGHT)

BottomFrame = Frame(win, bg="cyan", pady=2, width=1150, height=50, relief=RIDGE)
BottomFrame.grid(row=3, column=0)

Btitle = Label(BottomFrame, font=("Times", 20, "bold"), text="Created By: Tanmay Pandey", bd=21, bg="cyan", fg="black",
               justify=CENTER)
Btitle.grid(row=0, column=0)

# text area for link
imgtitle1 = Label(ImageFrame, font=("Times", 16, "bold"),
                  text="Enter the source of image you want for color detection.", bg="lemon chiffon", bd=21, fg="black",
                  justify=LEFT)
imgtitle1.grid(row=0, column=1)

imgtitle2 = Label(ImageFrame, font=("Times", 16, "bold"), text="Image Source:", bg="lemon chiffon", bd=21, fg="black",
                  justify=RIGHT)
imgtitle2.grid(row=1, column=0)

src = str()
TextPX = Entry(ImageFrame, font=("arial", 16, "bold"), bd=2, fg="blue", textvariable=src, width=80, justify=LEFT)
TextPX.grid(row=1, column=1, sticky=W)

csrc = str()
TextPY = Entry(RightFrame, font=("arial", 16, "bold"), bd=2, fg="blue", textvariable=csrc, width=26, justify=LEFT)
TextPY.grid(row=1, column=0, sticky=E)

# Labels

LeftLabel1 = Label(LeftFrame, font=("Times", 16, "bold"),
                   text="This Option is for color detection of a pixel in a image.\n Click to perform pixel detection\n\n\n\n",
                   bg="lemon chiffon", bd=21, fg="black", justify=CENTER)
LeftLabel1.grid(row=0, column=0)

RightLabel1 = Label(RightFrame, font=("Times", 16, "bold"),
                    text="This Option is for filtering a colour from image.\n (80% Accuracy)\n Fill the details and click the button to perform color filter",
                    bg="lemon chiffon", bd=21, fg="black", justify=CENTER)
RightLabel1.grid(row=0, column=0)

RightLabel2 = Label(RightFrame, font=("Times", 16, "bold"), text="Enter Colour Name: ", bg="lemon chiffon", bd=21,
                    fg="black")
RightLabel2.grid(row=1, column=0, sticky=W)

# Buttons
button1 = Button(LeftFrame, text="PIXEL COLOR DETECTION", font=("Times 16 bold"), height=2, width=44,
                 bg="OliveDrab2", command=Pixel_Button_Function)
button1.grid(row=1, column=0)

button2 = Button(RightFrame, text="COLOR FILTER", font=("Times 16 bold"), height=2, width=44, bg="OliveDrab2",
                 command=Filter_Button_Function)
button2.grid(row=3, column=0)

win.mainloop()
