import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import DobotDllType as DobotDll
from threading import Thread

class MainApplication:
    def __init__(self, window):
        
        self.window = window
        self.window.config(padx = 10, pady = 10)
        self.api = DobotDll.load()
        
        # Initialization of the camera frame
        self.canvas = tk.Canvas(window, width = 640, height = 480)
        self.canvas.grid(row = 0, column = 0, columnspan = 60, rowspan = 6, padx = 5)
        
        ######################################################################
        ####################### Camera buttons ############################### 
        ######################################################################        
        
        self.LiveBtn = tk.Button(self.window, text = "Go Live", command = self.LiveBtn_Click, width = 10, height = 1)
        self.LiveBtn.grid(row = 7, column = 0)
        
        self.PhotoBtn = tk.Button(self.window, text = "Take Photo", command = self.PhotoBtn_Click, width = 10, height = 1)
        self.PhotoBtn.grid(row = 7, column = 1)
        
        self.ResultLabel = tk.Label(self.window, text = "Result: ")
        self.ResultLabel.grid(row = 7, column = 2)
        
        ######################################################################
        #################### Control Robot Menu ############################## 
        ######################################################################
        
        self.group1 = tk.LabelFrame(self.window, text = "Control Robot", padx = 10, pady = 10, width = 300, height = 380)
        self.group1.grid(row = 0, column = 75, rowspan = 3, columnspan = 15)
        
        self.connectBtn = tk.Button(self.group1, text = "Connect", command = self.ConnectBtn_Click, padx = 0, pady = 0, width = 25, height = 1)
        self.connectBtn.grid(row = 0, column = 0, columnspan = 3)
        
        
        # Label and values for coordinates and joint angles
        self.jointAngle_label = tk.Label(self.group1, text = "Joint Angle")
        self.jointAngle_label.grid(row = 1, column = 0, padx = 0, pady = 5)
        
        self.coord_label = tk.Label(self.group1, text = "Coordinates")
        self.coord_label.grid(row = 1, column = 2, padx = 0, pady = 5)
        
        self.pos_list = []
        self.jointAngle_list = []
        for i in range(4):
            self.jointAngle_list.append(tk.Label(self.group1, text = "0.00"))
            self.jointAngle_list[i].grid(row = i + 2, column = 0, padx = 0, pady = 5)

            self.pos_list.append(tk.Label(self.group1, text = "0.00"))
            self.pos_list[i].grid(row = i + 2, column = 2, padx = 0, pady = 5)
        
        
        # Entry box for each coordinate     
        self.go_list = []
        for i in range(3):
            self.go_list.append(tk.Spinbox(self.group1, from_= -300, to = 300, textvariable = tk.StringVar(self.window, "0"), width = 5))
            self.go_list[i].grid(row = i + 2, column = 3)      
        
        self.goBtn = tk.Button(self.group1, text = "GO", command = self.GoBtn_Click, width = 5, height = 1)
        self.goBtn.grid(row = 5, column = 3)
        
        # Buttons to move the robot
        self.moveXP = tk.Button(self.group1, text = "X+", width = 5, height = 1)
        self.moveXP.bind("<ButtonPress>", lambda event, button = "moveXP" : self.OnMove(button))
        self.moveXP.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveXP.grid(row = 7, column = 0)
        
        self.moveYP = tk.Button(self.group1, text = "Y+", width = 5, height = 1)
        self.moveYP.bind("<ButtonPress>", lambda event, button = "moveYP" : self.OnMove(button))
        self.moveYP.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveYP.grid(row = 6, column = 1)
        
        self.moveZP = tk.Button(self.group1, text = "Z+", width = 5, height = 1)
        self.moveZP.bind("<ButtonPress>", lambda event, button = "moveZP" : self.OnMove(button))
        self.moveZP.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveZP.grid(row = 6, column = 3, pady = 5)
        
        self.moveXM = tk.Button(self.group1, text = "X-", width = 5, height = 1)
        self.moveXM.bind("<ButtonPress>", lambda event, button = "moveXM" : self.OnMove(button))
        self.moveXM.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveXM.grid(row = 7, column = 2)
        
        self.moveYM = tk.Button(self.group1, text = "Y-", width = 5, height = 1)
        self.moveYM.bind("<ButtonPress>", lambda event, button = "moveYM" : self.OnMove(button))
        self.moveYM.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveYM.grid(row = 8, column = 1)
        
        self.moveZM = tk.Button(self.group1, text = "Z-", width = 5, height = 1)
        self.moveZM.bind("<ButtonPress>", lambda event, button = "moveZM" : self.OnMove(button))
        self.moveZM.bind("<ButtonRelease>", lambda event, button = "release" : self.OnMove(button))
        self.moveZM.grid(row = 8, column = 3)
        
        ######################################################################
        #################### Data Acquisition Menu ########################### 
        ######################################################################
        
        self.group2 = tk.LabelFrame(self.window, text = "Data Acquisition", padx = 10, pady = 10, width = 300, height = 150)
        self.group2.grid(row = 4, column = 75,rowspan = 2, columnspan = 15)
        
   
        # Buttons to define each position
        self.defPosButtons = []
        Pos = ["Pos1", "Pos2", "Pos3"]
        for posbtns_index in range(len(Pos)):
            self.defPosButtons.append(tk.Button(self.group2, text = Pos[posbtns_index], command = lambda button = Pos[posbtns_index]: self.DefPos_Click(button), width = 5))
            self.defPosButtons[-1].grid(row = 0, column = posbtns_index)
            
        #self.defPosButtons[1].config(padx = 20)
        
        self.defCoord = tk.Label(self.group2, text = "Defined Coordinates")
        self.defCoord.grid(row = 1, column = 1, columnspan = 1, pady = 5)
        
        
        # Coordinates of defined position 1
        self.PosLabels_list = []
        for i in range(3):
            for j in range(3):
                self.PosLabels_list.append(tk.Label(self.group2, text = "0.00"))
                self.PosLabels_list[-1].grid(row = j+2, column = i)
                
        self.PosLabels_list[4].config(pady = 5)
        
        self.startAcq = tk.Button(self.group2, text = "Start Acquisition", padx = 1.5, width = 31)
        self.startAcq.grid(row = 5, column = 0, columnspan = 3)
    
        self.window.mainloop()

    ######################################################################
    ################### Camera Buttons Methods ########################### 
    ######################################################################        
        
    def LiveBtn_Click(self):
        if self.LiveBtn.cget("text") == "Go Live":            
            self.vid = MyVideoCapture(0)
            self.delay = 15
            self.update()
            self.LiveBtn.config(text = "Stop Live")
        else:
            self.vid.__del__()
            self.LiveBtn.config(text = "Go Live")
            
    def PhotoBtn_Click(self):
        if self.LiveBtn.cget("text") == "Go Live":
            self.vid = MyVideoCapture(0)
        else:
            self.LiveBtn.config(text = "Go Live")
        
        ret, frame = self.vid.get_frame()
        cv2.imwrite(time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        
        self.vid.__del__()

    def update(self):
        # Get a frame from the video source
        try:
            ret, frame = self.vid.get_frame()
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
                self.window.after(self.delay, self.update)
        except:
            pass

    ######################################################################
    ################# Data Acquisition Methods ########################### 
    ######################################################################  
    
    def DefPos_Click(self, button):
#        btnIndex = int(button[-1])
#        for i in range(3):
#            self.PosLabels_list[btnIndex+i-1].config(text = self.pos_list[i].cget("text"))
        
        if button == "Pos1":
            self.def_X.config(text = self.posX.cget("text"))
            self.def_Y.config(text = self.posY.cget("text"))
            self.def_Z.config(text = self.posZ.cget("text"))
        if button == "Pos2":
            self.def_X2.config(text = self.posX.cget("text"))
            self.def_Y2.config(text = self.posY.cget("text"))
            self.def_Z2.config(text = self.posZ.cget("text"))
        if button == "Pos3":
            self.def_X3.config(text = self.posX.cget("text"))
            self.def_Y3.config(text = self.posY.cget("text"))
            self.def_Z3.config(text = self.posZ.cget("text"))
        
    ######################################################################
    ################### Robot Control Methods ############################ 
    ######################################################################  

    def ConnectBtn_Click(self):
        if self.connectBtn.cget("text") == "Connect":
            self.connectBtn.config(text = "Disconnect")
            self.state = DobotDll.ConnectDobot(self.api, "", 115200)[0]
            DobotDll.SetQueuedCmdClear(self.api)
            self.OnMonitoring()
        else:
            self.connectBtn.config(text = "Connect")
            DobotDll.DisconnectDobot(self.api)
            
    def OnMonitoring(self):
        if self.connectBtn.cget("text") == "Disconnect":
            for i in range(4):
                self.pos_list[i].config(text = str(round(DobotDll.GetPose(self.api)[i],2)))
                self.jointAngle_list[i].config(text = str(round(DobotDll.GetPose(self.api)[i+4],2)))
            
            self.window.after(15, self.OnMonitoring)
            
######## I think it is possible to gather Jog and OnMove in a Dobot class to make the code more organized
            
    def Jog(self, x, y, z, r):
        cmd = DobotDll.JC.JogIdle
        if x > 0:
            cmd = DobotDll.JC.JogAPPressed
        if x < 0:
            cmd = DobotDll.JC.JogANPressed
        if y > 0:
            cmd = DobotDll.JC.JogBPPressed
        if y < 0:
            cmd = DobotDll.JC.JogBNPressed
        if z > 0:
            cmd = DobotDll.JC.JogCPPressed
        if z < 0:
            cmd = DobotDll.JC.JogCNPressed
        if r > 0:
            cmd = DobotDll.JC.JogDPPressed
        if r < 0:
            cmd = DobotDll.JC.JogDNPressed
        DobotDll.SetJOGCmd(self.api, 0, cmd)
        
    def OnMove(self, button):
        x = y = z = 0
        delta = 1
        if button != "release":
            if button == "moveXP":
                x += delta
            if button == "moveXM":
                x -= delta
            if button == "moveYP":
                y += delta
            if button == "moveYM":
                y -= delta
            if button == "moveZP":
                z += delta
            if button == "moveZM":
                z -= delta
            self.Jog(x, y, z, 0)
        else:
            self.Jog(0, 0, 0, 0)
        
    def GoBtn_Click(self):
        DobotDll.SetPTPCmd(self.api, DobotDll.PTPMode.PTPMOVJXYZMode, float(self.go_list[0].get()), float(self.go_list[1].get()), float(self.go_list[2].get()), 0, isQueued = 0)[0]
        DobotDll.SetQueuedCmdStartExec(self.api)
        DobotDll.SetQueuedCmdStopExec(self.api)
        
    def __del__(self):
        try:
            if self.state != None:
                DobotDll.DisconnectDobot(self.api)
            else:
                pass
        except:
            pass
        
        
    ######################################################################
    ################ Camera initialization and methods ################### 
    ######################################################################  
        
class MyVideoCapture:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(video_source)      
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")
#            
#        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
#        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return(ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

#class MyDobot:    
#    def __init__(self):
#        self.DobotApi = DobotDll.load()
#        
#    def dCon(self):          
#        self.state = DobotDll.ConnectDobot(self.DobotApi, "", 115200)[0]
#        DobotDll.SetQueuedCmdClear(self.DobotApi)
#        self.OnMonitoring()
#        if self.state != 0:
#            DobotDll.DisconnectDobot(self.DobotApi)
#            return "Connect"
#        return "Disconnect"
#    
#    def OnMonitoring(self):
#        self.positions = DobotDll.GetPose(self.api)
#        return ['%.2f' % elem for elem in self.positions]
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Product Inspection')
    MainApplication(root)
    