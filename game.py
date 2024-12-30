from tkinter import *
import random


class Function():
    
    def __init__(self, canvas, item):
        self.canvas = canvas 
        # intialize canvas object to use in the who program
        self.item = item
         # intialize the object which would interact with the ball
    
    def get_position(self): 
        # position of objects
        return self.canvas.coords(self.item)

    def move(self, x, y):
         # movement
        self.canvas.move(self.item, x, y)

    def delete(self): 
        # removing the object
        self.canvas.delete(self.item)


class Paddle(Function):
    def __init__(self, canvas, x, y):
        self.width = 40 # width of the paddle
        self.height = 5 # height of the paddle
        self.ball = None 

       
        paddle_object = canvas.create_rectangle(x - self.width , y - self.height ,x + self.width ,y + self.height ,fill='cyan')
        # creating paddle instance that will be called later
        Function.__init__(self, canvas, paddle_object) # inheritance

    def set_ball(self, ball): 
        # getting the position of the ball to set at the top of the paddle
        self.ball = ball
    
    def move(self, offset):
         # creating bounds for the paddle so it dosen't go off limit i.e got into the walls
        coords = self.get_position()
        width = self.canvas.winfo_width() 
        if coords[0] + offset >= 0 and coords[2] + offset <= width: 
            Function.move(self, offset, 0) 
            if self.ball is not None: 
                self.ball.move(offset, 0) 
                 # Moving the ball with the paddle

    def cheat(self , x): # cheat code
        self.height = x
        print(self.height)


class Block(Function): 
    COLORS = {1: 'green', 2: 'yellow', 3: 'red'} # storing color in respect to hits the blocks get gets

    def __init__(self, canvas, x, y, hits): 
     
        self.width = 33 # width of the block
        self.height = 10 # height of the block
        self.hits = hits 
        color = Block.COLORS[hits]  # setting the color same as the number of hits

        item = canvas.create_oval(x - self.width,   y - self.height,   x + self.width,   y + self.height,fill=color, tags='brick')
      
        Function.__init__(self, canvas, item) 

    def hit(self): 
        self.hits -= 1 
        # subracting the hits from the number of hits 
        if self.hits == 0: 
            self.delete()
             # deleting the block if the hits left are 0
        else:
            self.canvas.itemconfig(self.item, fill=Block.COLORS[self.hits])
             # else changing the color mentioned
    

class Ball(Function):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1] # setting the intial direction to right and up
        self.speed = 15
        item = canvas.create_oval(x - self.radius, y - self.radius,  x + self.radius, y + self.radius, fill='white')
       
        Function.__init__(self, canvas, item)
    def update(self):
        ball_coords = self.get_position()
        width = self.canvas.winfo_width()
        if ball_coords[0] <= 0 or ball_coords[2] >= width:
            self.direction[0] *= -1 
             # reverse x vector
        if ball_coords[1] <= 0:
            self.direction[1] *= -1 
             # reverse y vector
        x = self.direction[0] * self.speed 
         # scale by Ball's speed
        y = self.direction[1] * self.speed
        self.move(x, y)  # inherited method

    def collision_detection(self, removable_objects):
        ball_coords = self.get_position()
        ball_center_x = (ball_coords[0] + ball_coords[2]) * 0.5 
         # same as / 2
        if len(removable_objects) > 1:  
            # when collided with two of the blocks then flip the y axis
            self.direction[1] *= -1
        elif len(removable_objects) == 1: 
             # if not two collisions then do more 
            game_object = removable_objects[0]
            coords = game_object.get_position()
            if ball_center_x > coords[2]:
                self.direction[0] = 1
            elif ball_center_x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        # Do below regardless of how many collisions came in
        for game_object in removable_objects:
            if isinstance(game_object, Block):
                game_object.hit() 
                 # decrease the number of hits the object can take and if its zero then delete it.


class Game(Frame): 
    # inheriting Frame as a parent class
    def __init__(self, master): 
        Frame.__init__(self, master)
         # inhertance
        self.score = 100 
        # scores given to each player at the starting of the game
        self.width = 1280 
        self.height = 720 

        self.canvas = Canvas(self, bg='Black', width=self.width,   height=self.height)
         # making the canvas


        self.canvas.pack() 
        # placing the canvas on the screen
        self.pack() 
        self.objects = {} 
        # all the items that can collide with the ball i.e paddle and blocks
        self.ball_object = None
        self._paddle_y_start = 650 
        self.paddle = Paddle(self.canvas, self.width / 2, self._paddle_y_start)
         # making a paddle

        self.objects[self.paddle.item] = self.paddle 
        # adding the paddle to the canvas
        for x in range(5, self.width - 5, 80): 
            self.add_block(x + 37.5, 50, 3) 
            self.add_block(x + 37.5, 70, 2)
            self.add_block(x + 37.5, 90, 3)
            self.add_block(x + 37.5 ,110 , 1)

        self.hurt = None
         # setting the text on the screen as None
        self.setup_game() 
        self.canvas.focus_set() 
         # set focus on canvas 

      
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-15)) and self.canvas.bind('a', lambda _: self.paddle.move(-15))
        # binding two keys with funtion move to move the paddle to the left of the canvas
        self.canvas.bind('<Right>', lambda _: self.paddle.move(15)) and self.canvas.bind('d', lambda _: self.paddle.move(15))
        # binding two keys with function move to move the paddle to the right of the canvas
        

    def setup_game(self):
     
        self.add_ball() 
        self.setup_text()
        self.text = self.write_text(600, 200, "Press Spacebar")
        self.canvas.bind('<space>', lambda _: self.flag_start())
         # binding the pause button at the start of the game
        self.canvas.bind('<c>', lambda _: self.cheat_code1()) 
        self.canvas.bind('<Down>', lambda _: self.cheat_code2())
        self.canvas.bind('<h>' , lambda _: self.add_another_line())
        

    def add_ball(self): 
        if self.ball_object is not None: 
            self.ball_object.delete() 
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
         # finding the center of the paddle
        self.ball_object = Ball(self.canvas, x, 630) 
        self.paddle.set_ball(self.ball_object) 
         # store reference to it

    def add_block(self, x, y, hits): # add block function
        block = Block(self.canvas, x, y, hits)
        self.objects[block.item] = block
         # block item is the unique id which is it for each block on the screen

    def write_text(self, x, y, text, size='80'):
         # function that controls all the text placement on the canvas
        font = ('Helvetica', size) 
        return self.canvas.create_text(x, y, text=text, font=font , fill="white") 
        # returing the value as written text from function

    def setup_text(self):# calling the function to setup text
        text = "Scores: {}".format(self.score)
        if self.hurt is None:
            self.hurt = self.write_text(650 , 20, text, 15)
        else:
            self.canvas.itemconfig(self.hurt, text=text)
    
    def cheat_code1(self): 
        # function for cheatcode  1
        self.score += 30

    def cheat_code2(self):
        # function for cheatcode 2
        self.score -= 60


    def flag_start(self): 
        # initial start of the game
        self.canvas.unbind('<space>') 
        # unbinding the space event so the game dosen't start itself
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.main_loop()
        self.canvas.bind('<l>', lambda _: self.add_another_line())

    def main_loop(self):
        self.check_collisions() # checking for collision
        bricks_left = len(self.canvas.find_withtag('brick'))
        if bricks_left == 0:
            self.ball_object.speed = None
            self.write_text(300, 200, "You've won!")
             # if there are not any bricks left on the screen then you have won the game
        elif self.ball_object.get_position()[3] >= self.height:
            self.ball_object.speed = None
            self.score -= random.randint(40 , 50) 
            if self.score < 30:
                 # decrementing the score/life
                self.write_text(600, 340, "Game Over")
                self.write_in_file()
            else:
                self.after(1000, self.setup_game)
                 # resetting the game if the player has still score/life left
        else:
            self.ball_object.update() 
            # updating the position of the ball object
            self.after(50, self.main_loop) 

    def check_collisions(self):  
        # checking for the collisions
        ball_coords = self.ball_object.get_position()
        objects = self.canvas.find_overlapping(*ball_coords) 
        collisions_obj = [self.objects[x] for x in objects if x in self.objects]
         # only checking the objects that are in the objects dictionary
        self.ball_object.collision_detection(collisions_obj)
    
    def write_in_file(self): 
        # writing the score left after the game in the file
        file = open("leaderboard.txt" , "a")
        file.write(str(self.score) + "\n")
        file.close()

    def add_another_line(self):
         # Cheatcode for increasing the row for blocks
        for x in range(5, self.width - 5, 80):
            self.add_block(x + 37.5, 50, 3)
