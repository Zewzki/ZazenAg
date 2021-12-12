import threading
from time import time
import pigpio

from Config.SystemConfig import SystemConfig
from Config.Garden import Garden
from Config.Basin import Basin
from Config.Cell import Cell

class GardenManager():

    def __init__(self, configPath):

        self.ConfigPath = configPath

        self.SystemConfig = SystemConfig(self.ConfigPath)
        self.Running = False
    
    def Start(self):

        print('Starting...')

        self.RunThread = threading.Thread(target = self.Run)
        self.MonitorThread = threading.Thread(target = self.Monitor)

        self.Running = True

        self.RunThread.start()
        self.MonitorThread.start()
    
    def Run(self):

        print('Running...')

        while self.Running:
            
            for gardenName in self.SystemConfig.GardenList.keys():
                garden = self.SystemConfig.GardenList[gardenName]

                for cellName in garden.GetCellList().keys():
                    cell = garden.GetCellList()[cellName]
                    
                    lastSprayTime = float(cell.GetField('LastSpray'))
                    onTime = float(cell.GetField('OnTime'))
                    offTime = float(cell.GetField('OffTime'))

                    sprayPin = int(cell.GetField('SprayPin'))

                    if time() >= lastSprayTime + offTime:
                        cell.SetField('LastSpray', time())
                        print('turn on pin {0}'.format(sprayPin))
                        #turn on pin
                    if time() > lastSprayTime + onTime:
                        #turn off pin
                        print('turn off pin {0}'.format(sprayPin))
                    
                    garden.UpdateCell(cell)
                self.SystemConfig.UpdateGarden(garden)

        self.SystemConfig.Serialize(self.ConfigPath)

    def Monitor(self):

        print('Monitoring...')

        while self.Running:
            cmd = input()
            if cmd == 'quit' or cmd == 'exit':
                self.Running = False
                print('Exiting...')

if __name__ == '__main__':
    
    configPath = 'Config/Zazen-Config.config'

    manager = GardenManager(configPath)
    manager.Start()

