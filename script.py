import tkinter as tk
import time

block_positions = \
    [
        (2,11), (2,12), (2,13),
        (3,4), (3,5), (3,6), (3,11), (3,13),
        (4,4), (4,5), (4,6), (4,7), (4,13),
        (5,4), (5,5), (5,6), (5,7), (5,10), (5,11), (5,12), (5,13),
        (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12),
        (7,5), (7,6), (7,7), (7,8), (7,9), (7,10),
        (8,4), (8,5), (8,6), (8,7), (8,8), (8,9), (8,10),
        (9,4), (9,5),(9,6), (9,7), (9,9),
        (10,6), (10,7), (10,9),
        (11,6), (11,7), (11,9),
        ]

# block_positions = \
# [
#     (2,11), (2,12), (2,13),
#     (3,4), (3,5), (3,6), (3,11), (3,13),
#     (4,4), (4,5), (4,6), (4,7), (4,13),
#     (5,4), (5,5), (5,6), (5,7), (5,10), (5,11), (5,12), (5,13),
#     (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12),
#     (7,5), (7,6), (7,7), (7,8), (7,9), (7,10),
#     (8,5), (8,6), (8,7), (8,8), (8,9), (8,10),
#     (9,6), (9,7), (9,9),
#     (10,6), (10,7), (10,9),
#     (11,6), (11,7), (11,9),
# ]

pointers = {0:'↑', 1:'→', 2:'↓', 3:'←'}

start = (6, 2)
position = start
direction = 1 # 0 up 1 right 2 down 3 left

stack = list()
sleep_time = 0.1

gui = tk.Tk()
for k in range(15):
   for c in range(16):
       text = '#' if (k+1,c+1) in block_positions else '__'
       tk.Label(gui, text=text,
                borderwidth=2).grid(row=k,column=c)


def navigate():
    stack.append("#")
    draw_pointer(start)
    q1()


def q1():  # Start, facing right
    print("State 1")
    if i():
        r()
        q2()
    elif s():
        stack.append("*")
        f()
        l()
        q3()


def q2():
    print("State 2")
    if i():
        p()
        q7() # Do a right crawl
    elif s():
        f()
        l()
        q9()


def q3():
    """
    Turned left and now crawling
    :return:
    """
    print("State 3")
    if i():
        r()
        q4()
    elif s():
        f()
        l() # facing backwards
        q5()


def q4():
    print("State 4")
    if i():
        p()
        q1()
    elif s():
        stack.append("*")
        f()
        l()
        q3()


def q5():
    """
    Facing left, with block in front
    :return:
    """
    print("State 5")
    if i():
        r()
        q6()
    elif s():
        stack.pop()
        f()
        l()
        q7() # ??


def q6():
    print("State 6")
    if i():
        r()  # Facing right
        q1()
    elif s():
        f()
        l()
        q5()


def q7():
    """
    Turned right and now crawling
    :return:
    """
    print("State 7")
    if i():
        r()
        q8()
    elif s():
        f()
        l() # facing backwards
        q9()


def q8():
    print("State 8")
    if s():
        stack.pop()
        f()
        l()
        q7()
    elif i():
        p()
        q5()


def q9():
    print("State 9")
    if i() and stack[-1] == '#':
        p()
    elif i():
        q1()
    elif s():
        q1()


# Actions
def f():
    """
    Go forward
    :return:
    """
    y,x = position
    if direction == 0: # up
        update_position((y-1,x))
    elif direction == 1: # right
        update_position((y,x+1))
    elif direction == 2: # down
        update_position((y+1,x))
    elif direction == 3: # left
        update_position((y,x-1))


def p():
    """
    still
    :return:
    """
    update_direction(direction)


def l():
    """
    Rotate left
    :return:
    """
    update_direction(3 if direction == 0 else direction - 1)


def r():
    """
    rotate right
    :return:
    """
    update_direction(0 if direction == 3 else direction + 1)


#Inputs
def i():
    """
    island
    :return:
    """
    return not check_forward_empty()


def s():
    """
    sea
    :return:
    """
    return check_forward_empty()


# Methods
def update_position(p):
    """
    Update the position
    :param p:
    :return:
    """
    global position
    reposition_pointer(position, p)
    position = p

    gui.update()
    time.sleep(sleep_time)
    print(stack)


def update_direction(d):
    global direction
    direction = d
    draw_pointer(position)
    gui.update()
    time.sleep(sleep_time)
    print(stack)


def check_forward_empty():
    forward = ()

    y,x = position

    if direction == 0:
        forward = (y-1, x)
    elif direction == 1:
        forward = (y, x+1)
    elif direction == 2:
        forward = (y+1, x)
    elif direction == 3:
        forward = (y, x-1)

    return forward not in block_positions


def draw_pointer(p):
    tk.Label(gui, text=pointers[direction], borderwidth=2).grid(row=p[0]-1, column=p[1]-1)


def reposition_pointer(remove_from, add_to):
    tk.Label(gui, text='__', borderwidth=2).grid(row=remove_from[0]-1, column=remove_from[1]-1)
    draw_pointer(add_to)


navigate()
gui.mainloop()
