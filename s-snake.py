# from curses import KEY_RIGHT, KEY_UP
from PyQt5 import QtWidgets            
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import const  
import random

class Snake(QtWidgets.QMainWindow):
    def __init__(self):
        super(Snake, self).__init__()

        self.setWindowTitle("Snake") 
        self.setStyleSheet("background-color:#ADFF2F")
        self.statusbar=self.statusBar()
        self.statusbar.setStyleSheet("color:#2F4F4F		")

        self.setGeometry(500,500,const.WIN_WIDTH, const.WIN_HEIGHT)

        self.init_params()
        self.start_game()

    def init_params(self):
        self.direction="RIGHT"

        self.snake= [[const.START_X,const.START_Y],
                    [const.START_X-1,const.START_Y],
                    [const.START_X-2,const.START_Y]]

        self.snake_x_head=self.snake[0][0]
        self.snake_y_head=self.snake[0][1]

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.on_time)
        self.timer.start(const.SPEED)

        self.is_over=False
        self.apple_placed=False

    def on_time(self):
        self.move(self.direction)
     
    def start_game(self):
        self.timer.start(const.SPEED)


    def check_snake(self, x,y):
        if y > const.WIN_HEIGHT/const.WIN_MATRIX_HEIGHT or y <0 or x < 0 or x>const.WIN_WIDTH/const.WIN_MATRIX_WIDTH:
            self.is_over=True
            return False
        elif x == self.apple_x and y==self.apple_y:
            self.apple_placed=False
            return True
        
        elif [x,y] in self.snake:
                self.is_over=True
                return False

        self.snake.pop()
        return True 


    def move(self,direction):
        if direction == "DOWN" and self.check_snake(self.snake_x_head,self.snake_y_head+1):
            self.snake_y_head+=1
        elif direction == "UP" and self.check_snake(self.snake_x_head,self.snake_y_head-1):
                self.snake_y_head-=1
        elif direction == "RIGHT" and self.check_snake(self.snake_x_head+1,self.snake_y_head):
                self.snake_x_head+=1
        elif direction == "LEFT" and self.check_snake(self.snake_x_head-1,self.snake_y_head):
                self.snake_x_head-=1
        self.snake.insert(0,[self.snake_x_head,self.snake_y_head])

        self.repaint()
    #draw

    def keyPressEvent(self, e):
        if not self.is_over:
            if e.key()==QtCore.Qt.Key_Up and self.direction!= "DOWN":
                self.move("UP")
                self.direction= "UP"

            elif e.key()==QtCore.Qt.Key_Down and self.direction!= "UP":
                self.move("DOWN")
                self.direction= "DOWN"

            elif e.key()==QtCore.Qt.Key_Right and self.direction!= "LEFT":
                self.move("RIGHT")
                self.direction= "RIGHT"

            elif e.key()==QtCore.Qt.Key_Left and self.direction!= "RIGHT":
                self.move("LEFT")
                self.direction= "LEFT"


    def paintEvent(self,e):
        painter=QtGui.QPainter(self)

        self.draw_snake(painter)
        self.add_apple(painter)
        if self.is_over:
            self.game_over()
        painter.end()

    def draw_snake(self,painter):
        painter.setBrush(QtGui.QColor("#F0FFF0"))
        painter.drawRect(self.snake[0][0]*const.WIN_MATRIX_WIDTH,self.snake[0][1]*const.WIN_MATRIX_HEIGHT,
                            const.WIN_MATRIX_WIDTH,const.WIN_MATRIX_HEIGHT)
        painter.setBrush(QtGui.QColor(const.SNAKE_COLOR))

        game_lvl=-2
        for i in self.snake[1:]:
            painter.drawRect(i[0]*const.WIN_MATRIX_WIDTH,i[1]*const.WIN_MATRIX_HEIGHT,
                            const.WIN_MATRIX_WIDTH,const.WIN_MATRIX_HEIGHT)
            game_lvl+=1
            
        self.statusbar.showMessage(str(game_lvl))
     


    def generate_apple_coordination(self):

        self.apple_x= random.randint(0,((const.WIN_WIDTH/const.WIN_MATRIX_WIDTH)-2))
        self.apple_y= random.randint(0,((const.WIN_HEIGHT/const.WIN_MATRIX_HEIGHT)-2))
        
        
    def add_apple(self,painter):
        painter.setBrush(QtGui.QColor(const.APPLE_COLOR))
        if not self.apple_placed:
            self.generate_apple_coordination()
            self.apple_placed=True
        painter.drawRect(self.apple_x*const.WIN_MATRIX_WIDTH ,self.apple_y*const.WIN_MATRIX_HEIGHT, 
                        const.WIN_MATRIX_WIDTH,const.WIN_MATRIX_HEIGHT)
    


    def game_over(self):
        self.statusbar.showMessage("gamer over")


if __name__=="__main__":
    app= QtWidgets.QApplication(sys.argv)      
    win=Snake()
    win.show()
    sys.exit(app.exec_())                                               

