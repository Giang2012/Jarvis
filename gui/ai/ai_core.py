from PySide6.QtGui import *
from PySide6.QtCore import *
from gui.ai.reactor import Reactor
from gui.ai.ring import Ring
from gui.ai.particle_system import ParticleSystem
from gui.ai.orbit import Orbit
from gui.ai.background import LivingBackground
from gui.ai.pulse import Pulse
from gui.ai.floating_text import FloatingText
from gui.ai.data_fish import DataFish
from gui.ai.energy_link import EnergyLink
from gui.ai.glow import Glow
from gui.ai.mouse_gravity import MouseGravity
from gui.ai.ai_state import AIState
from gui.ai.eyes import AIEyes
from gui.ai.emotion import Emotion
from gui.ai.glass import GlassReflection
from gui.ai.radar import Radar
from gui.ai.data_stream import DataStream
from gui.ai.star import StarField
from gui.ai.voice_visualizer import VoiceVisualizer
from gui.ai.dynamic_ring import DynamicRing
from gui.ai.lightning import Lightning
from gui.ai.quantum_noise import QuantumNoise
import math


class AICore:

    def __init__(self):

        # =========================
        # Core
        # =========================

        self.time = 0

        self.state = AIState.IDLE
        self.emotion = Emotion.CALM

        # =========================
        # Main Objects
        # =========================

        self.reactor = Reactor()

        # =========================
        # Effects
        # =========================

        self.background = LivingBackground()

        self.glow = Glow()

        self.radar = Radar()

        self.glass = GlassReflection()

        self.pulse = Pulse()

        self.energy = EnergyLink()

        self.dynamicRing = DynamicRing()

        self.lightning = Lightning()

        self.noise = QuantumNoise()

        self.voice = VoiceVisualizer()

        self.stream = DataStream()

        self.starField = StarField()

        # =========================
        # Interaction
        # =========================

        self.gravity = MouseGravity()

        self.eyes = AIEyes()

        # =========================
        # Particle System
        # =========================

        self.particles = ParticleSystem()

        self.particles.setGravity(
            self.gravity
        )

        # =========================
        # Rings
        # =========================

        self.ring1 = Ring(
            radius=45,
            speed=0.50,
            width=2
        )

        self.ring2 = Ring(
            radius=70,
            speed=-0.30,
            width=2
        )

        self.ring3 = Ring(
            radius=95,
            speed=0.20,
            width=1
        )

        # =========================
        # Floating Text
        # =========================

        self.texts = [
            FloatingText()
            for _ in range(6)
        ]

        # =========================
        # Orbits
        # =========================

        self.orbits = [
            Orbit()
            for _ in range(12)
        ]

        # =========================
        # Data Fish
        # =========================

        self.fishes = [
            DataFish(
                angle=(i * 360 / 8),
                radius=55 + (i % 3) * 18,
                speed=0.25 + (i % 4) * 0.08,
                size=0.8 + (i % 3) * 0.25
            )
            for i in range(8)
        ]
    # --------------------------

    def draw(self, painter):

        self.update()

        # ----------------------------
        # Đồng bộ trạng thái
        # ----------------------------

        self.glow.setState(self.state.value)
        self.reactor.setState(self.state.value)

        # Test Voice (xóa sau khi có micro)
        self.voice.setLevel(
            abs(math.sin(self.time * 2))
        )

        painter.save()

        # ============================
        # Background
        # ============================

        self.background.draw(painter)

        self.starField.draw(painter)

        self.stream.draw(painter)

        self.noise.draw(painter)

        # ============================
        # Glow
        # ============================

        self.glow.draw(painter)

        self.radar.draw(painter)

        # ============================
        # Scale toàn bộ AI
        # ============================

        scale = 1 + math.sin(self.time) * 0.015

        painter.save()

        painter.scale(scale, scale)

        # ============================
        # Particles
        # ============================

        self.particles.draw(painter)

        self.energy.draw(painter)

        # ============================
        # Orbit
        # ============================

        for orbit in self.orbits:

            orbit.draw(painter)

        # ============================
        # Fish
        # ============================

        for fish in self.fishes:

            fish.draw(painter)

        # ============================
        # Energy Structure
        # ============================

        self.dynamicRing.draw(painter)

        # ============================
        # Voice
        # ============================

        self.voice.draw(painter)

        # ============================
        # Reactor
        # ============================


        self.reactor.draw(painter)

        self.lightning.draw(painter)

        self.eyes.draw(painter)

        self.pulse.draw(painter)

        # ============================
        # Text
        # ============================

        for text in self.texts:

            text.draw(painter)

        painter.restore()

        # ============================
        # Glass Reflection
        # ============================

        self.glass.draw(painter)

        painter.restore()
    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        self.time += 0.04

        # Sau này sẽ cập nhật Animation Engine ở đây


    # =====================================================
    # INPUT
    # =====================================================

    def setMouse(self, pos):

        self.gravity.setMouse(pos)

        self.eyes.setMouse(pos)


    # =====================================================
    # STATE
    # =====================================================

    def setState(self, state):

        self.state = state


    # =====================================================
    # EMOTION
    # =====================================================

    def setEmotion(self, emotion):

        self.emotion = emotion