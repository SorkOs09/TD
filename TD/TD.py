
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5, copy, sys, random
import ctypes


print("TOWER DEFENCE GAME")
print("__________________")
print("TOWER DEFENCE GAME")
print("__________________")


#
# new_grid - одномерный список объектов в grid
#

############################################
# Загрузка DLL

# компилируется через gcc
# g++ -c helper.cpp
# g++ -shared -o helper.dll helper.o

helper_class = ctypes.cdll.LoadLibrary('./helper_class.dll')

helper       = ctypes.cdll.LoadLibrary('./helper.dll')

# Загрузка DLL

############################################
file = open('map.txt', encoding='utf-8')
len_file_0 = len(file.readlines()[0])

evils = []


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
class Tower():
    def __init__(self, position):
        self.hp     = random.randint(5, 10)
        self.x      = position[1]
        self.y      = position[0]
        self.IsActivated = False
        file = open('map.txt', encoding='utf-8')
        f = file.readlines()[0]
        file.close()
        f = len(f.replace(' ', ''))-1
        #print(f)
        self.pos    = self.y*f+self.x
        self.button = PicButton(QPixmap("BB.png"))
    def Click(self):
        #print(self.x)
        #print(self.y)
        #print(self.pos)
        self.Activated()
    def UpdatePos(self, values, x = None, y = None):
        self.last_pos = self.pos
        if x:
            self.x    = x
        if y:
            self.y    = y
        self.pos = self.y*values+self.x
    def Activated(self):
        if ex.money - 10 > -1:
            self.button.pixmap = QPixmap('tower_0.png')
            ex.money          -= 10
            ex.label.setText("Money: " + str(ex.money) + " Score: " + str(ex.score) + " HP: " + str(ex.hp)) 
            self.IsActivated   = True

class Evil():
    def __init__(self, x, y, values):
        self.hp  = 10
        self.x   = x
        self.y   = y
        self.pos = y*len(values[0])+x 
        self.values = len(values[0])
        i           = random.randint(1, 3)
        self.image  = ['monsters/'+ str(i) + '/0.png', 'monsters/'+ str(i) + '/1.png', 'monsters/'+ str(i) + '/2.png']
        self.last_pos = self.pos
        self.path     = []
        self.step     = 0
        self.GetWay(1000)
        evils.append(self)
    def UpdatePos(self, x = None, y = None):
        self.last_pos = self.pos
        if x:
            self.x   = x
        if y:
            self.y   = y
        self.pos = self.y*self.values+self.x
    def GetWay(self, x):
        values_now = []
        i = -1
        f = open('map.txt', encoding='utf-8')
        for line in f.readlines():
            values_now.append([])
            i += 1
            for c in line:
                if   c == 's':
                    values_now[i].append(-1)
                    
                elif c == '0':
                    values_now[i].append(0)
                    
        f.close()
        values_now[self.y][self.x] = 1
        map  = copy.copy(values_now)
        path = []
        for d in range(1, x):
     
            for en in range(0, len(map)):
       
                for et in range(0, len(map[en])):
     
                    if map[en][et] == d:
                        if en-1>= 0:
                            if map[en-1][et] == 0:
                                map[en-1][et] = map[en][et]+1
                                path.append([en-1, et])

                            if et + 1 <= len(map[en])-1:
                                if map[en][et+1] == 0:
                                    map[en][et+1] = map[en][et]+1
                                    path.append([en, et+1])
                           
                            if en+1 <= len(map)-1:
                                if map[en+1][et] == 0:
                                    map[en+1][et] = map[en][et]+1
                                    path.append([en+1, et])

                            if et - 1 >= 0:
                                if map[en][et-1] == 0:
                                    map[en][et-1] = map[en][et]+1
                                    path.append([en, et-1])
        self.path = path
        
class TD(QWidget):
    def SetMap(self):
        

        self.positions = [(i,j) for i in range(len(self.values)) for j in range(22)]
        


        for evil in evils:
            btn    = self.new_grid[evil.pos]
            if evil.pos != 0 and type(self.new_grid[evil.pos-1]) == Tower and self.new_grid[evil.pos-1].IsActivated:
                evil.hp -= random.randint(1, 3)
                helper.Log(ctypes.c_wchar_p(str(evil) + " " + str(evil.hp)))
                self.new_grid[evil.pos-1].hp -= 1
                #print(self.new_grid[evil.pos-1].hp)
                
                if  self.new_grid[evil.pos-1].hp <= 0:
                    self.new_grid[evil.pos-1].IsActivated     = False
                    self.new_grid[evil.pos-1].button.pixmap = QPixmap('BB.png')
                elif self.new_grid[evil.pos-1].hp < 3:
                    self.new_grid[evil.pos-1].button.pixmap = QPixmap('tower_3.png')
                elif self.new_grid[evil.pos-1].hp < 7:
                    self.new_grid[evil.pos-1].button.pixmap = QPixmap('tower_2.png')
                elif  self.new_grid[evil.pos-1].hp < 10:
                    self.new_grid[evil.pos-1].button.pixmap = QPixmap('tower_1.png')
                
                

                #print('!!' + str(evil.hp)) 


            elif evil.pos != 0 and type(self.new_grid[evil.pos+1]) == Tower and self.new_grid[evil.pos+1].IsActivated:
                evil.hp -= random.randint(1, 3)
                helper.Log(ctypes.c_wchar_p(str(evil) + " " + str(evil.hp)))
                self.new_grid[evil.pos+1].hp -= 1
                #print(self.new_grid[evil.pos+1].hp)
                if  self.new_grid[evil.pos+1].hp <= 0:
                    self.new_grid[evil.pos+1].IsActivated   = False
                    self.new_grid[evil.pos+1].button.pixmap = QPixmap('BB.png')
                elif self.new_grid[evil.pos+1].hp < 3:
                    self.new_grid[evil.pos+1].button.pixmap = QPixmap('tower_3.png')
                elif self.new_grid[evil.pos+1].hp < 7:
                    self.new_grid[evil.pos+1].button.pixmap = QPixmap('tower_2.png')
                elif  self.new_grid[evil.pos+1].hp < 10:
                    self.new_grid[evil.pos+1].button.pixmap = QPixmap('tower_1.png')

                #print('!!' + str(evil.hp)) 


            elif evil.pos > len_file_0 and type(self.new_grid[evil.pos-len_file_0]) == Tower and self.new_grid[evil.pos-len_file_0].IsActivated:
                evil.hp -= random.randint(1, 3)
                helper.Log(ctypes.c_wchar_p(str(evil) + " " + str(evil.hp)))
                self.new_grid[evil.pos-len_file_0].hp -= 1
                #print(self.new_grid[evil.pos-len_file_0].hp)
                if  self.new_grid[evil.pos-len_file_0].hp <= 0:
                    self.new_grid[evil.pos-len_file_0].IsActivated     = False
                    self.new_grid[evil.pos-len_file_0].button.pixmap = QPixmap('BB.png')
                elif self.new_grid[evil.pos-len_file_0].hp < 3:
                    self.new_grid[evil.pos-len_file_0].button.pixmap = QPixmap('tower_3.png')
                elif self.new_grid[evil.pos-len_file_0].hp < 7:
                    self.new_grid[evil.pos-len_file_0].button.pixmap = QPixmap('tower_2.png')
                elif  self.new_grid[evil.pos-len_file_0].hp < 10:
                    self.new_grid[evil.pos-len_file_0].button.pixmap = QPixmap('tower_1.png')

                #print('!!' + str(evil.hp)) 


            elif evil.pos+len_file_0 < len(self.new_grid) and type(self.new_grid[evil.pos+len_file_0]) == Tower and self.new_grid[evil.pos+len_file_0].IsActivated:
                evil.hp -= random.randint(1, 3)
                helper.Log(ctypes.c_wchar_p(str(evil) + " " + str(evil.hp)))
                self.new_grid[evil.pos+len_file_0].hp -= 1
                #print(self.new_grid[evil.pos+len_file_0].hp)
                if  self.new_grid[evil.pos+len_file_0].hp <= 0:
                    self.new_grid[evil.pos+len_file_0].IsActivated     = False
                    self.new_grid[evil.pos+len_file_0].button.pixmap = QPixmap('BB.png')
                elif self.new_grid[evil.pos+len_file_0].hp < 3:
                    self.new_grid[evil.pos+len_file_0].button.pixmap = QPixmap('tower_3.png')
                elif self.new_grid[evil.pos+len_file_0].hp < 7:
                    self.new_grid[evil.pos+len_file_0].button.pixmap = QPixmap('tower_2.png')
                elif  self.new_grid[evil.pos+len_file_0].hp < 10:
                    self.new_grid[evil.pos+len_file_0].button.pixmap = QPixmap('tower_1.png')
                #print('!!' + str(evil.hp)) 



            


                
            
            if evil.hp > 7:
                pixmap = PyQt5.QtGui.QPixmap(evil.image[0])

            elif evil.hp > 5:
                pixmap = PyQt5.QtGui.QPixmap(evil.image[1])
            elif evil.hp >= 0:
                pixmap = PyQt5.QtGui.QPixmap(evil.image[2])
            else:
                pixmap = PyQt5.QtGui.QPixmap('BS.png')

                


                
            btn.setPixmap(pixmap)
            btn    = self.new_grid[evil.last_pos]

            pixmap = PyQt5.QtGui.QPixmap('BS.png')
  
            btn.setPixmap(pixmap)


            

    def GetMap(self):
        
        
        self.positions = [(i,j) for i in range(len(self.values)*len(self.values[0])) for j in range(len(self.values[0]))]
        self.new_grid  = []
        self.grid      = QGridLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.grid)
        

        
        values         = []
        for i in range(len(self.values)):
            for j in self.values[i]:
                values.append(j)

        if True:
            for position, name in zip(self.positions, values):
                if name == 0:
                    obj    = QLabel(self)
                    pixmap = PyQt5.QtGui.QPixmap('BS.png')
                    obj.setPixmap(pixmap)
                    self.grid.addWidget(obj, *position)
                elif name == -1:
                    obj = Tower(position)
                    obj.button.released.connect(obj.Click)
                    self.grid.addWidget(obj.button, *position)
                
                self.new_grid.append(obj)
       
            
    def __init__(self):
        super().__init__()
        self.money = 100
        self.score = 0
        self.hp    = 30
        self.label = QLabel("Money: " + str(self.money) + " Score: " + str(self.score) + " HP: " + str(self.hp))
        self.timer    = QBasicTimer()
        self.vbox     = QVBoxLayout()
        self.grid     = QGridLayout()
        self.new_grid  = []
        self.values    = []
        self.pause     = False
        self.game_over = False
        self.time      = 0
        self.time_respawn = 2000
        self.global_time  = 0
        s = -1
        f = open('map.txt', encoding='utf-8')
        self.values_now = []
        i = -1
        for line in f.readlines():
            self.values_now.append([])
            self.values.append([])
            i += 1
            for c in line:
                if   c == 's':
                    self.values_now[i].append(-1)
                    self.values[i].append(-1)
                elif c == '0':
                    self.values_now[i].append(0)
                    self.values[i].append(0)
        f.close()


       

        
        
        Evil(0, 12, self.values)
        self.values_now[evils[0].y][evils[0].x] = 1
        self.GetMap()

        self.initUI()
        
    def AddImage(self, grid):
        pic    = QLabel(self)
        pixmap = PyQt5.QtGui.QPixmap('BB.png')
        pic.setPixmap(pixmap)

        grid.addWidget(pic)
    def keyPressEvent(self, event):



        key = event.key()

        if key == Qt.Key_Escape and not self.game_over:
            if self.pause:
                self.pause = False
                self.timer.start(50, self)
                self.label.setText("Money: " + str(self.money) + " Score: " + str(self.score) + " HP: " + str(self.hp))

            else:
                self.pause = True
                self.timer.stop()
                self.label.setText("Money: " + str(self.money) + " Score: " + str(self.score) +  " HP: " + str(self.hp) + " PAUSE")


    #
    #ТАЙМЕР
    #
    def timerEvent(self, event):
        #
        #Если 200 МС прошло, то
        if event.timerId() == self.timer.timerId():
            self.time        += 200
            self.global_time += 200
            if self.global_time >= 1000:
                self.global_time = 0
                if self.time_respawn - 5 > 0:
                    self.time_respawn -= 5



    
            for e in evils:
                
                if e.hp <= 0:
                    btn    = self.new_grid[e.pos]
                    pixmap = PyQt5.QtGui.QPixmap('BS.png')
                    btn.setPixmap(pixmap)
                    evils.remove(e)
                    ex.money += 5
                    ex.score += 10
                    ex.label.setText("Money: " + str(ex.money) + " Score: " + str(ex.score) + " HP: " + str(ex.hp))
                    continue
                x_now = e.path[e.step][1]
                y_now = e.path[e.step][0]
                e.UpdatePos(x = x_now, y = y_now)
                if e.step < len(e.path)-1: 
                    e.step += 1
                else:
                    btn    = self.new_grid[e.last_pos]

                    pixmap = PyQt5.QtGui.QPixmap('BS.png')
                    btn.setPixmap(pixmap)
                    evils.remove(e)
                    ex.hp -= 10
                    helper.Log(ctypes.c_wchar_p(str(ex) + " " + str(ex.hp)))
                    ex.label.setText("Money: " + str(ex.money) + " Score: " + str(ex.score) + " HP: " + str(ex.hp))
                    if ex.hp <= 0:
                        self.pause = True
                        self.timer.stop()
                        self.label.setText("GAME OVER! YOUR SCORE: " + str(self.score))
                        helper_class.SetScore(ctypes.c_wchar_p(str(self.score)))
                        self.game_over = True
            if self.time >= self.time_respawn:
                self.time = 0

                Evil(0, 12, self.values)

            self.SetMap()
            self.update()
            
        else:
            super(TD, self).timerEvent(event)
    def initUI(self):  
        self.grid.setSpacing(0)
        self.setLayout(self.vbox)
        self.center()
        self.setWindowTitle('TD')
        self.timer.start(200, self)
        self.show()
    def center(self):

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.setFixedSize(size.width()*1, size.height()*1)
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)
        
if __name__ == '__main__':
    helper.DropLog()
    helper.GetMap()
    app = QApplication(sys.argv)
    ex  = TD()

    sys.exit(app.exec_())