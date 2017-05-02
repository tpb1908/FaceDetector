
class Painter():

    @staticmethod
    def rectangle(image, left, top, right, bottom, color, width):
        Painter.line(image, left, top, right, top, color, width)
        Painter.line(image, left, bottom, right, bottom, color, width)
        Painter.line(image, left, top, left, bottom, color, width)
        Painter.line(image, right, top, right, bottom, color, width)

    @staticmethod
    def line(image, y0, x0, y1, x1, color, width):
        deltax = float(x1 - x0)
        deltay = float(y1 - y0)

        if deltax == 0:
            for y in range(min(y0, y1), max(y0, y1)):
                Painter.point(image, x0, y, color, width)
        elif deltay == 0:
            for x in range(min(x0, x1), max(x0, x1)):
                Painter.point(image, x, y0, color, width)
        else:
            if deltay > deltax:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                deltax = float(x1 - x0)
                deltay = float(y1 - y0)

            deltaerr = abs(deltay / deltax)
            error = deltaerr - 0.5
            y = y0
            for x in range(x0, x1):
                Painter.point(image, x, y, color, width)
                error += deltaerr
                if error >= 0.5:
                    y += 1
                    error -= 1

    @staticmethod
    def point(image, x0, y0, color, size):
        for x in range(x0, min(x0 + size, image.shape[0])):
            for y in range(y0, min(y0 + size, image.shape[1])):
                image[x, y] = color

