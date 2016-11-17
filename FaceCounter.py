# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 13:54:09 2016

@author: johnsona15
"""


class FaceCounter(object):
    def __init__(self, shape, divider):
        self.height, self.width = shape
        self.divider = divider

        self.face_count = 0

    def update_count(self, matches, output_image=None):
        # self.log.debug("Updating count using %d matches...", len(matches))
        return