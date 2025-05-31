from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

stabbing_animation = False
stabbing_progress = 0
stab_complete = False


pending_limb_cut = False

stop_motion = False
character_fallen = False
remaining_limbs = 4
show_left_arm = True
show_right_arm = True
show_left_leg = True
show_right_leg = True

top_view_mode = False
first_person_view = False
hide_player_head = False
move_villain = False
door_gone = False
is_door_on_x_wall=True
door_pos = [300, 0] 
quiz_questions = [
    {
        "question": "What is the capital of Australia?",
        "options": ["A. London", "B. Canberra", "C. Berlin", "D. Sydney"],
        "correct_answer": 1  # Index 1 corresponds to "B. Canberra"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Venus", "B. Jupiter", "C. Mars", "D. Saturn"],
        "correct_answer": 2  # Index 2 corresponds to "C. Mars"
    },
    {
        "question": "What is the largest mammal?",
        "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Gorilla"],
        "correct_answer": 1  # Index 1 corresponds to "B. Blue Whale"
    },
    {
        "question": "When did the WWII started?",
        "options": ["A. 1912", "B. 1925", "C. 1939", "D. 1942"],
        "correct_answer": 2  # Index 2 corresponds to "C. 1939"
    }
]
quiz_active = False
current_question = 0
timer_start = 0
selected_option = -1
game_over_quiz = False
game_started = False
game_over = False
correct_answers = 0
question_start_time = 0
time_per_question = 15  

show_result = False
result_display_time = 0
display_result_duration = 2 
fovY = 90  
GRID_LENGTH = 600  
grid_size = GRID_LENGTH
cell_size = grid_size / 26
wall_height=180
correct_answers = 0
locks_animation=[0,0,0,0]

camera_pos = [10, 200, 500]  

camera_height = 150 
camera_mode = 0  
camera_angle_offset = 0 

saw_pos = [530, 530, 10]  
saw_picked_up = False  
pending_limb_cut = False 
saw_animation_angle = 0  


character_pos = [550, 290, 0]  
character_angle = 270  
character_scale = 0.8

moving_forward = 0
moving_backward = 0
turning_left = 0
turning_right = 0
animation_counter = 0  
character_height=20

HEAD_COLOR = (1.0, 0.8, 0.6) 
TORSO_COLOR = (0.2, 0.4, 0.8) 
ARM_COLOR = (0.2, 0.5, 0.8)  
LEG_COLOR = (0.2, 0.2, 0.5)  
FOOT_COLOR = (0.1, 0.1, 0.1)  



villain_pos = [40, 500, 0]  
villain_angle = -90  
villain_state = 0 
near_tv = False  

game_won = False
key_picked_up = False
box_pos = None 
box_size = None  
key_pos = None  
key_size = None 
INTERACTION_DISTANCE = 100  

from PIL import Image

show_menu = True  


def draw_background_image(image_path="new_bg.jpg", scale=1.2):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.tobytes()

        img_width, img_height = img.size
        scaled_width = int(img_width * scale)
        scaled_height = int(img_height * scale)

        x = (1000 - scaled_width) // 2
        y = (800 - scaled_height) // 2

        glEnable(GL_TEXTURE_2D)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + scaled_width, y)
        glTexCoord2f(1, 1); glVertex2f(x + scaled_width, y + scaled_height)
        glTexCoord2f(0, 1); glVertex2f(x, y + scaled_height)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glDeleteTextures([tex_id])
        glDisable(GL_TEXTURE_2D)

    except Exception as e:
        print(f"Error loading image: {e}")
        draw_text(300, 400, "[Background Missing]", GLUT_BITMAP_HELVETICA_18, [1, 0, 0])


def draw_text(x, y, text, font=GLUT_BITMAP_TIMES_ROMAN_24,color=[1,1,1]):
    colorx,colory,colorz=color[0],color[1],color[2]
    glColor3f(colorx,colory,colorz)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    

    
    gluOrtho2D(0, 1000, 0, 800) 

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
  
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
  
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


#-------------------------------------------------------ROOM------------------------------------------------------------------------------------------------------------
def draw_pipes():
    #small pipe
    glPushMatrix()
    glTranslatef(100, 20, 0)
    glColor3f(0.3, 0.1, 0) 
    gluCylinder(gluNewQuadric(), 7, 7, 160, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(100, 20, 130)
    glRotatef(90, 1, 0, 0)
    glColor3f(0.3, 0.1, 0)    
    gluCylinder(gluNewQuadric(), 7, 7, 20, 10, 10)
    glPopMatrix()
    #small pipe2
    glPushMatrix()
    glTranslatef(20, 100, 0)
    glColor3f(0.3, 0.1, 0) 
    gluCylinder(gluNewQuadric(), 7, 7, 160, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 100, 130)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.3, 0.1, 0)    
    gluCylinder(gluNewQuadric(), 7, 7, 20, 10, 10)
    glPopMatrix()

    #small pipe-3
    glPushMatrix()
    glTranslatef(20, 550, 0)
    glColor3f(0.3, 0.1, 0) 
    gluCylinder(gluNewQuadric(), 7, 7, 160, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 550, 130)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.3, 0.1, 0)    
    gluCylinder(gluNewQuadric(), 7, 7, 20, 10, 10)
    glPopMatrix()

    #small pipe -4
    glPushMatrix()
    glTranslatef(20, 580, 0)
    glColor3f(0.3, 0.1, 0) 
    gluCylinder(gluNewQuadric(), 7, 7, 160, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(20, 580, 130)
    glRotatef(90, 1, 0, 0)
    glColor3f(.5, .5, .5)   
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()
    #wrapped pipe
    glPushMatrix()
    glTranslatef(520, 40, 20)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.4, 0.4, 0.4) 
    gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(530, 40, 0)
    glColor3f(0.4, 0.4, 0.4) 
    gluCylinder(gluNewQuadric(), 10, 10, 20, 10, 10)
    glPopMatrix()
    #wrapped pipe-2
    glPushMatrix()
    glTranslatef(580, 570, 100)
    glRotatef(90, 1, 0, 0)
    glColor3f(.5, .5, .5) 
    gluCylinder(gluNewQuadric(), 2, 2, 515, 10, 10)
    glPopMatrix()
    #big pipe
    glPushMatrix()
    glTranslatef(580, 40, 0)
    glColor3f(0.3, 0.1, 0)  
    gluCylinder(gluNewQuadric(), 20,20, 160, 10, 10)
    glPopMatrix()
    #big pipe-2
    glPushMatrix()
    glTranslatef(580, 580, 0)
    glColor3f(0.3, 0.1, 0)  
    gluCylinder(gluNewQuadric(), 15,15, 160, 10, 10)
    glPopMatrix()
    glColor3f(0.8, 0.8, 0.8)  # Off-white for ceramic
def draw_tiled_wall(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    global cell_size, wall_height
    
  
    wall_length = max(abs(x2 - x1), abs(y2 - y1))
    num_tiles = int(wall_length / cell_size)
    
   
    is_x_axis = abs(y2 - y1) < abs(x2 - x1)
    
  
    for i in range(num_tiles):
        for j in range(int(wall_height / cell_size)):
           
            if is_x_axis:
                tx1 = x1 + i * cell_size
                ty1 = y1
                tz1 = j * cell_size
                
                tx2 = x1 + (i + 1) * cell_size
                ty2 = y1
                tz2 = j * cell_size
                
                tx3 = x1 + (i + 1) * cell_size
                ty3 = y1
                tz3 = (j + 1) * cell_size
                
                tx4 = x1 + i * cell_size
                ty4 = y1
                tz4 = (j + 1) * cell_size
            else:
                tx1 = x1
                ty1 = y1 + i * cell_size
                tz1 = j * cell_size
                
                tx2 = x1
                ty2 = y1 + (i + 1) * cell_size
                tz2 = j * cell_size
                
                tx3 = x1
                ty3 = y1 + (i + 1) * cell_size
                tz3 = (j + 1) * cell_size
                
                tx4 = x1
                ty4 = y1 + i * cell_size
                tz4 = (j + 1) * cell_size
            
           
            if (i + j) % 2 == 0:
                glColor3f(0.8, 0.8, 0.8)
            else:
                glColor3f (0.7, 0.7, 0.7)   
            
          
            glBegin(GL_QUADS)
            glVertex3f(tx1, ty1, tz1)
            glVertex3f(tx2, ty2, tz2)
            glVertex3f(tx3, ty3, tz3)
            glVertex3f(tx4, ty4, tz4)
            glEnd()
            
        
            line_width = cell_size * 0.03 
            glColor3f(0, 0, 0)  
            
           
            glBegin(GL_QUADS)
            if is_x_axis:
                glVertex3f(tx1, ty1 + 0.1, tz1)
                glVertex3f(tx2, ty2 + 0.1, tz2)
                glVertex3f(tx2, ty2 + 0.1, tz2 + line_width)
                glVertex3f(tx1, ty1 + 0.1, tz1 + line_width)
            else:
                glVertex3f(tx1 + 0.1, ty1, tz1)
                glVertex3f(tx1 + 0.1, ty2, tz2)
                glVertex3f(tx1 + 0.1, ty2, tz2 + line_width)
                glVertex3f(tx1 + 0.1, ty1, tz1 + line_width)
            glEnd()
            
           
            glBegin(GL_QUADS)
            if is_x_axis:
                glVertex3f(tx1, ty1 + 0.1, tz1)
                glVertex3f(tx1, ty1 + 0.1, tz4)
                glVertex3f(tx1 + line_width, ty1 + 0.1, tz4)
                glVertex3f(tx1 + line_width, ty1 + 0.1, tz1)
            else:
                glVertex3f(tx1 + 0.1, ty1, tz1)
                glVertex3f(tx1 + 0.1, ty1, tz4)
                glVertex3f(tx1 + 0.1, ty1 + line_width, tz4)
                glVertex3f(tx1 + 0.1, ty1 + line_width, tz1)
            glEnd()
#---------------------------------------------SAW---------------------------------------------------------------------------------------
def draw_saw():
    global saw_pos, saw_picked_up, saw_animation_angle
    
    if saw_picked_up:
       
        glPushMatrix()
       
        hand_offset_x = 35 * math.cos(math.radians(character_angle+270))
        hand_offset_y = 35 * math.sin(math.radians(character_angle+270))
        
        
        glTranslatef(character_pos[0] + hand_offset_x, character_pos[1] + hand_offset_y, 40)
        
        
        saw_animation_angle += 0.5
        glRotatef(character_angle + 180, 0, 0, 1)
        glRotatef(90, 1, 0, 0)  
        glRotatef(math.sin(saw_animation_angle/10) * 10, 0, 1, 0)  
        
        glScalef(0.3, 0.3, 0.3)  
    else:
        
        glPushMatrix()
        glTranslatef(saw_pos[0], saw_pos[1], saw_pos[2])
        glScalef(0.4, 0.4, 0.4)
    
   
    glColor3f(0.8, 0.8, 0.8)
    
    
    glBegin(GL_QUADS)
    
    glVertex3f(-100, 0, 0)
    glVertex3f(100, 0, 0)
    glVertex3f(100, 10, 0)
    glVertex3f(-100, 10, 0)
    
    # Back surface
    glVertex3f(-100, 0, -1)
    glVertex3f(100, 0, -1)
    glVertex3f(100, 30, -1)
    glVertex3f(-100, 30, -1)
    
    # Top edge
    glVertex3f(-100, 30, 0)
    glVertex3f(100, 30, 0)
    glVertex3f(100, 30, -1)
    glVertex3f(-100, 30, -1)
    

    glEnd()
    
 
    glBegin(GL_TRIANGLES)
    num_teeth = 40
    tooth_width = 150 / num_teeth
    tooth_height = 6
    
    for i in range(num_teeth):
        # Each tooth is a small triangle
        glVertex3f(-100 + i * tooth_width, 0, -1.5)  # Middle of blade thickness
        glVertex3f(-100 + (i + 0.5) * tooth_width, -tooth_height, -1.5)  # Tip of tooth
        glVertex3f(-100 + (i + 1) * tooth_width, 0, -1.5)  # Next tooth start
    glEnd()
    
    # Draw the handle (BIGGER HANDLE)
    glColor3f(0.76, 0.6, 0.42)  # Light wood color
    
    # Base of handle (connects to blade) - INCREASED DIMENSIONS
    glBegin(GL_QUADS)
    # Front face - wider and taller
    glVertex3f(60, -10, -8)
    glVertex3f(110, -10, -8)
    glVertex3f(110, 25, -8)
    glVertex3f(60, 25, -8)
    
    # Back face - wider and taller
    glVertex3f(60, -10, 6)
    glVertex3f(110, -10, 6)
    glVertex3f(110, 25, 6)
    glVertex3f(60, 25, 6)
    
    # Left side face
    glVertex3f(60, -10, -8)
    glVertex3f(60, -10, 6)
    glVertex3f(60, 25, 6)
    glVertex3f(60, 25, -8)
    
    # Right side face
    glVertex3f(110, -10, -8)
    glVertex3f(110, -10, 6)
    glVertex3f(110, 25, 6)
    glVertex3f(110, 25, -8)
    
    # Bottom face
    glVertex3f(60, -10, -8)
    glVertex3f(110, -10, -8)
    glVertex3f(110, -10, 6)
    glVertex3f(60, -10, 6)
    
    # Top face
    glVertex3f(60, 25, -8)
    glVertex3f(110, 25, -8)
    glVertex3f(110, 25, 6)
    glVertex3f(60, 25, 6)
    glEnd()
    
    glPopMatrix()  # End of saw drawing
def is_character_near_saw():
    # Define character size (approximate based on your character model)
    character_size = [30 * character_scale, 30 * character_scale, 80 * character_scale]
    
    # Define saw size (adjust these values based on your saw model)
    saw_size = [50, 50, 20]
    
    # so that character go near the saw is detected
    character_pos_3d = [character_pos[0], character_pos[1], 40]
    
    # Check collision between character and saw
    return check_collision(character_pos_3d, character_size, saw_pos, saw_size)
# Update handle_saw_interaction to use collision detection
def handle_saw_interaction():
    """Handle picking up the saw"""
    global saw_picked_up
    
    if is_character_near_saw() and not saw_picked_up and pending_limb_cut:
        saw_picked_up = True
        return True
    return False

def check_answer(selected_option):
    """Check if the selected answer is correct and handle consequences"""
    global quiz_active, current_question, game_won, key_picked_up, game_over_quiz
    global pending_limb_cut, saw_picked_up, timer_start
    
    # Get the correct answer for the current question
    correct_answer = quiz_questions[current_question]["correct"]
    
    if selected_option == correct_answer:
        # Correct answer handling
        print("Correct answer!")
        if current_question < len(quiz_questions) - 1:
            current_question += 1
            timer_start = time.time()  # Reset timer for next question
        else:
            # All questions answered correctly
            quiz_active = False
            game_won = True
            print("Quiz complete! You survived.")
    else:
        # Incorrect answer - trigger limb cutting sequence
        print("Incorrect answer! Go to the saw!")
        pending_limb_cut = True
        saw_picked_up = False
        quiz_active = False  # Pause the quiz until the limb is cut
        
#------------------------------------------------------------------------------------------------------------------------------------------------
def draw_steel_door(x, y, is_x_wall,door_color= (0.15, 0.15, 0.17)  ,frame_color=(0.1, 0.1, 0.1)):

    global wall_height, cell_size
    
    # Door dimensions
    door_width = cell_size * 4  # 6 cells wide
    door_height = wall_height * 0.8  # 80% of wall height
    
    # Steel black color
    z_offset = 0.5  # Small offset to prevent z-fighting with the wall
    
    # Draw the door frame first (slightly bigger than the door)
    frame_width = door_width * 1.1
    frame_height = door_height * 1.05
    
    glPushMatrix()
    
    if is_x_wall:  # Door on north or south wall
        # Door frame
        glColor3f(*frame_color)
        glBegin(GL_QUADS)
        # Front face of frame
        glVertex3f(x - frame_width/2, y + z_offset, 0)
        glVertex3f(x + frame_width/2, y + z_offset, 0)
        glVertex3f(x + frame_width/2, y + z_offset, frame_height)
        glVertex3f(x - frame_width/2, y + z_offset, frame_height)
        glEnd()
        
        # Door itself
        glColor3f(*door_color)
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(x - door_width/2, y + z_offset + 2, 0)
        glVertex3f(x + door_width/2, y + z_offset + 2, 0)
        glVertex3f(x + door_width/2, y + z_offset + 2, door_height)
        glVertex3f(x - door_width/2, y + z_offset + 2, door_height)
        glEnd()
        
        
   
    
    
    num_panels = 3
    panel_height = door_height / num_panels
    panel_inset = 1.0
    
    glColor3f(*[c * 0.9 for c in door_color])  # Slightly lighter for panels
    
    for i in range(num_panels):
        panel_z_bottom = i * panel_height
        panel_z_top = (i + 1) * panel_height
        
        if is_x_wall:
            glBegin(GL_QUADS)
            glVertex3f(x - door_width/2 + panel_inset, y + z_offset + 3, panel_z_bottom + panel_inset)
            glVertex3f(x + door_width/2 - panel_inset, y + z_offset + 3, panel_z_bottom + panel_inset)
            glVertex3f(x + door_width/2 - panel_inset, y + z_offset + 3, panel_z_top - panel_inset)
            glVertex3f(x - door_width/2 + panel_inset, y + z_offset + 3, panel_z_top - panel_inset)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glVertex3f(x + z_offset + 3, y - door_width/2 + panel_inset, panel_z_bottom + panel_inset)
            glVertex3f(x + z_offset + 3, y + door_width/2 - panel_inset, panel_z_bottom + panel_inset)
            glVertex3f(x + z_offset + 3, y + door_width/2 - panel_inset, panel_z_top - panel_inset)
            glVertex3f(x + z_offset + 3, y - door_width/2 + panel_inset, panel_z_top - panel_inset)
            glEnd()
    
    glPopMatrix()
def grid():
    global grid_size, wall_height, cell_size,door_gone
    num_cells=26
    
    
    for i in range(num_cells):
        for j in range(num_cells):
            # Calculate the corners of each cell
            x1 = i * cell_size
            y1 = j * cell_size
            x2 = (i + 1) * cell_size
            y2 = (j + 1) * cell_size
            
            
            if (i + j) % 2 == 0:
                base_color = (1, 1, 1)  # White
            else:
                base_color = (174/255, 193/255, 207/255) 
            
            
            glBegin(GL_QUADS)
            glColor3f(*base_color)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
            glEnd()
            
            
            line_width = cell_size * 0.03  # Very thin lines
            
            
            glBegin(GL_QUADS)
            glColor3f(0, 0, 0)  # Black for grid lines
            glVertex3f(x1, y1, 0.1)
            glVertex3f(x2, y1, 0.1)
            glVertex3f(x2, y1 + line_width, 0.1)
            glVertex3f(x1, y1 + line_width, 0.1)
            glEnd()
            
            # Draw vertical grid line at the left of the cell
            glBegin(GL_QUADS)
            glColor3f(0, 0, 0)  # Black for grid lines
            glVertex3f(x1, y1, 0.1)
            glVertex3f(x1 + line_width, y1, 0.1)
            glVertex3f(x1 + line_width, y2, 0.1)
            glVertex3f(x1, y2, 0.1)
            glEnd()
    
    
    # North wall (back)
    draw_tiled_wall(0, grid_size, 0,
                   grid_size, grid_size, 0,
                   grid_size, grid_size, wall_height,
                   0, grid_size, wall_height)
    
    # South wall (front)
    draw_tiled_wall(0, 0, 0,
                   grid_size, 0, 0,
                   grid_size, 0, wall_height,
                   0, 0, wall_height)
    if door_gone==False:
        draw_steel_door(grid_size/2, 0, True)
    # East wall (right)
    draw_tiled_wall(grid_size, 0, 0,
                   grid_size, grid_size, 0,
                   grid_size, grid_size, wall_height,
                   grid_size, 0, wall_height)
    
    # West wall (left)
    draw_tiled_wall(0, 0, 0,
                   0, grid_size, 0,
                   0, grid_size, wall_height,
                   0, 0, wall_height)
def draw_open_door(x, y, is_x_wall, door_color= (1,1,1)  ,frame_color=(0.1, 0.1, 0.1)):

    global wall_height, cell_size
    
    # Door dimensions
    door_width = cell_size * 4  # 6 cells wide
    door_height = wall_height * 0.8  # 80% of wall height
    
    # Steel black color
    z_offset = 0.5  
    
    
    frame_width = door_width * 1.1
    frame_height = door_height * 1.05
    
    glPushMatrix()
    
    if is_x_wall:  
        # Door frame
        glColor3f(*frame_color)
        glBegin(GL_QUADS)
        # Front face of frame
        glVertex3f(x - frame_width/2, y + z_offset, 0)
        glVertex3f(x + frame_width/2, y + z_offset, 0)
        glVertex3f(x + frame_width/2, y + z_offset, frame_height)
        glVertex3f(x - frame_width/2, y + z_offset, frame_height)
        glEnd()
        
        # Door itself
        glColor3f(*door_color)
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(x - door_width/2, y + z_offset + 2, 0)
        glVertex3f(x + door_width/2, y + z_offset + 2, 0)
        glVertex3f(x + door_width/2, y + z_offset + 2, door_height)
        glVertex3f(x - door_width/2, y + z_offset + 2, door_height)
        glEnd()
        
        
   
    
    glPopMatrix()
def draw_sink(x_pos,y_pos):

    wall_offset = 5
    
    # Sink dimensions
    sink_width = 40
    sink_depth = 30
    sink_height = 15
    
    # Position calculation
    z_pos = wall_height * 0.4  # Height from floor

    drain_radius = sink_width * 0.08
    # Draw the main sink body
    glPushMatrix()
    
    # Top rim of sink
    glColor3f(0,0,.9)
    glBegin(GL_QUADS)
    # Top surface
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset, z_pos-5)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset, z_pos-5)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset + sink_depth, z_pos-5)
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset + sink_depth, z_pos-5)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.9, 0.9, 0.92)
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset, z_pos - sink_height)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset, z_pos - sink_height)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset, z_pos)
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset, z_pos)
    
    # Left side face
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset, z_pos - sink_height)
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset + sink_depth, z_pos - sink_height)
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset + sink_depth, z_pos)
    glVertex3f(x_pos - sink_width/2, y_pos + wall_offset, z_pos)
    
    # Right side face
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset, z_pos - sink_height)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset + sink_depth, z_pos - sink_height)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset + sink_depth, z_pos)
    glVertex3f(x_pos + sink_width/2, y_pos + wall_offset, z_pos)
    
    
    glEnd()
    
    # Draw a simple tap/faucet
    glColor3f(0.9, 0.9, 0.92)
    glPushMatrix()
    glTranslatef(x_pos, y_pos + wall_offset + sink_depth - 1, z_pos + 15)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 8, 1)
    glPopMatrix()
    
    # Draw a simple drain
    glColor3f(0.3, 0.1, 0) 
    glPushMatrix()
    glTranslatef(x_pos, y_pos + wall_offset + (sink_depth/2), z_pos - (sink_height+55))
    gluCylinder(gluNewQuadric(), drain_radius, drain_radius, z_pos - sink_height+4, 8, 1)
    glPopMatrix()
    
    glPopMatrix()

#---------------------------------------------TV--------------------------------------------
def TV_box():
    # glColor3f(0.80, 0.66, 0.50)
    glColor3f(184/255, 123/255, 50/255)
    glPushMatrix()
    glTranslatef(40, 270, 36)
    glRotatef(90, 1, 0, 0)
    glScalef(1, 1, 1.4)
    glutSolidCube(70)
    glPopMatrix()

def check_tv_proximity():

    global near_tv, character_pos, character_scale
    

    tv_pos = [grid_size / 2, grid_size - 30, wall_height / 2 - 10]  # x, y, z

    tv_width = 80  # Width from front
    tv_depth = 60  # Depth from front to back
    tv_height = 60  # Height 

    buffer = 20
    tv_size = [tv_width + buffer, tv_depth + buffer, tv_height + buffer]
    
    # Character position and size (applying scale)
    char_pos = [character_pos[0], character_pos[1], character_height * character_scale / 2]
    char_size = [30 * character_scale, 30 * character_scale, character_height * character_scale]
    
    # Check collision
    is_colliding = check_collision(tv_pos, tv_size, char_pos, char_size)
    
    # Update near_tv flag
    near_tv = is_colliding
 
    if is_colliding:
       
        vec_x = character_pos[0] - tv_pos[0]
        vec_y = character_pos[1] - tv_pos[1]
        
        length = (vec_x**2 + vec_y**2)**0.5
        if length > 0:  # Avoid division by zero
            vec_x /= length
            vec_y /= length
            
            min_dist_x = (tv_size[0]/2 + char_size[0]/2) - abs(character_pos[0] - tv_pos[0])
            min_dist_y = (tv_size[1]/2 + char_size[1]/2) - abs(character_pos[1] - tv_pos[1])
            
           
            if min_dist_x < min_dist_y and min_dist_x > 0:
                push_dist = min_dist_x 
                character_pos[0] += push_dist * vec_x * 1.1  
            elif min_dist_y > 0:
                push_dist = min_dist_y
                character_pos[1] += push_dist * vec_y * 1.1  # Add 10% extra distance

def check_collision(obj1_pos, obj1_size, obj2_pos, obj2_size):

    half_size1 = [s/2 for s in obj1_size]
    half_size2 = [s/2 for s in obj2_size]
    

    min1 = [obj1_pos[i] - half_size1[i] for i in range(3)]
    max1 = [obj1_pos[i] + half_size1[i] for i in range(3)]
    min2 = [obj2_pos[i] - half_size2[i] for i in range(3)]
    max2 = [obj2_pos[i] + half_size2[i] for i in range(3)]

    x_overlap = min1[0] <= max2[0] and max1[0] >= min2[0]
    y_overlap = min1[1] <= max2[1] and max1[1] >= min2[1]
    z_overlap = min1[2] <= max2[2] and max1[2] >= min2[2]
    
    return x_overlap and y_overlap and z_overlap
def draw_tv(rotation_angle=0):
    global grid_size, wall_height,quiz_active
    
    # TV dimensions
    tv_width_front = 80  # Width of the front face (screen side)
    tv_width_back = 50   # Width of the back face (narrower)
    tv_height_front = 60  # Height of the front face
    tv_height_back = 40   # Height of the back face (smaller)
    tv_depth = 60        # Depth from front to back
    screen_inset = 5     # Frame around the screen
    
    # Position - center of north wall facing into the room
    x_pos = grid_size / 2
    y_pos = grid_size - tv_depth - 1  # Positioned away from the wall, facing into room
    z_pos = wall_height / 2 - 10 # Center height on wall
    
    glPushMatrix()
    
    
    glTranslatef(x_pos, y_pos + tv_depth/2, z_pos)  # Move to position where TV should be centered
    glRotatef(rotation_angle, 0, 0, 1)  # Rotate around Z-axis (vertical axis)
    
   
    x_pos, y_pos, z_pos = 300, -260, 27   
    
    
    glColor3f(0.3, 0.3, 0.3)  
    glBegin(GL_QUADS)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glEnd()
     
   
    glColor3f(0.1, 0.1, 0.1)  
    glBegin(GL_QUADS)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glEnd()
    
    
    glBegin(GL_QUADS)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glEnd()
    
    
    glBegin(GL_QUADS)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glEnd()
    
   
    glBegin(GL_QUADS)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos + tv_height_front/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos + tv_height_back/2)
    glEnd()
    
    
    glBegin(GL_QUADS)
    glVertex3f(x_pos - tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos + tv_width_front/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos + tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glVertex3f(x_pos - tv_width_back/2, y_pos - tv_depth/2, z_pos - tv_height_back/2)
    glEnd()
    
   
    if quiz_active:
        glColor3f(1.0, 1.0, 1.0)  # White for active screen
    else:
        glColor3f(0.1, 0.1, 0.2)  # Blue-ish for inactive
    screen_x1 = x_pos - tv_width_front/2 + screen_inset
    screen_x2 = x_pos + tv_width_front/2 - screen_inset
    screen_y = y_pos + tv_depth/2 + 1
    screen_z1 = z_pos - tv_height_front/2 + screen_inset
    screen_z2 = z_pos + tv_height_front/2 - screen_inset
    
    glBegin(GL_QUADS)
    glVertex3f(screen_x1, screen_y, screen_z1)
    glVertex3f(screen_x2, screen_y, screen_z1)
    glVertex3f(screen_x2, screen_y, screen_z2)
    glVertex3f(screen_x1, screen_y, screen_z2)
    glEnd()
    
    if quiz_active:
        glColor3f(1.0, 1.0, 1.0)  # White for active screen
    else:
        glColor3f(0.1, 0.1, 0.2)  # Blue-ish for inactive
    screen_x1 = x_pos - tv_width_front/2 + screen_inset
    screen_x2 = x_pos + tv_width_front/2 - screen_inset
    screen_y = y_pos + tv_depth/2 + 1
    screen_z1 = z_pos - tv_height_front/2 + screen_inset
    screen_z2 = z_pos + tv_height_front/2 - screen_inset
    
    glBegin(GL_QUADS)
    glVertex3f(screen_x1, screen_y, screen_z1)
    glVertex3f(screen_x2, screen_y, screen_z1)
    glVertex3f(screen_x2, screen_y, screen_z2)
    glVertex3f(screen_x1, screen_y, screen_z2)
    glEnd()
    
    
    
    button_size = 4
    button_spacing = 8
    buttons_y = y_pos + tv_depth/2 + 0.2
    buttons_z = z_pos - tv_height_front/2 + screen_inset/2
    
    # Draw 4 buttons
    for i in range(4):
        if i == 0:
            glColor3f(0.7, 0.0, 0.0)  # Red power button
        else:
            glColor3f(0.5, 0.5, 0.5)  # Gray buttons
            
        button_x = x_pos - tv_width_front/4 + (i * button_spacing)
        
        glBegin(GL_QUADS)
        glVertex3f(button_x - button_size/2, buttons_y, buttons_z - button_size/2)
        glVertex3f(button_x + button_size/2, buttons_y, buttons_z - button_size/2)
        glVertex3f(button_x + button_size/2, buttons_y, buttons_z + button_size/2)
        glVertex3f(button_x - button_size/2, buttons_y, buttons_z + button_size/2)
        glEnd()
    
    # TV stand/base
    base_width = tv_width_front * 0.6
    base_height = 10
    base_depth = 20
    
    glColor3f(0.1, 0.1, 0.1)  # Black for the base
    
    # Front face of base
    glBegin(GL_QUADS)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glEnd()
    
    # Back face of base
    glBegin(GL_QUADS)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2)
    glEnd()
    
    # Left face of base
    glBegin(GL_QUADS)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glEnd()
    
    # Right face of base
    glBegin(GL_QUADS)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2)
    glEnd()
    
    # Bottom face of base
    glBegin(GL_QUADS)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos + base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glVertex3f(x_pos - base_width/2, y_pos + tv_depth/2 - base_depth, z_pos - tv_height_front/2 - base_height)
    glEnd()
    
    glPopMatrix()

#---------------------------------------------key and box---------------------------------------------------------------------
def check_character_door_collision(door_pos, is_x_wall):
    global character_pos, character_scale
    
    # Door dimensions
    door_width = cell_size * 4
    door_height = wall_height * 0.8
    
    door_pos_3d = [door_pos[0], door_pos[1], door_height/2]
    
    # Door collision box size depends on if it's on x or y wall
    if is_x_wall:
        door_size = [door_width, 10, door_height]  # Thin in y direction
    else:
        door_size = [10, door_width, door_height]  # Thin in x direction
    
    character_size = [40 * character_scale, 40 * character_scale, 80 * character_scale]
    character_pos_3d = [character_pos[0], character_pos[1], character_height/2]
    
    dx = abs(character_pos[0] - door_pos[0])
    dy = abs(character_pos[1] - door_pos[1])
    distance = math.sqrt(dx*dx + dy*dy)
    

    is_facing_door = False
    if is_x_wall:

        angle_to_door = math.degrees(math.atan2(door_pos[1] - character_pos[1], door_pos[0] - character_pos[0]))
        if angle_to_door < 0:
            angle_to_door += 360
            

        character_facing = (character_angle + 270) % 360
        angle_diff = abs(character_facing - angle_to_door)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        is_facing_door = angle_diff < 45
    else:
        angle_to_door = math.degrees(math.atan2(door_pos[1] - character_pos[1], door_pos[0] - character_pos[0]))
        if angle_to_door < 0:
            angle_to_door += 360
            

        character_facing = (character_angle + 270) % 360
        angle_diff = abs(character_facing - angle_to_door)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        is_facing_door = angle_diff < 45
    
    return distance < INTERACTION_DISTANCE and is_facing_door
def handle_door_interaction(door_pos, is_x_wall):
    global key_picked_up, game_won,door_gone
    
    # First check if character is near the door
    if check_character_door_collision(door_pos, is_x_wall):
        if key_picked_up:
            # Open the door (this could trigger a room change, level complete, etc.)
            game_won = True
            # You could add a door opening animation or sound here
            # Maybe set a flag to indicate the door is now open
            door_gone=True
            print("You unlocked the door with the key!")
            
            return True
        else:
            # Display a message that player needs a key
            print("You need a key to open this door.")
            # You might want to set a flag to display this message on screen for a few seconds
            return False
    
    return False

def initialize_box_properties():
    global box_pos, box_size, key_pos, key_size

    center_x = grid_size / 2
    center_y = grid_size / 2
    
    # Box dimensions
    box_width = grid_size / 8
    box_height = grid_size / 10
    box_depth = grid_size / 5
    
    box_x = center_x
    box_y = center_y
    box_z = box_height/ 2
    
    # Store box position and size
    box_pos = [box_x, box_y, box_z+2]
    box_size = [box_width, box_depth, box_height]
    
    # Key dimensions
    key_length = box_width / 3
    key_width = key_length / 5
    key_thickness = key_width / 2
    
    # Key position
    key_x = box_x
    key_y = box_y
    key_z = box_height/2 + key_thickness/2 + 7  # Same as in createMagicalBox
    
    # Store key position and size
    key_pos = [key_x, key_y, key_z]
    key_size = [key_length, key_width, key_thickness]
def check_character_box_collision():
    global character_pos
    
    if box_pos is None or box_size is None:
        initialize_box_properties()
    
    character_width = 60 * character_scale
    character_height = 150 * character_scale  # Full height
    character_depth = 40 * character_scale

    char_center_x = character_pos[0]
    char_center_y = character_pos[1]
    char_center_z = character_height / 2  # Assuming Z is up
    
    char_pos_center = [char_center_x, char_center_y, char_center_z]
    char_size = [character_width, character_depth, character_height]
    
    # Check collision
    return check_collision(char_pos_center, char_size, box_pos, box_size)

def is_character_near_box():
    if box_pos is None:
        initialize_box_properties()
    
    # Calculate distance between character and box centers
    dx = character_pos[0] - box_pos[0]
    dy = character_pos[1] - box_pos[1]
    distance = math.sqrt(dx*dx + dy*dy)
    
    return distance < INTERACTION_DISTANCE

def try_pickup_key():
    global key_picked_up, game_won
    
    if game_won and is_character_near_box() and not key_picked_up:
        key_picked_up = True
        return True
    return False
def handle_box_collision():
    global character_pos, last_valid_pos
    
    # Push character back to last valid position
    last_pos = globals().get('last_valid_pos')
    
    if last_pos is not None:
        character_pos = last_pos.copy()
    else:
        # If no last valid position, just move slightly away from box
        dx = character_pos[0] - box_pos[0]
        dy = character_pos[1] - box_pos[1]
        
        # Normalize and move away
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
            character_pos[0] = box_pos[0] + dx * (box_size[0]/2 + 30)
            character_pos[1] = box_pos[1] + dy * (box_size[1]/2 + 30)
def draw_animated_locks(box_width, box_depth, keylock_size, keylock_spacing, keylock_z):
    global correct_answers, locks_animation
    
    for i in range(4):
        if i < correct_answers:
            # Calculate position
            lock_y = -box_depth/2 + box_depth/8 + (i * keylock_spacing * 1.5)
            
          
            elapsed = time.time() - locks_animation[i]
            anim_scale = min(1.0, elapsed * 2) 
            
            glPushMatrix()
            glTranslatef(box_width/2 + keylock_size/2, lock_y, keylock_z)
            glScalef(anim_scale, anim_scale * 0.8, anim_scale)  
            
            # Gold lock body
            glColor3f(0.9, 0.75, 0)
            glutSolidCube(keylock_size)
            
            # Black keyhole
            glColor3f(0.1, 0.1, 0.1)
            glTranslatef(0, -keylock_size/4, 0)
            glScalef(0.5, 0.3, 0.5)
            glutSolidTorus(keylock_size/4, keylock_size/2, 8, 8)
            
            glPopMatrix()

def update_magical_box():
    global box_pos, box_size, key_pos, key_size
    
    if box_pos is None or box_size is None:
        initialize_box_properties()
    
    
    if check_character_box_collision():
      
        handle_box_collision()

def modified_createMagicalBox():
    global grid_size, wall_height, key_picked_up, correct_answers
    
    center_x = grid_size / 2
    center_y = grid_size / 2
    
    # Box dimensions 
    box_width = grid_size / 8  
    box_height = grid_size / 10  
    box_depth = grid_size / 5  
    
    box_x = center_x
    box_y = center_y
    box_z = box_height / 2  
    keylock_size = box_width / 10
    keylock_spacing = box_width / 5
    keylock_z = -box_width / 15
    
    # Draw the main box
    glPushMatrix()
    glTranslatef(box_x, box_y, box_z+2)
    
    # Wooden box 
    glColor3f(0.6, 0.3, 0.1)  # Brown wood color
    
    # Front face
    glBegin(GL_QUADS)
    glVertex3f(-box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(box_width/2, -box_depth/2, box_height/2)
    glVertex3f(-box_width/2, -box_depth/2, box_height/2)
    glEnd()
    
    # Back face 
    glBegin(GL_QUADS)
    glVertex3f(-box_width/2, box_depth/2, -box_height/2)
    glVertex3f(box_width/2, box_depth/2, -box_height/2)
    glVertex3f(box_width/2, box_depth/2, box_height/2)
    glVertex3f(-box_width/2, box_depth/2, box_height/2)
    glEnd()
    
    # Left face
    glBegin(GL_QUADS)
    glVertex3f(-box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(-box_width/2, box_depth/2, -box_height/2)
    glVertex3f(-box_width/2, box_depth/2, box_height/2)
    glVertex3f(-box_width/2, -box_depth/2, box_height/2)
    glEnd()
    
    # Right face
    glBegin(GL_QUADS)
    glVertex3f(box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(box_width/2, box_depth/2, -box_height/2)
    glVertex3f(box_width/2, box_depth/2, box_height/2)
    glVertex3f(box_width/2, -box_depth/2, box_height/2)
    glEnd()
    
    # Bottom face
    glBegin(GL_QUADS)
    glVertex3f(-box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(box_width/2, -box_depth/2, -box_height/2)
    glVertex3f(box_width/2, box_depth/2, -box_height/2)
    glVertex3f(-box_width/2, box_depth/2, -box_height/2)
    glEnd()
    
    # Top Face
    glColor3f(0.5, 0.25, 0.08)
    glBegin(GL_QUADS)
    glVertex3f(-box_width/2, -box_depth/2, box_height/2)
    glVertex3f(box_width/2, -box_depth/2, box_height/2)
    glVertex3f(box_width/2, box_depth/2, box_height/2)
    glVertex3f(-box_width/2, box_depth/2, box_height/2)
    glEnd()
    
   
    draw_animated_locks(box_width, box_depth, keylock_size, keylock_spacing, keylock_z)
    
  
    if (game_won and not key_picked_up) or not game_won:
       
        key_length = box_width / 3 
        key_width = key_length / 5
        key_thickness = key_width / 2
 
        key_x = 0
        key_y = 0
        key_z = box_height/2 + key_thickness/2+7
        
        glPushMatrix()
        glTranslatef(key_x, key_y, key_z)
        #Key handle (circular part)
        glColor3f(0.9, 0.75, 0.0)  
        glPushMatrix()
        glTranslatef(-key_length/2 + key_width, 0, 0)
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(key_width/3, key_width, 12, 12)
        glPopMatrix()
        
        #Key shaft
        glPushMatrix()
        glScalef(key_length, key_width, key_thickness)
        glutSolidCube(1)
        glPopMatrix()
        
        #Key teeth
        teeth_count = 2
        teeth_spacing = key_length / (teeth_count + 2)
        
        for i in range(teeth_count):
            teeth_x = key_length/5 + (i * teeth_spacing)
            
            glPushMatrix()
            glTranslatef(teeth_x, 0, -key_thickness)
            glScalef(key_width/2, key_width, key_thickness)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()  
    
    glPopMatrix()  
    return False

def draw_key_in_hand():
    if key_picked_up:
        glPushMatrix()
        

        glTranslatef(character_pos[0], character_pos[1], 10)
        

        glRotatef(character_angle+180, 0, 0, 1)
        

        glTranslatef(30 * character_scale, 5 * character_scale, 10)

        glRotatef(100, 0, 0, 1)
        
        # Make key larger so it's more visible
        key_scale = 1.5
        glScalef(key_scale, key_scale, key_scale)
        
        # Key dimensions
        key_length = grid_size / 8 / 3
        key_width = key_length / 5
        key_thickness = key_width / 2

        glColor3f(1.0, 0.85, 0.0)  # Brighter gold
        
        # Key handle
        glPushMatrix()
        glTranslatef(-key_length/2 + key_width, 0, 0)
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(key_width/3, key_width, 12, 12)
        glPopMatrix()
        
        # Key shaft
        glPushMatrix()
        glScalef(key_length, key_width, key_thickness)
        glutSolidCube(1)
        glPopMatrix()
        
        # Key teeth
        teeth_count = 2
        teeth_spacing = key_length / (teeth_count + 2)
        
        for i in range(teeth_count):
            teeth_x = key_length/5 + (i * teeth_spacing)
            
            glPushMatrix()
            glTranslatef(teeth_x, 0, -key_thickness)
            glScalef(key_width/2, key_width, key_thickness)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()
def handle_key_interaction():
    if game_won and is_character_near_box() and not key_picked_up:
        if try_pickup_key():
            print("You picked up the key!")
            return True
    return False



# ========================================= KINFE ===============================================

def draw_knife():

    glPushMatrix()
    
    # Knife handle
    glColor3f(0.5, 0.25, 0.1)  # Dark brown wooden handle
    glPushMatrix()
    glScalef(0.5, 1.4, 0.5)  # Much wider and longer handle
    glutSolidCube(14)
    glPopMatrix()
    
    # Handle guard
    glColor3f(0.7, 0.6, 0.2)  # Brass-like guard
    glPushMatrix()
    glTranslatef(0, 10, 0)
    glScalef(0.9, 0.2, 0.7)  # Much larger guard
    glutSolidCube(14)
    glPopMatrix()
    
    # Knife blade
    glColor3f(0.8, 0.8, 0.8)  # Shiny silver blade
    glPushMatrix()
    glTranslatef(0, 18, 0)  # Position blade above handle

    glBegin(GL_TRIANGLES)
    # Front face of blade
    glVertex3f(0, 25, 0)      # Tip of blade (much longer)
    glVertex3f(-4, -8, 1.8)   # Bottom left (much wider)
    glVertex3f(4, -8, 1.8)    # Bottom right (much wider)
    
    # Back face of blade
    glVertex3f(0, 25, 0)      # Tip of blade
    glVertex3f(4, -8, -1.8)   # Bottom right
    glVertex3f(-4, -8, -1.8)  # Bottom left
    
    # Side faces
    # Right side
    glVertex3f(0, 25, 0)      # Tip
    glVertex3f(4, -8, 1.8)    # Bottom front
    glVertex3f(4, -8, -1.8)   # Bottom back
    
    # Left side
    glVertex3f(0, 25, 0)      # Tip
    glVertex3f(-4, -8, -1.8)  # Bottom back
    glVertex3f(-4, -8, 1.8)   # Bottom front
    
    # Bottom face
    glVertex3f(-4, -8, 1.8)   # Bottom front left
    glVertex3f(-4, -8, -1.8)  # Bottom back left
    glVertex3f(4, -8, 1.8)    # Bottom front right
    
    glVertex3f(4, -8, 1.8)    # Bottom front right
    glVertex3f(-4, -8, -1.8)  # Bottom back left
    glVertex3f(4, -8, -1.8)   # Bottom back right
    glEnd()
    
    # Blade edge highlight
    glColor3f(1.0, 1.0, 1.0)  # Bright white for edge highlight
    glBegin(GL_LINES)
    glVertex3f(0, 25, 0)      # Tip
    glVertex3f(4, -8, 1.8)    # Bottom right
    
    glVertex3f(0, 25, 0)      # Tip
    glVertex3f(-4, -8, 1.8)   # Bottom left
    
    # Add a center line down the blade for decoration
    glVertex3f(0, 25, 0)      # Tip
    glVertex3f(0, -8, 0)      # Center bottom
    glEnd()
    
    glPopMatrix()
    
    glPopMatrix()
# ========================================================================================
#----------------------------------------VILLIAN---------------------------------------------------------------------------------------------------------

def draw_spiral(radius=8, turns=3):
    glBegin(GL_LINE_STRIP)
    for i in range(100):
        angle = 2 * math.pi * turns * i / 100
        r = radius * i / 100
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()

def draw_villain_head():
    glPushMatrix()

    # Neck
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(0, 120, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 15, 12, 1)

    # Head (scaled sphere)
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(0, 0, 20)
    glRotatef(90, 1, 0, 0)
    glPushMatrix()
    glScalef(1.0, 1.3, 0.9)
    gluSphere(gluNewQuadric(), 28, 20, 20)
    glPopMatrix()

    # Spiral cheeks
    glColor3f(0.9, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(18, -10, 25)
    glScalef(0.8, 0.8, 0.8)
    draw_spiral()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-18, -10, 25)
    glScalef(0.8, 0.8, 0.8)
    draw_spiral()
    glPopMatrix()

    # Eyes: red sclera + black pupils
    for side in [10, -10]:
        glPushMatrix()

        glTranslatef(side, 0, 25)
        glColor3f(0, 0, 0)  # outside
        gluSphere(gluNewQuadric(), 8, 20, 20)

        glTranslatef(0, 0, 6)
        glColor3f(0.9, 0.1, 0.1)  # Red
        gluSphere(gluNewQuadric(), 5, 10, 5)

        glTranslatef(0, 0, 6)
        glColor3f(0, 0, 0)  # pupil
        gluSphere(gluNewQuadric(), 1.5, 10, 10)
        
        glPopMatrix()

    # Eyebrows
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 10, 28)
    for side, angle in [(10, -25), (-10, 25)]:
        glPushMatrix()
        glTranslatef(side, 0, 0)
        glRotatef(angle, 0, 0, -60)
        glScalef(10, 2, 2)
        glutSolidCube(1.7)
        glPopMatrix()
    glPopMatrix()

    # Nose
    glColor3f(0.75, 0.75, 0.75)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 3, 15, 8, 1)
    glPopMatrix()

    # Mouth - angular red smile
    
    glPushMatrix()
    glColor3f(0.9, 0.1, 0.1)
    glTranslatef(0, -5, 25)
    glLineWidth(3)
    glPopMatrix()

    # # Optional jaw piece
    glColor3f(0.9, 0, 0)
    glPushMatrix()
    glTranslatef(0, -25, 4)
    glScalef(1.2, 0.5, 1.0)
    glutSolidCube(20)
    glPopMatrix()

    # Red bow tie
    glPushMatrix()
    glTranslatef(0, -40, 20)
    glColor3f(0.9, 0.1, 0.1)
    glPushMatrix()
    glScalef(5, 5, 5)
    glutSolidCube(1)
    glPopMatrix()
    for side, angle in [(-10, 20), (10, -20)]:
        glPushMatrix()
        glTranslatef(side, 0, 0)
        glRotatef(angle, 0, 0, 1)
        glScalef(15, 7, 3)
        glutSolidCube(1)
        glPopMatrix()
    glPopMatrix()

    glPopMatrix()
def draw_villain_torso():
    glPushMatrix()
    
    # Main torso - black suit
    glColor3f(0.1, 0.1, 0.1)  # Black suit
    glTranslatef(0, 60, 0)  # Position torso above ground
    
    # Suit jacket
    glPushMatrix()
    glScalef(1.1, 1.5, 0.6)  # Wide shoulders, slightly thinner
    glutSolidCube(50)
    glPopMatrix()
    
    # White shirt beneath
    glColor3f(0.9, 0.9, 0.9)  # White shirt
    glPushMatrix()
    glTranslatef(0, 0, 3)  # Slightly in front of jacket
    glScalef(0.5, 1.4, 0.1)
    glutSolidCube(50)
    glPopMatrix()
    
    # Suit lapels
    glColor3f(0.1, 0.1, 0.1)  # Black lapels
    
    # Left lapel
    glPushMatrix()
    glTranslatef(-12, 10, 4)
    glRotatef(-20, 1, 0, 0)
    glRotatef(-10, 0, 0, 1)
    glScalef(0.3, 0.7, 0.1)
    glutSolidCube(50)
    glPopMatrix()
    
    # Right lapel
    glPushMatrix()
    glTranslatef(12, 10, 4)
    glRotatef(-20, 1, 0, 0)
    glRotatef(10, 0, 0, 1)
    glScalef(0.3, 0.7, 0.1)
    glutSolidCube(50)
    glPopMatrix()
    
    glPopMatrix()

def draw_villain_arm(side_factor):
    global animation_counter, stabbing_animation, stabbing_progress
    glPushMatrix()
    

    glTranslatef(side_factor * 35, 90, 0)
    
    # Suit sleeve (upper arm)
    glColor3f(0.1, 0.1, 0.1)  # Black suit
    
 
    base_arm_angle = 20 * side_factor  # Base angle for arms

    if side_factor == 1 and stabbing_animation:  # Right arm with stabbing animation
        # Single stab motion that extends forward
        if not stab_complete:
            # For the thrusting motion - from 0 to 45 degrees
            stab_factor = min(1.0, stabbing_progress / 15.0)
            arm_rotation = base_arm_angle - 60 * stab_factor
            elbow_rotation = -30 * stab_factor
        else:
            
            arm_rotation = base_arm_angle - 60
            elbow_rotation = -30
        
        
       
        glRotatef(arm_rotation, 1, 0, 0)
    else:
       
        glRotatef(base_arm_angle, 0, 0, 1)  # Angle arms slightly outward
    
    # Upper arm
    glPushMatrix()
    glScalef(0.5, 1, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    
    # Elbow joint
    glTranslatef(0, -25, 0)
    
  
    if side_factor == 1 and stabbing_animation:  # Right arm with stabbing animation
        glRotatef(20 + elbow_rotation, 1, 0, 0)  # Apply additional elbow rotation during stab
    else:
        glRotatef(20, 1, 0, 0)  # Regular angle
    
    glPushMatrix()
    glScalef(0.4, 1, 0.4)
    glutSolidCube(30)
    glPopMatrix()
    
    # Hand - white gloves
    glTranslatef(0, -20, 0)
    glColor3f(0.9, 0.9, 0.9)  # White gloves
    gluSphere(gluNewQuadric(), 8, 10, 10)
    
   
    if side_factor == 1:  # Right arm
        glPushMatrix()
        # Position knife in hand
        glTranslatef(0, 0, 0)
        
        # Rotate knife to be vertical - adjust for stabbing animation
        if stabbing_animation:
            glRotatef(90, 1, 0, 0)  # More horizontal for stabbing
        else:
            glRotatef(110, 1, 0, 0)  # Normal position
            
        glRotatef(10, 0, 0, 1)    # Slight angle to side
        glScalef(0.8, 0.8, 0.8)   # Scale knife appropriately
        draw_knife()
        glPopMatrix()
    
    glPopMatrix()

def draw_villain_leg(side_factor):
   
    glPushMatrix()
    
    # Hip joint position
    glTranslatef(side_factor * 15, 30, 0)
    
    # Upper leg - black pants
    glColor3f(0.1, 0.1, 0.1)  # Black pants
    
    # Upper leg
    glPushMatrix()
    glScalef(0.5, 1, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    
    # Knee joint
    glTranslatef(0, -25, 0)
    
    # Lower leg
    glPushMatrix()
    glScalef(0.4, 1, 0.4)
    glutSolidCube(30)
    glPopMatrix()
    
    # Foot - black dress shoes
    glTranslatef(0, -20, 5)
    glColor3f(0.05, 0.05, 0.05)  
    glPushMatrix()
    glScalef(1.1, 0.4, 1.8)  
    glutSolidCube(12)
    glPopMatrix()
    
    glPopMatrix()

def draw_villain():
    
    glPushMatrix()
    glScalef(0.8, 0.8, 0.8)
    
    
    glTranslatef(villain_pos[0], villain_pos[1], villain_pos[2]+20)
    
    glRotatef(villain_angle, 0, 0, 1)  # Rotate around Z-axis for XY plane movement
    glRotatef(90, 1, 0, 0)
    
    draw_villain_torso()
    draw_villain_head()
    draw_villain_arm(1)    # Right arm (with knife)
    draw_villain_arm(-1)   # Left arm
    draw_villain_leg(1)    # Right leg
    draw_villain_leg(-1)   # Left leg
    
    glPopMatrix()

def update_villain():
    """Update villain position and state"""
    global villain_pos, villain_angle, villain_state, stabbing_animation, stabbing_progress
    
    if move_villain:
        
        dx = character_pos[0] - villain_pos[0]
        dy = character_pos[1] - villain_pos[1]
        dz = character_pos[2] - villain_pos[2]
        
        
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
      
        if game_over and distance < 5:
            stabbing_animation = True
            
            stabbing_progress += 1
            return
        
        if distance < 900:  
            
            target_angle = math.degrees(math.atan2(dx, dz))
            

            angle_diff = (target_angle - villain_angle) % 360
            if angle_diff > 270:
                angle_diff -= 360
                
           
            max_rotation = 3.0
            if abs(angle_diff) > max_rotation:
             
                angle_change = max_rotation if angle_diff > 0 else -max_rotation
            else:
              
                angle_change = angle_diff
                
          
            rotation_speed = 1.5 
            villain_angle += angle_change * rotation_speed
            
            villain_angle = villain_angle % 360
            
           
            if distance > 2:  
                villain_state = 1 
                
                move_speed = 4.0
                total_dist = math.sqrt(dx*dx + dy*dy + dz*dz)  
                norm_dx = dx / total_dist
                norm_dy = dy / total_dist
               
                
                villain_pos[0] += move_speed * norm_dx
                villain_pos[1] += move_speed * norm_dy  
                villain_pos[2] += 0
            else:
                villain_state = 2  
                if game_over:
                    stabbing_animation = True
        else:
            villain_state = 0  # Idle state
# ================================================================================
def check_villain_character_collision():

    global villain_pos, character_pos, character_scale, game_over
    
    character_size = [5 * character_scale, 15 * character_scale, 5 * character_scale]
    villain_size = [5 * 0.8, 15 * 0.8, 5 * 0.8] 
    

    character_pos_adjusted = [
        character_pos[0],
        character_pos[1],
        character_pos[2] + (character_size[1] / 2) 
    ]
    

    villain_pos_adjusted = [
        villain_pos[0],
        villain_pos[1],
        villain_pos[2] + (villain_size[1] / 2)  
    ]
    
    return check_collision(
        character_pos_adjusted, character_size,
        villain_pos_adjusted, villain_size
    )

#---------------------------------hero---------------------------------------------------------------------------
def draw_head():
   
    glPushMatrix()
    
    # Neck
    glColor3f(0.9, 0.7, 0.6)
    glTranslatef(0, 120, 0)  # Position neck on top of torso
    glRotatef(-90, 1, 0, 0)  # Rotate to align with y-axis
    gluCylinder(gluNewQuadric(), 10, 10, 15, 12, 1)
    
    # Head
    if not hide_player_head:
        glColor3f(*HEAD_COLOR)
        glTranslatef(0, 0, 10)  # Move up to position head
        gluSphere(gluNewQuadric(), 25, 20, 20)  # Head sphere
    
    # Eyes
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # White eyes
    glTranslatef(10, -20, 0)
    gluSphere(gluNewQuadric(), 5, 10, 10)
    glColor3f(0.0, 0.0, 0.0)  # Black pupils
    glTranslatef(0, -3, 0)
    gluSphere(gluNewQuadric(), 2.5, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # White eyes
    glTranslatef(-10, -20, 0)
    gluSphere(gluNewQuadric(), 5, 10, 10)
    glColor3f(0.0, 0.0, 0.0)  # Black pupils
    glTranslatef(0, -3, 0)
    gluSphere(gluNewQuadric(), 2.5, 10, 10)
    glPopMatrix()
    
    # Mouth
    glColor3f(0.8, 0.3, 0.3)
    glTranslatef(0, -10, -16)
    glScalef(10, -5, 5)
    glutSolidCube(2)
    
    glPopMatrix()

def draw_torso():
    
    glPushMatrix()
    
    glColor3f(*TORSO_COLOR)
    glTranslatef(0, 60, 0)  
    glScalef(1.1, 1.5, 0.8)  
    glutSolidCube(50)       
    
    glPopMatrix()

def draw_arm(side_factor):
    glPushMatrix()
    
    # Shoulder joint position
    glTranslatef(side_factor * 30, 90, 0)
    
    # Upper arm
    glColor3f(*ARM_COLOR)
    glRotatef(30 * side_factor * math.sin(animation_counter / 10), 1, 0, 0) 
    glTranslatef(0, -20, 0)  
    
    # Upper arm
    glPushMatrix()
    glScalef(0.5, 1, 0.5)
    glutSolidCube(40)
    glPopMatrix()
    
    # Elbow joint
    glTranslatef(0, -25, 0)
    
    # Lower arm
    glRotatef(20 * side_factor * math.sin(animation_counter / 10 + 0.5), 1, 0, 0) 
    glPushMatrix()
    glScalef(0.4, 1, 0.4)
    glutSolidCube(30)
    glPopMatrix()
    
    # Hand
    glTranslatef(0, -20, 0)
    glColor3f(*HEAD_COLOR)  # Skin tone for hands
    gluSphere(gluNewQuadric(), 8, 10, 10)
    
    glPopMatrix()

def draw_leg(side_factor):
    
    glPushMatrix()
    
    # Hip joint position
    glTranslatef(side_factor * 15, 30, 0)
    
    # Upper leg
    glColor3f(*LEG_COLOR)
    glRotatef(-30 * side_factor * math.sin(animation_counter / 10), 1, 0, 0)  
    # Upper leg
    glPushMatrix()
    glScalef(0.5, 1, 0.5)
    glColor3f(0.2,0.2,0.4)
    glutSolidCube(40)
    glPopMatrix()
    
    # Knee joint
    glTranslatef(0, -25, 0)
    
    # Lower leg
    glRotatef(-20 * side_factor * math.sin(animation_counter / 10 + 0.5), 1, 0, 0)  
    glPushMatrix()
    glScalef(0.8, 1, 0.4)
    glutSolidCube(30)
    glPopMatrix()
    
    # Foot
    glTranslatef(0, -20, 5)
    glColor3f(*FOOT_COLOR)
    glPushMatrix()
    glScalef(1.2, 0.5, 1.5)
    glutSolidCube(12)
    glPopMatrix()
    
    glPopMatrix()

def draw_character():
    global character_scale, remaining_limbs, move_villain, character_fallen

    glPushMatrix()
    glScalef(character_scale, character_scale, character_scale)

    glTranslatef(character_pos[0]/character_scale, character_pos[1]/character_scale, 0.1/character_scale+20)
    if check_villain_character_collision():
        character_fallen = True
        glTranslatef(0, 0, 12)
        glRotatef(180, 1, 0, 0)   
     
    else:
        
        glRotatef(character_angle, 0, 0, 1)  
        glRotatef(90, 1, 0, 0)   

    draw_torso()
    draw_head()
    
  
    draw_limbs(remaining_limbs, character_fallen)


    glPopMatrix()
    
def draw_limbs(limb_count, is_fallen):
    
        if limb_count >= 4:
            draw_arm(-1.2)  
        if limb_count >= 3:
            draw_arm(1.2)  
        if limb_count >= 2:
            draw_leg(-1)    
        if limb_count >= 1:
            draw_leg(1)     


def update_character():
   
    global character_pos, character_angle, animation_counter, character_scale,last_valid_pos, stop_motion

    if not check_character_box_collision():
        last_valid_pos = character_pos.copy()
    
    if not stop_motion:
        if moving_forward or moving_backward:
            animation_counter += 1.5
    
  
    original_pos = character_pos.copy()
    
    
    movement_speed = 3.5
    if not stop_motion:
        if moving_forward:
            
            character_pos[0] += movement_speed * math.cos(math.radians(character_angle+270))
            character_pos[1] += movement_speed * math.sin(math.radians(character_angle+270))
        if moving_backward:
            character_pos[0] -= movement_speed * math.cos(math.radians(character_angle+270))
            character_pos[1] -= movement_speed * math.sin(math.radians(character_angle+270))
        
      
        rotation_speed = 3.0
        if turning_left:
            character_angle += rotation_speed
        if turning_right:
            character_angle -= rotation_speed
    
    
    margin = max(30 * character_scale, 30)  
    grid_limit = grid_size - margin
    

    if character_pos[0] < margin or character_pos[0] > grid_limit or \
    character_pos[1] < margin or character_pos[1] > grid_limit:
       
        character_pos = original_pos.copy()
    if check_character_box_collision():
        handle_box_collision()
#------------------------------------------------------------------------------Settings-------------------------------------------
def idle():
    global last_valid_pos,character_pos,game_over, stop_motion

    
    
    glutPostRedisplay()
    
    
    update_character()
    update_villain()
    if check_villain_character_collision():
            stop_motion = True
    # Enable depth testing for correct rendering of overlapping objects
    glEnable(GL_DEPTH_TEST)
    

    # =======================================================
def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  # Reset the projection matrix
   
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ratio is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

        
    if first_person_view:

        cam_x = character_pos[0]
        cam_y = character_pos[1] 
        cam_z = character_pos[2]+ 134 

        look_angle_rad = math.radians(character_angle + 270)

        
        l_x = cam_x + math.cos(look_angle_rad)
        l_y = cam_y + math.sin(look_angle_rad)
        l_z = cam_z  
        
        gluLookAt(cam_x, cam_y, cam_z,
                l_x, l_y, l_z,
                0, 0, 1)  
        
    else:
       
        x, y, z = camera_pos
        gluLookAt(x, y, z,          
            300, 200, 0,     
            0, 0, 1)      
       
    # ========================================================================

def showScreen():
    global game_over, hero_life, game_score, missing_bullet, camera_pos, cheat_mode
    global quiz_active, current_question, timer_start, selected_option
    global game_over_quiz, near_tv, move_villain, remaining_limbs, pending_limb_cut
    global saw_picked_up,last_valid_pos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    if show_menu:
        draw_background_image("new_bg.jpg", scale=1.2)


        glDisable(GL_DEPTH_TEST) 

        
        glColor3f(0.1, 0.1, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(400, 350)
        glVertex2f(600, 350)
        glVertex2f(600, 420)
        glVertex2f(400, 420)
        glEnd()

        
        draw_text(440, 275, "START GAME", GLUT_BITMAP_TIMES_ROMAN_24, [1, 0, 0])

        glEnable(GL_DEPTH_TEST)
        glutSwapBuffers()
        return

    setupCamera() 
    
    
    check_tv_proximity()
    
   
    grid()
    
    draw_sink(300,565)
    draw_sink(200,565)
    draw_pipes()
    draw_saw()
    initialize_box_properties()
    update_magical_box()
    modified_createMagicalBox()
    if key_picked_up and door_gone==False:
        draw_key_in_hand()
    draw_tv(-90)
    TV_box()
    draw_villain()
    draw_character()
    
   
    if quiz_active:
      
        elapsed_time = time.time() - timer_start
        remaining_time = max(0, 15 - int(elapsed_time))
        
        if remaining_time == 0 and not game_over_quiz or game_over==True :
            # Time's up!
            game_over_quiz = True
            
            move_villain = True
            draw_text(400, 600,"GAME OVER", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
        
        # =================================================
        elif game_over and game_won==False:
            draw_text(400, 600,"GAME OVER", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
            
            if not stabbing_animation:
                move_villain = True
            
          
        # =================================================

        elif game_over_quiz or game_over:
            draw_text(800, 750, f"Time: {remaining_time}s", GLUT_BITMAP_HELVETICA_18)
            if remaining_time == 0:
                
                move_villain = True
                game_over = True
                draw_text(400, 600,"GAME OVER", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
            else:
                if pending_limb_cut:
                    draw_text(400, 600,"Cut One of your limbs", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
        else:
            
            question = quiz_questions[current_question]
            
           
            draw_text(800, 750, f"Time: {remaining_time}s", GLUT_BITMAP_HELVETICA_18)
            
            
            draw_text(100, 700, f"Question {current_question + 1}: {question['question']}", GLUT_BITMAP_HELVETICA_18)
          
            y_pos = 600
            for i, option in enumerate(question["options"]):
                draw_text(120, y_pos, option, GLUT_BITMAP_HELVETICA_18)
                y_pos -= 50
            draw_text(400, 600, "Select an answer & SPACE to submit", GLUT_BITMAP_HELVETICA_18, [1,0,1])
    elif remaining_limbs==0 :
            game_over=True
            draw_text(400, 600,"GAME OVER", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
   
    if pending_limb_cut and game_over == False:
        if saw_picked_up:
            draw_text(400, 650, "Press 'c' to cut a limb!", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
        else:
            draw_text(400, 650, "Go to the saw and press 'p' to pick it up!", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
            
          
            if is_character_near_saw():
                draw_text(400, 620, "You are near the saw! Press 'p'", GLUT_BITMAP_HELVETICA_18, [0.0, 1.0, 0.0])
    
    if game_won and game_over==False and door_gone==False:
        draw_text(200, 600, "Congratulations! You won the game. Find the box and press 'k' to pick up the key!", GLUT_BITMAP_HELVETICA_18, [0,0,1])
    elif game_over and game_won==False:
         draw_text(400, 600,"GAME OVER", GLUT_BITMAP_HELVETICA_18, [1.0, 0.0, 0.0])
    elif door_gone==True and game_won and game_over==False:
        draw_open_door(grid_size/2, 0, True)
        print("!!!!!!!!!!!!You are Free!!!!!!!!!!!")
        
    glutSwapBuffers()
def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos

    if key == GLUT_KEY_UP:
        x+=5

    if key == GLUT_KEY_DOWN:
        x-=5 

    if key == GLUT_KEY_LEFT:
        y -= 10
         
    if key == GLUT_KEY_RIGHT:
        y += 10  
        
    camera_pos = (x, y, z)
def mouseListener(button, state, x, y):
    global camera_pos, quiz_active, timer_start, current_question, selected_option, game_over_quiz
    global GRID_LENGTH  
    
    global show_menu, game_started

    if show_menu:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if 400 <= x <= 600 and 280 <= (800 - y) <= 320:
                print("Start button clicked!")
                show_menu = False
                game_started = True
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        if 280 <= x <= 300 and 420 <= y <= 440:
            print("TV power button clicked! Starting quiz...")  
            quiz_active = True
            timer_start = time.time()
            current_question = 0
            selected_option = -1
            game_over_quiz = False
        
        
        elif not quiz_active and 450 <= x <= 650 and 450 <= y <= 600 and game_over==False and game_won==False:
            print("TV area clicked! Starting quiz...")  
            quiz_active = True
            timer_start = time.time()
            current_question = 0
            selected_option = -1
            game_over_quiz = False
        
       
        elif quiz_active and not game_over_quiz:
            if 100 <= x <= 500:
                
                option_height = 600
                for i in range(4):
                    if option_height - 15 <= (800 - y) <= option_height + 15:
                        selected_option = i
                        print(f"Selected option {i+1}")
                    option_height -= 50
    
   
    x_cam, y_cam, z_cam = camera_pos
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        z_cam -= 30
    camera_pos = (x_cam, y_cam, z_cam)


def keyboardListener(key, x, y):
    global moving_forward, moving_backward, turning_left, turning_right, camera_mode
    global camera_angle_offset, camera_height, camera_distance
    global quiz_active, current_question, timer_start, selected_option, game_over_quiz, near_tv
    global first_person_view, hide_player_head
    global game_won, key_picked_up, stop_motion
    global pending_limb_cut, remaining_limbs, character_fallen, saw_picked_up
    global current_question, timer_start, game_over_quiz, quiz_questions, game_over

    if key == b'x' :
        
        if check_character_door_collision(door_pos, is_door_on_x_wall):
            handle_door_interaction(door_pos, is_door_on_x_wall)
            elapsed_time = time.time() - timer_start
            remaining_time = max(0, 5 - int(elapsed_time))
            if remaining_time==0 and key_picked_up:
                glutLeaveMainLoop()

    if key == b'w':
        moving_forward += 1
    elif key == b's':
        moving_backward -= 1
    
    elif key == b'a':
        turning_left = True
    elif key == b'd':
        turning_right = True

    elif key == b'f':
        first_person_view = not first_person_view
        hide_player_head = first_person_view
    
   
    elif key == b'k':
        
        if handle_key_interaction():
            print("You picked up the key!")
        elif is_character_near_box() and not game_won:
            print("Complete the quiz first to unlock the key!")
        elif key_picked_up:
            print("You already have the key!")
        else:
            print("You need to be closer to the box to pick up the key.")
    
    elif key == b'p':
        if pending_limb_cut and is_character_near_saw() and not saw_picked_up and game_over == False:
            saw_picked_up = True
            print("You picked up the saw! Press 'c' to cut a limb.")
        elif saw_picked_up and game_over == False:
            print("You already have the saw!")
        elif not pending_limb_cut and game_over == False:
            print("You don't need the saw right now.")
        elif game_over == False:
            print("You need to be closer to the saw to pick it up.")
    
    elif key == b'c':
        if saw_picked_up and pending_limb_cut and remaining_limbs > 0 and game_over == False:
            remaining_limbs -= 1
            pending_limb_cut = False
            saw_picked_up = False
            quiz_active = True  
            game_over_quiz = False  
            timer_start = time.time() 

            print(f"Limb cut! Remaining limbs: {remaining_limbs}")

            if remaining_limbs == 0:
                character_fallen = True
                stop_motion = True
                game_over_quiz = True
                game_over = True
                quiz_active = False
                print("All limbs lost. Game Over!")
            elif current_question < len(quiz_questions) - 1:
                current_question += 1  
            else:
                quiz_active = False
                game_won = True
                print("Quiz complete! You survived.")
        elif pending_limb_cut and not saw_picked_up and game_over == False:
            print("You need to pick up the saw first! Get near the saw and press 'p'.")
        elif not pending_limb_cut and game_over == False:
            print("You don't need to cut a limb right now.")
    

    elif key == b' ' and quiz_active and not game_over_quiz:  
        if selected_option != -1:
            if selected_option == quiz_questions[current_question]["correct_answer"]:
                
                current_question += 1
                selected_option = -1
                timer_start = time.time()  
                
                if current_question >= len(quiz_questions):
                    
                    quiz_active = False
                    game_won = True  
                    
            else:
             
                
                pending_limb_cut = True  

                game_over_quiz = True
                
                if remaining_limbs <= 0:
                    game_over_quiz = True
                    character_fallen = True
                    move_state = True
                    stop_motion = True
                    game_over_time = time.time()
                    glRotatef(180, 0, 1, 0)

def keyboardUpListener(key, x, y):
    """Handles keyboard key releases"""
    global moving_forward, moving_backward, turning_left, turning_right
  
    if key == b'w':
        moving_forward = False
    elif key == b's':
        moving_backward = False
    elif key == b'a':
        turning_left = False
    elif key == b'd':
        turning_right = False
          
  
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    glutCreateWindow(b"SAW")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener) 
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)

    glutIdleFunc(idle) 
    glutMainLoop() 
    
if __name__ == "__main__":
    main()