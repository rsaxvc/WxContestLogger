#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer

class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(790, 200))
		self.db = db_manager()

		s = settings_manager()
		self.uuid = s.get( "uuid" )

		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		st1 = wx.StaticText(panel, label='MyCall')
		st1.SetFont(font)
		hbox1.Add(st1, flag=wx.RIGHT, border=8)
		self.tc1 = wx.TextCtrl(panel)
		self.tc1.Bind(wx.EVT_TEXT, self.OnSearchBoxUpdate)
		hbox1.Add(self.tc1, proportion=1)
		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		st1 = wx.StaticText(panel, label='TheirCall')
		st1.SetFont(font)
		hbox2.Add(st1, flag=wx.RIGHT, border=8)
		self.tc2 = wx.TextCtrl(panel)
		self.tc2.Bind(wx.EVT_TEXT, self.OnSearchBoxUpdate)
		hbox2.Add(self.tc2, proportion=1)
		vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		self.bands = [ 'Satellite', '1.25m', '2m', '6m', '10m', '20m', '40m', '80m', '160m' ]
		self.bandswitches = []
		style = wx.RB_GROUP
		for band in self.bands:
			rb = wx.RadioButton(panel, label=band, style=style )
			rb.SetFont(font)
			hbox3.Add(rb, flag=wx.RIGHT, border=8)
			self.bandswitches.append( rb )
			style = wx.RB_SINGLE
		vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		self.modes = [ 'cw', 'digital', 'phone' ]
		self.modeswitches = []
		style = wx.RB_GROUP
		for mode in self.modes:
			rb = wx.RadioButton(panel, label=mode, style=style)
			rb.SetFont(font)
			hbox4.Add(rb, flag=wx.RIGHT, border=8)
			self.modeswitches.append( rb )
			style = wx.RB_SINGLE
		vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)


		vbox.Add((-1, 10))

		hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		btn1 = wx.Button(panel, label='Create Log', size=(200, 30))
		btn1.Bind(wx.EVT_BUTTON, self.OnLogButtonClicked)
		hbox5.Add(btn1)

		btn2 = wx.Button(panel, label='Close', size=(70, 30))
		btn2.Bind(wx.EVT_BUTTON, self.OnCloseButtonClicked)
		hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)

		vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

		panel.SetSizer(vbox)

		self.DisplayView()

	def DisplayView(self):
		pass

	def OnSearchBoxUpdate(self,evnt):
		self.DisplayView()

	def OnCloseButtonClicked(self,evnt):
		self.Destroy()

	def OnLogButtonClicked(self,evnt):
		for i in range( 0, len( self.bands ) ):
			if( self.bandswitches[i].GetValue() ):
				print self.bands[i]
		self.db.insert_local_contact( self.uuid, "somedate.sometime", self.tc1.GetValue(), self.tc2.GetValue() )
		self.tc2.ChangeValue( "" )
		pass

if __name__ == '__main__':
	app = wx.App()
	Example(None, title='WxContextLogger - New Contact')
	app.MainLoop()
