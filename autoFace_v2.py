import maya.cmds as mc

from pymel.all import *
class RIBBON:

    #def setPatchSize(self,patches)
    def setNumberOfPatches(self,numberOfPatches):
        self.numberofPatches = numberOfPatches
    
    def createPatch(self,name):
        self.upperLipPatch = nurbsPlane(name = name, ch=1, d=3, v=1, p=(0, 0, 0), u=self.numberofPatches, w=self.numberofPatches, ax=(0, 1, 0), lr=0.1666666667)[0]
        
        #return patch
    
    def getWsPosByUvCoord(self,patch,u,v):        
        pos = pointPosition(PyNode(patch.uv[u][v]))      

    def placeDriverJnts(self):
        select(cl = True)
        
    def setNumberOfFollicles(self,numberOfFollicles):
        self.numberOfFollicles = numberOfFollicles
        
    def addFolliclesToPatch(self):
        
        #desiredSkinJoints = 8
        uOffsetVal = 1.0/self.numberOfFollicles
        currentUOffsetVal = 0
        follicles = []
        patchShape =PyNode(pickWalk(self.upperLipPatch ,d='down')[0])
        for each in range(0,self.numberOfFollicles +1):
        
#selected()
            #patchShape = PyNode(pickWalk(patch, d='down')[0])
            follicleShape = createNode('follicle') #name?
            follicle = PyNode(pickWalk(follicleShape, d='up')[0])
            
            # Connect Objects
            patchShape.local >> follicleShape.inputSurface
            patchShape.worldMatrix[0]>> follicleShape.inputWorldMatrix
            
            follicleShape.outRotate>> follicle.rotate
            follicleShape.outTranslate>> follicle.translate
            
            follicle.parameterU.set(currentUOffsetVal)
            currentUOffsetVal = currentUOffsetVal + uOffsetVal
            
            follicle.parameterV.set(.5)
            
            follicles.append(follicle)
        #delete (follicles[-1])
        #follicles.remove(follicles[-1])                
        self.follicles = follicles
    
    def addBindJointsToFollicles(self):
        i = 0
        bindJoints = []
        for each in self.follicles:
            select(each)
            bindJoint = joint(n = self.upperLipPatch+ "_bindJoint_" + str(i))#name
            bindJoint.radius.set(.2)
            bindJoints.append(bindJoints)
            i+=1
        #return bindJoints    
#create ribbon class
a = RIBBON()


class headRig():
    def showUI(cls):
        win = cls()
        win.create()
        return win
        
    def __init__(self):
        self.window = "optionsWindow"
        self.title = "Options Window"
        self.size = (400,300)

    def create(self):
        if mc.window(self.window,exists=True): 
            mc.deleteUI(self.window,window=True)

        self.window = mc.window(self.window, title = self.title, widthHeight = self.size, menuBar = True)
        self.mainForm = mc.formLayout(nd = 100)

        #self.column = mc.columnLayout(p = self.optionsForm, adjustableColumn = True)
        self.steps = mc.text(" Setup Steps: ", p = self.mainForm)
        self.frameGrp1 = mc.frameLayout(p = self.mainForm, label = "I - Global Skull Joint Locations", collapse = True, collapsable = True)
        mc.button(label = "Place Locators in General Positions", command = self.placeLocs)
        mc.button(label = "Parent Joints (Do not use until skinning is ready)", command = self.parJnts)
        self.frameGrp2 = mc.frameLayout(p = self.mainForm, label = "II - Local Controls for Global Rig", collapse = True, collapsable = True)
        mc.button(label = "Create All at General Locators and Group", command = self.crCtrls)
        mc.button(label = "Lock and Hide Scale and Visibility", command = self.lockScal)
        self.frameGrp3 = mc.frameLayout(p = self.mainForm, label = "III - Local Rigging", collapse = True, collapsable = True)
        mc.button(label = "Place Locators in Local Positions", command = self.local)
        mc.button(label = "Create Joints at Local Locators and Group", command = self.crLocal)
        self.frameGrp4 = mc.frameLayout(p = self.mainForm, label = "IV - Eyes Smart Blink", collapse = True, collapsable = True)
        self.eyeGrp = mc.radioButtonGrp(label = "Eye Center: ", labelArray2 = ["Left", "Right"], numberOfRadioButtons = 2, select = 1)
        mc.button(label = "Create Eye Joints", command = self.eyeJnt)
        mc.button(label = "Create Eye Locators", command = self.eyeLoc)
        self.dirGrp = mc.radioButtonGrp(label = "Locators' Parallel Direction: ", labelArray3 = ["x", "y", "z"], numberOfRadioButtons = 3, select = 1)
        self.degGrp = mc.radioButtonGrp(label = "Curve Degree: ", labelArray3 = ["1 Linear", "2 Quadratic", "3 Cubic"], numberOfRadioButtons = 3, select = 1)
        mc.button(label = "Create Curve", command = self.eyeCurve)
        self.frameGrp5 = mc.frameLayout(p = self.mainForm, label = "V - Mouth and Lips Ribbon", collapse = True, collapsable = True)
        mc.rowColumnLayout(numberOfColumns = 3, columnOffset = [(1, "both", 2), (2, "both", 2), (3, "both", 2)])
        mc.text(label = "Number of Patches: ", align = "right")
        self.patField = mc.intField()
        mc.button(label = " Create Patches ", command = self.patch)
        mc.text(label = "Number of Follicles: ", align = "right")
        self.folField= mc.intField()
        mc.button(label = " Create Follicles ", command = self.folli)
 
        mc.formLayout(self.mainForm, e = True, attachForm = ([self.steps, "top", 2],
                                                             [self.frameGrp1, "left", 2],
                                                             [self.frameGrp1, "right", 2],
                                                             [self.frameGrp2, "left", 2],
                                                             [self.frameGrp2, "right", 2],
                                                             [self.frameGrp3, "left", 2],
                                                             [self.frameGrp3, "right", 2],
                                                             [self.frameGrp4, "left", 2],
                                                             [self.frameGrp4, "right", 2],
                                                             [self.frameGrp5, "left", 2],
                                                             [self.frameGrp5, "right", 2],
                                                             [self.frameGrp5, "bottom", 2]),
                                            attachControl = ([self.frameGrp1, "top", 5, self.steps],
                                                             [self.frameGrp2, "top", 3, self.frameGrp1],
                                                             [self.frameGrp3, "top", 3, self.frameGrp2],
                                                             [self.frameGrp4, "top", 3, self.frameGrp3],
                                                             [self.frameGrp5, "top", 3, self.frameGrp4]))
                                                                
        mc.showWindow()

#create locators at general (hardcoded) locations
    def placeLocs(self, *args):
        #place locators in general positions
        locsPos = [[0, 145, -7], [0, 148, -5], [0, 152, -3.5], [0, 163.5, -3], [0, 164, -3], [0, 160.5, -5], [4.4, 165, 5.5], [-4.4, 165, 5.5]]
        self.names = ["neck1", "neck2", "head", "headBottom", "headTop", "jaw", "eyeLeft", "eyeRight"]
        counter = 0
        for pos in locsPos:
            mc.spaceLocator(name = self.names[counter] + "_loc", position = pos)
            mc.xform(centerPivots = True)
            counter += 1
            
#parent (connect) general joints for head           
    def parJnts(self, *args):
        mc.parent("neck1_jnt", world = True)
        
        #reparent groups first
        mc.parent("neck2_GRP", "neck1_ctrl")
        mc.parent("head_GRP", "neck2_ctrl")
        mc.parent("headBottom_GRP", "head_ctrl")
        mc.parent("headTop_GRP", "head_ctrl")
        mc.parent("jaw_GRP", "headBottom_ctrl")
        mc.parent("eyeLeft_GRP", "headTop_ctrl")
        mc.parent("eyeRight_GRP", "headTop_ctrl")
        #parent joints outside
        mc.parent("neck2_jnt", "neck1_jnt")
        mc.parent("head_jnt", "neck2_jnt")
        mc.parent("headBottom_jnt", "head_jnt")
        mc.parent("headTop_jnt", "head_jnt")
        mc.parent("jaw_jnt", "headBottom_jnt")
        mc.parent("eyeLeft_jnt", "headTop_jnt")
        mc.parent("eyeRight_jnt", "headTop_jnt")

#create control, joints at location of locators; group each, and parent groups in order of head joints
    def crCtrls(self, *args):
        mc.select(deselect = True)
        #get positions of the locators after(if) they've been moved
        self.neck1pos = mc.pointPosition("neck1_loc")
        self.neck2pos = mc.pointPosition("neck2_loc")
        self.headpos = mc.pointPosition("head_loc")
        self.headBpos = mc.pointPosition("headBottom_loc")
        self.headTpos = mc.pointPosition("headTop_loc")
        self.jawpos = mc.pointPosition("jaw_loc")
        self.eyeLpos = mc.pointPosition("eyeLeft_loc")
        self.eyeRpos = mc.pointPosition("eyeRight_loc")
            
        #create a control and joint at each locator and then group each
        counter = 0
        self.newLocPos = [self.neck1pos, self.neck2pos, self.headpos, self.headBpos, self.headTpos, self.jawpos, self.eyeLpos, self.eyeRpos]
        for pos in self.newLocPos:
            curv = mc.circle(name = self.names[counter] + "_ctrl", center = pos, radius = 1.5, ch = False)
            mc.xform(centerPivots = True)
            jnt = mc.joint(position = pos, absolute = True, radius = 0.5, name = self.names[counter] + "_jnt")
            mc.parent(jnt, world = True)
            mc.select(self.names[counter] + "_loc", curv, jnt)
            
            list = mc.ls(selection = True)
            print list
            for i in range(0, len(list) - 1):
                mc.parent(list[i + 1], list[i])
                
            mc.group(list[0], name = self.names[counter] + "_GRP")    
            counter += 1
        #parent the groups together
        mc.parent("neck2_GRP", "neck1_jnt")
        mc.parent("head_GRP", "neck2_jnt")
        mc.parent("headBottom_GRP", "head_jnt")
        mc.parent("headTop_GRP", "head_jnt")
        mc.parent("jaw_GRP", "headBottom_jnt")
        mc.parent("eyeLeft_GRP", "headTop_jnt")
        mc.parent("eyeRight_GRP", "headTop_jnt")
    
#lock and hide scale and visibility
    def lockScal(self, *args):
        counter = 0 
        scalAxis = ['.sx', '.sy', '.sz']
        for curv in self.newLocPos:
            for scal in scalAxis:
                mc.setAttr(self.names[counter] + "_ctrl" + scal, lock = True, keyable = False, channelBox = False)
                mc.setAttr(self.names[counter] + "_ctrl" + '.visibility', keyable = False, channelBox = False)
            counter += 1
#place locators in locations for local rigging 
    def local(self, *args):
        localPos = [(0, 205, -4), (4.8, 194, 7.5), (-4.8, 194, 7.5), (0, 194, 9.5), (0, 193.8, 12), (1.2, 194, 10.5), (-1.2, 194, 10.5), (7.1, 197.3, -1.7), (-7.1, 197.3, -1.7), (9.1, 198.5, -4.1), (-9.1, 198.5, -4.1), (0, 190.2, 9.4), (0, 187.8, 7.4)]
        self.localNames = ["headLocal", "cheekLeft", "cheekRight", "noseLocal", "noseTip", "nostrilLeft", "nostrilRight", "earLeft", "earRight", "earTipLeft", "earTipRight", "mouth", "chin"]
        counter = 0
        for pos in localPos:
            mc.spaceLocator(name = self.localNames[counter] + "_loc", position = pos)
            mc.xform(centerPivots = True)
            counter += 1
            
#create joints at all the locators in local rigging and then group them     
    def crLocal(self, *args):
        counter = 0
        
        self.headLocalPos = mc.pointPosition("headLocal_loc")
        self.cheekLeftPos = mc.pointPosition("cheekLeft_loc")
        self.checkRightPos = mc.pointPosition("cheekRight_loc")
        self.noseLocalPos = mc.pointPosition("noseLocal_loc")
        self.noseTipPos = mc.pointPosition("noseTip_loc")
        self.nostrilLeftPos = mc.pointPosition("nostrilLeft_loc")
        self.nostrilRightPos = mc.pointPosition("nostrilRight_loc")
        self.earLeftPos = mc.pointPosition("earLeft_loc")
        self.earRightPos = mc.pointPosition("earRight_loc")
        self.earTipRightPos = Pos = mc.pointPosition("earTipRight_loc")
        self.earTipLeftPos = mc.pointPosition("earTipLeft_loc")
        self.mouthPos = mc.pointPosition("mouth_loc")
        self.chinPos = mc.pointPosition("chin_loc")
        
        self.localLocPos = [self.headLocalPos, self.cheekLeftPos, self.checkRightPos, self.noseLocalPos, 
                            self.noseTipPos, self.nostrilLeftPos, self.nostrilRightPos, self.earLeftPos, 
                            self.earRightPos, self.earTipRightPos, self.earTipLeftPos, self.mouthPos, self.chinPos]
       
        for pos in self.localLocPos:
            jnt = mc.joint(position = pos, absolute = True, radius = 0.5, name = self.localNames[counter] + "_jnt")
            mc.parent(jnt, world = True)
            mc.select(self.localNames[counter] + "_loc", jnt)
            
            list = mc.ls(selection = True)
            print list
            for i in range(0, len(list) - 1):
                mc.parent(list[i + 1], list[i])
                
            mc.group(list[0], name = self.localNames[counter] + "_GRP")    
            counter += 1        
  
#create eye joints for left or right side        
    def eyeJnt(self, *args):
        eyeCenter = mc.radioButtonGrp(self.eyeGrp, query = True, select = True)
        if eyeCenter == 1:
            center = "L_Eye_Center"
        else:
            center = "R_Eye_Center"
        vtx = mc.ls(sl = 1 , fl = 1)
        
        for v in vtx :
            mc.select(cl =1 )
            jnt = mc.joint()
            pos = mc.xform(v , q =1 , ws =1 , t =1 )
            mc.xform(jnt , ws =1 , t = pos )
            posC = mc.xform(center , q =1 , ws =1 , t =1 )
            mc.select(cl =1)
            jntC = mc.joint()
            mc.xform(jntC , ws =1 , t = posC )
            mc.parent(jnt , jntC)
            mc.joint (jntC , e= 1 , oj = "xyz" , secondaryAxisOrient= "yup", ch = 1 , zso = 1 )

#create locators at all joints on eye curve
    def eyeLoc(self, *args):
        radioSel = mc.radioButtonGrp(self.eyeGrp, query = True, select = True)
        if radioSel == 1:
            worldObj = "L_eyeUpVec_loc"
        else:
            worldObj = "R_eyeUpVec_loc"
        vtx = mc.ls(sl = 1 , fl = 1)
        
        sel = mc.ls(sl =1)
    
        for s in sel :
            loc = mc.spaceLocator()[0]
            pos = mc.xform(s , q =1 , ws = 1 , t =1)
            mc.xform(loc , ws =1 , t =pos)
            par = mc.listRelatives(s , p =1 )[0]
            mc.aimConstraint(loc, par , mo = 1 , weight = 1 , aimVector = (1,0,0) , upVector = (0,1,0), worldUpType = "object" , worldUpObject = worldObj)

    def eyeCurve(self, *args):
        from operator import itemgetter
        
        locators = mc.ls(selection = True)
        posOrder = []
        for loc in locators:
            posOrder.append(mc.pointPosition(loc))
            
        orderDir = mc.radioButtonGrp(self.dirGrp, query = True, select = True)
        if orderDir == 1:
            #sort by first item, x, in list of (x, y, z) is index 0  
            posOrder = sorted(posOrder, key = itemgetter(0))
        elif orderDir == 2:
            #sort by second item, y, in list (x, y, z) is index 1
            posOrder = sorted(posOrder, key = itemgetter(1))
        else:
            #sort by third (last) item, z is index 2
            posOrder = sorted(posOrder, key = itemgetter(2))
        
        degree = mc.radioButtonGrp(self.degGrp, query = True, select = True)
        
        curv = mc.curve(d = degree, p = posOrder)      
        
    def patch(self, *args):
        patNum = mc.intField(self.patField, query = True, value = True)
        a.setNumberOfPatches(patNum)
        a.createPatch("Patch")
        
    def folli(self, *args):
        folNum = mc.intField(self.folField, query = True, value = True)
        a.setNumberOfFollicles(folNum)
        a.addFolliclesToPatch()
        
        a.numberOfFollicles
        a.addBindJointsToFollicles()    
        
win = headRig()
win.create()
