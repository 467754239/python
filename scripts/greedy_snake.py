from Tkinter import *  
import tkMessageBox,sys  
from random import randint  

class Grid(object):  
    def __init__(self,master=None,window_width=800,window_height=600,grid_width=50,offset=10):  
        self.height = window_height  
        self.width = window_width  
        self.grid_width = grid_width  
        self.offset = offset  
        self.grid_x = self.width/self.grid_width  
        self.grid_y = self.height/self.grid_width  
        self.bg = "#EBEBEB"  
        self.canvas = Canvas(master, width=self.width+2*self.offset, height=self.height+2*self.offset, bg=self.bg)  
        self.canvas.pack()  
        self.grid_list()  
    def draw(self, pos, color,):  
        x = pos[0]*self.grid_width + self.offset  
        y = pos[1]*self.grid_width + self.offset  
        self.canvas.create_rectangle(x, y, x+self.grid_width, y+self.grid_width,fill=color,outline=self.bg)  
    def grid_list(self):  
        grid_list = []  
        for y in range(0,self.grid_y):  
            for x in range(0,self.grid_x):  
                grid_list.append((x,y))  
        self.grid_list = grid_list  

class Food(object):  
    def __init__(self, Grid):  
        self.grid = Grid  
        self.color = "#23D978"          
        self.set_pos()  
    def set_pos(self):  
        x = randint(0,self.grid.grid_x - 1)  
        y = randint(0,self.grid.grid_y - 1)  
        self.pos =  (x, y)      
    def display(self):  
        self.grid.draw(self.pos,self.color)  

class Snake(object):  
    def __init__(self, Grid):  
        self.grid = Grid  
        self.body = [(10,6),(10,7),(10,8)]  
        self.direction = "Up"  
        self.status = ['run','stop']  
        self.speed = 300  
        self.color = "#5FA8D9"          
        self.food = Food(self.grid)  
        self.display_food()  
        self.gameover = False  
        self.score = 0  
    def available_grid(self):  
        return [i for i in self.grid.grid_list if i not in self.body[2:]]  
    def change_direction(self, direction):  
        self.direction = direction  
    def display(self):  
        for (x,y) in self.body:  
            self.grid.draw((x,y),self.color)  
    def display_food(self):  
        while(self.food.pos in self.body):  
            self.food.set_pos()  
        self.food.display()  
    def move(self):  
        head = self.body[0]  
        if self.direction == 'Up':  
            new = (head[0], head[1]-1)  
        elif self.direction == 'Down':  
            new = (head[0], head[1]+1)  
        elif self.direction == 'Left':  
            new = (head[0]-1,head[1])  
        else:  
            new = (head[0]+1,head[1])  
        if not self.food.pos == head:           
            pop = self.body.pop()  
            self.grid.draw(pop,self.grid.bg)  
        else:  
            self.display_food()  
            self.score += 1  
        self.body.insert(0,new)        
        if not new in self.available_grid():  
            self.status.reverse()              
            self.gameover = True  
        else:  
            self.grid.draw(new,color=self.color)  

class SnakeGame(Frame):  
    def __init__(self,master=None, *args, **kwargs):  
        Frame.__init__(self, master)  
        self.master = master  
        self.grid = Grid(master=master,*args, **kwargs)  
        self.snake = Snake(self.grid)  
        self.bind_all("<KeyRelease>", self.key_release)  
        self.snake.display()  
    def run(self):  
        if not self.snake.status[0] == 'stop':  
            self.snake.move()  
        if self.snake.gameover == True:  
            message =  tkMessageBox.showinfo("Game Over", "your score: %d" % self.snake.score)  
            if message == 'ok':  
                sys.exit()  
        self.after(self.snake.speed,self.run)  
    def key_release(self, event):  
        key = event.keysym  
        key_dict = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}  
        if key_dict.has_key(key) and not key == key_dict[self.snake.direction]:  
            self.snake.change_direction(key)  
            self.snake.move()  
        elif key == 'p':  
            self.snake.status.reverse()  

if __name__ == '__main__':  
    root = Tk()  
    snakegame = SnakeGame(root)  
    snakegame.run()  
    snakegame.mainloop()