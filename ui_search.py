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
		hbox1.Add(st1, flag=wx.RIGHT, border=8)
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
		self.lc = wx.ListCtrl(panel, style=wx.BORDER_SUNKEN)
		self.lc.InsertColumn(0,"Callsign")
		hbox3.Add(self.lc, proportion=1, flag=wx.EXPAND)
		vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

		vbox.Add((-1, 25))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		btn1 = wx.Button(panel, label='Ok', size=(70, 30))
		hbox5.Add(btn1)
		btn2 = wx.Button(panel, label='Close', size=(70, 30))
		btn2.Bind(wx.EVT_BUTTON, self.OnCloseButtonClicked)

		hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
		vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

		panel.SetSizer(vbox)

		TIMER_ID = 10000
		self.timer = wx.Timer(panel, TIMER_ID)
		self.timer.Start(10000)
		wx.EVT_TIMER(panel, TIMER_ID, self.OnTimer)  # call the on_timer function

		self.DisplayView()

	def DisplayView(self):
		self.lc.DeleteAllItems()
		j = 0
		for i in self.db.search( self.filter ):
			self.lc.InsertStringItem( j, i.theircall )
			j = j + 1

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
