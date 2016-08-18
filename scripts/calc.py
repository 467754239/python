#coding:gbk

from Tkinter import *  
  
#���������Ϳ��  
def frame(root, side):  
    w = Frame(root)  
    w.pack(side = side, expand = YES, fill = BOTH)  
    return w  
#������ť  
def button(root, side, text, command = None):  
    w = Button(root, text = text, command = command)  
    w.pack(side = side, expand = YES, fill = BOTH)  
    return w  
#�̳���Frame�࣬��ʼ���������Ĳ���  
class Calculator(Frame):  
    def __init__(self):  
          
        Frame.__init__(self)  
          
        self.pack(expand = YES, fill = BOTH)  
        self.master.title('Simple Calculater')  
          
        display = StringVar()  
        #��������  
        Entry(self, relief = SUNKEN,  
              textvariable = display).pack(side = TOP, expand = YES,  
                                           fill = BOTH)  
        #��Ӻ����Ϳ���Լ�����İ�ť  
        for key in('123', '456', '789', '-0.'):  
            keyF = frame(self, TOP)  
            for char in key:  
                button(keyF, LEFT, char, lambda w = display, c = char:w.set(w.get() + c))  
        #��Ӳ�������ť  
        opsF = frame(self, TOP)  
        for char in '+-*/=':  
            if char == '=':  
                btn = button(opsF, LEFT, char)  
                btn.bind('<ButtonRelease - 1>', lambda e, s = self, w = display:s.calc(w), '+')  
  
            else:  
                btn = button(opsF, LEFT, char, lambda w = display, s = '%s' %char:w.set(w.get() + s))  
        #��������ť  
        clearF = frame(self, BOTTOM)  
        button(clearF, LEFT, 'clear', lambda w = display:w.set(''))  
  
    #����eval����������ʽ��ֵ  
    def calc(self, display):  
        try:  
            display.set(eval(display.get()))  
        except:  
            display.set("ERROR")  
#��������  
if __name__ == '__main__':  
    print('ok')  
    Calculator().mainloop()  