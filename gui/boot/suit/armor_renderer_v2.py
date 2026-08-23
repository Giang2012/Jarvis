from gui.boot.suit.helmet import Helmet
from gui.boot.suit.chest import Chest
from gui.boot.suit.arm import Arm
from gui.boot.suit.leg import Leg
from gui.boot.suit.shoulder import Shoulder
from gui.boot.suit.reactor import SuitReactor
from gui.boot.suit.spark import Spark
from gui.boot.suit.arc import ElectricArc
from gui.boot.suit.eyes import Eyes
from gui.common.effects.camera import CameraShake
from gui.common.effects.flash import Flash
from gui.common.effects.body_scanner import BodyScanner
from gui.boot.suit.hud_data import HUDData
from gui.boot.suit.faceplate import FacePlate
from gui.boot.suit.lock_indicator import LockIndicator
from gui.boot.suit.wireframe import WireFrame
from gui.boot.suit.grid import HologramGrid
from gui.boot.suit.digital_code import DigitalCode
from gui.boot.suit.reactor_hud import ReactorHUD
from gui.boot.suit.reactor_status import ReactorStatus
from gui.boot.suit.servo_light import ServoLight
from gui.boot.suit.servo_sparks import ServoSparks
from gui.boot.suit.lock_effect import LockEffect

class ArmorRendererV2:

    def __init__(self):

        self.helmet = Helmet()
        self.chest = Chest()

        self.leftShoulder = Shoulder(True)
        self.rightShoulder = Shoulder(False)

        self.leftArm = Arm(True)
        self.rightArm = Arm(False)

        self.leftLeg = Leg(True)
        self.rightLeg = Leg(False)

        self.reactor = SuitReactor()
        self.sparks = []

        self.flash = Flash()

        for i in range(60):

            self.sparks.append(
                Spark()
            )
        self.arcLeft = ElectricArc()
        self.arcRight = ElectricArc()

        self.eyes = Eyes()

        self.camera = CameraShake()

        self.stage = -1

        self.scanner = BodyScanner()

        self.hud = HUDData()

        self.faceplate = FacePlate()

        self.wire = WireFrame()

        self.grid = HologramGrid()

        self.code = DigitalCode()

        self.reactorHud = ReactorHUD()

        self.status = ReactorStatus()

        self.servo = ServoLight()

        self.sparks = ServoSparks()

        self.lock = LockEffect()

        self.lockHead = LockIndicator(-180,-150,"HEAD")
        self.lockChest = LockIndicator(-180,-10,"CHEST")
        self.lockLeft = LockIndicator(120,-20,"LEFT ARM")
        self.lockRight = LockIndicator(120,50,"RIGHT ARM")
        self.lockPower = LockIndicator(-180,150,"POWER")
        # ==========================
        # Assemble Animation
        # ==========================

        self.time = 0

    # ===================================

    def update(self):


        if self.time < 420:
            self.time += 3

        oldStage = self.stage

        if self.time < 60:

            self.stage = 0

        elif self.time < 120:

            self.stage = 1

        elif self.time < 180:

            self.stage = 2

        elif self.time < 240:

            self.stage = 3

        elif self.time < 340:

            self.stage = 4

        else:

            self.stage = 5


        if oldStage != self.stage:

            self.camera.shake(8)

        if self.stage == 5 and oldStage != 5:

            self.flash.trigger()

    # ===================================

    def draw(self, painter):

        self.update()

        if self.time > 40:

            self.grid.draw(painter)

        if self.time > 80:

            self.code.draw(painter)
            self.servo.draw(painter)
            self.sparks.draw(painter)

        if self.time < 360:

            self.wire.draw(painter)

        dx, dy = self.camera.offset()

        painter.save()

        painter.translate(dx, dy)

        # ---------------- Helmet ----------------

        self.helmet.draw(painter)

        if self.time > 395:

            self.faceplate.draw(painter)

        if self.time > 120:

            self.lock.draw(
                painter,
                0,
                -175,
                "HELMET LOCKED"
            )

        # ---------------- Shoulders ----------------

        if self.time > 120:

            self.leftShoulder.draw(painter)
            self.rightShoulder.draw(painter)

        # ---------------- Chest ----------------

        if self.time > 60:

            self.chest.draw(painter)

        if self.time > 180:

            self.lock.draw(
                painter,
                0,
                150,
                "CHEST LOCKED"
            )

        # ---------------- Arms ----------------

        if self.time > 180:

            self.leftArm.draw(painter)
            self.rightArm.draw(painter)

            if self.time > 240:

                self.lock.draw(
                    painter,
                    -170,
                    40,
                    "ARM LOCKED"
                )
        # ---------------- Legs ----------------

        if self.time > 240:

            self.leftLeg.draw(painter)
            self.rightLeg.draw(painter)

            if self.time > 300:

                self.lock.draw(
                    painter,
                    170,
                    260,
                    "LEG LOCKED"
                )

        # ---------------- Reactor ----------------

        if self.time > 340:

            self.reactor.draw(painter)

        if self.time > 360:

            self.reactorHud.draw(painter)

            self.status.draw(painter)

        if self.time > 360:

            self.scanner.draw(painter)

        if self.time > 390:

            self.hud.draw(painter)

        if self.time > 70:
            self.lockHead.draw(painter)

        if self.time > 140:
            self.lockChest.draw(painter)

        if self.time > 220:
            self.lockLeft.draw(painter)

        if self.time > 270:
            self.lockRight.draw(painter)

        if self.time > 360:
            self.lockPower.draw(painter)

        if self.time > 390:

            self.eyes.draw(painter)

        if self.time > 340:

            painter.save()

            painter.translate(-55,25)

            self.arcLeft.draw(painter)

            painter.restore()

            painter.save()

            painter.translate(55,25)

            painter.scale(-1,1)

            self.arcRight.draw(painter)

            painter.restore()

        if self.time > 330:

            for s in self.sparks:

                s.draw(painter)

        painter.restore()

        self.flash.draw(
            painter,
            painter.viewport()
        )