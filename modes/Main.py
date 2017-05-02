
import filters
from modes.Mode import Mode


class Main(Mode):
    NAME = "Main"

    def __init__(self):
        super(Main, self).__init__()

    def filters(self):

        return [
            filters.Fps.Fps.NAME, 
            filters.Info.Info.NAME, 
            filters.Landmarks.Landmarks.NAME,
            filters.MovementVector.MovementVector.NAME,
            filters.FaceHighlighter.FaceHighlighter.NAME,
            filters.EyeHighlighter.EyeHighlighter.NAME, 
            filters.CountingLine.CountingLine.NAME,
            filters.Recolour.Recolour.NAME, 
            filters.FaceTransform.FaceTransform.NAME,
            filters.Rec.Rec.NAME
        ]
