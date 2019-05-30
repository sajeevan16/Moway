#this is used for creating the executable file
#of application
import sys
from cx_Freeze import setup, Executable
setup( name = "Moway", version = "1.0",
       description = "The project is about designing and developing a virtual self-driving car using reinforcement learning.",
       executables = [Executable("Allinone.py", base = "Win32GUI")])
