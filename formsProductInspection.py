import tkinter as tk

root = tk.Tk()

root.title('Motorcycle Inspection')
root.geometry('978x594')

app = tk.Frame(root)
app.pack()

group1 = tk.LabelFrame(app, text = "Control Robot", padx = 10, pady = 10, width = 300, height = 380)
group1.grid(row = 0, column = 4)

connectBtn = tk.Button(group1, text = "Connect", padx = 0, pady = 0, width = 25, height = 1)
connectBtn.grid(row = 0, column = 0, columnspan = 3)

# Label and values for each angle joint
jointAngle_label = tk.Label(group1, text = "Joint Angle")
jointAngle_label.grid(row = 1, column = 0, padx = 0, pady = 5)

jointAngle1 = tk.Label(group1, text = "0.00")
jointAngle1.grid(row = 2, column = 0, padx = 0, pady = 5)

jointAngle2 = tk.Label(group1, text = "0.00")
jointAngle2.grid(row = 3, column = 0, padx = 0, pady = 5)

jointAngle3 = tk.Label(group1, text = "0.00")
jointAngle3.grid(row = 4, column = 0, padx = 0, pady = 5)

jointAngle4 = tk.Label(group1, text = "0.00")
jointAngle4.grid(row = 5, column = 0, padx = 0, pady = 5)

# Label and values for each coordinate
coord_label = tk.Label(group1, text = "Coordinates")
coord_label.grid(row = 1, column = 2, padx = 0, pady = 5)

posX = tk.Label(group1, text = "0.00")
posX.grid(row = 2, column = 2, padx = 0, pady = 5)

posY = tk.Label(group1, text = "0.00")
posY.grid(row = 3, column = 2, padx = 0, pady = 5)

posZ = tk.Label(group1, text = "0.00")
posZ.grid(row = 4, column = 2, padx = 0, pady = 5)

posR = tk.Label(group1, text = "0.00")
posR.grid(row = 5, column = 2, padx = 0, pady = 5)

goX = tk.Spinbox(group1, from_= 0, to = 300)
goX.config(width = 5)
goX.grid(row = 2, column = 3)

goY = tk.Spinbox(group1, from_= 0, to = 300)
goY.config(width = 5)
goY.grid(row = 3, column = 3)

goZ = tk.Spinbox(group1, from_= 0, to = 300)
goZ.config(width = 5)
goZ.grid(row = 4, column = 3)

goBtn = tk.Button(group1, text = "GO", width = 5, height = 1)
goBtn.grid(row = 5, column = 3)

moveXP = tk.Button(group1, text = "X+", width = 5, height = 1)
moveXP.grid(row = 7, column = 0)

moveYP = tk.Button(group1, text = "Y+", width = 5, height = 1)
moveYP.grid(row = 6, column = 1)

moveZP = tk.Button(group1, text = "Z+", width = 5, height = 1)
moveZP.grid(row = 6, column = 3, pady = 5)

moveXM = tk.Button(group1, text = "X-", width = 5, height = 1)
moveXM.grid(row = 7, column = 2)

moveYM = tk.Button(group1, text = "Y-", width = 5, height = 1)
moveYM.grid(row = 8, column = 1)

moveZM = tk.Button(group1, text = "Z-", width = 5, height = 1)
moveZM.grid(row = 8, column = 3)


group2 = tk.LabelFrame(app, text = "Data Acquisition", padx = 10, pady = 10, width = 300, height = 150)
group2.grid(row = 1, column = 4)

defPos1 = tk.Button(group2, text = "Pos1", width = 5)
defPos1.grid(row = 0, column = 0)

defPos2 = tk.Button(group2, text = "Pos2", width = 5)
defPos2.grid(row = 0, column = 1, padx = 20)

defPos3 = tk.Button(group2, text = "Pos3", width = 5)
defPos3.grid(row = 0, column = 2)

defCoord = tk.Label(group2, text = "Defined Coordinates")
defCoord.grid(row = 1, column = 1, columnspan = 1, pady = 5)

def_X = tk.Label(group2, text = "0.00")
def_X.grid(row = 2, column = 0)

def_Y = tk.Label(group2, text = "0.00")
def_Y.grid(row = 3, column = 0)

def_Z = tk.Label(group2, text = "0.00")
def_Z.grid(row = 4, column = 0)

def_X2 = tk.Label(group2, text = "0.00")
def_X2.grid(row = 2, column = 1)

def_Y2 = tk.Label(group2, text = "0.00")
def_Y2.grid(row = 3, column = 1, pady = 5)

def_Z2 = tk.Label(group2, text = "0.00")
def_Z2.grid(row = 4, column = 1)

def_X3 = tk.Label(group2, text = "0.00")
def_X3.grid(row = 2, column = 2)

def_Y3 = tk.Label(group2, text = "0.00")
def_Y3.grid(row = 3, column = 2)

def_Z3 = tk.Label(group2, text = "0.00")
def_Z3.grid(row = 4, column = 2)

startAcq = tk.Button(group2, text = "Start Acquisition", padx = 1.5, width = 31)
startAcq.grid(row = 5, column = 0, columnspan = 3)

root.mainloop()
