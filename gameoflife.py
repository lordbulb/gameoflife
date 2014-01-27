#! /usr/bin/python2.5
from Tkinter import *
import tkMessageBox
from tkSimpleDialog import *
from random import random
from math import sqrt

"""
Main logic of the application
"""
class Board(object):
    """
    Class representing the board of the world where the simulation takes place
    It includes all of the game logic, including creation and death of cells as well as subsequent generations
    """

    neighbour_places = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self,speed=1,to_live=(2,3),to_born=(3,)):
        self.points={}
        self.speed=speed
        self.to_live=to_live
        self.to_born=to_born

    def add_cell(self,(x,y)):
        self.points.update({(x,y):0})
        neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places]
        self.points[(x,y)]=sum([(a,b) in self.points for (a,b) in neighbours])
        for n in neighbours:
            if n in self.points: self.points[n]+=1

    def kill(self,(x,y)):
        del self.points[(x,y)]
        neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places]
        for n in neighbours:
            if n in self.points: self.points[n]-=1

    def generation(self):
        to_die=[(x,y) for (x,y) in self.points if self.points[(x,y)] not in self.to_live]
        to_be_born=[]
        for p1,p2 in self.points:
            neighbours=[(p1+_,p2+__) for (_,__) in self.neighbour_places]
            for (x,y) in neighbours:
                if (x,y) not in self.points:
                    new_neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places]
                    if sum([(a,b) in self.points for (a,b) in new_neighbours]) in self.to_born: to_be_born.append((x,y))
        to_be_born=list(set(to_be_born))
        for _ in to_die: self.kill(_)
        for _ in to_be_born: self.add_cell(_)


class Hexa_Board(object):
    """Class representing the hexagonal version of the simulation"""
    neighbour_places_odd = [(-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, 0), (1, 1)]
    neighbour_places_even = [(-1, -1), (-1, 0), (0, -1),
                    (0, 1), (1, -1), (1, 0)]

    def __init__(self,speed=1,to_live=(2,3),to_born=(3,)):
        self.points={}
        self.speed=speed
        self.to_live=to_live
        self.to_born=to_born

    def add_cell(self,(x,y)):
        self.points.update({(x,y):0})
        if not x%2:
            neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_even]
        else:
            neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_odd]
            
        self.points[(x,y)]=sum([(a,b) in self.points for (a,b) in neighbours])
        for n in neighbours:
            if n in self.points: self.points[n]+=1

    def kill(self,(x,y)):
        del self.points[(x,y)]
        if not x%2:
            neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_even]
        else:
            neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_odd]

        for n in neighbours:
            if n in self.points: self.points[n]-=1

    def generation(self):
        to_die=[(x,y) for (x,y) in self.points if self.points[(x,y)] not in self.to_live]
        to_be_born=[]
        neighbours=[]
        for p1,p2 in self.points:
            if not p1%2:
                neighbours+=[(p1+_,p2+__) for (_,__) in self.neighbour_places_even]
            else:
                neighbours+=[(p1+_,p2+__) for (_,__) in self.neighbour_places_odd]

        for (x,y) in neighbours:
                if (x,y) not in self.points:
                    if not x%2:
                        new_neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_even]
                    else:
                        new_neighbours=[(x+_,y+__) for (_,__) in self.neighbour_places_odd]
                    if sum([(a,b) in self.points for (a,b) in new_neighbours]) in self.to_born: to_be_born.append((x,y))
        to_be_born=list(set(to_be_born))
        for _ in to_die: self.kill(_)
        for _ in to_be_born: self.add_cell(_)


class Game(object):
    """The main class of the game including the main GUI components"""
    def __init__(self):

        self.tk = Tk()
        self.tk.title("Game of life")
        self.init_menu()
        self.board = None
        self.welcome = Label(self.tk, padx = 20, pady = 20, text = help_string)
        self.welcome.pack()

        self.tk.mainloop()

    def init_menu(self):

        menu = Menu(self.tk)

        file = Menu(menu, tearoff=0)
        file.add_command(label = "About", command = lambda: tkMessageBox.showinfo("Game of Life", "Miroslav Mihov's Game of life\nJune 2008\nVersion 0.1"),underline=0)
        file.add_command(label = "Help", command = lambda: tkMessageBox.showinfo("Help", help_string),underline=0)
        file.add_separator()
        file.add_command(label = "Quit", command = self.tk.quit,underline=0)

        menu.add_cascade(label = "File", menu = file, underline=0)

        game = Menu(menu, tearoff=0)
        game.add_command(label="New", command=lambda: self.new_board(), underline=0)
        game.add_command(label="New Random", command=lambda: self.random_game(), underline=4)
        game.add_command(label="New Hexagon", command=lambda: self.hexagon_game(), underline=4)
        game.add_command(label="New Random Hexagon", command=lambda: self.random_hexagon(), underline=2)

        menu.add_cascade(label = "New Game", menu = game, underline=0)

        self.tk.config(menu = menu)

    def random_hexagon(self):

        if self.welcome:
            self.welcome.pack_forget()
            self.welcome.destroy()
        if self.board:
            self.board.hide()

        cell_number = askinteger("Game Of Life", "Enter the number of cells to apper on field(>0 and <2500)")
        
        field=Hexa_Board()
        cells=[[]]*50
        for i in range(0,50):
            cells[i]=[random() for j in range(0,50)]
        cells=[(x,y) for x in range(0,50) for y in range(0,50) if cells[x][y]<float(float(cell_number)/2500)]
        for x,y in cells:
            field.add_cell((x,y))
    
        self.board = Hexa_Draw(field,self.tk)
        self.board.pack()

    def random_game(self):

        if self.welcome:
            self.welcome.pack_forget()
            self.welcome.destroy()
        if self.board:
            self.board.hide()

        cell_number = askinteger("Game Of Life", "Enter the number of cells to apper on field(>0 and <10000)")
        
        field=Board()
        cells=[[]]*100
        for i in range(0,100):
            cells[i]=[random() for j in range(0,100)]
        cells=[(x,y) for x in range(0,100) for y in range(0,100) if cells[x][y]<float(float(cell_number)/10000)]
        for x,y in cells:
            field.add_cell((x,y))
    
        self.board = Draw(field,self.tk)
        self.board.pack()

    def new_board(self):
        if self.welcome:
            self.welcome.pack_forget()
            self.welcome.destroy()
        if self.board:
            self.board.hide()

        field = Board()
        self.board = Draw(field,self.tk)
        self.board.pack()

    def hexagon_game(self):
        if self.welcome:
            self.welcome.pack_forget()
            self.welcome.destroy()
        if self.board:
            self.board.hide()

        field = Hexa_Board()
        self.board = Hexa_Draw(field,self.tk)
        self.board.pack()

class Draw(Frame):
    """Class representing one instance of the simulation as well as the GUI components for controlling it"""
    def __init__(self, field, root):
        Frame.__init__(self, root)
        self.field=field
        self.generations=0
        self.upper=(0,0)
        self.lower=(100*SIZE,100*SIZE)
        self.condition ="Stopped"
        self.coloured=False
        self.clickable=True
        self.shape='oval'
        
        self.canvas = Canvas(root, width=100*SIZE, height=100*SIZE, bg=BGCOLOUR)
        self.canvas.pack(side=RIGHT)
        self.status = Frame(root)
        self.status.pack(side=RIGHT)
        
        self.start=Button(self.status, text="Start", command=self.starting, width=15)
        self.start.pack(side=TOP)

        self.stop=Button(self.status, text="Stop", command=self.stopping, width=15)
        self.stop.pack(side=TOP)

        self.speed=Button(self.status, text="Speed:%d"%self.field.speed, command=self.set_speed, width=15)
        self.speed.pack(side=TOP)

        self.to_live=Button(self.status, text="To live: "+reduce(lambda x,y: x+y, map(str,self.field.to_live),''), command=self.set_to_live, width=15)
        self.to_live.pack(side=TOP)

        self.to_born=Button(self.status, text="To be born: "+reduce(lambda x,y: x+y, map(str,self.field.to_born),''), command=self.set_to_born, width=15)
        self.to_born.pack(side=TOP)

        self.colour_on_off=Button(self.status, text="Colouring OFF", command=self.colouring_on_off, width=15)
        self.colour_on_off.pack(side=TOP)

        self.live_clicking=Button(self.status, text="Live clicking ON", command=self.live_click, width=15)
        self.live_clicking.pack(side=TOP)

        self.set_shape=Button(self.status, text="Shape: oval", command=self.setting_shape, width=15)
        self.set_shape.pack(side=TOP)

        self.gen_label=Label(self.status, text="Generations: 0", width=15)
        self.gen_label.pack(side=TOP)

        self.cell_label=Label(self.status, text="Cells: %d" %len(self.field.points), width=15)
        self.cell_label.pack(side=TOP)

        self.redraw()
        
        
        root.bind("<Return>", lambda _: self.starting())
        root.bind("<Escape>", lambda _: self.stopping())
        root.bind("<Down>", lambda _: self.key_press(0,MOVE))
        root.bind("<Up>", lambda _: self.key_press(0,-MOVE))
        root.bind("<Left>", lambda _: self.key_press(-MOVE,0))
        root.bind("<Right>", lambda _: self.key_press(MOVE,0))
        root.bind("<Key-Home>", lambda _: self.key_press(-MOVE,-MOVE))
        root.bind("<Key-Next>", lambda _: self.key_press(MOVE,MOVE))
        root.bind("<Key-Prior>", lambda _: self.key_press(MOVE,-MOVE))
        root.bind("<Key-Delete>", lambda _: self.key_press(-MOVE,MOVE))
        self.canvas.bind("<Button-1>", lambda _: self.new_point(_, fill=CELLCOLOUR))
        self.canvas.bind("<Button-3>", lambda _: self.del_point(_, fill=BGCOLOUR))

    def live_click(self):
        self.clickable= not self.clickable
        if self.clickable: self.live_clicking['text']="Live clicking ON"
        else: self.live_clicking['text']="Live clicking OFF" 

        if self.clickable and self.condition=="Running":
            self.canvas.bind("<Button-1>", lambda _: self.new_point(_, fill=CELLCOLOUR))
            self.canvas.bind("<Button-3>", lambda _: self.del_point(_, fill=BGCOLOUR))
        elif self.condition=="Running":
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
        

    def colouring_on_off(self):
        self.coloured= not self.coloured
        if self.coloured: self.colour_on_off['text']="Colouring ON"
        else: self.colour_on_off['text']="Colouring OFF"

    def setting_shape(self):
        if self.shape=='oval':
            self.shape='rectangle'
            self.set_shape['text']="Shape: rectangle"
        else:
            self.shape='oval'
            self.set_shape['text']="Shape: oval"
        self.redraw()

    def starting(self):
        if self.condition=="Stopped":
            self.condition = "Running"

            if not self.clickable:
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Button-3>")

            self.next_frame()
            
    def stopping(self):
        if self.condition=="Running":
            self.condition="Stopped"

            #if not self.clickable:
            self.canvas.bind("<Button-1>", lambda _: self.new_point(_, fill=CELLCOLOUR))
            self.canvas.bind("<Button-3>", lambda _: self.del_point(_, fill=BGCOLOUR))

            self.after_cancel(self.next)

    def set_speed(self):
        speed = -1
        while speed and speed<0:
            speed = askinteger("Game Of Life", "Enter the time in milliseconds between drawing two generations:")
        if speed:
            self.field.speed=speed
            self.speed['text']="Speed %d" %speed

    def set_to_live(self):
        cell_number='a'
        while cell_number and not all([(True if i>'0' and i<'9' else False) for i in cell_number]):
            cell_number = askstring("Game Of Life", "Enter the number of needed neighbours to keep on living")
        if cell_number:
            self.to_live['text']="To live: "+cell_number
            self.field.to_live=tuple([int(x) for x in cell_number])

    def set_to_born(self):
        cell_number='a'
        while cell_number and not all([(True if i>='0' and i<'9' else False) for i in cell_number]):
            cell_number = askstring("Game Of Life", "Enter the number of needed neighbours to be born (more than 0)")
        if cell_number:
            self.to_born['text']="To be born: "+cell_number
            self.field.to_born=tuple([int(x) for x in cell_number])
        
    def hide(self):
        self.canvas.pack_forget()
        self.status.pack_forget()
        self.canvas.destroy()
        self.status.destroy()
        self.pack_forget()
        self.destroy()

    def del_point(self,point, **kwargs):
        if ((point.x+self.upper[0])/SIZE,(point.y+self.upper[1])/SIZE) in self.field.points:
            self.field.kill(((point.x+self.upper[0])/SIZE,(point.y+self.upper[1])/SIZE))
            #self.canvas._create(self.shape,[(point.x/SIZE)*SIZE, (point.y/SIZE)*SIZE, (point.x/SIZE)*SIZE + SIZE - 1, (point.y/SIZE)*SIZE + SIZE - 1],**kwargs)
            if self.shape=='oval': self.canvas.create_oval((point.x/SIZE)*SIZE, (point.y/SIZE)*SIZE, (point.x/SIZE)*SIZE + SIZE - 1, (point.y/SIZE)*SIZE + SIZE - 1, **kwargs)
            else: self.canvas.create_rectangle((point.x/SIZE)*SIZE, (point.y/SIZE)*SIZE, (point.x/SIZE)*SIZE + SIZE - 1, (point.y/SIZE)*SIZE + SIZE - 1, **kwargs)
            self.cell_label['text']="Cells: %d" %len(self.field.points)

    def new_point(self, point, **kwargs):
        if ((point.x+self.upper[0])/SIZE,(point.y+self.upper[1])/SIZE) not in self.field.points:
            x, y = point.x,point.y
            #self.canvas._create(self.shape,[(x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1], **kwargs)
            if self.shape=='oval': self.canvas.create_oval((x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1, **kwargs)
            else:self.canvas.create_rectangle((x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1, **kwargs)
            self.field.add_cell(((x+self.upper[0])/SIZE,(y+self.upper[1])/SIZE))
            self.cell_label['text']="Cells: %d" %len(self.field.points)

    def put_point(self, point, **kwargs):
        x, y = point[0]*SIZE-self.upper[0], point[1]*SIZE-self.upper[1]
        #self.canvas._create(self.shape,[(x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1], **kwargs)
        if self.shape=='oval': self.canvas.create_oval((x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1, **kwargs)
        else: self.canvas.create_rectangle((x/SIZE)*SIZE, (y/SIZE)*SIZE, (x/SIZE)*SIZE + SIZE - 1, (y/SIZE)*SIZE + SIZE - 1, **kwargs)

    def is_shape(self,x,y,shape):
        new_shape=[(x+__,y+_,___) for (_,__,___) in shape]
        return all([((x,y) in self.new_points)==z for (x,y,z) in new_shape])

    def redraw(self):
        for i in self.canvas.find_all(): self.canvas.delete(i)
    
        self.new_points={}
        for x,y in self.field.points:
            if  x*SIZE in range(self.upper[0],self.lower[0]+1) and y*SIZE in range(self.upper[1],self.lower[1]+1):
                self.new_points.update({(x,y):CELLCOLOUR})

        if self.coloured:
            for x,y in self.new_points:
                if self.new_points[(x,y)]==CELLCOLOUR:
                    for shape,colour in SHAPES:
                        if self.is_shape(x,y,shape):
                            for (a,b,c) in shape:
                                if c: self.new_points[(x+b),(y+a)]=colour
                            break

        for x,y in self.new_points: self.put_point((x,y), fill=self.new_points[(x,y)])

    def key_press(self, x,y):
        self.upper = self.upper[0]+x,self.upper[1]+y
        self.lower = self.lower[0]+x,self.lower[1]+y
        self.redraw()

    def next_frame(self):
        self.field.generation()
        self.redraw()
        self.generations+=1
        self.gen_label['text']="Generations: %s" %self.generations
        self.cell_label['text']="Cells: %d" %len(self.field.points)
        self.next=self.after(self.field.speed, self.next_frame)

SIZE=10
MOVE=3*SIZE
BGCOLOUR='black'
CELLCOLOUR='white'

A=SIZE/2
B=SIZE*sqrt(3)/2
C=SIZE
HEX_MOVE=int(B*6)

class Hexa_Draw(Draw):
    def __init__(self, field, root):
        Frame.__init__(self, root)
        self.field=field
        self.generations=0
        self.upper=(0,0)
        self.lower=(75*C,int(100*B))
        self.condition ="Stopped"
        self.clickable=True
        
        self.canvas = Canvas(root, width=75*SIZE, height=int(100*B), bg=BGCOLOUR)
        self.canvas.pack(side=RIGHT)
        self.status = Frame(root)
        self.status.pack(side=RIGHT)
        
        self.start=Button(self.status, text="Start", command=self.starting, width=15)
        self.start.pack(side=TOP)

        self.stop=Button(self.status, text="Stop", command=self.stopping, width=15)
        self.stop.pack(side=TOP)

        self.speed=Button(self.status, text="Speed:%d"%self.field.speed, command=self.set_speed, width=15)
        self.speed.pack(side=TOP)

        self.to_live=Button(self.status, text="To live: "+reduce(lambda x,y: x+y, map(str,self.field.to_live),''), command=self.set_to_live, width=15)
        self.to_live.pack(side=TOP)

        self.to_born=Button(self.status, text="To be born: "+reduce(lambda x,y: x+y, map(str,self.field.to_born),''), command=self.set_to_born, width=15)
        self.to_born.pack(side=TOP)

        self.live_clicking=Button(self.status, text="Live clicking ON", command=self.live_click, width=15)
        self.live_clicking.pack(side=TOP)

        self.gen_label=Label(self.status, text="Generations: 0", width=15)
        self.gen_label.pack(side=TOP)

        self.cell_label=Label(self.status, text="Cells: %d" %len(self.field.points), width=15)
        self.cell_label.pack(side=TOP)

        self.redraw()
        
        
        root.bind("<Return>", lambda _: self.starting())
        root.bind("<Escape>", lambda _: self.stopping())
        root.bind("<Down>", lambda _: self.key_press(0,HEX_MOVE))
        root.bind("<Up>", lambda _: self.key_press(0,-HEX_MOVE))
        root.bind("<Left>", lambda _: self.key_press(-2*MOVE,0))
        root.bind("<Right>", lambda _: self.key_press(2*MOVE,0))
        root.bind("<Key-Home>", lambda _: self.key_press(-2*MOVE,-HEX_MOVE))
        root.bind("<Key-Next>", lambda _: self.key_press(2*MOVE,HEX_MOVE))
        root.bind("<Key-Prior>", lambda _: self.key_press(2*MOVE,-HEX_MOVE))
        root.bind("<Key-Delete>", lambda _: self.key_press(-2*MOVE,HEX_MOVE))
        self.canvas.bind("<Button-1>", lambda _: self.new_point(_, fill=CELLCOLOUR))
        self.canvas.bind("<Button-3>", lambda _: self.del_point(_, fill=BGCOLOUR))


    def del_point(self,point, **kwargs):
        if (int((point.x + self.upper[0])/(1.5*C)),int((point.y+self.upper[1])/(2*B))) in self.field.points:
            self.field.kill((int((point.x+self.upper[0])/(1.5*C)),int((point.y+self.upper[1])/(2*B))))
            if not int(point.x/(1.5*C))%2:
                x,y=int(int(point.x/(1.5*C))*1.5*C), int(int(point.y/(2*B))*2*B)
            else:
                x,y=int(int(point.x/(1.5*C))*1.5*C), int(int(point.y/(2*B))*2*B+B)
            self.canvas.create_polygon(x, int(y+B), A+x, y, A+C+x, y, 2*C+x, int(B+y), A+C+x, int(2*B+y), A+x, int(2*B+y), **kwargs)
            self.cell_label['text']="Cells: %d" %len(self.field.points)

    def new_point(self, point, **kwargs):
        if (int((point.x+self.upper[0])/(1.5*C)),int((point.y+self.upper[1])/(2*B))) not in self.field.points:
            x, y = int(point.x/(1.5*C)),int(point.y/(2*B))
            self.field.add_cell((int(x+self.upper[0]/(1.5*C)),int(y+self.upper[1]/(2*B))))
            if not x%2: x, y = x*1.5*C, int(y*2*B)
            else: x,y=x*1.5*C, int(y*2*B+B)
            self.canvas.create_polygon(x, int(y+B), A+x, y, A+C+x, y, 2*C+x, int(B+y), A+C+x, int(2*B+y), A+x, int(2*B+y), **kwargs)
            self.cell_label['text']="Cells: %d" %len(self.field.points)

    def put_point(self, point, **kwargs):
        if point[0]%2: x, y = point[0]*1.5*C-self.upper[0], int(point[1]*2*B+B-self.upper[1])
        else: x, y = point[0]*1.5*C-self.upper[0], int(point[1]*2*B-self.upper[1])
        self.canvas.create_polygon(x, int(y+B), A+x, y, A+C+x, y, 2*C+x, int(B+y), A+C+x, int(2*B+y), A+x, int(2*B+y), **kwargs)
        
    def is_shape(self,x,y,shape):
        new_shape=[(x+__,y+_,___) for (_,__,___) in shape]
        return all([((x,y) in self.new_points)==z for (x,y,z) in new_shape])

    def redraw(self):
        for i in self.canvas.find_all(): self.canvas.delete(i)
    
        for x,y in self.field.points:
            if self.upper<(x*1.5*C,y*2*B)<self.lower: self.put_point((x,y), fill=CELLCOLOUR)


SIZE=10
MOVE=SIZE*3
BGCOLOUR='black'
CELLCOLOUR='white'

BLOCK=[(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-1,0),(0,0,1),(0,1,1),(0,2,0),(1,-1,0),(1,0,1),(1,1,1),(1,2,0),(2,-1,0),(2,0,0),(2,1,0),(2,2,0)]
BLINKER1=[(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(-1,3,0),(0,-1,0),(0,0,1),(0,1,1),(0,2,1),(0,3,0),(1,-1,0),(1,0,0),(1,1,0),(1,2,0),(1,3,0)]
BLINKER2=[(-1,-1,0),(-1,0,0),(-1,1,0),(0,-1,0),(0,0,1),(0,1,0),(1,-1,0),(1,0,1),(1,1,0),(2,-1,0),(2,0,1),(2,1,0),(3,-1,0),(3,0,0),(3,1,0)]
BOAT1=[(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(-1,3,0),(0,-1,0),(0,0,1),(0,1,1),(0,2,0),(0,3,0),(1,-1,0),(1,0,1),(1,1,0),(1,2,1),(1,3,0),(2,-1,0),(2,0,0),(2,1,1),(2,2,0),(2,3,0),(3,-1,0),(3,0,0),(3,1,0),(3,2,0),(3,3,0)]
BOAT2=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,1),(0,2,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,1),(1,2,0),(2,-2,0),(2,-1,0),(2,0,1),(2,1,0),(0,2,0)]
BOAT3=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,0),(0,2,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,1),(1,2,0),(2,-2,0),(2,-1,0),(2,0,1),(2,1,1),(0,2,0)]
BOAT4=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,0),(0,2,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,1),(1,2,0),(2,-2,0),(2,-1,1),(2,0,1),(2,1,0),(0,2,0)]
GLIDER11=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,0),(0,2,0),(1,-2,0),(1,-1,1),(1,0,1),(1,1,0),(1,2,0),(2,-2,0),(2,-1,1),(2,0,0),(2,1,1),(2,2,0),(3,-2,0),(3,-1,0),(3,0,0),(3,1,0),(3,2,0)]
GLIDER12=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,1),(0,0,1),(0,1,1),(0,2,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,0),(1,2,0),(2,-2,0),(2,-1,0),(2,0,1),(2,1,0),(2,2,0),(3,-2,0),(3,-1,0),(3,0,0),(3,1,0),(3,2,0)]
GLIDER13=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,1),(0,0,1),(0,1,0),(0,2,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,1),(1,2,0),(2,-2,0),(2,-1,1),(2,0,0),(2,1,0),(2,2,0),(3,-2,0),(3,-1,0),(3,0,0),(3,1,0),(3,2,0)]
GLIDER14=[(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,1),(0,2,0),(1,-2,0),(1,-1,1),(1,0,1),(1,1,0),(1,2,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,1),(2,2,0),(3,-2,0),(3,-1,0),(3,0,0),(3,1,0),(3,2,0)]
GLIDER21=[(-2,-3,0),(-2,-2,0),(-2,-1,0),(-2,0,0),(-2,1,0),(-1,-3,0),(-1,-2,0),(-1,-1,1),(-1,0,0),(-1,1,0),(0,-3,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,0),(1,-3,0),(1,-2,1),(1,-1,1),(1,0,1),(1,1,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0)]
GLIDER22=[(-2,-3,0),(-2,-2,0),(-2,-1,0),(-2,0,0),(-2,1,0),(-1,-3,0),(-1,-2,1),(-1,-1,0),(-1,0,1),(-1,1,0),(0,-3,0),(0,-2,0),(0,-1,1),(0,0,1),(0,1,0),(1,-3,0),(1,-2,0),(1,-1,1),(1,0,0),(1,1,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0)]
GLIDER23=[(-2,-3,0),(-2,-2,0),(-2,-1,0),(-2,0,0),(-2,1,0),(-1,-3,0),(-1,-2,0),(-1,-1,0),(-1,0,1),(-1,1,0),(0,-3,0),(0,-2,1),(0,-1,0),(0,0,1),(0,1,0),(1,-3,0),(1,-2,0),(1,-1,1),(1,0,1),(1,1,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0)]
GLIDER24=[(-2,-3,0),(-2,-2,0),(-2,-1,0),(-2,0,0),(-2,1,0),(-1,-3,0),(-1,-2,1),(-1,-1,0),(-1,0,0),(-1,1,0),(0,-3,0),(0,-2,0),(0,-1,1),(0,0,1),(0,1,0),(1,-3,0),(1,-2,1),(1,-1,1),(1,0,0),(1,1,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0)]
GLIDER31=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 1), (1, 1, 1), (1, 2, 0), (2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 0), (2, 2, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)]
GLIDER32=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 1), (1, 1, 1), (1, 2, 0), (2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 1), (2, 2, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)]
GLIDER33=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (1, -2, 0), (1, -1, 1), (1, 0, 0), (1, 1, 1), (1, 2, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 1), (2, 2, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)]
GLIDER34=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 1), (1, 2, 0), (2, -2, 0), (2, -1, 0), (2, 0, 1), (2, 1, 0), (2, 2, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)]
GLIDER41=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 1), (-2, 1, 0), (-2, 2, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)]
GLIDER42=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-2, -2, 0), (-2, -1, 1), (-2, 0, 0), (-2, 1, 0), (-2, 2, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 0), (-1, 1, 1), (-1, 2, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)]
GLIDER43=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-2, -2, 0), (-2, -1, 1), (-2, 0, 0), (-2, 1, 1), (-2, 2, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)]
GLIDER44=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 1), (-2, 2, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (-1, 2, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)]
LAND1=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0), (1, -2, 0), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 1), (1, 3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 1), (2, 1, 1), (2, 2, 0), (2, 3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)]
LAND2=[(-2, -3, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-1, -3, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 0), (-1, 1, 0), (0, -3, 0), (0, -2, 1), (0, -1, 0), (0, 0, 1), (0, 1, 0), (1, -3, 0), (1, -2, 1), (1, -1, 0), (1, 0, 1), (1, 1, 0), (2, -3, 0), (2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0)]
TOAD1=[(-1,-3,0),(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-3,0),(0,-2,0),(0,-1,1),(0,0,1),(0,1,1),(0,2,0),(1,-3,0),(1,-2,1),(1,-1,1),(1,0,1),(1,1,0),(1,2,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0),(2,2,0)]
TOAD3=[(-1,-3,0),(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-3,0),(0,-2,1),(0,-1,1),(0,0,1),(0,1,0),(0,2,0),(1,-3,0),(1,-2,0),(1,-1,1),(1,0,1),(1,1,1),(1,2,0),(2,-3,0),(2,-2,0),(2,-1,0),(2,0,0),(2,1,0),(2,2,0)]
TOAD2=[(-1,-3,0),(-1,-2,0),(-1,-1,0),(-1,0,0),(-1,1,0),(-1,2,0),(0,-3,0),(0,-2,0),(0,-1,0),(0,0,1),(0,1,0),(0,2,0),(1,-3,0),(1,-2,1),(1,-1,0),(1,0,0),(1,1,1),(1,2,0),(2,-3,0),(2,-2,1),(2,-1,0),(2,0,0),(2,1,1),(2,2,0),(3,-3,0),(3,-2,0),(3,-1,1),(3,0,0),(3,1,0),(3,2,0),(4,-3,0),(4,-2,0),(4,-1,0),(4,0,0),(4,1,0),(4,2,0)]
TOAD4=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0),(-1, 3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 0), (0, 3, 0),(1, -2, 0), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 1), (1, 3, 0),(2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 0), (2, 2, 1), (2, 3, 0),(3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 1), (3, 2, 0),(3, 3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0),(4, 3, 0)]
TOAD5=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -2, 0), (-2, -1, 1), (-2, 0, 0), (-2, 1, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (1, -2, 0), (1, -1, 0), (1, 0, 1), (1, 1, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0)]
TOAD6=[(-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 1), (-2, 1, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (1, -2, 0), (1, -1, 1), (1, 0, 0), (1, 1, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0)]
TOAD7=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 1), (1, 3, 0), (2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 1), (3, 1, 1), (3, 2, 0), (3, 3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
TOAD8=[(-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0), (1, -2, 0), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 1), (2, 3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 1), (3, 1, 1), (3, 2, 0), (3, 3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
LWSS1=[(-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -3, 0), (0, -2, 1), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0), (1, -3, 0), (1, -2, 1), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 1), (1, 3, 0), (2, -3, 0), (2, -2, 1), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (3, -3, 0), (3, -2, 0), (3, -1, 1), (3, 0, 0), (3, 1, 0), (3, 2, 1), (3, 3, 0), (4, -3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
LWSS2=[(-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0), (1, -3, 0), (1, -2, 0), (1, -1, 1), (1, 0, 1), (1, 1, 1), (1, 2, 1), (1, 3, 0), (2, -3, 0), (2, -2, 1), (2, -1, 1), (2, 0, 0), (2, 1, 1), (2, 2, 1), (2, 3, 0), (3, -3, 0), (3, -2, 0), (3, -1, 1), (3, 0, 1), (3, 1, 0), (3, 2, 0), (3, 3, 0), (4, -3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
LWSS3=[(-4, -3, 0), (-4, -2, 0), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-3, -3, 0), (-3, -2, 1), (-3, -1, 0), (-3, 0, 0), (-3, 1, 1), (-3, 2, 0), (-3, 3, 0), (-2, -3, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-2, 2, 1), (-2, 3, 0), (-1, -3, 0), (-1, -2, 1), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 1), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 1), (0, 3, 0), (1, -3, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0)]
LWSS4=[(-4, -3, 0), (-4, -2, 0), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 1), (-3, 1, 1), (-3, 2, 0), (-3, 3, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 1), (-2, 0, 0), (-2, 1, 1), (-2, 2, 1), (-2, 3, 0), (-1, -3, 0), (-1, -2, 1), (-1, -1, 1), (-1, 0, 1), (-1, 1, 1), (-1, 2, 0), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (0, 2, 0), (0, 3, 0), (1, -3, 0), (1, -2, 0), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0)]
LWSS5=[(-3, -4, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -4, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 1), (-2, 0, 1), (-2, 1, 0), (-1, -4, 0), (-1, -3, 1), (-1, -2, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 0), (0, -4, 0), (0, -3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (1, -4, 0), (1, -3, 0), (1, -2, 0), (1, -1, 0), (1, 0, 1), (1, 1, 0), (2, -4, 0), (2, -3, 1), (2, -2, 0), (2, -1, 1), (2, 0, 0), (2, 1, 0), (3, -4, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0)]
LWSS6=[(-3, -4, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -4, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-1, -4, 0), (-1, -3, 1), (-1, -2, 1), (-1, -1, 1), (-1, 0, 0), (-1, 1, 0), (0, -4, 0), (0, -3, 1), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (1, -4, 0), (1, -3, 0), (1, -2, 1), (1, -1, 1), (1, 0, 1), (1, 1, 0), (2, -4, 0), (2, -3, 0), (2, -2, 1), (2, -1, 1), (2, 0, 0), (2, 1, 0), (3, -4, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0)]
LWSS7=[(-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-3, 4, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 1), (-2, 2, 0), (-2, 3, 1), (-2, 4, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (-1, 4, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0), (1, -1, 0), (1, 0, 1), (1, 1, 0), (1, 2, 0), (1, 3, 1), (1, 4, 0), (2, -1, 0), (2, 0, 1), (2, 1, 1), (2, 2, 1), (2, 3, 0), (2, 4, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0), (3, 4, 0)]
LWSS8=[(-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-3, 4, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 1), (-2, 2, 1), (-2, 3, 0), (-2, 4, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 1), (-1, 2, 1), (-1, 3, 0), (-1, 4, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 1), (0, 4, 0), (1, -1, 0), (1, 0, 0), (1, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 1), (2, 3, 0), (2, 4, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0), (3, 4, 0)]
LWSS9=[(-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 1), (0, 3, 0), (1, -3, 0), (1, -2, 1), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, 2, 1), (1, 3, 0), (2, -3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 1), (2, 3, 0), (3, -3, 0), (3, -2, 1), (3, -1, 0), (3, 0, 0), (3, 1, 1), (3, 2, 0), (3, 3, 0), (4, -3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
LWSS10=[(-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 0), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (0, 2, 0), (0, 3, 0), (1, -3, 0), (1, -2, 1), (1, -1, 1), (1, 0, 1), (1, 1, 1), (1, 2, 0), (1, 3, 0), (2, -3, 0), (2, -2, 1), (2, -1, 1), (2, 0, 0), (2, 1, 1), (2, 2, 1), (2, 3, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 1), (3, 1, 1), (3, 2, 0), (3, 3, 0), (4, -3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 0), (4, 1, 0), (4, 2, 0), (4, 3, 0)]
LWSS11=[(-4, -3, 0), (-4, -2, 0), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 1), (-3, 0, 0), (-3, 1, 0), (-3, 2, 1), (-3, 3, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-2, 2, 0), (-2, 3, 0), (-1, -3, 0), (-1, -2, 1), (-1, -1, 0), (-1, 0, 0), (-1, 1, 0), (-1, 2, 1), (-1, 3, 0), (0, -3, 0), (0, -2, 1), (0, -1, 1), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0)]
LWSS12=[(-4, -3, 0), (-4, -2, 0), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 1), (-3, 0, 1), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 1), (-2, 0, 0), (-2, 1, 1), (-2, 2, 1), (-2, 3, 0), (-1, -3, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 1), (-1, 2, 1), (-1, 3, 0), (0, -3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0)]
LWSS13=[(-3, -4, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -4, 0), (-2, -3, 1), (-2, -2, 0), (-2, -1, 1), (-2, 0, 0), (-2, 1, 0), (-1, -4, 0), (-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 0), (0, -4, 0), (0, -3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (1, -4, 0), (1, -3, 1), (1, -2, 0), (1, -1, 0), (1, 0, 1), (1, 1, 0), (2, -4, 0), (2, -3, 0), (2, -2, 1), (2, -1, 1), (2, 0, 1), (2, 1, 0), (3, -4, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0)]
LWSS14=[(-3, -4, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-2, -4, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 1), (-2, 0, 0), (-2, 1, 0), (-1, -4, 0), (-1, -3, 0), (-1, -2, 1), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, -4, 0), (0, -3, 1), (0, -2, 0), (0, -1, 1), (0, 0, 1), (0, 1, 0), (1, -4, 0), (1, -3, 1), (1, -2, 1), (1, -1, 1), (1, 0, 0), (1, 1, 0), (2, -4, 0), (2, -3, 0), (2, -2, 1), (2, -1, 0), (2, 0, 0), (2, 1, 0), (3, -4, 0), (3, -3, 0), (3, -2, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0)]
LWSS15=[(-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-3, 4, 0), (-2, -1, 0), (-2, 0, 1), (-2, 1, 1), (-2, 2, 1), (-2, 3, 0), (-2, 4, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 0), (-1, 2, 0), (-1, 3, 1), (-1, 4, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 0), (0, 3, 0), (0, 4, 0), (1, -1, 0), (1, 0, 1), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0), (2, -1, 0), (2, 0, 0), (2, 1, 1), (2, 2, 0), (2, 3, 1), (2, 4, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0), (3, 4, 0)]
LWSS16=[(-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-3, 4, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-2, 2, 1), (-2, 3, 0), (-2, 4, 0), (-1, -1, 0), (-1, 0, 0), (-1, 1, 1), (-1, 2, 1), (-1, 3, 1), (-1, 4, 0), (0, -1, 0), (0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 1), (0, 4, 0), (1, -1, 0), (1, 0, 1), (1, 1, 1), (1, 2, 1), (1, 3, 0), (1, 4, 0), (2, -1, 0), (2, 0, 0), (2, 1, 1), (2, 2, 1), (2, 3, 0), (2, 4, 0), (3, -1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0), (3, 4, 0)]
PULSAR1=[(-5, -6, 0), (-5, -5, 0), (-5, -4, 0), (-5, -3, 0), (-5, -2, 0), (-5, -1, 0), (-5, 0, 0), (-5, 1, 0), (-5, 2, 0), (-5, 3, 0), (-5, 4, 0), (-5, 5, 0), (-5, 6, 0), (-5, 7, 0), (-5, 8, 0),
         (-4, -6, 0), (-4, -5, 0), (-4, -4, 0), (-4, -3, 1), (-4, -2, 1), (-4, -1, 1), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 1), (-4, 4, 1), (-4, 5, 1), (-4, 6, 0), (-4, 7, 0), (-4, 8, 0),
         (-3, -6, 0), (-3, -5, 0), (-3, -4, 0), (-3, -3, 0), (-3, -2, 0), (-3, -1, 0), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 0), (-3, 4, 0), (-3, 5, 0), (-3, 6, 0), (-3, 7, 0), (-3, 8, 0),
         (-2, -6, 0), (-2, -5, 1), (-2, -4, 0), (-2, -3, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 1), (-2, 1, 0), (-2, 2, 1), (-2, 3, 0), (-2, 4, 0), (-2, 5, 0), (-2, 6, 0), (-2, 7, 1), (-2, 8, 0),
         (-1, -6, 0), (-1, -5, 1), (-1, -4, 0), (-1, -3, 0), (-1, -2, 0), (-1, -1, 0), (-1, 0, 1), (-1, 1, 0), (-1, 2, 1), (-1, 3, 0), (-1, 4, 0), (-1, 5, 0), (-1, 6, 0), (-1, 7, 1), (-1, 8, 0),
         (0, -6, 0), (0, -5, 1), (0, -4, 0), (0, -3, 0), (0, -2, 0), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 1), (0, 3, 0), (0, 4, 0), (0, 5, 0), (0, 6, 0), (0, 7, 1), (0, 8, 0),
         (1, -6, 0), (1, -5, 0), (1, -4, 0), (1, -3, 1), (1, -2, 1), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 0), (1, 7, 0), (1, 8, 0),
         (2, -6, 0), (2, -5, 0), (2, -4, 0), (2, -3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0), (2, 5, 0), (2, 6, 0), (2, 7, 0), (2, 8, 0),
         (3, -6, 0), (3, -5, 0), (3, -4, 0), (3, -3, 1), (3, -2, 1), (3, -1, 1), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 1), (3, 4, 1), (3, 5, 1), (3, 6, 0), (3, 7, 0), (3, 8, 0),
         (4, -6, 0), (4, -5, 1), (4, -4, 0), (4, -3, 0), (4, -2, 0), (4, -1, 0), (4, 0, 1), (4, 1, 0), (4, 2, 1), (4, 3, 0), (4, 4, 0), (4, 5, 0), (4, 6, 0), (4, 7, 1), (4, 8, 0),
         (5, -6, 0), (5, -5, 1), (5, -4, 0), (5, -3, 0), (5, -2, 0), (5, -1, 0), (5, 0, 1), (5, 1, 0), (5, 2, 1), (5, 3, 0), (5, 4, 0), (5, 5, 0), (5, 6, 0), (5, 7, 1), (5, 8, 0),
         (6, -6, 0), (6, -5, 1), (6, -4, 0), (6, -3, 0), (6, -2, 0), (6, -1, 0), (6, 0, 1), (6, 1, 0), (6, 2, 1), (6, 3, 0), (6, 4, 0), (6, 5, 0), (6, 6, 0), (6, 7, 1), (6, 8, 0),
         (7, -6, 0), (7, -5, 0), (7, -4, 0), (7, -3, 0), (7, -2, 0), (7, -1, 0), (7, 0, 0), (7, 1, 0), (7, 2, 0), (7, 3, 0), (7, 4, 0), (7, 5, 0), (7, 6, 0), (7, 7, 0), (7, 8, 0),
         (8, -6, 0), (8, -5, 0), (8, -4, 0), (8, -3, 1), (8, -2, 1), (8, -1, 1), (8, 0, 0), (8, 1, 0), (8, 2, 0), (8, 3, 1), (8, 4, 1), (8, 5, 1), (8, 6, 0), (8, 7, 0), (8, 8, 0),
         (9, -6, 0), (9, -5, 0), (9, -4, 0), (9, -3, 0), (9, -2, 0), (9, -1, 0), (9, 0, 0), (9, 1, 0), (9, 2, 0), (9, 3, 0), (9, 4, 0), (9, 5, 0), (9, 6, 0), (9, 7, 0), (9, 8, 0)]
PULSAR2=[(-6, -7, 0), (-6, -6, 0), (-6, -5, 0), (-6, -4, 0), (-6, -3, 0), (-6, -2, 0), (-6, -1, 0), (-6, 0, 0), (-6, 1, 0), (-6, 2, 0), (-6, 3, 0), (-6, 4, 0), (-6, 5, 0), (-6, 6, 0), (-6, 7, 0), (-6, 8, 0), (-6, 9, 0),
         (-5, -7, 0), (-5, -6, 0), (-5, -5, 0), (-5, -4, 0), (-5, -3, 0), (-5, -2, 1), (-5, -1, 0), (-5, 0, 0), (-5, 1, 0), (-5, 2, 0), (-5, 3, 0), (-5, 4, 1), (-5, 5, 0), (-5, 6, 0), (-5, 7, 0), (-5, 8, 0), (-5, 9, 0),
         (-4, -7, 0), (-4, -6, 0), (-4, -5, 0), (-4, -4, 0), (-4, -3, 0), (-4, -2, 1), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-4, 4, 1), (-4, 5, 0), (-4, 6, 0), (-4, 7, 0), (-4, 8, 0), (-4, 9, 0),
         (-3, -7, 0), (-3, -6, 0), (-3, -5, 0), (-3, -4, 0), (-3, -3, 0), (-3, -2, 1), (-3, -1, 1), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 1), (-3, 4, 1), (-3, 5, 0), (-3, 6, 0), (-3, 7, 0), (-3, 8, 0), (-3, 9, 0),
         (-2, -7, 0), (-2, -6, 0), (-2, -5, 0), (-2, -4, 0), (-2, -3, 0), (-2, -2, 0), (-2, -1, 0), (-2, 0, 0), (-2, 1, 0), (-2, 2, 0), (-2, 3, 0), (-2, 4, 0), (-2, 5, 0), (-2, 6, 0), (-2, 7, 0), (-2, 8, 0), (-2, 9, 0),
         (-1, -7, 0), (-1, -6, 1), (-1, -5, 1), (-1, -4, 1), (-1, -3, 0), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (-1, 2, 1), (-1, 3, 1), (-1, 4, 0), (-1, 5, 0), (-1, 6, 1), (-1, 7, 1), (-1, 8, 1), (-1, 9, 0),
         (0, -7, 0), (0, -6, 0), (0, -5, 0), (0, -4, 1), (0, -3, 0), (0, -2, 1), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 1), (0, 3, 0), (0, 4, 1), (0, 5, 0), (0, 6, 1), (0, 7, 0), (0, 8, 0), (0, 9, 0),
         (1, -7, 0), (1, -6, 0), (1, -5, 0), (1, -4, 0), (1, -3, 0), (1, -2, 1), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 1), (1, 4, 1), (1, 5, 0), (1, 6, 0), (1, 7, 0), (1, 8, 0), (1, 9, 0),
         (2, -7, 0), (2, -6, 0), (2, -5, 0), (2, -4, 0), (2, -3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0), (2, 5, 0), (2, 6, 0), (2, 7, 0), (2, 8, 0), (2, 9, 0),
         (3, -7, 0), (3, -6, 0), (3, -5, 0), (3, -4, 0), (3, -3, 0), (3, -2, 1), (3, -1, 1), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 1), (3, 4, 1), (3, 5, 0), (3, 6, 0), (3, 7, 0), (3, 8, 0), (3, 9, 0),
         (4, -7, 0), (4, -6, 0), (4, -5, 0), (4, -4, 1), (4, -3, 0), (4, -2, 1), (4, -1, 0), (4, 0, 1), (4, 1, 0), (4, 2, 1), (4, 3, 0), (4, 4, 1), (4, 5, 0), (4, 6, 1), (4, 7, 0), (4, 8, 0), (4, 9, 0),
         (5, -7, 0), (5, -6, 1), (5, -5, 1), (5, -4, 1), (5, -3, 0), (5, -2, 0), (5, -1, 1), (5, 0, 1), (5, 1, 0), (5, 2, 1), (5, 3, 1), (5, 4, 0), (5, 5, 0), (5, 6, 1), (5, 7, 1), (5, 8, 1), (5, 9, 0),
         (6, -7, 0), (6, -6, 0), (6, -5, 0), (6, -4, 0), (6, -3, 0), (6, -2, 0), (6, -1, 0), (6, 0, 0), (6, 1, 0), (6, 2, 0), (6, 3, 0), (6, 4, 0), (6, 5, 0), (6, 6, 0), (6, 7, 0), (6, 8, 0), (6, 9, 0),
         (7, -7, 0), (7, -6, 0), (7, -5, 0), (7, -4, 0), (7, -3, 0), (7, -2, 1), (7, -1, 1), (7, 0, 0), (7, 1, 0), (7, 2, 0), (7, 3, 1), (7, 4, 1), (7, 5, 0), (7, 6, 0), (7, 7, 0), (7, 8, 0), (7, 9, 0),
         (8, -7, 0), (8, -6, 0), (8, -5, 0), (8, -4, 0), (8, -3, 0), (8, -2, 1), (8, -1, 0), (8, 0, 0), (8, 1, 0), (8, 2, 0), (8, 3, 0), (8, 4, 1), (8, 5, 0), (8, 6, 0), (8, 7, 0), (8, 8, 0), (8, 9, 0),
         (9, -7, 0), (9, -6, 0), (9, -5, 0), (9, -4, 0), (9, -3, 0), (9, -2, 1), (9, -1, 0), (9, 0, 0), (9, 1, 0), (9, 2, 0), (9, 3, 0), (9, 4, 1), (9, 5, 0), (9, 6, 0), (9, 7, 0), (9, 8, 0), (9, 9, 0),
         (10, -7, 0), (10, -6, 0), (10, -5, 0), (10, -4, 0), (10, -3, 0), (10, -2, 0), (10, -1, 0), (10, 0, 0), (10, 1, 0), (10, 2, 0), (10, 3, 0), (10, 4, 0), (10, 5, 0), (10, 6, 0), (10, 7, 0), (10, 8, 0), (10, 9, 0)]
PULSAR3=[(-5, -6, 0), (-5, -5, 0), (-5, -4, 0), (-5, -3, 0), (-5, -2, 0), (-5, -1, 0), (-5, 0, 0), (-5, 1, 0), (-5, 2, 0), (-5, 3, 0), (-5, 4, 0), (-5, 5, 0), (-5, 6, 0), (-5, 7, 0), (-5, 8, 0),
         (-4, -6, 0), (-4, -5, 0), (-4, -4, 0), (-4, -3, 1), (-4, -2, 1), (-4, -1, 0), (-4, 0, 0), (-4, 1, 0), (-4, 2, 0), (-4, 3, 0), (-4, 4, 1), (-4, 5, 1), (-4, 6, 0), (-4, 7, 0), (-4, 8, 0),
         (-3, -6, 0), (-3, -5, 0), (-3, -4, 0), (-3, -3, 0), (-3, -2, 1), (-3, -1, 1), (-3, 0, 0), (-3, 1, 0), (-3, 2, 0), (-3, 3, 1), (-3, 4, 1), (-3, 5, 0), (-3, 6, 0), (-3, 7, 0), (-3, 8, 0),
         (-2, -6, 0), (-2, -5, 1), (-2, -4, 0), (-2, -3, 0), (-2, -2, 1), (-2, -1, 0), (-2, 0, 1), (-2, 1, 0), (-2, 2, 1), (-2, 3, 0), (-2, 4, 1), (-2, 5, 0), (-2, 6, 0), (-2, 7, 1), (-2, 8, 0),
         (-1, -6, 0), (-1, -5, 1), (-1, -4, 1), (-1, -3, 1), (-1, -2, 0), (-1, -1, 1), (-1, 0, 1), (-1, 1, 0), (-1, 2, 1), (-1, 3, 1), (-1, 4, 0), (-1, 5, 1), (-1, 6, 1), (-1, 7, 1), (-1, 8, 0),
         (0, -6, 0), (0, -5, 0), (0, -4, 1), (0, -3, 0), (0, -2, 1), (0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 2, 1), (0, 3, 0), (0, 4, 1), (0, 5, 0), (0, 6, 1), (0, 7, 0), (0, 8, 0),
         (1, -6, 0), (1, -5, 0), (1, -4, 0), (1, -3, 1), (1, -2, 1), (1, -1, 1), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 0), (1, 7, 0), (1, 8, 0),
         (2, -6, 0), (2, -5, 0), (2, -4, 0), (2, -3, 0), (2, -2, 0), (2, -1, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0), (2, 5, 0), (2, 6, 0), (2, 7, 0), (2, 8, 0),
         (3, -6, 0), (3, -5, 0), (3, -4, 0), (3, -3, 1), (3, -2, 1), (3, -1, 1), (3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 1), (3, 4, 1), (3, 5, 1), (3, 6, 0), (3, 7, 0), (3, 8, 0),
         (4, -6, 0), (4, -5, 0), (4, -4, 1), (4, -3, 0), (4, -2, 1), (4, -1, 0), (4, 0, 1), (4, 1, 0), (4, 2, 1), (4, 3, 0), (4, 4, 1), (4, 5, 0), (4, 6, 1), (4, 7, 0), (4, 8, 0),
         (5, -6, 0), (5, -5, 1), (5, -4, 1), (5, -3, 1), (5, -2, 0), (5, -1, 1), (5, 0, 1), (5, 1, 0), (5, 2, 1), (5, 3, 1), (5, 4, 0), (5, 5, 1), (5, 6, 1), (5, 7, 1), (5, 8, 0),
         (6, -6, 0), (6, -5, 1), (6, -4, 0), (6, -3, 0), (6, -2, 1), (6, -1, 0), (6, 0, 1), (6, 1, 0), (6, 2, 1), (6, 3, 0), (6, 4, 1), (6, 5, 0), (6, 6, 0), (6, 7, 1), (6, 8, 0),
         (7, -6, 0), (7, -5, 0), (7, -4, 0), (7, -3, 0), (7, -2, 1), (7, -1, 1), (7, 0, 0), (7, 1, 0), (7, 2, 0), (7, 3, 1), (7, 4, 1), (7, 5, 0), (7, 6, 0), (7, 7, 0), (7, 8, 0),
         (8, -6, 0), (8, -5, 0), (8, -4, 0), (8, -3, 1), (8, -2, 1), (8, -1, 0), (8, 0, 0), (8, 1, 0), (8, 2, 0), (8, 3, 0), (8, 4, 1), (8, 5, 1), (8, 6, 0), (8, 7, 0), (8, 8, 0),
         (9, -6, 0), (9, -5, 0), (9, -4, 0), (9, -3, 0), (9, -2, 0), (9, -1, 0), (9, 0, 0), (9, 1, 0), (9, 2, 0), (9, 3, 0), (9, 4, 0), (9, 5, 0), (9, 6, 0), (9, 7, 0), (9, 8, 0)]


SHAPES=[(BLOCK,'red'),
        (BLINKER1,'orange'),(BLINKER2,'orange'),
        (BOAT1,'yellow'),(BOAT2,'yellow'),(BOAT3,'yellow'),(BOAT4,'yellow'),
        (GLIDER11,'blue'),(GLIDER12,'blue'),(GLIDER13,'blue'),(GLIDER14,'blue'),
        (GLIDER21,'blue'),(GLIDER22,'blue'),(GLIDER23,'blue'),(GLIDER24,'blue'),
        (GLIDER31,'blue'),(GLIDER32,'blue'),(GLIDER33,'blue'),(GLIDER34,'blue'),
        (GLIDER41,'blue'),(GLIDER42,'blue'),(GLIDER43,'blue'),(GLIDER44,'blue'),
        (TOAD1,'green'),(TOAD2,'green'),(TOAD3, 'green'), (TOAD4, 'green'),
        (TOAD5, 'green'), (TOAD6, 'green'), (TOAD7, 'green'), (TOAD8, 'green'),
        (LAND1, 'cyan'),(LAND2, 'cyan'),
        (LWSS1, 'maroon'), (LWSS2, 'maroon'), (LWSS3, 'maroon'), (LWSS4, 'maroon'),
        (LWSS5, 'maroon'), (LWSS6, 'maroon'), (LWSS7, 'maroon'), (LWSS8, 'maroon'),
        (LWSS9, 'maroon'), (LWSS10, 'maroon'), (LWSS11, 'maroon'), (LWSS12, 'maroon'),
        (LWSS13, 'maroon'), (LWSS14, 'maroon'),
        (PULSAR1, 'red'), (PULSAR2, 'green'), (PULSAR3, 'blue'),]


help_string="""Game Of Life

How to play:

By clicking the left mouse button you place a cell on the board.

By clicking the right mouse button you kill a cell already on the board.

You can change the rules by which the new generations are calculated by typing the corresponding numbers after clicking the corresponding buttons.

You can change the speed of the game by clicking the "Speed" button.

You can turn on and off placing new cells while the game is running by clicking the "Live clicking" button.

You can turn on colouring of the basic shapes by clicking the "Colouring" button.

WARNING!!! Colouring is very CPU intensive because my code is crappy."""



if __name__ == "__main__":            
    Game() 
