# LambdaGators: Lambda Calculus Illustrator #
By Anarav Patel, Charles Rule, and Michael Rizzo 

For CS-314 Principles of Programming Languages Spring 2019 with Professor Ames. The goal was to make an application that can dynamically illustrate the computational steps of Lambda Calculus with the Alligator analogy. We loved this analogy as much as Professor Ames and it helped demystify lambda calculus by turning it into a fun subject. We wanted to take it one step further by making it into an interactive version that goes beyond basic expressions. We hope future students will want to use our final project and have the same enjoyable experience.  

We would like to acknowledge Bret Victor for [the initial concept.](http://worrydream.com/AlligatorEggs/) This is the same source that Professor Ames used in class. As well, we would like to thank Silas Gyger for his open source [Pygame_TextInput.py module.](https://github.com/Nearoo/pygame-text-input)

## Getting Started ##
There are two ways to install our project: downloading the executable or downloading the repository and running FILENAME.

Prequisites for running the FILENAME are provided below. 

### Prerequisites ###
The libraries our project uses are 

[Pygame](https://www.pygame.org/)
[Pygame_TextInput](https://github.com/Nearoo/pygame-text-input)

To install these libraries, there exists a pip install for Pygame but not Pygame_TextInput. A version of this library is provided in the repository or can be found [here.](https://github.com/Nearoo/pygame-text-input)

Then run FILENAME with Python 3.6 or newer, and an application window should appear. 

## How to Use LambdaGators ##
To use LambdaGators, let us first review the essential parts of a lambda expression.

There are three components, the variable, the function and the application.

We chose to represent the components in the following ways:

A variable can be named using any single lowercase ASCII letter, a-z, i.e. 
```
<variable>

x
```
These will be represented as eggs when an illustration is generated.

A function is usually denoted with a "λ" lowercase lambda  symbol but for convience sake, we chose a "\\" foward-slash. A basic function has two parts, the parameter and the body, which are both collections of variables:
```
\<parameters>.<body>

\xyz.abc
```
These will be represented as alligators when an illustration is generated.

An application is a function next to another variable or function:
```
<function><variable/function> 

(\xyz.abc)def

(\x.x)(\y.y)b

(\x.\y.abc)def
```

In the application window, type any combination of the three parts above into the textbar and hit enter and Voila! Alligators and Eggs appear!

Click the next button to perform the first step of reduction on your function. The illustration will update. After this you can keep clicking next until the expression is completely reduced or you can click the previous button to go back a step in the reduction. Finally you can repeat the whole process with a new expression. To quit, click the exit button. 

Have fun illustrating lambda calculus!
