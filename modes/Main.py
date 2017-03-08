from filters.CountingLine import CountingLine
from filters.EyeHighlighter import EyeHighlighter
from filters.FaceHighlighter import FaceHighlighter
from filters.FaceTransform import FaceTransform
from filters.Fps import Fps
from filters.Info import Info
from filters.Landmarks import Landmarks
from filters.Recolour import Recolour
from modes.Mode import Mode


class Main(Mode):
    NAME = "Main"

    def __init__(self):
        super(Main, self).__init__()

    def filters(self):
        return [Fps.NAME, Info.NAME, Landmarks.NAME, FaceHighlighter.NAME, EyeHighlighter.NAME, CountingLine.NAME,
                Recolour.NAME, FaceTransform.NAME]
