import math
class DashboardAnimation:
    def __init__(self): self._entries={}; self._time=0
    def update(self,dt=.016):
        self._time+=dt
        for e in self._entries.values():
            if e["state"]=="in":
                e["entry"]=min(1,e["entry"]+.055)
                if e["entry"]>=1:e["state"]="orbit"
            elif e["state"]=="out": e["entry"]=max(0,e["entry"]-.065)
            else:e["angle"]+=e["speed"]
    @staticmethod
    def ease(t): return max(0,min(1,t))**2*(3-2*max(0,min(1,t)))
    def activate(self,panel,side,index,total):
        k=id(panel)
        if k in self._entries:
            e=self._entries[k]; e["state"]="orbit" if e["entry"]>=1 else "in"; e["index"]=index; e["total"]=max(1,total); return
        self._entries[k]={"panel":panel,"side":-1 if side<0 else 1,"index":index,"total":max(1,total),
                          "angle":-math.pi/2+(index-(total-1)/2)*.9,"speed":.0028+index*.00055,"entry":0,"state":"in"}
    def deactivate(self,panel,side):
        e=self._entries.get(id(panel))
        if e:e["side"]=-1 if side<0 else 1;e["state"]="out"
    def remove_finished(self):
        for k,e in list(self._entries.items()):
            if e["state"]=="out" and e["entry"]<=0:del self._entries[k]
    def position_for(self,panel,cx,cy,cw,ch):
        e=self._entries.get(id(panel))
        if e is None:self.activate(panel,1,0,1);e=self._entries[id(panel)]
        t=self.ease(e["entry"]); a=e["angle"]
        if e["total"]>1:a+=(e["index"]-(e["total"]-1)/2)*.34
        rx=max(335,cw*.64); ry=max(250,ch*.48)
        ox=cx+math.cos(a)*rx; oy=cy+math.sin(a)*ry
        sx=cx+e["side"]*(cw+650); sy=cy+math.sin(a)*(ry+80)
        x=sx+(ox-sx)*t;y=sy+(oy-sy)*t;d=(math.sin(a)+1)/2;s=.82+d*.18
        return x-panel.width*s/2,y-panel.height*s/2,s,d
