import streamlit as st
import time
import datetime


class View:
    def __init__(self, controller, model):
        self.remain_time = 60
        self.run = False
        self.controller = controller
        self.model = model
        self.model.register_observer(self)
    
    def countdown(self):
        ph = st.empty()
        while self.run:
            self.update_remain_time()
            start_time = time.time() 
            ph.metric("Countdown", self.remain_time)
            self.controller.decrease_remain_time()
            time.sleep(1 - time.time()-start_time)
    
    def update_remain_time(self):
        self.remain_time = self.model.get_remain_time()
    
    def get_time_from_user(self):
        if st.button('+1'):
            self.controller.increase_remain_time()
        
        if st.button("-1"):
            self.controller.decrease_remain_time()
        
        remain_time = int(st.text_input('Movie title', self.remain_time))
        self.controller.set_remain_time(remain_time)
        self.remain_time = self.model.get_remain_time()
        
    def display(self):
        self.get_time_from_user()
        start = st.button("Start")
        stop_button = st.button("Stop")
        if start:
            self.run = True
            if stop_button:
                self.run = False
                self.countdown()