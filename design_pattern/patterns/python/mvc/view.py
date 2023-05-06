import streamlit as st
import time
import asyncio


class View:
    def __init__(self):
        self.remain_time = 60
        self.run = True
    
    async def window(self):
        ph = st.empty()
        while self.run:
            ph.metric("Countdown", self.remain_time)
            await asyncio.sleep(1)
            self.remain_time-=1
        ph.metric("Countdown", self.remain_time)
    
    def show_button(self):
        if st.button("stop"):
            self.run = False

    

if __name__ == "__main__":
    view = View()
    view.show_button()
    asyncio.run(view.window())