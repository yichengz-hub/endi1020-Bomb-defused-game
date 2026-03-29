import time
import random
from pynput import keyboard
from LCDDriver import LCDDriver

# Setup Driver
lcd = LCDDriver('/dev/tty.usbserial-0001', width=240, height=280)

# --- COLOR CALIBRATION ---
# If your background is black, BG_COL must be 0. 
# If it's still leaving white marks, try BG_COL = 10 or 15.
DOT_COL, PLAYER_COL, GOAL_COL, BG_COL = 1, 3, 2, 0 
GRID_STEP = 40  
OFFSET_X, OFFSET_Y = 20, 40 
SIZE = 6 

MAZES = [
    {"id": 1, "circles": [(0,1), (5,2)], "walls": ["v01", "v12", "h10", "h11", "v30", "v31", "v32", "h03", "h13", "h23"]},
    {"id": 2, "circles": [(1,3), (4,1)], "walls": ["h11", "h21", "h31", "v11", "v12", "v32", "v33", "h44", "h54"]},
    {"id": 3, "circles": [(4,3), (5,3)], "walls": ["v10", "v11", "v12", "v13", "v14", "v30", "v31", "v32", "v33", "h24", "h34"]},
    {"id": 4, "circles": [(0,0), (0,3)], "walls": ["h10", "h20", "v21", "v22", "v23", "v30", "v31", "h43", "h53"]},
    {"id": 5, "circles": [(4,2), (3,5)], "walls": ["v10", "v11", "v12", "v13", "v14", "h23", "h33", "h43", "h53", "v44", "v45"]},
    {"id": 6, "circles": [(5,0), (3,4)], "walls": ["v10", "v11", "v12", "v31", "v32", "v33", "h23", "h33", "v42", "v43", "v44"]},
    {"id": 7, "circles": [(1,0), (1,5)], "walls": ["h12", "h22", "h32", "v23", "v24", "v25", "v41", "v42", "v54", "v55"]},
    {"id": 8, "circles": [(3,0), (2,3)], "walls": ["v11", "v12", "v13", "v14", "h22", "h32", "h42", "v30", "v31", "h44", "h54"]},
    {"id": 9, "circles": [(2,1), (0,5)], "walls": ["v10", "v11", "v12", "v13", "h21", "h31", "v33", "v34", "v35", "h42", "h52"]}
]

current_maze = random.choice(MAZES)
gx, gy = 0, 0 
keys_pressed = set()

def on_press(key):
    try: keys_pressed.add(key.char.lower())
    except: pass
def on_release(key):
    try: keys_pressed.remove(key.char.lower())
    except: pass

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def get_coords(tx, ty):
    return OFFSET_X + (tx * GRID_STEP), OFFSET_Y + (ty * GRID_STEP)

def draw_player(tx, ty, color):
    sx, sy = get_coords(tx, ty)
    # Renders triangle at dot
    lcd._send_triangle(sx, sy-SIZE, sx-SIZE, sy+SIZE, sx+SIZE, sy+SIZE, color)

def draw_single_dot(tx, ty, color):
    sx, sy = get_coords(tx, ty)
    lcd._send_rect(sx-1, sy-1, 2, 2, color)

def refresh_node(tx, ty):
    """Cleanly restores a node without leaving boxes."""
    # 1. Erase Triangle by drawing it in Background color
    draw_player(tx, ty, BG_COL)
    # 2. Put the dot back
    draw_single_dot(tx, ty, DOT_COL)
    # 3. If it's a goal node, redraw the circle around it
    if (tx, ty) in current_maze['circles']:
        sx, sy = get_coords(tx, ty)
        lcd._send_rect(sx-8, sy-8, 16, 2, GOAL_COL)
        lcd._send_rect(sx-8, sy+6, 16, 2, GOAL_COL)
        lcd._send_rect(sx-8, sy-8, 2, 16, GOAL_COL)
        lcd._send_rect(sx+6, sy-8, 2, 16, GOAL_COL)

def init_game():
    global gx, gy, current_maze
    lcd.clear()
    # Draw all dots
    for ix in range(6):
        for iy in range(6):
            draw_single_dot(ix, iy, DOT_COL)
    
    # Spawn far from goal
    possible = []
    for tx in range(6):
        for ty in range(6):
            if min(abs(tx-cx)+abs(ty-cy) for cx,cy in current_maze['circles']) >= 3:
                possible.append((tx,ty))
    
    gx, gy = random.choice(possible)
    # Draw goals and player
    for cx, cy in current_maze['circles']:
        refresh_node(cx, cy)
    draw_player(gx, gy, PLAYER_COL)

lcd.init_screen(240, 280)
init_game()

try:
    while True:
        if 'r' in keys_pressed:
            current_maze = random.choice(MAZES)
            init_game()
            time.sleep(0.5)

        nx, ny = gx, gy
        move_key = None
        if 'w' in keys_pressed: ny -= 1; move_key = 'w'
        elif 's' in keys_pressed: ny += 1; move_key = 's'
        elif 'a' in keys_pressed: nx -= 1; move_key = 'a'
        elif 'd' in keys_pressed: nx += 1; move_key = 'd'

        if move_key:
            # Check move valid logic
            is_valid = False
            if 0 <= nx <= 5 and 0 <= ny <= 5:
                wall = f"v{gx}{gy}" if nx > gx else f"v{nx}{ny}" if nx < gx else f"h{gx}{gy}" if ny > gy else f"h{nx}{ny}"
                if wall not in current_maze['walls']:
                    is_valid = True
            
            if is_valid:
                # REFRESH OLD POSITION (Erase triangle)
                refresh_node(gx, gy)
                
                gx, gy = nx, ny
                
                # DRAW NEW POSITION
                draw_player(gx, gy, PLAYER_COL)

                if (gx, gy) in current_maze['circles']:
                    lcd.clear()
                    lcd.draw_text(60, 120, "SOLVED", size=3, color=GOAL_COL)
                    time.sleep(2)
                    current_maze = random.choice(MAZES)
                    init_game()
            
            time.sleep(0.2)
        time.sleep(0.01)

except KeyboardInterrupt:
    listener.stop()