from tkinter import *
from random import randint

class Saper:

  def __init__(self):
    self.root = Tk()
    self.root.geometry("288x218")
    self.root.update_idletasks()
    size_width = self.root.winfo_width()
    size_height = self.root.winfo_height()
    self.root.minsize(size_width,size_height)
    self.root.maxsize(size_width,size_height)
    self.root.title("Minesweeper")
    self.draw_board()
    self.root.mainloop()


  def draw_board(self):
      self.ui = Frame(self.root)
      self.ui.grid()
      self.flags = 10
      self.flags_counter = Label(self.ui,text=str(self.flags))
      self.flags_counter.grid(row=0,column=0)
      self.Face = Button(self.ui, text=":)", width=10,command=lambda:self.restart())
      self.Face.grid(row=0,column=1)
      self.Frame = Frame(self.root)
      self.Frame.grid()
      self.alive = True
      self.win = False
      self.generate_buttons()


  def generate_buttons(self):
      self.buttons = []
      self.clicked = []
      self.defused = []
      self.first_click = False
      i = 0
      for r in range(8):
          for c in range(8):
                  x = Button(self.Frame, borderwidth=1,width=4,command=lambda j=i:self.button_action(j),disabledforeground="black")
                  x.grid(row=r, column=c)
                  x.bind('<Button-3>',lambda k,z=i:self.left(z))
                  #x.config(text=str(i))
                  i += 1
                  self.buttons.append(x)

  def left(self,id):
   if self.alive == True and self.win == False and self.first_click == True:
     if not(id in self.clicked):
       button = self.buttons[id]
       if button["state"] == NORMAL  and self.flags>0:
          button["state"] = DISABLED
          button.config(text="F")
          self.defused.append(id)
          self.flags -= 1
       elif button["state"] == DISABLED:
          button["state"] = NORMAL
          button.config(text="")
          self.flags += 1
          for i in range(len(self.defused)):
              if self.defused[i] == id:
                  del self.defused[i]
                  break
     self.flags_counter.config(text=str(self.flags))

  def button_action(self,id):
      #first click
      if self.first_click == False:
          self.generate_mines(id)
          self.generate_numbers()
          self.check_number(id)
      else:
      #after first click
       if self.alive:
           #mine pick
           if id in self.mines:
               self.bad_pick(id)
           #good pick
           else:
               self.check_number(id)
       self.check_win()

  def generate_mines(self,first):
      self.first_click = True
      self.mines=[]
      while(len(self.mines) <= 9):
          x = randint(0,63)
          if not(x in self.mines) and x != first:
              self.mines.append(x)
              #self.buttons[x].config(text="X")
      self.mines.sort()
      print(self.mines)

  def restart(self):
      if self.alive == False or self.win == True:
          self.Frame.destroy()
          self.ui.destroy()
          self.draw_board()

  def check_win(self):
      if self.alive == True and len(self.clicked) == 54:
          self.win=True
          self.disable_all_buttons()
          self.Face.config(text=":D")
          self.check_defused()

  def disable_all_buttons(self):
      for buttons in self.buttons:
          buttons["state"]=DISABLED

#hardest part
  def generate_numbers(self):
      #directionery to save what buttons has which number
      self.numbers = {}
      #walls tables to not check if numbers has one if is not on far left/right
      self.right_wall = []
      self.left_wall = []
      for i in range(7, 64, 8):
          self.right_wall.append(i)
      for i in range(0, 57, 8):
          self.left_wall.append(i)
      for button in range(len(self.buttons)):
          if not(button in self.mines):
              number = 0
              #integers to check if mine is in same row as number
              row_min=0
              row_max=7
              while(True):
                  if button >= row_min and button <= row_max:
                      break
                  else:
                      row_min+=8
                      row_max+=8
              #left side numbers
              if button-1 in self.mines and (button-1 >= row_min and button-1 <= row_max):
                            number+=1
              #right side_numbers
              if button+1 in self.mines and (button+1 >= row_min and button+1 <= row_max):
                            number+=1
              #up numbers
              if button + 8 in self.mines:
                      number += 1
              #down number

              if button - 8 in self.mines:
                      number+=1
              #sideways numbers
              #right
              if not(button in self.right_wall):
                  if button+9 in self.mines:
                      number+=1
                  if button - 7 in self.mines:
                      number += 1
              #left
              if not (button in self.left_wall):
                  if button-9 in self.mines:
                      number+=1
                  if button + 7 in self.mines:
                      number += 1
              #add numbers to dictionery
              if number != 0:
                  self.numbers[button] = number

  def set_number(self,id):
      self.buttons[id].config(text=str(self.numbers[id]))

  def check_number(self,id):
      self.good_pick(id)
      if not(id in self.mines) and not(id in self.numbers):
          self.show_hidden(id)

  def show_hidden(self,id):
      empty = []
      empty.append(id)
      for emp in empty:
          self.show_hidden_operation_minus(emp,1,self.left_wall,empty)
          self.show_hidden_operation_plus(emp,1,self.right_wall,empty)
          self.show_hidden_operation_minus(emp, 7, self.right_wall, empty)
          self.show_hidden_operation_plus(emp, 7, self.left_wall, empty)
          self.show_hidden_operation_plus(emp, 9, self.right_wall, empty)
          self.show_hidden_operation_minus(emp, 9, self.left_wall, empty)
          self.show_hidden_operation_minus(emp,8,[-2], empty)
          self.show_hidden_operation_plus(emp, 8, [-2], empty)
      print(empty)
      if len(empty) > 0:
       for id in empty:
           self.shower_minus(id, 1, self.left_wall)
           self.shower_minus(id, 7, self.right_wall)
           self.shower_minus(id, 9, self.left_wall)
           self.shower_minus(id, 8, [-2])
           self.shower_plus(id, 1, self.right_wall)
           self.shower_plus(id, 7, self.left_wall)
           self.shower_plus(id, 9, self.right_wall)
           self.shower_plus(id, 8, [-2])

  def show_hidden_operation_minus(self,emp,step,wall,empty):
      if not (emp - step in self.mines) and not (emp - step in self.numbers) and emp-step >= 0 and not (emp - step in empty):
          self.good_pick(emp)
          if not (emp in wall):
              empty.append(emp - step)

  def show_hidden_operation_plus(self,emp,step,wall,empty):
      if not (emp + step in self.mines) and not (emp + step in self.numbers) and emp+step <= 63 and not (emp + step in empty):
          self.good_pick(emp)
          if not (emp in wall):
              empty.append(emp + step)

  def shower_minus(self,id,step,wall):
      if not(id - step in self.mines) and not(id in wall) and id - step >=0:
          self.good_pick(id-step)
      elif not (id - step in self.mines) and id in wall and id - step >= 0:
              self.good_pick(id)

  def shower_plus(self,id,step,wall):
      if not(id + step in self.mines) and not(id in wall) and id + step <= 63:
          self.good_pick(id+step)
      elif not (id + step in self.mines) and id in wall and id + step <= 63:
              self.good_pick(id)


  def good_pick(self,id):
    if not id in self.clicked:
      if id in self.numbers:
          self.set_number(id)
      button=self.buttons[id]
      button.config(bg="gray")
      button["state"]=DISABLED
      self.clicked.append(id)

  def bad_pick(self,id):
      self.buttons[id].config(text="X")
      self.buttons[id].config(bg="red")
      for mine in self.mines:
          button = self.buttons[mine]
          if button["state"] != DISABLED:
              button.config(text="X")
      self.disable_all_buttons()
      self.alive = False
      self.Face.config(text=":(")
      self.check_defused()

  def check_defused(self):
      for mine in self.mines:
          if mine in self.defused:
              self.buttons[mine].config(text="R")
#############################################
Saper()




