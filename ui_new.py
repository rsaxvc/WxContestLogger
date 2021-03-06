#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from db_manager import db_manager
from settings_manager import settings_manager
from dbframe import framer

class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, 
			size=(790, 300))
		self.db = db_manager()

		settings = settings_manager()
		self.uuid = settings.get( "uuid" )

		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		settings = settings_manager()

		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(9)

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		if(True):
			st1 = wx.StaticText(panel, label='TheirCall')
			st1.SetFont(font)
			hbox.Add(st1, flag=wx.TOP, border=8)

			self.tcTheirCall = wx.TextCtrl(panel)
			hbox.Add(self.tcTheirCall, flag=wx.EXPAND, proportion=1)

			st1 = wx.StaticText(panel, label='Class')
			st1.SetFont(font)
			hbox.Add(st1, flag=wx.LEFT|wx.TOP, border=6)

			self.tcTheirClass = wx.TextCtrl(panel)
			hbox.Add(self.tcTheirClass, flag=wx.EXPAND, proportion=1)

			st1 = wx.StaticText(panel, label='Section')
			st1.SetFont(font)
			hbox.Add(st1, flag=wx.LEFT|wx.TOP, border=6)

			self.tcTheirSection = wx.TextCtrl(panel)
			hbox.Add(self.tcTheirSection, flag=wx.EXPAND, proportion=1)

		vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.bands = [ 'Satellite', '1.25m', '2m', '6m', '10m', '20m', '40m', '80m', '160m' ]
		self.bandswitches = []
		last_band = settings.get( "logger.band" )
		style = wx.RB_GROUP
		for band in self.bands:
			rb = wx.RadioButton(panel, label=band, style=style )
			rb.SetFont(font)
			if( band == last_band ):
				rb.SetValue( True )
			hbox.Add(rb, flag=wx.RIGHT, border=8, proportion=1)
			self.bandswitches.append( rb )
			style = 0
		vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.modes = [ 'cw', 'digital', 'phone' ]
		self.modeswitches = []
		last_mode = settings.get( "logger.mode" )
		style = wx.RB_GROUP
		for mode in self.modes:
			rb = wx.RadioButton(panel, label=mode, style=style)
			rb.SetFont(font)
			if( mode == last_mode ):
				rb.SetValue( True )
			hbox.Add(rb, flag=wx.RIGHT, border=8)
			self.modeswitches.append( rb )
			style = 0
		vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		vbox.Add((-1, 10))

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		st1 = wx.StaticText(panel, label='MyCall')
		st1.SetFont(font)
		hbox.Add(st1, flag=wx.LEFT|wx.TOP, border=6)

		self.tcMyCall = wx.TextCtrl(panel)
		self.tcMyCall.SetValue( settings.get( "logger.mycall" ) )
		hbox.Add(self.tcMyCall, flag=wx.BOTTOM, border=5)

		btnClear = wx.Button(panel, label='Clear', size=(70, 30))
		btnClear.Bind(wx.EVT_BUTTON, self.OnClearButtonClicked)
		hbox.Add(btnClear, flag=wx.BOTTOM, border=5)

		btnCreate = wx.Button(panel, label='Create Log', size=(200, 30))
		btnCreate.Bind(wx.EVT_BUTTON, self.OnLogButtonClicked)
		hbox.Add(btnCreate, flag=wx.BOTTOM, border=5)

		btnClose = wx.Button(panel, label='Close', size=(70, 30))
		btnClose.Bind(wx.EVT_BUTTON, self.OnCloseButtonClicked)
		hbox.Add(btnClose, flag=wx.BOTTOM, border=5)

		vbox.Add(hbox, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

		panel.SetSizer(vbox)

	def OnCloseButtonClicked(self,evnt):
		settings = settings_manager()

		for i in range( 0, len( self.bands ) ):
			if( self.bandswitches[i].GetValue() ):
				settings.put( "logger.band", self.bands[i] )

		for i in range( 0, len( self.modes ) ):
			if( self.modeswitches[i].GetValue() ):
				settings.put( "logger.mode", self.modes[i] )

		settings.put( "logger.mycall", self.tcMyCall.GetValue() )
		settings.save()
		self.Destroy()

	def OnClearButtonClicked(self,evnt):
		self.tcTheirCall.ChangeValue( "" )
		self.tcTheirClass.ChangeValue( "" )
		self.tcTheirSection.ChangeValue( "" )

	def OnLogButtonClicked(self,evnt):
		if( self.tcTheirCall.GetValue() == "" ):
			return
		band=""
		for i in range( 0, len( self.bands ) ):
			if( self.bandswitches[i].GetValue() ):
				band = self.bands[i]

		mode=""
		for i in range( 0, len( self.modes ) ):
			if( self.modeswitches[i].GetValue() ):
				mode = self.modes[i]

		from localtimeutil import local8601
		self.db.insert_local_contact( self.uuid, local8601(), self.tcMyCall.GetValue(), self.tcTheirCall.GetValue(), band, mode, self.tcTheirClass.GetValue(), self.tcTheirSection.GetValue() )
		self.OnClearButtonClicked(self)

if __name__ == '__main__':
	app = wx.App()
	Example(None, title='WxContextLogger - New Contact')
	app.MainLoop()
