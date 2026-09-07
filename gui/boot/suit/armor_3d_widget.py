
from __future__ import annotations

import math
from dataclasses import dataclass

from PySide6.QtCore import QTimer
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL import GL
from OpenGL import GLU


@dataclass
class Module:
    name: str
    target: tuple[float, float, float]
    scale: tuple[float, float, float]
    start: tuple[float, float, float]
    delay: float
    duration: float
    shape: str = "capsule"


class Armor3DWidget(QOpenGLWidget):
    """
    V10 cinematic original powered armor.
    Real OpenGL scene, smoother easing, coherent connected anatomy,
    joint rings/actuators, curved-ish shells, and assembly animation.
    """

    def __init__(self, parent=None):
        fmt = QSurfaceFormat()
        fmt.setDepthBufferSize(24)
        fmt.setSamples(8)
        QSurfaceFormat.setDefaultFormat(fmt)
        super().__init__(parent)

        self.t = 0.0
        self._running = True
        self.modules = self._make_modules()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def _make_modules(self):
        p = []

        def a(name, target, scale, start, delay, duration=.62, shape="capsule"):
            p.append(Module(name, target, scale, start, delay, duration, shape))

        # feet -> shins -> knees -> thighs
        a("L foot", (-.72,-3.35,.05), (.72,.42,1.05), (-5,-4,-2), .15, .55, "foot")
        a("R foot", (.72,-3.35,.05), (.72,.42,1.05), (5,-4,2), .18, .55, "foot")
        a("L shin", (-.72,-2.45,0), (.58,1.18,.58), (-4.8,-2.7,-1), .32)
        a("R shin", (.72,-2.45,0), (.58,1.18,.58), (4.8,-2.7,1), .36)
        a("L knee", (-.72,-1.42,.18), (.62,.42,.62), (-4.2,-1.4,-1), .52, .48, "joint")
        a("R knee", (.72,-1.42,.18), (.62,.42,.62), (4.2,-1.4,1), .55, .48, "joint")
        a("L thigh", (-.74,-.55,0), (.72,1.25,.68), (-4.5,.2,-1), .68)
        a("R thigh", (.74,-.55,0), (.72,1.25,.68), (4.5,.2,1), .72)

        # pelvis / waist / chest
        a("pelvis", (0,-1.0,.02), (1.48,.72,.70), (0,-5,2), .86, .72, "shell")
        a("waist", (0,.05,0), (1.38,.48,.64), (0,4,-2), 1.02, .58, "shell")
        a("abdomen", (0,.78,.02), (1.48,.98,.68), (0,4.5,2), 1.18, .70, "shell")
        a("chest", (0,1.82,.03), (2.05,1.16,.86), (0,5,-2), 1.34, .78, "chest")
        a("collar", (0,2.62,.03), (1.05,.34,.60), (0,4,-2), 1.55, .46, "joint")
        a("reactor", (0,1.86,.58), (.48,.48,.20), (0,6,1), 1.70, .52, "reactor")

        # shoulders -> upper arms -> elbows -> forearms -> hands
        a("L shoulder", (-1.65,1.72,0), (.66,.64,.86), (-4,3,-1), 1.60, .50, "joint")
        a("R shoulder", (1.65,1.72,0), (.66,.64,.86), (4,3,1), 1.63, .50, "joint")
        a("L upper", (-2.05,.93,0), (.60,1.02,.66), (-4.8,1.5,-1), 1.76, .62)
        a("R upper", (2.05,.93,0), (.60,1.02,.66), (4.8,1.5,1), 1.79, .62)
        a("L elbow", (-2.05,-.05,.02), (.57,.40,.60), (-4.3,-.2,-1), 2.04, .44, "joint")
        a("R elbow", (2.05,-.05,.02), (.57,.40,.60), (4.3,-.2,1), 2.07, .44, "joint")
        a("L fore", (-2.05,-.92,0), (.62,1.08,.70), (-4.8,-1.5,-1), 2.18, .62)
        a("R fore", (2.05,-.92,0), (.62,1.08,.70), (4.8,-1.5,1), 2.21, .62)
        a("L wrist", (-2.05,-1.80,.02), (.48,.30,.52), (-3.8,-2.5,-1), 2.44, .42, "joint")
        a("R wrist", (2.05,-1.80,.02), (.48,.30,.52), (3.8,-2.5,1), 2.47, .42, "joint")
        a("L hand", (-2.05,-2.10,.02), (.58,.42,.70), (-3.6,-3.1,-1), 2.58, .52, "hand")
        a("R hand", (2.05,-2.10,.02), (.58,.42,.70), (3.6,-3.1,1), 2.61, .52, "hand")

        # helmet comes last
        a("helmet", (0,3.30,.03), (1.02,.92,.88), (0,6,2), 2.82, .82, "helmet")
        a("visor", (0,3.27,.77), (.72,.25,.13), (0,6,.5), 3.15, .46, "visor")
        return p

    def stop(self):
        self._running = False
        if self.timer.isActive():
            self.timer.stop()

    def start(self):
        self._running = True
        if not self.timer.isActive():
            self.timer.start(16)

    def _tick(self):
        if not self._running:
            return
        self.t += 0.016
        if self.t > 8.5:
            self.t = 4.9 + (self.t - 8.5) % 4.2
        self.update()

    @staticmethod
    def _ease(x):
        x = max(0.0, min(1.0, x))
        return x*x*x*(x*(x*6-15)+10)

    def initializeGL(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        GL.glEnable(GL.GL_LIGHT1)
        GL.glEnable(GL.GL_NORMALIZE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
        GL.glClearColor(.006, .009, .015, 1)

    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, max(1, h))
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(31.0, w/max(1,h), .1, 100)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslatef(0, -.12, -14.8)

        # Subtle finished-state breathing/turn.
        finished = self.t > 4.9
        yaw = -7.0 + (math.sin((self.t-4.9)*.65)*3.0 if finished else 0)
        GL.glRotatef(yaw, 0, 1, 0)
        GL.glRotatef(1.5, 1, 0, 0)

        self._lights()

        # Draw inner frame first for depth.
        self._draw_inner_frame()

        for m in self.modules:
            self._draw_module(m)

        # Reactor glow pass (simple additive-looking transparent disc).
        self._draw_reactor_glow()

    def _lights(self):
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, (4,5,8,1))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (1,1,1,1))
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_SPECULAR, (.7,.7,.7,1))
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_POSITION, (-5,1,4,1))
        GL.glLightfv(GL.GL_LIGHT1, GL.GL_DIFFUSE, (.28,.38,.55,1))

    def _draw_inner_frame(self):
        self._mat("frame")
        for x in (-1.05, 1.05):
            GL.glPushMatrix()
            GL.glTranslatef(x, .75, -.25)
            self._cylinder(.055, 2.0, 12)
            GL.glPopMatrix()

    def _progress(self, m):
        if self.t < m.delay:
            return 0
        return self._ease((self.t-m.delay)/m.duration)

    def _draw_module(self, m):
        k = self._progress(m)
        if k <= 0: return

        sx,sy,sz = m.start
        tx,ty,tz = m.target
        # Spring-like arrival without jitter.
        s = math.sin(k*math.pi) * (1-k) * .18
        x = sx+(tx-sx)*k
        y = sy+(ty-sy)*k
        z = sz+(tz-sz)*k+s

        GL.glPushMatrix()
        GL.glTranslatef(x,y,z)

        if k < .96:
            GL.glRotatef((1-k)*42, 0, 1, 0)
            GL.glRotatef(math.sin(k*math.pi)*(1-k)*18, 1, 0, 0)

        self._mat(m.shape)

        sx,sy,sz = m.scale
        if m.shape == "joint":
            self._joint(sx, sy, sz)
        elif m.shape == "helmet":
            self._helmet(sx,sy,sz)
        elif m.shape == "visor":
            self._visor(sx,sy,sz)
        elif m.shape == "chest":
            self._chest(sx,sy,sz)
        elif m.shape == "reactor":
            self._reactor(sx,sy,sz)
        elif m.shape == "hand":
            self._hand(sx,sy,sz)
        elif m.shape == "foot":
            self._foot(sx,sy,sz)
        else:
            self._capsule(sx,sy,sz)

        GL.glPopMatrix()


    def _cylinder(self, radius, height, segments=20):
        """Small utility cylinder used by the internal mechanical frame."""
        q = GLU.gluNewQuadric()
        GLU.gluQuadricNormals(q, GLU.GLU_SMOOTH)
        GLU.gluCylinder(q, radius, radius * 0.94, height, segments, 2)

        GL.glPushMatrix()
        GL.glRotatef(180, 1, 0, 0)
        GLU.gluDisk(q, 0, radius, segments, 1)
        GL.glPopMatrix()

        GL.glPushMatrix()
        GL.glTranslatef(0, 0, height)
        GLU.gluDisk(q, 0, radius * 0.94, segments, 1)
        GL.glPopMatrix()

        GLU.gluDeleteQuadric(q)

    def _mat(self, kind):
        if kind in ("reactor","visor"):
            GL.glColor3f(.055,.24,.38)
        elif kind == "joint" or kind == "frame":
            GL.glColor3f(.075,.085,.105)
        else:
            GL.glColor3f(.30,.34,.39)

    def _capsule(self,sx,sy,sz):
        GL.glPushMatrix()
        GL.glScalef(sx,sy,sz)
        self._rounded_cube()
        GL.glPopMatrix()

    def _rounded_cube(self):
        # Beveled-looking cube: central body + smaller end caps.
        self._cube()
        for sy in (-.46,.46):
            GL.glPushMatrix()
            GL.glTranslatef(0,sy,0)
            GLU.gluNewQuadric()
            GL.glScalef(.92,.10,.92)
            self._cube()
            GL.glPopMatrix()

    def _cube(self):
        GL.glBegin(GL.GL_QUADS)
        faces = [
            ((0,0,1),(-.5,-.5,.5,.5,-.5,.5,.5,.5,.5,-.5,.5,.5)),
            ((0,0,-1),(.5,-.5,-.5,-.5,-.5,-.5,-.5,.5,-.5,.5,.5,-.5)),
            ((0,1,0),(-.5,.5,.5,.5,.5,.5,.5,.5,-.5,-.5,.5,-.5)),
            ((0,-1,0),(-.5,-.5,-.5,.5,-.5,-.5,.5,-.5,.5,-.5,-.5,.5)),
            ((1,0,0),(.5,-.5,.5,.5,-.5,-.5,.5,.5,-.5,.5,.5,.5)),
            ((-1,0,0),(-.5,-.5,-.5,-.5,-.5,.5,-.5,.5,.5,-.5,.5,-.5)),
        ]
        for n,v in faces:
            GL.glNormal3f(*n)
            for i in range(0,12,3):
                GL.glVertex3f(v[i],v[i+1],v[i+2])
        GL.glEnd()

    def _joint(self,sx,sy,sz):
        GL.glPushMatrix()
        GL.glRotatef(90,1,0,0)
        q=GLU.gluNewQuadric()
        GLU.gluCylinder(q,sx*.55,sx*.48,sy*.65,24,2)
        GLU.gluDisk(q,0,sx*.55,24,1)
        GL.glTranslatef(0,0,sy*.65)
        GLU.gluDisk(q,0,sx*.48,24,1)
        GLU.gluDeleteQuadric(q)
        GL.glPopMatrix()

    def _chest(self,sx,sy,sz):
        # Layered chest: broad shell + inset center plate.
        self._capsule(sx,sy,sz)
        GL.glPushMatrix()
        GL.glTranslatef(0,0,sz*.52)
        GL.glScalef(sx*.43,sy*.68,sz*.16)
        self._capsule(1,1,1)
        GL.glPopMatrix()

    def _helmet(self,sx,sy,sz):
        GL.glPushMatrix()
        GL.glScalef(sx,sy,sz)
        q=GLU.gluNewQuadric()
        GLU.gluSphere(q,1,32,20)
        GLU.gluDeleteQuadric(q)
        GL.glPopMatrix()
        # Jaw guard
        GL.glPushMatrix()
        GL.glTranslatef(0,-sy*.58,sz*.25)
        GL.glScalef(sx*.68,sy*.26,sz*.52)
        self._capsule(1,1,1)
        GL.glPopMatrix()

    def _visor(self,sx,sy,sz):
        GL.glScalef(sx,sy,sz)
        self._cube()

    def _reactor(self,sx,sy,sz):
        GL.glPushMatrix()
        GL.glRotatef(90,1,0,0)
        q=GLU.gluNewQuadric()
        GLU.gluCylinder(q,sx,sx*.9,sy,32,2)
        GLU.gluDisk(q,0,sx,32,1)
        GL.glTranslatef(0,0,sy)
        GLU.gluDisk(q,0,sx*.9,32,1)
        GLU.gluDeleteQuadric(q)
        GL.glPopMatrix()

    def _hand(self,sx,sy,sz):
        self._capsule(sx,sy,sz)
        # Three compact finger modules.
        for i in (-.25,0,.25):
            GL.glPushMatrix()
            GL.glTranslatef(i*sx, -sy*.52, sz*.05)
            GL.glScalef(sx*.18, sy*.38, sz*.28)
            self._cube()
            GL.glPopMatrix()

    def _foot(self,sx,sy,sz):
        GL.glPushMatrix()
        GL.glTranslatef(0,-sy*.1,sz*.16)
        GL.glScalef(sx,sy,sz)
        self._cube()
        GL.glPopMatrix()

    def _draw_reactor_glow(self):
        if self.t < 2.15:
            return
        alpha = min(.32, (self.t-2.15)/1.5*.32)
        GL.glDisable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)
        GL.glColor4f(.02,.45,1.0,alpha)
        GL.glPushMatrix()
        GL.glTranslatef(0,1.86,.72)
        GL.glScalef(.42,.42,.03)
        q=GLU.gluNewQuadric()
        GLU.gluDisk(q,0,1,32,1)
        GLU.gluDeleteQuadric(q)
        GL.glPopMatrix()
        GL.glDisable(GL.GL_BLEND)
        GL.glEnable(GL.GL_LIGHTING)
