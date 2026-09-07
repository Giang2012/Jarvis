import math,time
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QPainter,QColor,QFont
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow
from OpenGL.GL import *
from OpenGL.GLU import *
from .armor_model import ArmorModel

class Showroom3D(QOpenGLWidget):
    def __init__(self,parent=None):
        super().__init__(parent); self.model=ArmorModel(); self.t0=time.perf_counter(); self.last=self.t0
        self.yaw=0; self.pitch=5; self.dist=8.4; self.auto=True; self.model.assembly_enabled=True; self.drag=False; self.lastpos=None; self.fps=60
        self.timer=QTimer(self); self.timer.timeout.connect(self.update); self.timer.start(16); self.setFocusPolicy(Qt.StrongFocus)
    def initializeGL(self):
        glClearColor(.006,.010,.018,1); glEnable(GL_DEPTH_TEST); glEnable(GL_CULL_FACE); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA); glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING); glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.16,0.18,0.22,1.0))
        for i,(pos,dif) in enumerate([((4,-6,8,1),(.62,.72,.95,1)),((-5,-3,5,1),(.28,.45,.90,1)),((0,4,3,1),(.08,.14,.24,1))]):
            light=GL_LIGHT0+i; glEnable(light); glLightfv(light,GL_POSITION,pos); glLightfv(light,GL_DIFFUSE,dif)
        glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS,72)
    def resizeGL(self,w,h):
        glViewport(0,0,w,max(1,h)); glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(38,w/max(1,h),.1,100); glMatrixMode(GL_MODELVIEW)
    def grid(self):
        glDisable(GL_LIGHTING); glColor4f(.035,.18,.30,.55); glLineWidth(1); glBegin(GL_LINES)
        for i in range(-18,19): glVertex3f(i*.5,-9,-1.0); glVertex3f(i*.5,9,-1.0); glVertex3f(-9,i*.5,-1.0); glVertex3f(9,i*.5,-1.0)
        glEnd(); glEnable(GL_LIGHTING)
    def rings(self,t):
        glDisable(GL_LIGHTING); glColor4f(.03,.42,.9,.55)
        for r,spd in ((2.1,12),(2.55,-8),(3.0,5)):
            glPushMatrix(); glTranslatef(0,0,-.92); glRotatef(t*spd,0,0,1); glBegin(GL_LINE_LOOP)
            for i in range(96): a=2*math.pi*i/96; glVertex3f(r*math.cos(a),r*math.sin(a),0)
            glEnd(); glPopMatrix()
        glEnable(GL_LIGHTING)
    def paintGL(self):
        now=time.perf_counter(); dt=now-self.last; self.last=now; self.fps=self.fps*.9+(1/max(dt,.001))*.1; t=now-self.t0
        if self.auto: self.yaw+=dt*6
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT); glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        y=math.radians(self.yaw); p=math.radians(self.pitch); cx=math.sin(y)*math.cos(p)*self.dist; cy=-math.cos(y)*math.cos(p)*self.dist; cz=3.7+math.sin(p)*self.dist
        gluLookAt(cx,cy,cz,0,0,3.0,0,0,1); self.grid(); self.rings(t)
        glPushMatrix(); glTranslatef(0,0,-.87); glColor4f(.025,.07,.11,1); gluCylinder(self.model.q,2.25,2.25,.28,64,2); glTranslatef(0,0,.28); glColor4f(.02,.20,.34,1); gluCylinder(self.model.q,1.9,1.9,.07,64,2); glPopMatrix()
        self.model.draw(t); self.hud(t)
    def hud(self,t):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing); w,h=self.width(),self.height()
        def tx(x,y,s,n=11,a=220): p.setPen(QColor(120,205,255,a)); p.setFont(QFont('Segoe UI',n,QFont.DemiBold)); p.drawText(x,y,s)
        def panel(x,y,pw,ph,title): p.setPen(QColor(55,170,235,120)); p.setBrush(QColor(3,14,25,145)); p.drawRoundedRect(x,y,pw,ph,10,10); tx(x+14,y+23,title,11)
        panel(22,22,250,170,'SYSTEM OVERVIEW'); tx(38,58,'CPU       18%'); tx(38,84,'GPU       11%'); tx(38,110,'AI CORE   ONLINE'); tx(38,136,'RENDER    OPENGL 3D'); tx(38,162,f'FPS       {self.fps:4.1f}')
        panel(w-272,22,250,170,'JARVIS CORE'); tx(w-256,58,'OLLAMA    CONNECTED'); tx(w-256,84,'MEMORY    ONLINE'); tx(w-256,110,'TOOLS     READY'); tx(w-256,136,'CAMERA    STANDBY'); tx(w-256,162,'SHOWROOM  V11')
        cx,cy=w//2,int(h*.45); p.setPen(QColor(70,190,255,100)); p.drawEllipse(cx-24,cy-24,48,48); p.drawLine(cx-38,cy,cx-10,cy); p.drawLine(cx+10,cy,cx+38,cy); p.drawLine(cx,cy-38,cx,cy-10); p.drawLine(cx,cy+10,cx,cy+38)
        tx(24,h-26,'JARVIS SHOWROOM  /  REAL-TIME 3D ARMOR',10,180); tx(w-310,h-26,'DRAG ROTATE   WHEEL ZOOM   SPACE AUTO',9,170); p.end()
    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton: self.drag=True; self.lastpos=e.position(); self.auto=False
    def mouseMoveEvent(self,e):
        if self.drag and self.lastpos is not None:
            d=e.position()-self.lastpos; self.yaw+=d.x()*.45; self.pitch=max(-12,min(25,self.pitch-d.y()*.25)); self.lastpos=e.position()
    def mouseReleaseEvent(self,e):
        if e.button()==Qt.LeftButton: self.drag=False
    def wheelEvent(self,e): self.dist=max(7.0,min(15.5,self.dist-e.angleDelta().y()*.008))
    def keyPressEvent(self,e):
        if e.key()==Qt.Key_Space: self.auto=not self.auto
        elif e.key()==Qt.Key_A: self.model.assembly_enabled=True; self.t0=time.perf_counter()
        elif e.key()==Qt.Key_R: self.yaw=0; self.pitch=5; self.dist=8.4; self.auto=True; self.model.assembly_enabled=True; self.t0=time.perf_counter(); self.model.assembly_enabled=True
    def closeEvent(self,e): self.timer.stop(); self.model.close(); super().closeEvent(e)

class ShowroomWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('JARVIS Showroom V11'); self.resize(1440,900); self.setCentralWidget(Showroom3D(self))
