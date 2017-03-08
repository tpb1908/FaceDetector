from ui.Mode import Mode
from collections import OrderedDict
from filters.Fps import Fps
from filters.Info import Info
from filters.Recolour import Recolour
from filters.EyeHighlighter import EyeHighlighter
from filters.FaceHighlighter import FaceHighlighter
from filters.Landmarks import Landmarks
from filters.FaceTransform import FaceTransform
from filters.CountingLine import CountingLine

class Main(Mode):

    NAME = "Main"

    def __init__(self, height):
        super(Main, self).__init__()

        self._filters = OrderedDict()
        self._filters[Fps.NAME] = Fps(True)
        self._filters[Info.NAME] = Info(False)
        self._filters[Landmarks.NAME] = Landmarks(True)
        self._filters[FaceHighlighter.NAME] = FaceHighlighter(True)
        self._filters[EyeHighlighter.NAME] = EyeHighlighter(True)
        self._filters[CountingLine.NAME] = CountingLine(height / 2, True)
        self._filters[Recolour.NAME] = Recolour(True)
        self._filters[FaceTransform.NAME] = FaceTransform(False)


    def filters(self):
        return self._filters