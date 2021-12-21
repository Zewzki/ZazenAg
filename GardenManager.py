import threading
from time import time, gmtime
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
        self.SprayQueue = []
        
        logging.info('Loading System Configuration')
        self.SystemConfig = SystemConfig(self.ConfigPath)
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
                    print(f'{lastSprayTest} : {type(lastSprayTest)}')
                    
                    lastSprayTimeMs = float(cell.GetField('LastSpray'))
                    sprayDurationMs = float(cell.GetField('SprayDuration'))
                    timeBetweenSpraysMs = float(cell.GetField('TimeBetweenSprays'))
                    sprayPin = int(cell.GetField('SprayPin'))
                    
                    lightOnTime = str(cell.GetField('LightOnTimeOfDay')).split(':')
                    lightOffTime = str(cell.GetField('LightOffTimeOfDay')).split(':')
                    associatedLight = str(cell.GetField('AssociatedLight'))

                    currTimeMs = time()
                    currTimeOfDay = gmtime()

                    if currTimeMs >= lastSprayTimeMs + timeBetweenSpraysMs:
                        if not cell in self.SprayQueue:
                            self.SprayQueue.append(cell)
                            cell.SetField('LastSpray', time())
                            print('turn on pin {0}'.format(sprayPin))
                            logging.debug('Turning on')
                            #turn on pin
                    if currTimeMs > lastSprayTimeMs + sprayDurationMs:
                        #turn off pin
                        print('turn off pin {0}'.format(sprayPin))
                    
                    if self.IsTimeWithinRange(lightOnTime, lightOffTime, (currTimeOfDay[3], currTimeOfDay[4])):
                        #turn on overhead light
                        print('f')

                    garden.UpdateCell(cell)
                self.SystemConfig.UpdateGarden(garden)
            
            if not len(self.SprayQueue) == 0:
                frontOfLine = self.SprayQueue[0]
        
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
        currentTimeDecimal = float(currentTime[3]) + (float(currentTime[4]) / 60.0)

        if endTimeDecimal > startTimeDecimal:
            return currentTimeDecimal > startTimeDecimal and currentTimeDecimal < endTimeDecimal
        else:
            return currentTimeDecimal < startTimeDecimal and currentTimeDecimal > endTimeDecimal
        
        return False

if __name__ == '__main__':
    
    configPath = 'Config/Zazen-Config.config'

    manager = GardenManager(configPath)
    manager.Start()

