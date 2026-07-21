from kernel.kernel import kernel
from kernel.events import Events
from kernel.state import AIStatus


class StatusService:

    @staticmethod
    def set_ready():

        kernel.state.status = AIStatus.READY

        kernel.events.emit(
            Events.STATUS_CHANGED,
            AIStatus.READY
        )

    @staticmethod
    def set_listening():

        kernel.state.status = AIStatus.LISTENING

        kernel.events.emit(
            Events.STATUS_CHANGED,
            AIStatus.LISTENING
        )

    @staticmethod
    def set_thinking():

        kernel.state.status = AIStatus.THINKING

        kernel.events.emit(
            Events.STATUS_CHANGED,
            AIStatus.THINKING
        )

    @staticmethod
    def set_speaking():

        kernel.state.status = AIStatus.SPEAKING

        kernel.events.emit(
            Events.STATUS_CHANGED,
            AIStatus.SPEAKING
        )