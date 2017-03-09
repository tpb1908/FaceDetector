from modes.Mode import Mode
import filters


class Capture(Mode):
    NAME = "Capture"

    def __init__(self):
        super(Capture, self).__init__()
        self._enrollee = None

    def filters(self):
        return [filters.Fps.Fps.NAME, filters.Info.Info.NAME, filters.Landmarks.Landmarks.NAME,
                filters.FaceHighlighter.FaceHighlighter.NAME, filters.FaceTransform.FaceTransform.NAME,
                filters.Recolour.Recolour.NAME]

    def enrollee(self):
        return self._enrollee

    def set_enrollee(self, name):
        self._enrollee = name
