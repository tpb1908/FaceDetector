from ui.Mode import Mode
from collections import OrderedDict

from filters.Fps import Fps
from filters.Info import Info
from filters.Recolour import Recolour
from filters.FaceHighlighter import FaceHighlighter
from filters.Landmarks import Landmarks
from filters.FaceTransform import FaceTransform

class Capture(Mode):

    NAME = "Capture"

    def __init__(self):
        super(Capture, self).__init__()

        self._filters = OrderedDict()
        self._filters[Fps.NAME] = Fps(True)
        self._filters[Info.NAME] = Info(False)
        self._filters[Landmarks.NAME] = Landmarks(True)
        self._filters[FaceHighlighter.NAME] = FaceHighlighter(True)
        self._filters[FaceTransform.NAME] = FaceTransform(False)
        self._filters[Recolour.NAME] = Recolour(True)

    def get_filters(self):
        return self._filters