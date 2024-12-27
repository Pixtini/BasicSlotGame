#This is the old project
from Reports import *
from SlotLogic import *
from SlotData import *

config = "/Users/connorkelly/Documents/Work/BasicSlotGame/BasicSlot.xlsx"

class BaseGame(Spin): 
    def __init__(self, reelType):
        super().__init__(reelType)
    
    def baseSpin(self):
        super().spin() #Spin function from parent class
        self.totalPay = self.slotGame.totalPayout
        self.freeSpinFlag = self.slotGame.freeGameCheck #To check if trigger FG


class FreeGame(Spin):
    def __init__(self, reelType):
        super().__init__(reelType)

    def freeSpin(self):
        self.totalFreePay = 0 
        for _ in range(int(self.slotData.freeSpinCount)):
            super().spin()
            self.totalFreePay += self.slotGame.totalPayout

class Main:
    def __init__(self, spinCount, config):
        self.slotData = SlotData(config)
        self.slotData.importData()
        self.report = Report(spinCount) #Inits the report to log later
        self.baseSpin = BaseGame(self.slotData.baseReels)
        self.freeSpin = FreeGame(self.slotData.freeReels)

    def spin(self): 
        self.baseSpin.baseSpin()
        if self.baseSpin.freeSpinFlag == 3:
            self.freeSpin.freeSpin()
            self.report.log(self.baseSpin.totalPay, self.freeSpin.totalFreePay, self.baseSpin.freeSpinFlag) #Logs data, to be printed into the report
        else:
            self.report.log(self.baseSpin.totalPay, 0, self.baseSpin.freeSpinFlag)  # Zero for no free game pay  

    def sim(self):
        for i in range(self.report.spinCount):  
            self.spin()
            if i % (self.report.spinCount/10) == 0:
                print(f"{i / (self.report.spinCount/10) }")
        self.report.reportPrint()
    
main = Main(1000000, config)
main.sim()

