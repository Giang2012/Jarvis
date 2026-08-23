
from gui.hud.reactor_component import ReactorComponent
from gui.hud.glow_component import GlowComponent
from gui.hud.particle_component import ParticleComponent
from gui.hud.energy_component import EnergyComponent
from gui.hud.eyes_component import EyesComponent


from gui.engine.object import Object

class AIObject(Object):

    def __init__(self):

        super().__init__()

        self.name = "AI Core"

        self.addComponent(ReactorComponent())
        self.addComponent(GlowComponent())
        self.addComponent(ParticleComponent())
        self.addComponent(EnergyComponent())
        self.addComponent(EyesComponent())