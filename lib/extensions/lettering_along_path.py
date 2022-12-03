# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import sys
from math import atan2, degrees

from inkex import Transform, errormsg
from inkex.units import convert_unit
from shapely.ops import substring

from ..elements import Stroke
from ..i18n import _
from ..svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_LETTERING, SVG_GROUP_TAG
from ..utils import DotDict
from ..utils import Point as InkstitchPoint
from .base import InkstitchExtension


class LetteringAlongPath(InkstitchExtension):
    '''
    This extension aligns an Ink/Stitch Lettering group along a path
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-o", "--options", type=str, default=None, dest="page_1")
        self.arg_parser.add_argument("-i", "--info", type=str, default=None, dest="page_2")
        self.arg_parser.add_argument("-s", "--stretch-spaces", type=int, default="", dest="stretch_spaces")

    def effect(self):
        text, path = self.get_selection()

        # we ignore everything but the first path/text
        text_bbox = text.bounding_box()
        text_y = text_bbox.bottom
        glyphs = [glyph for glyph in text.iterdescendants(SVG_GROUP_TAG) if len(glyph.label) == 1]

        path = Stroke(path).as_multi_line_string().geoms[0]
        path_length = path.length

        if self.options.stretch_spaces:
            self.load_settings(text)
            text = self.settings["text"]
            space_indices = [i for i, t in enumerate(text) if t == " "]
            text_width = convert_unit(text_bbox.width, "px", self.svg.unit)

            if len(text) - 1 != 0:
                stretch_space = (path_length - text_width) / (len(text) - 1)
            else:
                stretch_space = 0
        else:
            stretch_space = 0
            space_indices = []

        self.transform_glyphs(glyphs, path, stretch_space, space_indices, text_y)

    def transform_glyphs(self, glyphs, path, stretch_space, space_indices, text_y):
        distance = 0
        old_bbox = None
        i = 0

        for glyph in glyphs:
            # dimensions
            bbox = glyph.bounding_box()
            width = bbox.width
            x = bbox.left

            # adjust position
            if old_bbox:
                distance += bbox.left - old_bbox.right + stretch_space

            if self.options.stretch_spaces and i in space_indices:
                distance += stretch_space
                i += 1

            new_distance = distance + width

            # calculate and apply transform
            first = substring(path, distance, distance)
            last = substring(path, new_distance, new_distance)

            angle = degrees(atan2(last.y - first.y, last.x - first.x)) % 360
            translate = InkstitchPoint(first.x, first.y) - InkstitchPoint(x, text_y)

            transform = Transform(f"rotate({angle}, {first.x}, {first.y}) translate({translate.x} {translate.y})")
            glyph.transform = transform @ glyph.transform

            # set values for next iteration
            distance = new_distance
            old_bbox = bbox
            i += 1

    def load_settings(self, text):
        """Load the settings saved into the text element"""

        self.settings = DotDict({
            "text": "",
            "back_and_forth": False,
            "font": None,
            "scale": 100,
            "trim_option": 0
        })

        if INKSTITCH_LETTERING in text.attrib:
            try:
                self.settings.update(json.loads(text.get(INKSTITCH_LETTERING)))
            except (TypeError, ValueError):
                pass

    def get_selection(self):
        groups = list()
        paths = list()

        for node in self.svg.selection:
            lettering = False
            if node.tag == SVG_GROUP_TAG and INKSTITCH_LETTERING in node.attrib:
                groups.append(node)
                lettering = True
                continue

            for group in node.iterancestors(SVG_GROUP_TAG):
                if INKSTITCH_LETTERING in group.attrib:
                    groups.append(group)
                    lettering = True
                    break

            if not lettering and node.tag in EMBROIDERABLE_TAGS:
                paths.append(node)

        if not groups or not paths:
            errormsg(_("Please select one path and one Ink/Stitch lettering group."))
            sys.exit(1)

        return [groups[0], paths[0]]
