# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Jan 26 13:25:28 2011

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class Reports_list(wx.MDIChildFrame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: reports_list.__init__
        kwds["style"] = wx.MAXIMIZE|wx.SIMPLE_BORDER
        wx.MDIChildFrame.__init__(self, *args, **kwds)
        self.label_report = wx.StaticText(self, -1, "Reporte :")
        self.list_box_report = wx.ListBox(self, -1, choices=[], style=wx.LB_SORT)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: reports_list.__set_properties
        self.SetTitle("frame_3")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: reports_list.__do_layout
        sizer_report_list = wx.BoxSizer(wx.VERTICAL)
        sizer_report_list.Add(self.label_report, 0, wx.ALL|wx.EXPAND, 0)
        sizer_report_list.Add(self.list_box_report, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(sizer_report_list)
        sizer_report_list.Fit(self)
        self.Layout()
        # end wxGlade

# end of class reports_list


