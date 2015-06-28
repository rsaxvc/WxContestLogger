#!/usr/bin/python
# -*- coding: utf-8 -*-

#snagged from the WxPython Tutorial

import wx
from db_manager import db_manager

class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(790, 350))
		self.db = db_manager()
		self.filter = self.db.filter()
		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		st1 = wx.StaticText(panel, label='Contact Callsign')
		st1.SetFont(font)
		hbox1.Add(st1, flag=wx.TOP, border=6)
		self.tc = wx.TextCtrl(panel)
		self.tc.Bind(wx.EVT_TEXT, self.OnSearchBoxUpdate)
		hbox1.Add(self.tc, proportion=1)
		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		st2 = wx.StaticText(panel, label='Matching Callsigns')
		st2.SetFont(font)
		hbox2.Add(st2)
		vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.lc = wx.ListCtrl(panel, style=wx.BORDER_SUNKEN | wx.LC_REPORT)
		self.lc.InsertColumn(0,"MyCall")
		self.lc.InsertColumn(1,"TheirCall")
		self.lc.InsertColumn(2,"Class")
		self.lc.InsertColumn(3,"Section")
		self.lc.InsertColumn(4,"DateTime")
		self.lc.InsertColumn(5,"Band")
		self.lc.InsertColumn(6,"Mode")
		hbox3.Add(self.lc, proportion=1, flag=wx.EXPAND)
		vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

		vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		self.bands = [ 'Satellite', '1.25m', '2m', '6m', '10m', '20m', '40m', '80m', '160m' ]
		self.bandswitches = []
		for band in self.bands:
			cb = wx.CheckBox(panel, label=band )
			cb.SetFont(font)
			cb.SetValue( True )
			hbox5.Add(cb, flag=wx.RIGHT, border=8, proportion=1)
			self.bandswitches.append( cb )
		vbox.Add(hbox5, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		self.modes = [ 'cw', 'digital', 'phone' ]
		self.modeswitches = []
		for mode in self.modes:
			cb = wx.CheckBox(panel, label=mode)
			cb.SetFont(font)
			cb.SetValue( True )
			hbox6.Add(cb, flag=wx.RIGHT, border=8)
			self.modeswitches.append( cb )
		close_btn = wx.Button(panel, label='Close', size=(70, 30))
		close_btn.Bind(wx.EVT_BUTTON, self.OnCloseButtonClicked)
		hbox6.Add(close_btn, flag=wx.LEFT|wx.BOTTOM, border=5)

#		vbox.Add(hbox15, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
#		vbox.Add((-1, 10))
		vbox.Add(hbox6, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

		panel.SetSizer(vbox)

		TIMER_ID = 1000
		self.timer = wx.Timer(panel, TIMER_ID)
		self.timer.Start(1000)
		wx.EVT_TIMER(panel, TIMER_ID, self.OnTimer)  # call the on_timer function

		self.DisplayView()

	def DisplayView(self):
		self.lc.DeleteAllItems()
		for i in self.db.search( self.filter ):
			self.lc.Append([i.mycall, i.theircall, i.class_, i.section, i.datetime, i.band, i.mode])

	def OnSearchBoxUpdate(self,evnt):
		self.filter.contains = self.tc.GetValue()
		self.DisplayView()

	def OnCloseButtonClicked(self,evnt):
		self.timer.Stop()
		self.Destroy()

	def OnTimer(self,event):
		self.DisplayView()
		pass

if __name__ == '__main__':
	app = wx.App()
	Example(None, title='WxContextLogger - Search Contacts')
	app.MainLoop()

