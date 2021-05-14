# Moway

## For Virtual self-driving car using reinforcement learning

##### Version 1.0

#### V.Sajeevan.

#### 31th May, 2019


### Introduction

The project is about designing and developing a virtual self-driving car using
reinforcement learning to mimic the behavior when it is running with a set of another
self-driving car or human cars. This can be used to observe the impact that the
self-driving car can have on damping the traffic bottlenecks caused by manned vehicles.
This framework can be simulatable in a different traffic situation and different
phenomena.

### Setup Environmentvenv venv


#### Install python3.6.8

Visit the python offical page, Download and Install python-3.6.8
https://www.python.org/downloads/release/python-368/

#### Clone the project Moway
```sh
$ git clone https://github.com/sajeevan16/Moway.git
$ cd Moway
```

#### Setup Virtual Environment (Optinal, Recommended)
```sh
$ pip install virtualenv
$ venv venv

// If Windows
$ venv\Scripts\activate

// If Linux
$ source venv/bin/activate
```

#### Install & Run
```sh
$ python install.py
$ python Moway.py
```

### Requirements

Python 3.6.8

pygame==1.9.4
numpy==1.16.1
keras==2.2.4
tensorflow==1.13.1
argh==0.26.2
h5py==2.10.0

# User manuals

### Process Overview

The product can runnable using the executable file. First of all, decide the model name
and gave it into the Input box and select the Train Button if you want to train a model
otherwise you want to Play the model you can select the Play button. Next, you meet the
Environment creational user interface, Here you can create different traffic situation and
different phenomena Using Different maps, and cars and obstacles. Then you can
proceed with the simulation.

### Workflow

#### 1. Main Menu

![01  MainMenu](https://user-images.githubusercontent.com/37554141/58656630-4d50e600-833a-11e9-9918-c3c17e4c6177.png)

Train - Gave the new model name and Press the Train Button in The Menu. You
will be taken to the Environment creational user interface
Play - Gave the already trained model name and Press the Play Button in The
Menu. You will be taken to the Environment creational user interface

#### 2. Environment Creator

![02  Environment Create](https://user-images.githubusercontent.com/37554141/58656664-593ca800-833a-11e9-900a-b7af21bbb2d2.png)


![03  Environment Create-2](https://user-images.githubusercontent.com/37554141/93644433-9d682600-fa1f-11ea-88cf-713554a52865.png)

First, User can Change The map using Right and Left Arrow Keys, And also user
can Change the adding obstacle or manned car using Up and Down Arrow Keys.
User can set the location of the obstacle by using mouse Click button and also set
the angle of obstacle by releasing the mouse button.

Right, Left Arrows     -     Change Environment Map
Up, Down Arrows     -     Change Obstacles / Cars
Z     -     Undo the Last Action
M     -     Exit To Main Menu
Enter     -     Enter to the Simulation (Train / Play)
User can Establish the Obstacle/Car in the correct position Using Mouse click
and Drag and Release the mouse click to the Facing Direction

#### 3. Simulation

![04  Traing](https://user-images.githubusercontent.com/37554141/58656683-5e99f280-833a-11e9-83c9-9ea54548acb8.png)


![05  Playing](https://user-images.githubusercontent.com/37554141/58656689-6194e300-833a-11e9-8ffa-163e52615e6a.png)


When Training User can View The Epsilon Value, Max Distance, Last Distance,
Total Frames, fps Details in the Below. User can save the model(Reinforcement
Learning Car) by press the S key. You can exit to the Main Menu By Press M Key.
There is also autosave after ever 5000 frames trained.

S     -     Save The Model
M     -     Exit to Main Menu

### Contact us

If you encounter issues not addressed by this user guide, please contact us for additional
support. You can contact us via ​sajeevan.16@cse.mrt.ac.lk​. The reply will be given within a
business day.

