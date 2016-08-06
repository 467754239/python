## 
> 状态机示例

```python
#coding:utf-8

import random
from time import sleep

class Car(object):
    def stop(self):
        print "Stop!!!"
 
    def go(self):
        print "Goooooo!!!"
              
    def attach_fsm(self, state, fsm):
        # state 0
        # fsm = stop_fsm()
        self.curr_state = state    
        self.fsm = fsm

    def change_state(self, new_state, new_fsm):
        self.curr_state = new_state
        self.fsm.exit_state(self)
        self.fsm = new_fsm
        self.fsm.enter_state(self)
        self.fsm.exec_state(self)   

    def keep_state(self):
        self.fsm.exec_state(self)              
              
class base_fsm(object):
    def enter_state(self, obj):
        raise NotImplementedError()
    
    def exec_state(self, obj):
        raise NotImplementedError()
    
    def exit_state(self, obj):
        raise NotImplementedError()              

class stop_fsm(base_fsm):
    def enter_state(self, obj):
        print "Car%s enter stop state!"%(id(obj))
 
    def exec_state(self, obj):
        print "Car%s in stop state!"%(id(obj))
        obj.stop()
 
    def exit_state(self, obj):
        print "Car%s exit stop state!"%(id(obj))
              
              
class run_fsm(base_fsm):
    def enter_state(self, obj):
        print "Car%s enter run state!"%(id(obj))
 
    def exec_state(self, obj):
        print "Car%s in run state!"%(id(obj))
        obj.go()
 
    def exit_state(self, obj):
        print "Car%s exit run state!"%(id(obj))              
              
class fsm_mgr(object):
    def __init__(self):
        self._fsms = {}
        self._fsms[0] = stop_fsm()
        self._fsms[1] = run_fsm()
    
    def get_fsm(self, state):
        return self._fsms[state]
    
    def frame(self, objs, state):
        # state 0 or 1
        for obj in objs:
            if state == obj.curr_state:
                obj.keep_state()
            else:
                obj.change_state(state, self._fsms[state])

class World(object):
    def init(self):
        self._cars = []
        self._fsm_mgr = fsm_mgr()
        self.__init_car()
 
    def __init_car(self):
        for i in xrange(1):   # 生产汽车
            tmp = Car()
            tmp.attach_fsm(0, self._fsm_mgr.get_fsm(0))
            self._cars.append(tmp)
 
    def __frame(self):
        self._fsm_mgr.frame(self._cars, state_factory())
 
    def run(self):
        while True:
            print '_cars:%s', self._cars
            self.__frame()
            sleep(3)

def state_factory():
    return random.randint(0, 1)

if __name__ == "__main__":
       world = World()
       world.init()
       world.run()
```
