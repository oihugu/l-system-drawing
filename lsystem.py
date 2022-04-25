from PIL import Image
import numpy as np
from svg_turtle import SvgTurtle as Turtle
from cairosvg import svg2png


class LSystem():

    def __init__(self, rules, axiom, iterations, segment_length, alpha_zero, angle) -> None:
        self.SYSTEM_RULES = rules  # generator system rules for l-system
        self.axiom = axiom  # self.axiom (initial string)
        self.iterations = iterations  # number of self.iterations
        self.seg_length = segment_length
        self.alpha_zero = alpha_zero
        self.angle = angle


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
        for command in self.SYSTEM_RULES:
            turtle.pd()
            if command in ["F", "G", "R", "L"]:
                turtle.forward(self.seg_length)
            elif command == "f":
                turtle.pu()  # pen up - not drawing
                turtle.forward(self.seg_length)
            elif command == "+":
                turtle.right(self.angle)
            elif command == "-":
                turtle.left(self.angle)
            elif command == "[":
                stack.append((turtle.position(), turtle.heading()))
            elif command == "]":
                turtle.pu()  # pen up - not drawing
                position, heading = stack.pop()
                turtle.goto(position)
                turtle.setheading(heading)


    def set_turtle(self):
        r_turtle = Turtle(2500,2500)  # recursive turtle
        r_turtle.screen.title("L-System Derivation")
        r_turtle.speed(0)  # adjust as needed (0 = fastest)
        r_turtle.setheading(self.alpha_zero)  # initial heading
        return r_turtle




    def run(self):
        model = self.derivation()  #axiom (initial string), nth iterations 
        self.SYSTEM_RULES = model[-1]  # last iteration
        # Set turtle parameters and draw L-System
        r_turtle = self.set_turtle()  # create turtle object
        self.draw_l_system(r_turtle)  # draw model
        r_turtle.save_as("lsystem.svg")  # save as svg file
        svg2png("lsystem.svg", "lsystem.png")  # convert to png file
        crop_image("lsystem.png")


def crop_image(image_path):
    # crop image to remove white space
    # https://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
    image=Image.open(image_path)
    image.load()

    image_data = np.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

    new_image = Image.fromarray(image_data_new)
    new_image.save(image_path)