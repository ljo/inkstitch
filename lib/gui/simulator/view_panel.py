# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from ...debug.debug import debug
from ...i18n import _
from . import SimulatorPreferenceDialog
from . import DesignInfoDialog


class ViewPanel(ScrolledPanel):
    """"""

    @debug.time
    def __init__(self, parent, detach_callback):
        """"""
        self.parent = parent
        self.detach_callback = detach_callback
        ScrolledPanel.__init__(self, parent)
        self.SetupScrolling(scroll_y=True, scroll_x=False)

        self.button_style = wx.BU_EXACTFIT | wx.BU_NOTEXT

        self.control_panel = parent.cp

        self.btnNpp = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnNpp.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_npp)
        self.btnNpp.SetBitmap(self.control_panel.load_icon('npp'))
        self.btnNpp.SetToolTip(_('Display needle penetration point (O)'))
        self.btnJump = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnJump.SetToolTip(_('Show jump stitches'))
        self.btnJump.SetBitmap(self.control_panel.load_icon('jump'))
        self.btnJump.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('jump', event))
        self.btnTrim = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnTrim.SetToolTip(_('Show trims'))
        self.btnTrim.SetBitmap(self.control_panel.load_icon('trim'))
        self.btnTrim.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('trim', event))
        self.btnStop = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnStop.SetToolTip(_('Show stops'))
        self.btnStop.SetBitmap(self.control_panel.load_icon('stop'))
        self.btnStop.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('stop', event))
        self.btnColorChange = wx.BitmapToggleButton(self, -1, style=self.button_style)
        self.btnColorChange.SetToolTip(_('Show color changes'))
        self.btnColorChange.SetBitmap(self.control_panel.load_icon('color_change'))
        self.btnColorChange.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.on_marker_button('color_change', event))

        self.btnInfo = wx.BitmapButton(self, -1, style=self.button_style)
        self.btnInfo.SetToolTip(_('Open info dialog'))
        self.btnInfo.SetBitmap(self.control_panel.load_icon('info'))
        self.btnInfo.Bind(wx.EVT_BUTTON, self.on_info_button)

        self.btnBackgroundColor = wx.ColourPickerCtrl(self, -1, colour='white', size=((40, -1)))
        self.btnBackgroundColor.SetToolTip(_("Change background color"))
        self.btnBackgroundColor.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_update_background_color)

        self.btnSettings = wx.BitmapButton(self, -1, style=self.button_style)
        self.btnSettings.SetToolTip(_('Open settings dialog'))
        self.btnSettings.SetBitmap(self.control_panel.load_icon('settings'))
        self.btnSettings.Bind(wx.EVT_BUTTON, self.on_settings_button)

        if self.detach_callback:
            self.btnDetachSimulator = wx.BitmapButton(self, -1, style=self.button_style)
            self.btnDetachSimulator.SetToolTip(_('Detach/attach simulator window'))
            self.btnDetachSimulator.SetBitmap(self.control_panel.load_icon('detach_window'))
            self.btnDetachSimulator.Bind(wx.EVT_BUTTON, lambda event: self.control_panel.detach_callback())

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        show_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Show")), wx.VERTICAL)
        show_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        show_inner_sizer.Add(self.btnNpp, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnJump, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnTrim, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnStop, 0, wx.ALL, 2)
        show_inner_sizer.Add(self.btnColorChange, 0, wx.ALL, 2)
        show_sizer.Add(0, 2, 0)
        show_sizer.Add(show_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        show_sizer.Add(0, 2, 0)
        outer_sizer.Add(show_sizer, 0, wx.EXPAND)
        outer_sizer.Add(0, 10, 0)

        info_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Info")), wx.VERTICAL)
        info_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        info_inner_sizer.Add(self.btnInfo, 0, wx.EXPAND | wx.ALL, 2)
        info_sizer.Add(0, 2, 0)
        info_sizer.Add(info_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        info_sizer.Add(0, 2, 0)
        outer_sizer.Add(info_sizer, 0, wx.EXPAND)
        outer_sizer.Add(0, 10, 0)

        settings_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Settings")), wx.VERTICAL)
        settings_inner_sizer = wx.BoxSizer(wx.VERTICAL)
        settings_inner_sizer.Add(self.btnBackgroundColor, 0, wx.EXPAND | wx.ALL, 2)
        settings_inner_sizer.Add(self.btnSettings, 0, wx.EXPAND | wx.ALL, 2)
        if self.detach_callback:
            settings_inner_sizer.Add(self.btnDetachSimulator, 0, wx.ALL, 2)
        settings_sizer.Add(0, 2, 0)
        settings_sizer.Add(settings_inner_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        settings_sizer.Add(0, 2, 0)
        outer_sizer.Add(settings_sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(outer_sizer)

    def set_drawing_panel(self, drawing_panel):
        self.drawing_panel = drawing_panel

    def on_update_background_color(self, event):
        self.set_background_color(event.Colour)

    def set_background_color(self, color):
        self.btnBackgroundColor.SetColour(color)
        self.drawing_panel.SetBackgroundColour(color)
        self.drawing_panel.Refresh()

    def on_toggle_npp_shortcut(self, event):
        self.btnNpp.SetValue(not self.btnNpp.GetValue())
        self.toggle_npp(event)

    def toggle_npp(self, event):
        self.drawing_panel.Refresh()

    def on_marker_button(self, marker_type, event):
        self.control_panel.slider.enable_marker_list(marker_type, event.GetEventObject().GetValue())
        if marker_type == 'jump':
            self.drawing_panel.Refresh()

    def on_settings_button(self, event):
        settings_panel = SimulatorPreferenceDialog(self, title=_('Simulator Preferences'))
        settings_panel.Show()

    def on_info_button(self, event):
        self.info_panel = DesignInfoDialog(self, title=_('Design Info'))
        self.info_panel.Show()
