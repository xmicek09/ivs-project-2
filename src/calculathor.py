# -*- coding: utf-8 -*-
"""Kalkukačka
IVS Project 2

Authors:
    Patrik Demský xdemsk00
    Richard Míček xmicek09

Date:
    20.4.2020
"""
from tkinter import *
import math_lib as math

err_msg = "Syntax ERROR"

def is_integer(value):
    """Checks if string is convertible to integer

    Returns:
        bool: Can/Can't be converted
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    """Checks if string is convertible to float

    Returns:
        bool: Can/Can't be converted
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def replace_ternary(result, temp, i):
    """Replaces part of the equation with the result"""
    del result[i-1]
    del result[i-1]
    del result[i-1]
    result.insert(i-1, str(temp))

def replace_binary(result, temp, i):
    """Replaces part of the equation with the result"""
    del result[i]
    del result[i]
    result.insert(i, str(temp))

def set_err_msg(result, err_msg):
    """Sets error message"""
    result.clear()
    result.append(err_msg)

def low_priority_op(result, temp, i):
    """Calculating low priority operations

    Returns:
        int: Counter
    """
    if result[i] == '+':
        if result[i+1] == '-':
            replace_binary(result, result[i+1], i)
        elif (i-1) < 0 and is_float(result[i+1]):
            result.remove(result[i]) 
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.add(float(result[i-1]), float(result[i+1]))
            replace_ternary(result, temp, i)
            i -= 1
        elif not is_float(result[i-1]) or not is_float(result[i+1]):
            set_err_msg(result, err_msg)
            return 0

    if result[i] == '-':
        if result[i+1] == '+':
            replace_binary(result, result[i], i)
            if (i-1) < 0: 
                return 0
            else:
                return i
        elif (i-1) < 0 and is_float(result[i+1]):
            temp = - float(result[i+1])
            replace_binary(result, temp, i)
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.sub(float(result[i-1]), float(result[i+1]))
            replace_ternary(result, temp, i)
            i -= 1
        elif not is_float(result[i-1]) or not is_float(result[i+1]):
            set_err_msg(result, err_msg)
            return 0

    return (i + 1)

def mid_priority_op(result, temp, i):
    """Calculating middle priority operations

    Returns:
        int: Counter
    """
    if result[i] == '*':
        if (i-1) < 0 :
            set_err_msg(result, err_msg)
            return 0 
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.mul(float(result[i-1]), float(result[i+1]))
            replace_ternary(result, temp, i)
            i -= 1
        elif not is_float(result[i-1]) or not is_float(result[i+1]):
            set_err_msg(result, err_msg)
            return 0
            
    if result[i] == '/':
        if (i-1) < 0:
            set_err_msg(result, err_msg)
            return 0 
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.div(float(result[i-1]), float(result[i+1]))
            replace_ternary(result, temp, i)
            i -= 1
        elif not is_float(result[i-1]) or not is_float(result[i+1]):
            set_err_msg(result, err_msg)
            return 0 
    return (i + 1)

def high_priority_op(result, temp, i):
    """Calculating high priority operations

    Returns:
        int: Counter
    """
    if result[i] == '^':
        if (i-1) < 0 :
            set_err_msg(result, err_msg)
            return 0 
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.exp(float(result[i-1]), float(result[i+1]))
            replace_ternary(result, temp, i)
            i -= 1
        elif not is_float(result[i-1]) or not is_float(result[i+1]):
            set_err_msg(result, err_msg)
            return 0
            
    if result[i] == '√':
        if ((i-1) < 0 or not is_float(result[i-1])) and is_float(result[i+1]):
            temp = math.ext(float(result[i+1]), 2)
            replace_binary(result, temp, i)
            i -= 1
        elif is_float(result[i-1]) and is_float(result[i+1]):
            temp = math.ext(float(result[i+1]), float(result[i-1]))
            replace_ternary(result, temp, i)
            i -= 1
        else:
            set_err_msg(result, err_msg)
            return 0 
    return (i + 1)

def highest_priority_op(result, temp, i):
    if result[i] == '-':
        if ((i-1) < 0 or not is_float(result[i-1])) and is_float(result[i+1]):
            temp = - float(result[i+1])
            replace_binary(result, temp, i)
    if result[i] == '!':
        if is_integer(result[i+1]) and int(result[i+1]) >= 0:
            temp = math.fact(int(result[i+1]))
            replace_binary(result, temp, i)
            i -= 1
        elif not is_integer(result[i+1]) or int(result[i+1]) < 0:
            set_err_msg(result, err_msg)
            return 0 
    return (i + 1)

def calculate(result):
    """Performs the calculation of the equation

    Returns:
        string: Result of equation
    """
    temp = 0
    i = 0
    result = result.split()
    # Going through each member of the list to check for signs
    if len(result) <= 1:
        result.clear()
        return result
    while(len(result) > 1):
        while(result.count('!') != 0 or result.count('-') != 0) and i < len(result):
            i = highest_priority_op(result, temp, i)
        else:
            i = 0
        while(result.count('^') != 0 or result.count('√') != 0):
            i = high_priority_op(result, temp, i)
        else:
            i = 0
        while(result.count('*') != 0 or result.count('/') != 0):
            i = mid_priority_op(result, temp, i)
        else:
            i = 0
        while(result.count('+') != 0 or result.count('-') != 0):
            i = low_priority_op(result, temp, i)
        else:
            i = 0

    return result[0]   

class Calculator:
    """Calculator class, holds the entire gui code"""
    def __init__(self, master):
        self.master = master
        master.title("CalculaThor")

        # text screen
        self.screen = Text(master, state='disabled', width=32, height=5, border = 1, background="light grey", foreground="black")

        # position screen in window
        self.screen.grid(row=0,column=0,columnspan=4,padx=5,pady=5)
        self.screen.configure(state='normal')

        # create buttons using method createButton
        button1 = Button(root,text='1',width=8, height=2, command=lambda: self.buttonClick('1'))
        button2 = Button(root,text='2',width=8, height=2, command=lambda: self.buttonClick('2'))
        button3 = Button(root,text='3',width=8, height=2, command=lambda: self.buttonClick('3'))
        button4 = Button(root,text='4',width=8, height=2, command=lambda: self.buttonClick('4'))
        button5 = Button(root,text='5',width=8, height=2, command=lambda: self.buttonClick('5'))
        button6 = Button(root,text='6',width=8, height=2, command=lambda: self.buttonClick('6'))
        button7 = Button(root,text='7',width=8, height=2, command=lambda: self.buttonClick('7'))
        button8 = Button(root,text='8',width=8, height=2, command=lambda: self.buttonClick('8'))
        button9 = Button(root,text='9',width=8, height=2, command=lambda: self.buttonClick('9'))
        button10 = Button(root,text='0',width=18, height=2, command=lambda: self.buttonClick('0'))  
        button11 = Button(root,text='.',width=8, height=2, command=lambda: self.buttonClick('.'))
        button12 = Button(root,text='+',width=8, height=2, background='orange', command=lambda: self.buttonClick(' + '))
        button13 = Button(root,text='-',width=8, height=2, background='orange', command=lambda: self.buttonClick(' - '))
        button14 = Button(root,text='*',width=8, height=2, command=lambda: self.buttonClick(' * '))
        button15 = Button(root,text='/',width=8, height=2, command=lambda: self.buttonClick(' / '))
        button16 = Button(root,text='=',width=8, height=5, background='orange', command=lambda: self.buttonClick('eq'))
        button17 = Button(root,text='|x|',width=8, height=2, command=lambda: self.buttonClick('abs'))  
        button18 = Button(root,text='^',width=8, height=2, command=lambda: self.buttonClick(' ^ '))
        button19 = Button(root,text='√',width=8, height=2, command=lambda: self.buttonClick(' √ '))
        button20 = Button(root,text='AC',width=8, height=2, background='orange', command=lambda: self.clear())
        button21 = Button(root,text='DEL',width=8, height=2, background='orange', command=lambda: self.buttonClick('del'))
        button22 = Button(root,text='!',width=8, height=2, command=lambda: self.buttonClick(' ! '))

        # buttons stored in list
        buttons = [button17,button18,button19,button20,button22,button14,button15,button21,button7,button8,button9,button12,
        button4,button5,button6,button13,button1,button2,button3,button10,button11,button16]

        # intialize counter
        count = 0
        # arrange buttons with grid manager
        for row in range(1,6): #rows
            for column in range(4): #column
                buttons[count].grid(row=row,column=column)
                count += 1
        #arrange last line
        # arrange "0"
        buttons[19].grid(row=6,column=0,columnspan=2)
        #arrange ","
        buttons[20].grid(row=6,column=2)
        #arrange "="
        buttons[21].grid(row=5,column=3,rowspan=2)
    
    def clear(self):
        """Method to clear the screen"""
        self.screen.delete("1.0", END)

    def screen_del(self):
        """Function decides whether to delete one or three characters depending on the last character on screen"""
        scr_text = self.screen.get("1.0", END)
        scr_text = scr_text.split()
        if(is_float(scr_text[len(scr_text)-1]) or is_integer(scr_text[len(scr_text)-1])):
            self.screen.delete("end-2c", END)
        else:
            self.screen.delete("end-4c", END)

    def createButton(self,val,write=True,width=5):
        """This function creates a button, and takes one compulsory argument, the value that should be on the button"""
        return Button(self.master, text=val,command = lambda: self.click(val,write), width=8, height = 2)

    def buttonClick(self,butt_type):
        """Checks the button type, if it's a number or operand it gets typed out into the text box, otherwise function calls occur
        """
        equation = self.screen.get("1.0", END)  
        if butt_type == 'del':
            self.screen_del()
        elif butt_type == 'eq':        
            if is_float(equation[len(equation)-2]) or is_integer(equation[len(equation)-1]):
                self.clear()
                result = calculate(equation)
                self.screen.insert(END, result)
        elif butt_type == 'abs':
            temp = equation.split()
            if len(temp) == 2 and temp[0] == '-' and is_float(temp[1]): 
                result = float(temp[1])
                result = str(math.abs(result))
                self.clear()
                self.screen.insert(END, result)
            elif len(temp) == 1 and equation[0] == '-':
                result = float(equation)
                result = str(math.abs(result))
                self.clear()
                self.screen.insert(END, result)
        else:
            self.screen.insert(END, butt_type)
        
        
"""End of Calculator class
"""

root = Tk()
root.geometry("269x342")
my_gui = Calculator(root)
root.resizable(width=False, height=False)

root.mainloop()
