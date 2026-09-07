from __future__ import annotations
import math, random
from dataclasses import dataclass
from typing import List, Tuple
from PySide6.QtCore import QPointF
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF

Vec3 = Tuple[float,float,float]

@dataclass
class Face:
    pts: List[Vec3]
    shade: float
    edge: bool = True

class ArmorRendererV2:
    """Procedural pseudo-3D powered armor renderer.

    Uses real 3D coordinates, perspective projection, face depth sorting and
    animated assembly. It intentionally avoids external 3D dependencies so the
    existing PySide6 BootScreen can keep calling paint(painter, center, scale).
    """
    def __init__(self):
        self.t = 0.0
        self.rng = random.Random(7)
        self.spark_seed = [self.rng.random() for _ in range(90)]

    def update(self, dt=0.016):
        self.t += max(0.0, float(dt))

    # ---------- 3D math ----------
    @staticmethod
    def _rot(v: Vec3, rx=0, ry=0, rz=0) -> Vec3:
        x,y,z=v
        cx,sx=math.cos(rx),math.sin(rx); cy,sy=math.cos(ry),math.sin(ry); cz,sz=math.cos(rz),math.sin(rz)
        y,z=y*cx-z*sx,y*sx+z*cx
        x,z=x*cy+z*sy,-x*sy+z*cy
        x,y=x*cz-y*sz,x*sz+y*cz
        return x,y,z

    @staticmethod
    def _add(a,b): return a[0]+b[0],a[1]+b[1],a[2]+b[2]

    def _project(self, v: Vec3, cx, cy, s):
        x,y,z=v
        # camera sits in front; perspective makes side depth visible
        f=520.0
        q=f/(f+z*0.75)
        return QPointF(cx+x*s*q, cy+y*s*q), z

    def _box(self, c:Vec3, size:Vec3, rot=(0,0,0), bevel=0.0, shade=1.0) -> List[Face]:
        sx,sy,sz=[v/2 for v in size]
        verts=[(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),
               (-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
        verts=[self._add(c,self._rot(v,*rot)) for v in verts]
        # outward winding, front/back + sides
        idx=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
        normals=[(0,0,-1),(0,0,1),(0,-1,0),(1,0,0),(0,1,0),(-1,0,0)]
        faces=[]
        light=(0.25,-0.65,-0.72)
        ll=math.sqrt(sum(k*k for k in light)); light=tuple(k/ll for k in light)
        for ids,n in zip(idx,normals):
            nn=self._rot(n,*rot)
            dot=max(0.0,sum(nn[i]*light[i] for i in range(3)))
            faces.append(Face([verts[i] for i in ids], 0.34+0.66*dot*shade))
        return faces

    def _cyl(self,c:Vec3,r,depth,rot=(0,0,0),n=12,shade=1.0) -> List[Face]:
        # cylinder axis is local Y; rings give curved 3D volume
        pts=[]
        for yy in (-depth/2,depth/2):
            ring=[]
            for i in range(n):
                a=2*math.pi*i/n
                ring.append(self._add(c,self._rot((r*math.cos(a),yy,r*math.sin(a)),*rot)))
            pts.append(ring)
        faces=[]
        for i in range(n):
            faces.append(Face([pts[0][i],pts[0][(i+1)%n],pts[1][(i+1)%n],pts[1][i]], 0.42+0.58*(0.5+0.5*math.cos(2*math.pi*(i/n)-0.8))*shade))
        faces.append(Face(list(reversed(pts[0])),0.45*shade)); faces.append(Face(pts[1],0.65*shade))
        return faces

    def _part(self, faces, p, c, s, outline=True):
        # depth-sort at render time; kept as raw faces
        return faces

    # ---------- anatomy / assembly ----------
    def _assembly(self):
        t=self.t
        # Assembly envelope: 0..7.0 sec. After that, idle micro motion.
        start={
            'pelvis':2.0,'torso':1.45,'neck':1.65,'head':0.95,
            'l_shoulder':2.0,'r_shoulder':2.0,'l_upper':2.25,'r_upper':2.25,
            'l_elbow':2.65,'r_elbow':2.65,'l_fore':2.85,'r_fore':2.85,'l_hand':3.25,'r_hand':3.25,
            'l_hip':2.55,'r_hip':2.55,'l_thigh':2.75,'r_thigh':2.75,'l_knee':3.15,'r_knee':3.15,
            'l_shin':3.35,'r_shin':3.35,'l_boot':3.75,'r_boot':3.75,'reactor':4.0
        }
        out=[]
        def active(name):
            a=start[name]
            return max(0,min(1,(t-a)/0.48))
        def appear(pos,name,axis=(0, -1, 0)):
            k=active(name)
            # cubic ease-out
            e=1-(1-k)**3
            return (pos[0]+axis[0]*(1-e)*55,pos[1]+axis[1]*(1-e)*55,pos[2]+axis[2]*(1-e)*55)
        # body proportions, z positive means toward camera in this renderer
        out.append(('pelvis',self._box(appear((0,105,2),'pelvis'),(92,48,46),rot=(0,0,0.0),shade=.98)))
        out.append(('torso',self._box(appear((0,18,0),'torso'),(132,154,62),rot=(0,0,0),shade=1.0)))
        # chest layered plates: angled to create curved silhouette
        out.append(('chest',self._box(appear((0,-4,34),'torso'),(112,78,16),rot=(math.radians(-5),0,0),shade=1.08)))
        out.append(('chest2',self._box(appear((0,42,36),'torso'),(96,42,15),rot=(math.radians(7),0,0),shade=.98)))
        for y,w in [(-33,52),(-2,58),(28,53),(56,45)]:
            out.append(('abd',self._box(appear((0,y,34),'torso'),(w,20,15),rot=(math.radians(2),0,0),shade=.9)))
        # neck and head shell
        out.append(('neck',self._cyl(appear((0,-76,0),'neck'),18,30,n=12,shade=.9)))
        out.append(('head',self._box(appear((0,-116,0),'head'),(76,88,72),rot=(math.radians(-4),0,0),shade=1.02)))
        out.append(('jaw',self._box(appear((0,-91,38),'head'),(58,28,22),rot=(math.radians(-2),0,0),shade=.92)))
        out.append(('face',self._box(appear((0,-125,38),'head'),(52,25,11),rot=(math.radians(-5),0,0),shade=.82)))
        # shoulders + arms: explicit joint chain
        for side,sg in [('l',-1),('r',1)]:
            x=sg*83
            out.append((side+'_shoulder',self._cyl(appear((x,-25,0),side+'_shoulder'),30,42,rot=(0,0,math.radians(90)),n=12,shade=1.0)))
            out.append((side+'_upper',self._box(appear((sg*105,10,0),side+'_upper'),(42,74,48),rot=(0,0,math.radians(sg*4)),shade=.98)))
            out.append((side+'_elbow',self._cyl(appear((sg*105,51,2),side+'_elbow'),22,28,rot=(0,0,math.radians(90)),n=12,shade=.9)))
            out.append((side+'_fore',self._box(appear((sg*105,88,0),side+'_fore'),(46,70,50),rot=(0,0,math.radians(sg*-5)),shade=.96)))
            out.append((side+'_wrist',self._cyl(appear((sg*105,125,1),side+'_hand'),15,20,rot=(0,0,math.radians(90)),n=12,shade=.85)))
            out.append((side+'_hand',self._box(appear((sg*105,145,0),side+'_hand'),(40,42,48),rot=(math.radians(5),0,math.radians(sg*3)),shade=.98)))
            # little knuckle guards
            for dx in (-12,0,12):
                out.append((side+'_knuckle',self._box(appear((sg*105+dx,166,4),side+'_hand'),(9,18,17),shade=.84)))
        # hips + legs
        for side,sg in [('l',-1),('r',1)]:
            x=sg*37
            out.append((side+'_hip',self._cyl(appear((x,130,0),side+'_hip'),23,34,rot=(0,0,math.radians(90)),n=12,shade=.9)))
            out.append((side+'_thigh',self._box(appear((x,181,0),side+'_thigh'),(55,92,58),rot=(math.radians(2),0,math.radians(sg*2)),shade=.98)))
            out.append((side+'_knee',self._cyl(appear((x,233,8),side+'_knee'),24,28,rot=(0,0,math.radians(90)),n=12,shade=.9)))
            out.append((side+'_shin',self._box(appear((x,280,0),side+'_shin'),(48,86,54),rot=(math.radians(-2),0,math.radians(sg*1)),shade=.95)))
            out.append((side+'_ankle',self._cyl(appear((x,327,2),side+'_boot'),15,22,rot=(0,0,math.radians(90)),n=12,shade=.84)))
            out.append((side+'_boot',self._box(appear((x+sg*7,346,10),side+'_boot'),(56,40,82),rot=(math.radians(4),0,math.radians(sg*2)),shade=1.0)))
        out.append(('reactor',self._cyl(appear((0,20,43),'reactor'),25,12,n=18,shade=1.0)))
        return out

    def paint(self, painter:QPainter, center, scale):
        # The existing BootScreen may pass a QPointF or tuple.
        cx=float(center.x()) if hasattr(center,'x') else float(center[0])
        cy=float(center.y()) if hasattr(center,'y') else float(center[1])
        faces=[]
        for name,fs in self._assembly():
            for f in fs:
                faces.append((sum(v[2] for v in f.pts)/len(f.pts),name,f))
        # farther first
        faces.sort(key=lambda q:q[0])
        for _,name,f in faces:
            pts=[]; zs=[]
            for v in f.pts:
                q,z=self._project(v,cx,cy,scale)
                pts.append(q); zs.append(z)
            # avoid drawing faces behind the camera
            if max(zs)>390: continue
            # metallic neutral palette with slight blue/steel bias, reactor handled later
            sh=max(.22,min(1.15,f.shade))
            base=42+int(82*sh)
            # front-facing faces brighter; edges create hard-surface readability
            fill=QColor(base,base+min(10,int(8*sh)),base+min(18,int(16*sh)),245)
            if 'face' in name:
                fill=QColor(92,98,106,250)
            painter.setBrush(QBrush(fill))
            painter.setPen(QPen(QColor(18,22,28,230), max(1.0,0.9*scale)))
            painter.drawPolygon(QPolygonF(pts))
        self._details(painter,cx,cy,scale)

    def _details(self,p,cx,cy,s):
        # seam lines and luminous reactor, projected in front of shell
        def line(a,b,pen):
            qa,_=self._project(a,cx,cy,s); qb,_=self._project(b,cx,cy,s); p.setPen(pen); p.drawLine(qa,qb)
        pen=QPen(QColor(8,12,17,210),max(1,1.2*s))
        # central seams
        for y in (-65,-25,12,47,80): line((0,y,45),(0,y+10,45),pen)
        line((-52,-25,43),(52,-25,43),pen); line((-47,0,44),(47,0,44),pen)
        # joint pistons
        joint_pen=QPen(QColor(155,165,175,230),max(1,1.8*s))
        for sg in (-1,1):
            line((sg*105,50,18),(sg*105,87,18),joint_pen)
            line((sg*37,228,18),(sg*37,270,18),joint_pen)
        # reactor pulse
        pulse=0.82+0.18*math.sin(self.t*7)
        q,_=self._project((0,20,51),cx,cy,s)
        r=16*s*pulse
        p.setBrush(QBrush(QColor(95,180,235,190))); p.setPen(QPen(QColor(150,215,255,240),max(1,2*s)))
        p.drawEllipse(q,r,r)
        p.setBrush(QBrush(QColor(210,245,255,235))); p.setPen(QPen(QColor(190,235,255,240),max(1,1*s)))
        p.drawEllipse(q,5*s,5*s)
        # helmet visor slit
        a,_=self._project((-23,-127,43),cx,cy,s); b,_=self._project((23,-127,43),cx,cy,s)
        p.setPen(QPen(QColor(110,205,245,235),max(1,2.4*s))); p.drawLine(a,b)
        # animated servo sparks around joints during assembly / idle pulses
        if self.t<6.5:
            p.setPen(QPen(QColor(190,220,235,180),max(1,1*s)))
            for i,u in enumerate(self.spark_seed[:24]):
                tt=(self.t*1.9+u*3.7)%1
                if tt>.72:
                    x=(u-.5)*250; y=180+(u*410)%170
                    q,_=self._project((x,y,28),cx,cy,s)
                    p.drawPoint(q)
