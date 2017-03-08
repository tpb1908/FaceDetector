from filters.FaceHighlighter import FaceHighlighter
from filters.FaceTransform import FaceTransform
from filters.Fps import Fps
from filters.Info import Info
from filters.Landmarks import Landmarks
from filters.Recolour import Recolour
from modes.Mode import Mode


class Capture(Mode):

    NAME = "Capture"

    def __init__(self):
        super(Capture, self).__init__()

    def filters(self):
        return [Fps.NAME, Info.NAME, Landmarks.NAME, FaceHighlighter.NAME, FaceTransform.NAME, Recolour.NAME]