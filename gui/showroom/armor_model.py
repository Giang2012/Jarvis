import math
from OpenGL.GL import *
from OpenGL.GLU import *


class ArmorModel:
    """JARVIS full-body cinematic powered armor.

    Coordinate convention: X = left/right, Y = front/back (front is -Y),
    Z = vertical.  The suit is built as wrapped shells around an inner frame,
    so the rear and side surfaces are real geometry rather than a front-only
    presentation.
    """
    RED = (0.32, 0.012, 0.008, 1.0)
    RED2 = (0.62, 0.022, 0.012, 1.0)
    RED_HI = (0.88, 0.055, 0.018, 1.0)
    RED_DARK = (0.16, 0.010, 0.007, 1.0)
    GOLD = (0.52, 0.20, 0.015, 1.0)
    GOLD_HI = (0.95, 0.50, 0.035, 1.0)
    METAL = (0.055, 0.072, 0.095, 1.0)
    METAL2 = (0.070, 0.085, 0.105, 1.0)
    JOINT = (0.040, 0.050, 0.065, 1.0)
    CYAN = (0.01, 0.62, 1.0, 1.0)
    WHITE = (0.65, 0.90, 1.0, 1.0)

    def __init__(self):
        self.q = gluNewQuadric()
        self.assembly_enabled = True

    @staticmethod
    def ease(x):
        x = max(0.0, min(1.0, x))
        return x * x * (3.0 - 2.0 * x)

    def amount(self, t, start, duration=0.58):
        if not self.assembly_enabled:
            return 1.0
        return self.ease((t - start) / duration)

    def pose(self, name, t):
        # Small assembly offsets only. The finished suit stays anatomically connected.
        starts = {
            "pelvis": (0.00, 0.18, -0.28, 0.0, 0.0, 0.0, 0.45),
            "torso": (0.00, 0.18, 0.30, 0.0, 0.0, 0.0, 0.52),
            "neck": (0.00, 0.08, 0.20, 0.0, 0.0, 0.0, 0.40),
            "head": (0.00, 0.12, 0.28, 0.0, 0.0, 0.0, 0.50),
            "left_arm": (-0.28, 0.10, 0.18, 0.0, 0.0, -5.0, 0.64),
            "right_arm": (0.28, 0.10, 0.18, 0.0, 0.0, 5.0, 0.70),
            "left_leg": (-0.08, 0.08, -0.28, 0.0, 0.0, -2.0, 0.82),
            "right_leg": (0.08, 0.08, -0.28, 0.0, 0.0, 2.0, 0.88),
        }
        order = {"pelvis": 0.0, "torso": 0.30, "neck": 0.52, "head": 0.64,
                 "left_arm": 0.78, "right_arm": 0.86, "left_leg": 1.02, "right_leg": 1.10}
        x, y, z, rx, ry, rz, delay = starts[name]
        a = self.amount(t, order[name], delay)
        return x * (1-a), y * (1-a), z * (1-a), rx * (1-a), ry * (1-a), rz * (1-a), a

    def begin(self, name, t):
        x, y, z, rx, ry, rz, a = self.pose(name, t)
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(rx, 1, 0, 0); glRotatef(ry, 0, 1, 0); glRotatef(rz, 0, 0, 1)
        s = 0.985 + 0.015 * a
        glScalef(s, s, s)
        return a

    def end(self):
        glPopMatrix()

    def close(self):
        if self.q:
            gluDeleteQuadric(self.q)
            self.q = None

    def mat(self, c, shininess=96):
        glColor4f(*c)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, c)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, min(128.0, max(0.0, float(shininess))))

    def sphere(self, scale, c, seg=40, rings=26):
        self.mat(c)
        glPushMatrix(); glScalef(*scale); gluSphere(self.q, 1.0, seg, rings); glPopMatrix()

    def cylinder(self, r1, r2, h, c, seg=36):
        self.mat(c)
        gluCylinder(self.q, r1, r2, h, seg, 2)
        glPushMatrix(); glRotatef(180, 1, 0, 0); gluDisk(self.q, 0, r1, seg, 1); glPopMatrix()
        glPushMatrix(); glTranslatef(0, 0, h); gluDisk(self.q, 0, r2, seg, 1); glPopMatrix()

    def capsule(self, radius, half_len, c, axis="z", scale=(1, 1, 1)):
        glPushMatrix()
        if axis == "x": glRotatef(90, 0, 1, 0)
        elif axis == "y": glRotatef(-90, 1, 0, 0)
        glScalef(*scale)
        self.cylinder(radius, radius * 0.92, half_len * 2, c, 36)
        glTranslatef(0, 0, half_len); self.sphere((radius, radius, radius), c, 32, 20)
        glTranslatef(0, 0, -2 * half_len); self.sphere((radius, radius, radius), c, 32, 20)
        glPopMatrix()

    def panel(self, pts, depth, c, y, bevel=0.055, shine=108):
        """Beveled extruded panel. pts are (x,z); y is its center depth."""
        self.mat(c, shine)
        n = len(pts); d = depth * 0.5
        cx = sum(p[0] for p in pts) / n; cz = sum(p[1] for p in pts) / n
        maxr = max(math.hypot(x-cx, z-cz) for x, z in pts) + 1e-5
        k = max(0.78, 1.0 - bevel / maxr)
        inner = [(cx + (x-cx)*k, cz + (z-cz)*k) for x, z in pts]

        glBegin(GL_POLYGON); glNormal3f(0, 1, 0)
        for x, z in reversed(pts): glVertex3f(x, y-d, z)
        glEnd()
        glBegin(GL_POLYGON); glNormal3f(0, -1, 0)
        for x, z in inner: glVertex3f(x, y+d, z)
        glEnd()
        glBegin(GL_QUADS)
        for i in range(n):
            x,z=pts[i]; X,Z=pts[(i+1)%n]
            dx=X-x; dz=Z-z; L=max(math.hypot(dx,dz),1e-6)
            glNormal3f(dz/L, 0, -dx/L)
            glVertex3f(x,y-d,z); glVertex3f(X,y-d,Z); glVertex3f(X,y+d,Z); glVertex3f(x,y+d,z)
        glEnd()
        glBegin(GL_QUADS)
        for i in range(n):
            x,z=pts[i]; X,Z=pts[(i+1)%n]; xi,zi=inner[i]; xI,zI=inner[(i+1)%n]
            glNormal3f(0, -1, 0)
            glVertex3f(x,y+d,z); glVertex3f(X,y+d,Z); glVertex3f(xI,y+d+.025,zI); glVertex3f(xi,y+d+.025,zi)
        glEnd()

    def ring(self, r, depth, c, y, segments=40):
        self.mat(c, 112)
        glPushMatrix(); glTranslatef(0,y,0); glRotatef(90,1,0,0)
        gluDisk(self.q, r*0.82, r, segments, 2)
        glPopMatrix()

    def seam(self, pts, y, c=(0.008,0.012,0.018,1), width=1.2):
        glDisable(GL_LIGHTING); glColor4f(*c); glLineWidth(width)
        glBegin(GL_LINE_STRIP)
        for x,z in pts: glVertex3f(x,y,z)
        glEnd(); glEnable(GL_LIGHTING)

    def actuator(self, x, y, z, length, radius=.045, axis="z"):
        glPushMatrix(); glTranslatef(x,y,z)
        if axis == "x": glRotatef(90,0,1,0)
        elif axis == "y": glRotatef(-90,1,0,0)
        self.cylinder(radius, radius*.84, length, self.GOLD_HI, 24)
        glPopMatrix()

    def joint(self, x, y, z, r=.15, axis="x"):
        glPushMatrix(); glTranslatef(x,y,z)
        if axis == "y": glRotatef(90,1,0,0)
        elif axis == "z": glRotatef(90,0,1,0)
        self.cylinder(r, r*.88, .13, self.METAL2, 32)
        glTranslatef(0,0,.13); self.cylinder(r*.62,r*.50,.045,self.GOLD,28)
        glPopMatrix()
        self.sphere((r*.82,r*.66,r*.82), self.JOINT, 28, 18)

    def chest(self):
        glPushMatrix(); glTranslatef(0,0,4.15)
        # Inner rib cage gives the armor a continuous body volume.
        self.sphere((.92,.40,1.14), self.METAL, 44, 28)
        # Pectoral shells wrap around the front and taper toward sternum.
        for s in (-1,1):
            pts=[(s*.06,.68),(s*.30,.84),(s*.68,.66),(s*.82,.25),(s*.67,-.05),(s*.38,-.16),(s*.12,.02)]
            self.panel(pts,.25,self.RED2,-.54, .065, 116)
            self.panel([(s*.13,.60),(s*.34,.72),(s*.60,.56),(s*.66,.30),(s*.38,.14),(s*.16,.25)],.09,self.RED_HI,-.68,.035,120)
        # Center sternum and lower chest.
        self.panel([(-.17,.76),(-.10,.91),(.10,.91),(.17,.76),(.15,.18),(0,.02),(-.15,.18)],.16,self.METAL2,-.69,.035,118)
        self.panel([(-.62,.12),(-.44,-.10),(0,-.22),(.44,-.10),(.62,.12),(.48,-.40),(0,-.56),(-.48,-.40)],.20,self.RED,-.55,.05,112)
        # Side ribs wrap toward the back.
        for s in (-1,1):
            self.sphere((.26,.46,.78), self.RED_DARK, 32, 22)
            glTranslatef(s*.72,.06,0)
            self.sphere((.25,.43,.72), self.RED, 32, 22)
            glTranslatef(-s*.72,-.06,0)
        self.seam([(-.62,.22),(-.45,.02),(-.25,-.12),(0,-.20),(.25,-.12),(.45,.02),(.62,.22)],-.72)
        glPopMatrix()

    def abdomen(self):
        glPushMatrix(); glTranslatef(0,0,3.02)
        # Four overlapping plates create a natural taper from ribs to waist.
        for i,(z,w) in enumerate([(0.62,.68),(0.30,.62),(-.02,.55),(-.32,.48)]):
            pts=[(-w,.18),(w,.18),(w*.90,-.08),(w*.56,-.25),(0,-.32),(-w*.56,-.25),(-w*.90,-.08)]
            self.panel(pts,.16,self.RED2 if i<2 else self.RED,-.51-i*.015,.045,110)
        self.panel([(-.18,.62),(.18,.62),(.22,-.25),(0,-.40),(-.22,-.25)],.10,self.METAL2,-.64,.03,116)
        self.seam([(-.56,.42),(-.46,.20),(-.40,-.05),(-.32,-.27)],-.68)
        self.seam([(.56,.42),(.46,.20),(.40,-.05),(.32,-.27)],-.68)
        glPopMatrix()

    def pelvis(self):
        glPushMatrix(); glTranslatef(0,0,2.40)
        self.sphere((.74,.37,.52),self.METAL,40,24)
        self.panel([(-.70,.28),(-.45,.50),(0,.56),(.45,.50),(.70,.28),(.58,-.18),(.30,-.38),(0,-.46),(-.30,-.38),(-.58,-.18)],.23,self.RED2,-.50,.06,112)
        self.panel([(-.27,.30),(.27,.30),(.31,-.12),(.15,-.34),(0,-.40),(-.15,-.34),(-.31,-.12)],.11,self.METAL2,-.64,.03,118)
        for s in (-1,1):
            self.panel([(s*.35,.27),(s*.69,.12),(s*.63,-.27),(s*.40,-.39),(s*.25,-.08)],.16,self.RED_HI,-.59,.045,112)
        # Rear hip wrap.
        self.panel([(-.64,.26),(-.36,.48),(0,.53),(.36,.48),(.64,.26),(.52,-.16),(.25,-.30),(0,-.25),(-.25,-.30),(-.52,-.16)],.18,self.RED_DARK,.48,.05,106)
        glPopMatrix()

    def neck(self):
        glPushMatrix(); glTranslatef(0,0,5.34)
        self.cylinder(.28,.32,.25,self.METAL2,32)
        self.sphere((.40,.32,.22),self.JOINT,32,18)
        self.panel([(-.48,.12),(-.30,.34),(0,.40),(.30,.34),(.48,.12),(.27,-.18),(-.27,-.18)],.16,self.METAL2,-.40,.04,112)
        glPopMatrix()

    def helmet(self):
        glPushMatrix(); glTranslatef(0,0,6.15)
        # Full shell, with front faceplate and rear shell both present.
        self.sphere((.57,.46,.70),self.RED2,48,32)
        self.sphere((.49,.40,.57),self.RED_DARK,44,28)
        # Crown/temple shells.
        self.panel([(-.48,.45),(-.30,.66),(0,.72),(.30,.66),(.48,.45),(.39,.15),(0,.27),(-.39,.15)],.20,self.RED_HI,-.38,.045,116)
        # Brow and visor surround.
        self.panel([(-.40,.20),(-.25,.34),(0,.30),(.25,.34),(.40,.20),(.32,-.02),(0,-.12),(-.32,-.02)],.12,self.METAL2,-.61,.035,120)
        glDisable(GL_LIGHTING); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE); glDepthMask(GL_FALSE)
        glColor4f(.02,.65,1.0,.95)
        glBegin(GL_QUADS); glVertex3f(-.30,-.69,.14); glVertex3f(-.07,-.70,.20); glVertex3f(.07,-.70,.20); glVertex3f(.30,-.69,.14); glEnd()
        glDepthMask(GL_TRUE); glDisable(GL_BLEND); glEnable(GL_LIGHTING)
        # Cheeks + jaw create a narrower lower face.
        for s in (-1,1):
            self.panel([(s*.13,-.02),(s*.45,.04),(s*.40,-.30),(s*.25,-.47),(s*.10,-.38)],.15,self.GOLD,-.53,.035,110)
        self.panel([(-.27,-.34),(-.14,-.48),(0,-.54),(.14,-.48),(.27,-.34),(.18,-.55),(-.18,-.55)],.14,self.RED,-.56,.035,112)
        # Rear cap panel.
        self.panel([(-.42,.25),(-.28,.52),(0,.61),(.28,.52),(.42,.25),(.32,-.24),(0,-.42),(-.32,-.24)],.16,self.RED,.43,.04,110)
        glPopMatrix()

    def arm(self, s):
        # Shoulder at z 4.65, upper arm to 3.95, forearm to 3.15.
        glPushMatrix(); glTranslatef(s*1.05,0,4.66)
        self.sphere((.43,.40,.34),self.METAL2,36,22)
        self.panel([(-.38,.24),(-.22,.43),(0,.50),(.30,.38),(.42,.10),(.25,-.20),(-.18,-.24),(-.40,-.04)],.22,self.RED2,-.39,.055,114)
        self.sphere((.29,.28,.22),self.JOINT,32,20)
        glPopMatrix()

        glPushMatrix(); glTranslatef(s*1.08,0,4.05)
        self.capsule(.25,.29,self.METAL,scale=(1.0,1.05,1.0))
        self.panel([(-.29,.28),(-.18,.42),(.18,.42),(.29,.25),(.25,-.25),(.14,-.39),(-.14,-.39),(-.25,-.25)],.19,self.RED_HI,-.34,.045,114)
        self.panel([(-.18,.18),(.18,.18),(.16,-.27),(0,-.37),(-.16,-.27)],.08,self.RED,-.46,.025,116)
        self.joint(0,-.31,-.35,.14,"y")
        glPopMatrix()

        glPushMatrix(); glTranslatef(s*1.08,0,3.35)
        self.capsule(.27,.31,self.METAL,scale=(1.0,1.06,1.0))
        self.panel([(-.31,.32),(-.20,.48),(.20,.48),(.31,.30),(.27,-.28),(.12,-.43),(-.12,-.43),(-.27,-.28)],.20,self.RED2,-.36,.05,114)
        self.panel([(-.18,.22),(.18,.22),(.16,-.28),(0,-.38),(-.16,-.28)],.08,self.GOLD,-.48,.025,112)
        # Rear forearm shell closes the volume.
        self.panel([(-.25,.30),(-.15,.45),(.15,.45),(.25,.28),(.22,-.27),(0,-.38),(-.22,-.27)],.13,self.RED_DARK,.34,.04,106)
        glPopMatrix()

        glPushMatrix(); glTranslatef(s*1.08,-.02,2.72)
        self.sphere((.22,.25,.16),self.JOINT,30,18)
        self.panel([(-.24,.13),(-.14,.24),(.14,.24),(.24,.12),(.18,-.13),(0,-.20),(-.18,-.13)],.16,self.METAL2,-.32,.035,110)
        # Palm + compact finger block.
        self.panel([(-.20,.08),(-.12,.22),(.12,.22),(.20,.08),(.16,-.22),(.06,-.32),(-.06,-.32),(-.16,-.22)],.18,self.RED_DARK,-.36,.035,106)
        for i in range(3):
            glPushMatrix(); glTranslatef(s*(-.10+i*.10),-.45,2.54)
            self.capsule(.045,.09,self.GOLD_HI,scale=(1,.9,1)); glPopMatrix()
        glPopMatrix()

    def leg(self, s):
        # Hip socket.
        self.joint(s*.50,.02,2.13,.19,"x")
        # Thigh.
        glPushMatrix(); glTranslatef(s*.50,0,1.66)
        self.capsule(.38,.38,self.METAL,scale=(1.0,1.12,1.0))
        self.panel([(-.40,.44),(-.22,.58),(.22,.58),(.40,.38),(.33,-.28),(.16,-.48),(-.16,-.48),(-.33,-.28)],.22,self.RED2,-.38,.055,114)
        self.panel([(-.25,.28),(-.12,.43),(.12,.43),(.25,.27),(.20,-.22),(0,-.38),(-.20,-.22)],.08,self.RED_HI,-.50,.03,116)
        # Rear thigh wrap.
        self.panel([(-.33,.35),(-.18,.50),(.18,.50),(.33,.33),(.27,-.30),(0,-.44),(-.27,-.30)],.15,self.RED_DARK,.38,.045,106)
        glPopMatrix()
        # Knee.
        glPushMatrix(); glTranslatef(s*.50,-.02,.98)
        self.sphere((.34,.30,.25),self.JOINT,34,22)
        self.panel([(-.28,.18),(-.17,.34),(0,.39),(.17,.34),(.28,.18),(.20,-.19),(0,-.28),(-.20,-.19)],.18,self.RED_HI,-.38,.04,112)
        self.panel([(-.13,.12),(.13,.12),(.11,-.17),(0,-.25),(-.11,-.17)],.08,self.GOLD,-.50,.025,114)
        glPopMatrix()
        # Shin and ankle.
        glPushMatrix(); glTranslatef(s*.50,0,.35)
        self.capsule(.30,.34,self.METAL,scale=(1.0,1.12,1.0))
        self.panel([(-.32,.38),(-.20,.52),(.20,.52),(.32,.34),(.27,-.30),(.14,-.45),(-.14,-.45),(-.27,-.30)],.20,self.RED2,-.37,.05,114)
        self.panel([(-.18,.26),(.18,.26),(.16,-.27),(0,-.39),(-.16,-.27)],.08,self.GOLD,-.49,.025,112)
        self.panel([(-.29,.28),(-.16,.40),(.16,.40),(.29,.28),(.25,-.25),(0,-.38),(-.25,-.25)],.13,self.RED_DARK,.35,.04,106)
        glPopMatrix()
        # Boot gives the leg a believable termination.
        glPushMatrix(); glTranslatef(s*.50,-.08,-.28)
        self.sphere((.34,.54,.20),self.METAL2,36,22)
        self.panel([(-.36,.16),(-.22,.30),(.22,.30),(.38,.12),(.42,-.18),(.22,-.30),(-.26,-.30),(-.42,-.15)],.22,self.RED_HI,-.48,.045,112)
        self.panel([(-.20,.10),(.20,.10),(.25,-.15),(-.25,-.15)],.09,self.GOLD,-.61,.025,112)
        glPopMatrix()

    def back_suit(self):
        # Full upper-back shell.
        glPushMatrix(); glTranslatef(0,.18,4.16)
        self.sphere((.90,.39,1.12),self.METAL,42,26)
        self.panel([(-.76,.48),(-.46,.78),(0,.88),(.46,.78),(.76,.48),(.62,.04),(.34,-.20),(0,-.10),(-.34,-.20),(-.62,.04)],.24,self.RED2,.50,.065,114)
        for s in (-1,1):
            self.panel([(s*.08,.62),(s*.43,.72),(s*.66,.40),(s*.54,.03),(s*.23,.14)],.12,self.RED_HI,.64,.04,110)
        # Spine vertebrae and lower-back shell.
        for i,z in enumerate((.46,.20,-.06,-.32,-.58,-.82)):
            w=.11 if i<3 else .14
            self.panel([(-w,z+.12),(w,z+.12),(w*.90,z-.05),(w*.55,z-.15),(-w*.55,z-.15),(-w*.90,z-.05)],.10,self.METAL2,.71,.022,118)
        glPopMatrix()
        glPushMatrix(); glTranslatef(0,.16,3.02)
        self.panel([(-.55,.38),(-.34,.55),(0,.62),(.34,.55),(.55,.38),(.48,-.38),(0,-.52),(-.48,-.38)],.20,self.RED_DARK,.49,.055,108)
        self.panel([(-.30,.30),(0,.46),(.30,.30),(.26,-.25),(0,-.38),(-.26,-.25)],.10,self.METAL2,.62,.025,114)
        glPopMatrix()
        # Rear arm/leg shells close the suit from 360 degrees.
        for s in (-1,1):
            glPushMatrix(); glTranslatef(s*1.08,.28,4.04)
            self.panel([(-.26,.40),(-.15,.52),(.15,.52),(.26,.34),(.22,-.30),(0,-.42),(-.22,-.30)],.15,self.RED_DARK,.38,.045,106)
            glPopMatrix()
            glPushMatrix(); glTranslatef(s*.50,.28,1.64)
            self.panel([(-.33,.42),(-.18,.56),(.18,.56),(.33,.36),(.28,-.34),(0,-.47),(-.28,-.34)],.16,self.RED_DARK,.38,.045,106)
            glTranslatef(0,0,-1.30)
            self.panel([(-.28,.38),(-.16,.51),(.16,.51),(.28,.32),(.23,-.32),(0,-.43),(-.23,-.32)],.15,self.RED_DARK,.36,.04,106)
            glPopMatrix()

    def reactor(self, t):
        glPushMatrix(); glTranslatef(0,-.91,4.05)
        pulse=.88+.12*math.sin(t*3.4)
        glDisable(GL_LIGHTING); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE); glDepthMask(GL_FALSE)
        glColor4f(.02,.55,1,.14*pulse); glScalef(1,.7,1); gluSphere(self.q,.62,36,24)
        glDepthMask(GL_TRUE); glDisable(GL_BLEND); glEnable(GL_LIGHTING)
        self.cylinder(.43,.38,.10,self.METAL2,48)
        glTranslatef(0,0,.10); self.cylinder(.29,.22,.065,self.CYAN,48)
        glDisable(GL_LIGHTING); glColor4f(*self.WHITE); glBegin(GL_TRIANGLE_FAN); glVertex3f(0,-.02,.15)
        for i in range(33):
            a=2*math.pi*i/32; glVertex3f(.17*math.cos(a),-.02+.17*math.sin(a),.15)
        glEnd(); glEnable(GL_LIGHTING)
        glPopMatrix()

    def draw(self, t):
        # Pose each major anatomical assembly; the back shell is drawn separately
        # so it remains a real part of the suit during rotation.
        a=self.begin("pelvis",t); self.pelvis(); self.end()
        a=self.begin("torso",t); self.chest(); self.abdomen(); self.back_suit(); self.end()
        a=self.begin("neck",t); self.neck(); self.end()
        a=self.begin("head",t); self.helmet(); self.end()
        a=self.begin("left_arm",t); self.arm(-1); self.end()
        a=self.begin("right_arm",t); self.arm(1); self.end()
        a=self.begin("left_leg",t); self.leg(-1); self.end()
        a=self.begin("right_leg",t); self.leg(1); self.end()
        self.reactor(t)
