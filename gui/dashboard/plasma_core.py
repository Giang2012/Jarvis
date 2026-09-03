import math, random
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QRadialGradient

class PlasmaCore:
    def __init__(self, seed=731):
        rng=random.Random(seed); self.particles=[]; self.t=0.0; self.pulse=0.0
        for _ in range(1250):
            self.particles.append({
                "r":rng.random()**1.75,"a":rng.random()*math.tau,
                "speed":rng.uniform(.0015,.009),"size":rng.choice((.6,.8,1,1.2,1.6,2)),
                "alpha":rng.randint(35,175),"phase":rng.random()*math.tau})
    def update(self,dt=.016):
        self.t+=dt; self.pulse=(math.sin(self.t*2)+1)/2
    def draw(self,painter,center,radius,accent=None):
        accent=QColor(accent or "#00D8FF"); cx,cy=center.x(),center.y()
        painter.save(); painter.setRenderHint(QPainter.Antialiasing)
        g=QRadialGradient(QPointF(cx,cy),radius)
        a=QColor(accent); a.setAlpha(105+int(self.pulse*20))
        b=QColor(accent); b.setAlpha(28); z=QColor(accent); z.setAlpha(0)
        g.setColorAt(0,a); g.setColorAt(.28,b); g.setColorAt(.72,z); g.setColorAt(1,z)
        painter.setPen(QPen(Qt.NoPen)); painter.setBrush(QBrush(g))
        painter.drawEllipse(QRectF(cx-radius,cy-radius,radius*2,radius*2))
        painter.setBrush(Qt.NoBrush)
        for i,f in enumerate((.3,.43,.56,.69,.82,.94)):
            c=QColor(accent); c.setAlpha(max(7,34-i*4+int(self.pulse*6)))
            painter.setPen(QPen(c,1.15 if i<3 else .8))
            rr=radius*f; painter.drawEllipse(QRectF(cx-rr,cy-rr,rr*2,rr*2))
        for p in self.particles:
            ang=p["a"]+self.t*p["speed"]*75
            rr=radius*(p["r"]+math.sin(self.t*1.7+p["phase"])*.025)
            x=cx+math.cos(ang)*rr; y=cy+math.sin(ang)*rr*.76
            depth=(math.sin(ang*1.7+p["phase"])+1)/2
            c=QColor(accent); c.setAlpha(int(max(18,min(220,p["alpha"]*(.55+depth*.75)))))
            painter.setPen(QPen(Qt.NoPen)); painter.setBrush(QBrush(c))
            s=p["size"]*(.65+depth*.8); painter.drawEllipse(QRectF(x-s,y-s,s*2,s*2))
        core=radius*(.055+self.pulse*.008)
        g2=QRadialGradient(QPointF(cx,cy),core*2.6)
        white=QColor(240,255,255,245); c=QColor(accent); c.setAlpha(175); clear=QColor(accent); clear.setAlpha(0)
        g2.setColorAt(0,white); g2.setColorAt(.18,c); g2.setColorAt(.65,clear); g2.setColorAt(1,clear)
        painter.setBrush(QBrush(g2)); painter.drawEllipse(QRectF(cx-core*2.6,cy-core*2.6,core*5.2,core*5.2))
        painter.restore()
