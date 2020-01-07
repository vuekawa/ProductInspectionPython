import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import DobotDllType as DobotDll

class MainApplication:
    def __init__(self, window):
        self.window = window
        self.api = DobotDll.load()
        
        # Initialization of the camera frame
        self.canvas = tk.Canvas(window, width = 640, height = 480)
        self.canvas.grid(row = 0, column = 0, columnspan = 60, rowspan = 6)
        
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
        self.group1.grid(row = 0, column = 75,rowspan = 3, columnspan = 15)
        
        self.connectBtn = tk.Button(self.group1, text = "Connect", command = self.ConnectDobot, padx = 0, pady = 0, width = 25, height = 1)
        self.connectBtn.grid(row = 0, column = 0, columnspan = 3)
        
        
        # Label and values for each angle joint
        self.jointAngle_label = tk.Label(self.group1, text = "Joint Angle")
        self.jointAngle_label.grid(row = 1, column = 0, padx = 0, pady = 5)
        
        self.jointAngle1 = tk.Label(self.group1, text = "0.00")
        self.jointAngle1.grid(row = 2, column = 0, padx = 0, pady = 5)
        
        self.jointAngle2 = tk.Label(self.group1, text = "0.00")
        self.jointAngle2.grid(row = 3, column = 0, padx = 0, pady = 5)
        
        self.jointAngle3 = tk.Label(self.group1, text = "0.00")
        self.jointAngle3.grid(row = 4, column = 0, padx = 0, pady = 5)
        
        self.jointAngle4 = tk.Label(self.group1, text = "0.00")
        self.jointAngle4.grid(row = 5, column = 0, padx = 0, pady = 5)
        
        
        # Label and values for each coordinate
        self.coord_label = tk.Label(self.group1, text = "Coordinates")
        self.coord_label.grid(row = 1, column = 2, padx = 0, pady = 5)
        
        self.posX = tk.Label(self.group1, text = "0.00")
        self.posX.grid(row = 2, column = 2, padx = 0, pady = 5)
        
        self.posY = tk.Label(self.group1, text = "0.00")
        self.posY.grid(row = 3, column = 2, padx = 0, pady = 5)
        
        self.posZ = tk.Label(self.group1, text = "0.00")
        self.posZ.grid(row = 4, column = 2, padx = 0, pady = 5)
        
        self.posR = tk.Label(self.group1, text = "0.00")
        self.posR.grid(row = 5, column = 2, padx = 0, pady = 5)
        
        
        # Entry box for each coordinate       
        self.goX = tk.Spinbox(self.group1, from_= -300, to = 300, textvariable = tk.StringVar(self.window, "0"))
        self.goX.config(width = 5)
        self.goX.grid(row = 2, column = 3)
        
        self.goY = tk.Spinbox(self.group1, from_= -300, to = 300, textvariable = tk.StringVar(self.window, "0"))
        self.goY.config(width = 5)
        self.goY.grid(row = 3, column = 3)
        
        self.goZ = tk.Spinbox(self.group1, from_= -300, to = 300, textvariable = tk.StringVar(self.window, "0"))
        self.goZ.config(width = 5)
        self.goZ.grid(row = 4, column = 3)
        
        self.goBtn = tk.Button(self.group1, text = "GO", command = self.GoBtn_Click, width = 5, height = 1)
        self.goBtn.grid(row = 5, column = 3)
        
        
        # Buttons to move the robot
        self.moveXP = tk.Button(self.group1, text = "X+", width = 5, height = 1)
        self.moveXP.grid(row = 7, column = 0)
        
        self.moveYP = tk.Button(self.group1, text = "Y+", width = 5, height = 1)
        self.moveYP.grid(row = 6, column = 1)
        
        self.moveZP = tk.Button(self.group1, text = "Z+", width = 5, height = 1)
        self.moveZP.grid(row = 6, column = 3, pady = 5)
        
        self.moveXM = tk.Button(self.group1, text = "X-", width = 5, height = 1)
        self.moveXM.grid(row = 7, column = 2)
        
        self.moveYM = tk.Button(self.group1, text = "Y-", width = 5, height = 1)
        self.moveYM.grid(row = 8, column = 1)
        
        self.moveZM = tk.Button(self.group1, text = "Z-", width = 5, height = 1)
        self.moveZM.grid(row = 8, column = 3)
        
        ######################################################################
        #################### Data Acquisition Menu ########################### 
        ######################################################################
        
        self.group2 = tk.LabelFrame(self.window, text = "Data Acquisition", padx = 10, pady = 10, width = 300, height = 150)
        self.group2.grid(row = 4, column = 75,rowspan = 2, columnspan = 15)
        
   
        # Buttons to define each position
        self.defPos1 = tk.Button(self.group2, text = "Pos1", width = 5)
        self.defPos1.grid(row = 0, column = 0)
        
        self.defPos2 = tk.Button(self.group2, text = "Pos2", width = 5)
        self.defPos2.grid(row = 0, column = 1, padx = 20)
        
        self.defPos3 = tk.Button(self.group2, text = "Pos3", width = 5)
        self.defPos3.grid(row = 0, column = 2)
        
        self.defCoord = tk.Label(self.group2, text = "Defined Coordinates")
        self.defCoord.grid(row = 1, column = 1, columnspan = 1, pady = 5)
        
        
        # Coordinates of defined position 1
        self.def_X = tk.Label(self.group2, text = "0.00")
        self.def_X.grid(row = 2, column = 0)
        
        self.def_Y = tk.Label(self.group2, text = "0.00")
        self.def_Y.grid(row = 3, column = 0)
        
        self.def_Z = tk.Label(self.group2, text = "0.00")
        self.def_Z.grid(row = 4, column = 0)
        
        
        # Coordinates of defined position 2
        self.def_X2 = tk.Label(self.group2, text = "0.00")
        self.def_X2.grid(row = 2, column = 1)
        
        self.def_Y2 = tk.Label(self.group2, text = "0.00")
        self.def_Y2.grid(row = 3, column = 1, pady = 5)
        
        self.def_Z2 = tk.Label(self.group2, text = "0.00")
        self.def_Z2.grid(row = 4, column = 1)
        
        
        # Coordinates of defined position 3
        self.def_X3 = tk.Label(self.group2, text = "0.00")
        self.def_X3.grid(row = 2, column = 2)
        
        self.def_Y3 = tk.Label(self.group2, text = "0.00")
        self.def_Y3.grid(row = 3, column = 2)
        
        self.def_Z3 = tk.Label(self.group2, text = "0.00")
        self.def_Z3.grid(row = 4, column = 2)
        
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
    ################### Robot Control Methods ############################ 
    ######################################################################  

    def ConnectDobot(self):
        if self.connectBtn.cget("text") == "Connect":
            self.connectBtn.config(text = "Disconnect")
            self.state = DobotDll.ConnectDobot(self.api, "", 115200)     
            self.OnMonitoring()
        else:
            self.connectBtn.config(text = "Connect")
            DobotDll.SetQueuedCmdClear(self.api)
            DobotDll.DisconnectDobot(self.api)
            
    def OnMonitoring(self):
        if self.connectBtn.cget("text") == "Disconnect":
            self.posX.config(text = str(round(DobotDll.GetPose(self.api)[0],2)))
            self.posY.config(text = str(round(DobotDll.GetPose(self.api)[1],2)))
            self.posZ.config(text = str(round(DobotDll.GetPose(self.api)[2],2)))
            self.posR.config(text = str(round(DobotDll.GetPose(self.api)[3],2)))
            
            self.jointAngle1.config(text = str(round(DobotDll.GetPose(self.api)[4],2)))
            self.jointAngle2.config(text = str(round(DobotDll.GetPose(self.api)[5],2)))
            self.jointAngle3.config(text = str(round(DobotDll.GetPose(self.api)[6],2)))
            self.jointAngle4.config(text = str(round(DobotDll.GetPose(self.api)[7],2)))
            
            self.window.after(15, self.OnMonitoring)
            
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
        
    def GoBtn_Click(self):
        DobotDll.SetPTPCmd(self.api, DobotDll.PTPMode.PTPMOVJXYZMode, float(self.goX.get()), float(self.goY.get()), float(self.goZ.get()), 0, isQueued = 0)[0]
        DobotDll.SetQueuedCmdStartExec(self.api)
        DobotDll.SetQueuedCmdStopExec(self.api)
        
    def __del__(self):
        if self.state == 0:
            pass
        else:
            DobotDll.DisconnectDobot(self.api)

class MyVideoCapture:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")
            
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return(ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#            else:
#                return(ret, None)
#        else:
#            return(ret, None)
            
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    #MainApplication(tk.Tk(), "Product Inspection")
    root = tk.Tk()
    root.title('Product Inspection')
    MainApplication(root)
    
    #root.geometry('978x594')
    #root.mainloop()