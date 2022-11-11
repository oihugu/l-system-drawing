from PIL import Image
import numpy as np
from svg_turtle import SvgTurtle as Turtle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os
import cv2
import json

class LSystem():

    def __init__(self, rules, axiom, iterations, segment_length, alpha_zero, angle, image_size) -> None:
        self.SYSTEM_RULES = rules  # generator system rules for l-system
        self.axiom = axiom  # self.axiom (initial string)
        self.iterations = iterations  # number of self.iterations
        self.seg_length = segment_length
        self.alpha_zero = alpha_zero
        self.angle = angle
        self.image_size = image_size


    def derivation(self):
        derived = [self.axiom]  # seed
        for _ in range(self.iterations):
            next_seq = derived[-1]
            next_axiom = [self.rule(char) for char in next_seq]
            derived.append(''.join(next_axiom))
        return derived


    def rule(self,sequence):
        if sequence in self.SYSTEM_RULES:
            return self.SYSTEM_RULES[sequence]
        return sequence


    def draw_l_system(self, turtle):
        stack = []
        commands = []
        for command in self.SYSTEM_RULES:
            turtle.pd()
            if command in ["F", "G", "R", "L"]:
                turtle.forward(self.seg_length)
            elif command == "f":
                commands.append({'pen_up': 0})
                commands.append({'foward': 0})
                #turtle.pu()  # pen up - not drawing
                #turtle.forward(self.seg_length)
            elif command == "+":
                commands.append({'right': self.angle})
                #turtle.right(self.angle)
            elif command == "-":
                commands.append({'left': self.angle})
                #turtle.left(self.angle)
            elif command == "[":
                commands.append({'stack_append': (turtle.position(), turtle.heading())})
                #stack.append((turtle.position(), turtle.heading()))
            elif command == "]":
                commands.append({'pen_up': 0})
                commands.append({'stack_pop': 0})
                #turtle.pu()  # pen up - not drawing
                #position, heading = stack.pop()
                #turtle.goto(position)
                #turtle.setheading(heading)
        with open('../temp/l_sys_draw.json', 'w') as file: 
            file.write(json.dumps(commands))

    def set_turtle(self):
        r_turtle = Turtle(*self.image_size)  # recursive turtle
        r_turtle.screen.title("L-System Derivation")
        r_turtle.speed(0)  # adjust as needed (0 = fastest)
        r_turtle.setheading(self.alpha_zero)  # initial heading
        return r_turtle




    def run(self, output_dir ,image_name):
        if not os.path.exists(f'{output_dir}/{image_name}'):
            os.mkdir(f'{output_dir}/{image_name}')
        model = self.derivation()  #axiom (initial string), nth iterations 
        self.SYSTEM_RULES = model[-1]  # last iteration
        # Set turtle parameters and draw L-System
        r_turtle = self.set_turtle()  # create turtle object
        r_turtle.width(10)
        self.draw_l_system(r_turtle)  # draw model
        # Save image
        svg_file_path = f"{output_dir}/{image_name}/{image_name}.svg"
        png_file_path = f"{output_dir}/{image_name}/{image_name}.png"
        #cut_png_file_path = f"{output_dir}/{image_name}/C_{image_name}.png"
        r_turtle.save_as(svg_file_path)  # save as svg file
        drawing = svg2rlg(svg_file_path)
        drawing.scale(600/72, 600/72)
        renderPM.drawToFile(drawing, png_file_path, fmt="PNG", dpi=600)
        img = cv2.imread(png_file_path)
        img = img[0:6250, 2000:2000+6250]
        cv2.imwrite(png_file_path, img)


def crop_image(image_path):
    # crop image to remove white space
    pass
    

    