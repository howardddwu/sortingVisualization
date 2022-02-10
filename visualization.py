from re import I
import pygame
import random
import math

pygame.init()
#this class stores the information used to draw the UI
class drawingInfo:
    # define a bunch of colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE
   
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192 ,192, 192)
    ]
    
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    #paddings inside of the window
    SIDE_PAD = 100
    TOP_PAD = 150
    #initialization of the window
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualization") #title of the program
        self.set_list(lst)
    
    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.column_width = round((self.width - self.SIDE_PAD)/len(lst))# to calculate the width of each column
        self.column_height = math.floor((self.height - self.TOP_PAD)/(self.max_val - self.min_val))# to calculate the height of each column
        self.start_x = self.SIDE_PAD // 2 # the starting x position

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2,40))
    
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.GREEN)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2,65))
    
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions ={}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                    draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.column_width # starting x position
        y = draw_info.height - (val - draw_info.min_val) * draw_info.column_height # starting y position
        color = draw_info.GRADIENTS[i%3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.column_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_random_list(n,min,max):
    lst = []
    for i in range(n):
        val = random.randint(min,max)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1>num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info,{j:draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
        
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1 :draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def main():
    # nend a loop to keep this program running and stay, otherwise it will show the list then end
    run = True     # a variable to keep track of the while loop
    clock = pygame.time.Clock()
    
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_random_list(n,min_val,max_val)
    draw_info = drawingInfo(800,600,lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble sort"
    sorting_algorithm_generator = None

    while run:  
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                soting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_random_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()