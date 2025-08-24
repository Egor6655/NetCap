#gui core module
import dearpygui.dearpygui as gui
import BackendCore
import LoggingManager
import GeoNetCore
import SpeedUtil
import repeater
import time
import subprocess
import os
import logging as log
from threading import Timer

class Frontend:
    def __init__(self,title):
        self.Speed = SpeedUtil.Speed
        self.title = title
        self.speed = False
        self.series = None

        self.downX = []
        self.downY = []

        self.upX = []
        self.upY = []

        self.logging = repeater.RepeatTimer(5, LoggingManager.startLoggingLoop)


    def updateTable(self):
        """realtime updater of table (now 0.5 secs)"""
        data = BackendCore.get_network_connections()

        for i in range(0, 255):
            for j in range(0, 10):
                try:
                    gui.configure_item(str(i) + " " + str(j), default_value=data[i][j])
                except Exception:
                    LoggingManager.logWarning(Exception.args)
                    pass





    def guiMainLoop(self):

        gui.create_context()


        with gui.viewport_menu_bar():
            with gui.menu(label="Settings"):
                gui.add_checkbox(label="Show speed", callback=self.setSpeedSettings)
                gui.add_checkbox(label="Draw download speed plot", callback=self.setSpeedSettings)
                gui.add_checkbox(label="Draw upload speed plot", callback=self.setSpeedSettings)
                #TODO: style options
                gui.add_menu_item(label="Style options(TODO)", callback=self.recordingSettings)



            with gui.menu(label="Recording"):
                gui.add_menu_item(label="start logging", callback=self.recordingSettings)
                gui.add_menu_item(label="stop logging", callback=self.recordingSettings)
                gui.add_menu_item(label="open logs folder", callback=self.openLog)
                gui.add_menu_item(label="delete system logs", callback=self.systemLogDeleter)
                gui.add_menu_item(label="delete capture logs", callback=self.logDeleter)

            with gui.menu(label="Map Ip Data"):
                gui.add_text("you need wait until 30-40 seconds")
                gui.add_menu_item(label="open map", callback=self.openMap)


            gui.create_viewport(title=self.title, width=1280, height=720)
        with gui.window(tag="mainWin", pos=(0, 0), no_close=True, horizontal_scrollbar=True,min_size=(800,700)):

            with gui.table(header_row=True, resizable=True, tag="mainTable",borders_outerH=True):
                gui.add_table_column(label="fd")
                gui.add_table_column(label="family")
                gui.add_table_column(label="type")
                gui.add_table_column(label="local")
                gui.add_table_column(label="remote")
                gui.add_table_column(label="status")
                gui.add_table_column(label="pid")
                gui.add_table_column(label="process")
                gui.add_table_column(label="status")
                gui.add_table_column(label="directory")
                for i in range(0, 255):
                    with gui.table_row():
                        for j in range(0, 10):
                            gui.add_text(" ",tag=str(i)+" "+str(j))
        with gui.window(tag="speedWin",pos=(800,0),no_close=True,min_size=(400,600),):
            gui.add_text("",tag="speedText")


        timer = repeater.RepeatTimer(0.5,self.updateTable)
        timer.start()

        speedTimer = repeater.RepeatTimer(1, self.SpeedLoop)
        speedTimer.start()

        Timer(1, self.DownloadPlotBackend).start()

        gui.setup_dearpygui()
        gui.show_viewport()
        gui.start_dearpygui()
        gui.destroy_context()

    def recordingSettings(self,sender):
        print(f"Menu Item: {sender}")
        if sender==29:
            self.logging.start()
        if sender==30:
            self.logging.stop()
    def setSpeedSettings(self,sender,appdata):
        print(sender)
        if appdata :
            if sender==24:
                gui.configure_item("speedText", default_value="speed")
                self.speed=True
            if sender == 25:
                with gui.plot(label="download",height=200, width=400,parent="speedWin", tag="plot download"):
                    gui.add_plot_legend()
                    gui.add_plot_axis(gui.mvXAxis, label="time (seconds) ")
                    gui.add_plot_axis(gui.mvYAxis, label="speed (kb/s)", tag="y_axis")
                    gui.add_line_series(self.downX, self.downY, parent="y_axis",tag="download")
            if sender == 26:
                with gui.plot(label="upload",height=200, width=400,parent="speedWin", tag="plot upload"):
                    gui.add_plot_legend()
                    gui.add_plot_axis(gui.mvXAxis, label="time (seconds) ")
                    gui.add_plot_axis(gui.mvYAxis, label="speed (kb/s)", tag="y_axis_up")
                    gui.add_line_series(self.upX, self.upY, parent="y_axis_up",tag="upload")

        else:
            if sender == 24:
                gui.configure_item("speedText", default_value="")
                self.speed = False
            if sender == 25:
                gui.delete_item("plot download")
            if sender == 26:
                gui.delete_item("plot upload")


    def SpeedLoop(self):
        if self.speed:
            download_speed, upload_speed = BackendCore.get_network_traffic()
            gui.configure_item("speedText", default_value="download: "+str(download_speed)+"kb/s upload: "+ str(upload_speed)+"kb/s")

    def DownloadPlotBackend(self):
        i=0
        while True:
            download_speed, upload_speed = BackendCore.get_network_traffic()
            time.sleep(1)
            self.downX.append(i)
            self.downY.append(float(download_speed))

            self.upX.append(i)
            self.upY.append(float(upload_speed))
            i+=1
            try:
                gui.set_value("download", [self.downX, self.downY])
                gui.set_value("upload", [self.upX, self.upY])
            except Exception:
                LoggingManager.logWarning(Exception.args)
                pass
    def openMap(self):
        Timer(1, GeoNetCore.setLocationDataToHtml()).start()

    def openLog(self):
        print(os.getcwd())
        subprocess.Popen("explorer /select,"+os.getcwd())
    def logDeleter(self):
        log.shutdown()
        os.remove(os.getcwd()+"\\NetCap_Capture_Log.log")
    def systemLogDeleter(self):
        log.shutdown()
        os.remove(os.getcwd()+"\\NetCap_Log.log")
