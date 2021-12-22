import threading
from time import time, gmtime, sleep
import pigpio
import logging

from Config.SystemConfig import SystemConfig
from Config.Garden import Garden
from Config.Basin import Basin
from Config.Cell import Cell

class GardenManager():

    def __init__(self, configPath):

        logging.basicConfig(filename = 'Log/gardenManagerLog.log',
                            filemode = 'w',
                            format = '%(asctime)s %(message)s',
                            datefmt = '%m/%d/%Y %I:%M:%S',
                            level = logging.DEBUG,
                            encoding = 'utf-8',)
        
        logging.info('Initializing System')

        self.ConfigPath = configPath
        
        logging.info('Loading System Configuration')
        self.SystemConfig = SystemConfig(self.ConfigPath)

        self.LoadCellToLightConfiguration()

        self.Running = False
    
    def Start(self):

        print('Starting...')
        logging.info('Starting...')

        self.RunThread = threading.Thread(target = self.Run)
        self.MonitorThread = threading.Thread(target = self.Monitor)

        self.Running = True

        self.RunThread.start()
        self.MonitorThread.start()
    
    def Run(self):

        print('Running...')
        logging.info('Running GardenManager...')

        while self.Running:
            
            for gardenName, garden in self.SystemConfig.GardenList.items():

                for cellName, cell in garden.GetCellList().items():

                    lastSprayTest = cell.GetField('LastSpray')
                    
                    lastSprayTimeMs = float(cell.GetField('LastSpray'))
                    sprayDurationMs = float(cell.GetField('SprayDuration'))
                    timeBetweenSpraysMs = float(cell.GetField('TimeBetweenSprays'))
                    sprayPin = int(cell.GetField('SprayPin'))

                    lightOnTime = str(cell.GetField('LightOnTimeOfDay')).split(':')
                    lightOffTime = str(cell.GetField('LightOffTimeOfDay')).split(':')
                    associatedLightName = str(cell.GetField('AssociatedLight'))
                    associatedLightPin = self.GetLightPinFromName(garden, associatedLightName)

                    currTimeMs = time()
                    currTimeOfDay = gmtime()

                    if currTimeMs >= lastSprayTimeMs + timeBetweenSpraysMs and not self.SprayManagement[sprayPin]:
                        self.SprayManagement[sprayPin] = 1
                        cell.SetField('LastSpray', time())
                        logging.debug('Turning On Spray Pin {0}'.format(sprayPin))
                        # turn on pin

                    if currTimeMs > lastSprayTimeMs + sprayDurationMs and self.SprayManagement[sprayPin]:
                        self.SprayManagement[sprayPin] = 0
                        logging.debug('Turning Off Spray Pin {0}'.format(sprayPin))
                        # turn off pin

                    if self.IsTimeWithinRange(lightOnTime, lightOffTime, (currTimeOfDay[3], currTimeOfDay[4])):
                        if self.LightManagement[associatedLightPin]:
                            self.LightManagement[associatedLightPin] = 1
                            logging.info('Turning On Light Pin {0}'.format(associatedLightPin))
                        else:
                            self.LightManagement[associatedLightPin] = 0
                            logging.info('Turning Off Light Pin {0}'.format(associatedLightPin))

                    garden.UpdateCell(cell)
                self.SystemConfig.UpdateGarden(garden)

            sleep(self.SystemConfig.SystemDelayMs)
        
        logging.debug('Performing config serialization...')
        self.SystemConfig.Serialize(self.ConfigPath)
        logging.debug('GardenManager stopped')

    def Monitor(self):

        print('Monitoring...')
        logging.info('Running Command Monitor...')

        while self.Running:
            cmd = input()
            if cmd == 'quit' or cmd == 'exit':
                print('Exiting...')
                logging.debug('"{0}" received, halting threads...'.format(cmd))
                self.Running = False
            elif cmd == 'printInfo':
                print('Info:')
                print(self.SystemConfig)
            elif cmd == 'help':
                print('-Help Menu-')
                print('quit || exit\t-\tExit program')
                print('printInfo\t\t-\tPrint current system configuration')
        
        logging.info('Monitor stopped')
    
    def IsTimeWithinRange(self, startTime, endTime, currentTime):

        startTimeDecimal = float(startTime[0]) + (float(startTime[1]) / 60.0)
        endTimeDecimal = float(endTime[0]) + (float(endTime[1]) / 60.0)
        currentTimeDecimal = float(currentTime[0]) + (float(currentTime[1]) / 60.0)

        if endTimeDecimal > startTimeDecimal:
            return currentTimeDecimal > startTimeDecimal and currentTimeDecimal < endTimeDecimal
        else:
            return currentTimeDecimal < startTimeDecimal and currentTimeDecimal > endTimeDecimal
    
    def LoadCellToLightConfiguration(self):

        self.SprayManagement = {}
        self.LightManagement = {}

        for gardenName, garden in self.SystemConfig.GardenList.items():

            lightList = garden.GetLightList()

            for cellName, cell in garden.GetCellList().items():

                sprayPin = int(cell.GetField('SprayPin'))
                associatedLightName = str(cell.GetField('AssociatedLight'))
                associatedLightPin = int(lightList[associatedLightName].GetField('ControlPin'))
            
                self.SprayManagement[sprayPin] = 0
                self.LightManagement[associatedLightPin] = 0
    
    def GetLightPinFromName(self, garden, lightName):

        lightList = garden.GetLightList()

        for listName, listLight in lightList.items():
            if listName == lightName:
                return listLight.GetField('ControlPin')
        return -1

if __name__ == '__main__':
    
    configPath = 'Config/Zazen-Config.config'

    manager = GardenManager(configPath)
    manager.Start()

