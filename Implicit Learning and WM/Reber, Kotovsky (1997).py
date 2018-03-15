#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#psychopy version: 1.85.6

from __future__ import division
from psychopy import locale_setup, gui, visual, core, data, event, sound
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
from tkinter import Tk
from random import choice, randint
from collections import OrderedDict
import numpy as np
import os
import sys



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

with open(os.path.join('statistics about participant', 'stats.csv'), 'r') as f:
    lines_data = f.readlines()
    line_1 = lines_data[0].strip('\n').split(',')
    line_2 = lines_data[1].strip('\n').split(',')
    info_participant = OrderedDict({cond: int(qty) for cond,qty in zip(line_1, line_2)})
possible_conditions_1 = {cond: int(qty) for cond,qty in info_participant.items() if int(qty) <= 20}

condition_mapping_1 = (u'Control', u'One', u'Two', u'Three')
condition_mapping_2 = ('Control_0', 'Control_2', 'One_0', 'One_2', 'Two_0', 'Two_2', 'Three_0', 'Three_2')


with open(os.path.join('statistics about participant', 'stats_2.csv'), 'r') as f:
    lines_data = f.readlines()
    line_1 = lines_data[0].strip('\n').split(',')
    line_2 = lines_data[1].strip('\n').split(',')
    info_participant_2 = OrderedDict({cond: int(qty) for cond,qty in zip(line_1, line_2)})
possible_conditions_2 = {cond: int(qty) for cond,qty in info_participant_2.items() if int(qty) <= 10}



# Store info about the experiment session
expName = u'Implicit Learning and WM'
expInfo = {u'participant': u''} 
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
condition_wm_1 = choice(possible_conditions_1.items())
expInfo[u'group'] = condition_mapping_1.index(condition_wm_1[0]) #group == WM_CONDITION
expInfo[u'Experiment part'] = u'1'



# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = os.path.join(_thisDir, u'data\\{}_{}_{}'.format(expInfo['participant'], expName, expInfo['date']))

exp = data.ExperimentHandler(name=expName,
    extraInfo=expInfo, runtimeInfo=None,
    originPath=_thisDir,
    savePickle=True, saveWideText=True,
    dataFileName=filename)



#PREFERENCE
TIME_BETWEEN_SOUND = 2




def circle_factory(name, position):
    return visual.Circle(
                            win=win, name=name,
                            edges=100, radius=100, pos=position,
                            lineWidth=3, lineColor=[-1,-1,-1], 
                            fillColor=[1,1,1], opacity=0, interpolate=True, autoDraw=True,
                          )


def box_factory(name, position, size):
    return visual.Rect(
                        win=win, name=name,
                        width=size, height=size, pos=position,
                        lineWidth=3, lineColor=[-1,-1,-1], 
                        fillColor=[1,1,1], opacity=0, interpolate=True, autoDraw=True,
                        )


def box_open_factory(name, position, size):
    return visual.Rect(
                        win=win, name=name,
                        width=size, height=3, pos=position,
                        lineWidth=1, lineColor=[1,1,1], 
                        fillColor=[1,1,1], opacity=0, interpolate=True, autoDraw=True,
                        )


def chosen_object(mouse, list_of_objects):
    for object in list_of_objects:
        if mouse.isPressedIn(object, buttons=[0]):
            return object
    return False


def board_state(circles, boxes):
    state = []
    for box, circle in zip(boxes, circles):
        state.append(box.overlaps(circle))
    state += [True]
    return np.array(state)


def can_move(obj, condition):
    if not isinstance(obj, visual.Circle):
        return False
    index = obj.name
    if (condition[index] == True) and all(condition[index+1:5] == False):
        return True
    return False

lst = ['A', 'C', 'D', 'W', 'F']
if expInfo[u'group']in (u'1', u'2', u'3'):
    number = int(expInfo[u'group'])
else:
    number = 2

overall_instruction_text = u'''Здравствуйте! 
В процессе эксперимента Вам будет необходимо решить задачу 
(инструкция на следующем слайде) и выполнить второстепенное задание. 
В качестве второстепенного задания Вам будет необходимо слушать буквы английского алфавита и запоминать их. 
Когда прозвучит специальный звуковой сигнал, Вам будет необходимо нажать на клавиатуре букву, 
которая была произнесена {} от звукового сигнала. 
То есть в последовательности: A C D W F *звуковой сигнал* 
необходимо нажать на клавиатуре букву "{}"
Если Вам всё понятно, то нажмите пробел.'''.format(number, lst[-int(number)])



problem_instruction = u'''Цель задания - вынуть все пять шаров из коробок. 
Шар можно вынуть или положить обратно в коробку, нажав на него компьютерной мышью. 
Шар можно вынуть или положить обратно в коробку только в том случае, если верхняя часть коробки открыта. 
Например, прямо сейчас два шара справа можно вынуть, а три слева – нельзя. 
В процессе вынимания и возвращения шаров в коробки верхушки коробок будут открываться и закрываться. 
Суть задания в том, чтобы двигать шары определенным образом, открывая нужные коробки. 
Так, Вы сможете вынуть все шары из коробок.'''



#Get screen resolution
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


win = visual.Window(
    size=[screen_width, screen_height], fullscr=True, 
    screen=0, color=[1,1,1], units = 'pix')


whole_experiment_clock = core.Clock()
mouse = event.Mouse(win=win)

#create all needed objects
STEP = 250
OBJECT_PLACE = xrange( -STEP*2, STEP*2+1, STEP )
OBJECTS_NAMES = range(1,6)
Y_POSITION = 0
HOW_FAR_TO_MOVE = 300
BOX_SIZE = 250



for (name, pos) in zip( OBJECTS_NAMES, OBJECT_PLACE):
    exec u'box_{0} = box_factory( {0}, ({1},{2}), {3} )'.format(name, pos, Y_POSITION, BOX_SIZE)
    exec u'circle_{0} = circle_factory( {0}, ({1},{2}) )'.format(name, pos, Y_POSITION)
    exec u'box_op_{0} = box_open_factory( {0}, ({1},{2}), {3} )'.format(name, pos, Y_POSITION+BOX_SIZE/2,  BOX_SIZE-BOX_SIZE*0.02)



BOXES = (box_1, box_2, box_3, box_4, box_5)
CIRCLES = (circle_1, circle_2, circle_3, circle_4, circle_5)
BOX_OPEN = (box_op_1, box_op_2, box_op_3, box_op_4, box_op_5)
BEEP_SOUND = u'stimuli\\zbeep.wav'
SOUNDS = tuple([u'stimuli\\{}.wav'.format(char) for char in 'QWERTYUIOPASDFGHJKLZXCVBNM'] + [BEEP_SOUND]*2)

instruction_text = visual.TextStim(win=win, pos=(0, -300), opacity=1, color='black', text=problem_instruction, height = 30, wrapWidth=2000)
if expInfo[u'group'] in ('1', '2', '3'):
    secondary_task_text = u'Напишите звук, который был {} назад\nОтвет должен состоять из одной буквы\n\
Для ответа нажмите enter'.format(expInfo[u'group'])
else:
    secondary_task_text = u'Напишите любой звук, главное не выбирайте один и тот же\nОтвет должен состоять из одной буквы\n\
Для ответа нажмите enter'
secondary_task_instruction = visual.TextStim(win=win, pos=(0, 300), opacity=1, color=u'black', text=secondary_task_text, height = 50, wrapWidth=2000)

secondary_task_window = visual.TextStim(win=win, pos=(0, 0), opacity=1, color=u'black', text=u'', height = 200)

mouse.clicks = 0
mouse.time = []
sound_gen = sound.Sound(secs=TIME_BETWEEN_SOUND)
sound_to_play = choice(SOUNDS[:-2])
sound_gen.setSound(sound_to_play)
should_report = True



pressed_down = False #allowing only single mouse clicks



to_display_list = []
to_display_str = u''
sounds = [sound_to_play[-5]]


for experiment in range(2):

    for circle, box_op, box in zip(CIRCLES, BOX_OPEN, BOXES):
        box_op.opacity = 0
        box.opacity = 0
        circle.opacity = 0


    t = whole_experiment_clock.getTime()
    moves = 0
    if experiment == 0:
        overall_instruction = visual.TextStim(win=win, pos=(0, 0), opacity=1, color=u'black', text=overall_instruction_text, height = 30, wrapWidth=1500)
        while True:
            if event.getKeys(['space']):
                event.clearEvents(eventType='keyboard')
                break
            overall_instruction.draw()
            win.flip()
            if event.getKeys(keyList=["escape"]):
                core.quit()


    elif experiment == 1:
        expInfo[u'Experiment part'] = u'2'
        condition_wm_2 = choice(possible_conditions_2.items())
        type_cond = condition_mapping_2.index(condition_wm_2[0])
        expInfo[u'group'] = 0 if type_cond % 2 == 0 else 2#group == WM_CONDITION
        for circle in CIRCLES:
            circle.pos -= (0, HOW_FAR_TO_MOVE)
        second_task_instruction = visual.TextStim(win=win, pos=(0, 0), opacity=1, color=u'black', text=u'Сейчас нужно будет решить задачу ещё раз\n\
        Если готовы нажмите пробел', height = 30, wrapWidth=1500)

        while True:
            if event.getKeys(['space']):
                event.clearEvents(eventType='keyboard')
                break
            second_task_instruction.draw()
            win.flip()
            if event.getKeys(keyList=["escape"]):
                core.quit()



    for circle, box_op, box in zip(CIRCLES, BOX_OPEN, BOXES):
        box_op.opacity = 1
        box.opacity = 1
        circle.opacity = 1



    trial = core.Clock()
    trial.reset()
    time = 0
    while True:
        if event.getKeys(keyList=["escape"]):
            sound_gen.stop()
            exp.nextEntry()
            core.quit()
        


        t = trial.getTime()
        

        instruction_text.draw()

        if sound_gen.status == NOT_STARTED:
            time = trial.getTime()
            if sound_to_play != BEEP_SOUND:
                sound_itself = sound_to_play[-5]
                sounds.append(sound_itself)
            sound_gen.play()

        if sound_to_play == BEEP_SOUND and sound_gen.status == FINISHED and should_report:
            event.clearEvents(eventType='keyboard')
            while True:
                keyboard_presses = event.getKeys() #отчёт сюда
                for circle, box_op, box in zip(CIRCLES, BOX_OPEN, BOXES):
                    box_op.opacity = 0
                    box.opacity = 0
                    circle.opacity = 0

                secondary_task_instruction.draw()
                if len(keyboard_presses) > 0:
                    was_pressed = keyboard_presses[0]
                    if was_pressed == 'escape':
                        sound_gen.stop()
                        core.quit()

                    if was_pressed == 'return' and len(to_display_str) == 1:
                        exp.addData('Move number', moves)
                        exp.addData('Board state', condition_to_move[:6])
                        exp.addData(u'Sounds between respons' , sounds)
                        exp.addData(u'Participant chousen', to_display_str)
                        exp.addData(u'Corectness of WM task', 1 if to_display_str == sounds[-int(expInfo[u'group'])] else 0)
                        exp.addData(u'Time', t)
                        del sounds[:]
                        to_display_str = u''
                        del to_display_list[:]
                        should_report = False
                        for circle, box_op, box in zip(CIRCLES, BOX_OPEN, BOXES):
                            if can_move(circle, condition_to_move):
                                box_op.opacity = 0
                            box.opacity = 1
                            circle.opacity = 1
                        break


                    if was_pressed == 'backspace' and len(to_display_list) != 0:
                        del to_display_list[-1]
                    elif len(was_pressed) == 1:
                        to_display_list.append(was_pressed.upper())
                    to_display_str = ''.join(to_display_list)
                    del keyboard_presses[:]


                secondary_task_window.text = to_display_str
                secondary_task_window.draw()
                win.flip()


        if sound_gen.status == FINISHED and time+sound_gen.secs<t:
            should_report = True
            sound_gen.status = NOT_STARTED
            sound_to_play = choice(SOUNDS) if len(sounds) > int(expInfo[u'group']) and sound_to_play != BEEP_SOUND else SOUNDS[randint(0, len(SOUNDS)-3)]
            sound_gen.setSound(sound_to_play)

        condition_to_move = board_state(CIRCLES, BOXES)
        clicked = chosen_object(mouse, CIRCLES)
        can = can_move(clicked, condition_to_move)

    #problem is solved checker
        if True not in condition_to_move[:5]:
            exp.nextEntry()
            event.clearEvents(eventType='keyboard')
            break

        for circle, box_op in zip(CIRCLES, BOX_OPEN):
            if can_move(circle, condition_to_move):
                box_op.opacity = 1
            else:
                box_op.opacity = 0


        if mouse.getPressed()[0]:
            if not pressed_down:
                    if can:
                        clicked.pos += (0,HOW_FAR_TO_MOVE) if clicked.pos[1] == 0 else (0, -HOW_FAR_TO_MOVE)
                    pressed_down = True
                    moves += 1
                    exp.addData('Move number', moves)
                    exp.addData('Board state', condition_to_move[:6])
                    exp.addData(u'Time', t)
                    exp.nextEntry()
        else: 
            pressed_down = False



        win.flip()



result = u"Спасибо за участие\nЭксперимент занял {:.0f} минут и {:.2f} секунд\nДля выхода нажмите любую клавишу"
final_words = visual.TextStim(win=win, pos=(0, 0), opacity=1, color='black', text=result, height = 50, wrapWidth=1650)
while True:
    if event.getKeys():
        break
    t = whole_experiment_clock.getTime()
    final_words.text = result.format(t//60, t%60)
    final_words.draw()
    win.flip()

print info_participant, info_participant_2


with open(os.path.join('statistics about participant', 'stats.csv'), 'w') as f:
    info_participant[condition_wm_1[0]] += 1
    for line in range(1,3):
        if line == 1:
            f.write(u'{},{},{},{}\n'.format(*info_participant.keys()))
        else:
            f.write(u'{},{},{},{}\n'.format(*info_participant.values()))


with open(os.path.join('statistics about participant', 'stats_2.csv'), 'w') as f:
    info_participant_2[condition_wm_2[0]] += 1
    for line in range(1,3):
        if line == 1:
            f.write(u'{},{},{},{},{},{}\n'.format(*info_participant_2.keys()))
        else:
            f.write(u'{},{},{},{},{},{}\n'.format(*info_participant_2.values()))

core.quit()














