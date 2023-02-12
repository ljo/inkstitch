import re
from copy import copy
from math import degrees

from inkex import DirectedLineSegment, Path
from shapely.geometry import LineString
from shapely.ops import substring

from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..utils import string_to_floats
from .stitch import Stitch


class Lock:
    def __init__(self, lock_id=None, name=None, path=None, scale_percent=100, scale_absolute=0.7):

        self.id: str = lock_id
        self.name: str = name
        self.path: str = path
        self.scale_percent: float = scale_percent
        self.scale_absolute: float = scale_absolute

    def __repr__(self):
        return "Lock(%s, %s, %s, %s, %s)" % (self.id, self.name, self.path, self.scale_percent, self.scale_absolute)

    def copy(self, scale_percent=None, scale_absolute=None):
        cp = copy(self)
        cp.set('scale_percent', scale_percent or self.scale_percent)
        cp.set('scale_absolute', scale_absolute or self.scale_absolute)
        return cp

    def set(self, attribute, value):
        setattr(self, attribute, value)


class CustomLock(Lock):
    def stitches(self, stitches, pos):
        if not self.path:
            return half_stitch.stitches(stitches, pos)

        if not re.match("^ *[0-9 .,-]*$", self.path):
            path = Path(self.path)
            if not path or len(list(path.end_points)) < 3:
                return half_stitch.stitches(stitches, pos)
            else:
                return SVGLock(self.id,
                               self.name,
                               self.path,
                               self.scale_percent,
                               self.scale_absolute).stitches(stitches, pos)
        else:
            path = string_to_floats(self.path, " ")
            if path:
                return AbsoluteLock(self.id,
                                    self.name,
                                    self.path,
                                    self.scale_percent,
                                    self.scale_absolute).stitches(stitches, pos)
            else:
                return half_stitch.stitches(stitches, pos)


class RelativeLock(Lock):
    def stitches(self, stitches, pos):
        if pos == "end":
            stitches = list(reversed(stitches))

        path = string_to_floats(self.path, " ")

        to_previous = stitches[1] - stitches[0]
        length = to_previous.length()

        lock_stitches = []
        if length > 0.5 * PIXELS_PER_MM:

            # Travel back one stitch, stopping halfway there.
            # Then go forward one stitch, stopping halfway between
            # again.

            # but travel at most 1.5 mm
            length = min(length, 1.5 * PIXELS_PER_MM)

            direction = to_previous.unit()

            for delta in path:
                lock_stitches.append(Stitch(stitches[0] + delta * length * direction, tags=('lock_stitch')))
        else:
            # Too short to travel part of the way to the previous stitch; just go
            # back and forth to it a couple times.
            for i in (1, 0, 1, 0):
                lock_stitches.append(stitches[i])
        return lock_stitches


class AbsoluteLock(Lock):
    def stitches(self, stitches, pos):
        if pos == "end":
            stitches = list(reversed(stitches))

        # make sure the path consists of only floats
        path = string_to_floats(self.path, " ")

        # get the length of our lock stitch path
        if pos == 'start':
            lock_pos = []
            lock = 0
            # reverse the list to make sure we end with the first stitch of the target path
            for tie_path in reversed(path):
                lock = lock - tie_path * self.scale_absolute
                lock_pos.insert(0, lock)
        if pos == 'end':
            lock_pos = []
            lock = 0
            for tie_path in path:
                lock = lock + tie_path * self.scale_absolute
                lock_pos.append(lock)
        max_lock_length = max(lock_pos)

        # calculate the amount stitches we need from the target path
        # and generate a line
        upcoming = [stitches[0]]
        for stitch in stitches[1:]:
            to_start = stitch - upcoming[-1]
            upcoming.append(stitch)
            if to_start.length() >= max_lock_length:
                break
        line = LineString(upcoming)

        # add tie stitches
        lock_stitches = []
        for i, tie_path in enumerate(lock_pos):
            if tie_path < 0:
                stitch = Stitch(stitches[0] + tie_path * (stitches[1] - stitches[0]).unit())
            else:
                stitch = substring(line, start_dist=tie_path, end_dist=tie_path)
                stitch = Stitch(stitch.x, stitch.y, tags=('lock_stitch',))
            lock_stitches.append(stitch)
        return lock_stitches


class SVGLock(Lock):
    def stitches(self, stitches, pos):
        if pos == "end":
            stitches = list(reversed(stitches))

        path = Path(self.path)

        # convert from mm to px and scale according to scale_percent setting
        scale = PIXELS_PER_MM * (self.scale_percent / 100)
        path.scale(scale, scale, True)

        end_points = list(path.end_points)

        lock = DirectedLineSegment(end_points[-2], end_points[-1])
        lock_stitch_angle = lock.angle

        stitch = DirectedLineSegment((stitches[0].x, stitches[0].y),
                                     (stitches[1].x, stitches[1].y))
        stitch_angle = stitch.angle

        # rotate and translate the lock stitch
        path.rotate(degrees(stitch_angle - lock_stitch_angle), lock.start, True)
        translate = stitch.start - lock.start
        path.translate(translate.x, translate.y, True)

        # Remove direction indicator from path and also
        # remove start:last/end:first stitch (it is the position of the first/last stitch of the target path)
        path = list(path.end_points)[:-2]

        if pos == 'end':
            path = reversed(path)

        lock_stitches = []
        for i, stitch in enumerate(path):
            stitch = Stitch(stitch[0], stitch[1], tags=('lock_stitch',))
            lock_stitches.append(stitch)
        return lock_stitches


def get_lock_stitch_by_id(pos, lock_type, default="half_stitch"):
    id_list = [lock.id for lock in LOCK_DEFAULTS[pos]]

    try:
        lock = LOCK_DEFAULTS[pos][id_list.index(lock_type)]
    except ValueError:
        lock = LOCK_DEFAULTS[pos][id_list.index(default)]
    return lock


half_stitch = RelativeLock("half_stitch", _("Half Stitch"), "0 0.5 1 0.5 0")
arrow = SVGLock("arrow", _("Arrow"), "M 0.5,0.3 0.3,1.31 -0.11,0.68 H 0.9 L 0.5,1.31 0.4,0.31 V 0.31 1.3")
back_forth = AbsoluteLock("back_forth", _("Back and forth"), "1 1 -1 -1")
bowtie = SVGLock("bowtie", _("Bowtie"), "M 0,0 -0.39,0.97 0.3,0.03 0.14,1.02 0,0 V 0.15")
cross = SVGLock("cross", _("Cross"), "M 0,0 -0.7,-0.7 0.7,0.7 0,0 -0.7,0.7 0.7,-0.7 0,0 -0,-0.7")
star = SVGLock("star", _("Star"), "M 0.67,-0.2 C 0.27,-0.06 -0.22,0.11 -0.67,0.27 L 0.57,0.33 -0.5,-0.27 0,0.67 V 0 -0.5")
simple = SVGLock("simple", _("Simple"), "M -0.03,0 0.09,0.81 0,1.49 V 0 0.48")
triangle = SVGLock("triangle", _("Triangle"), "M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82")
zigzag = SVGLock("zigzag", _("Zig-zag"), "M -0.25,0.2 0.17,0.77 -0.22,1.45 0.21,2.05 -0.03,3 0,0")
custom = CustomLock("custom", _("Custom"))

LOCK_DEFAULTS = {'start': [half_stitch, arrow, back_forth, bowtie, cross, star, simple, triangle, zigzag, custom],
                 'end': [half_stitch, arrow, back_forth, cross, bowtie, star, simple, triangle, zigzag, custom]}
