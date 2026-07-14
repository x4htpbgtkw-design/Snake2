import turtle
import random
import json
import os

# Game settings configuration constants
DELAY = 100  # Frame refresh delay rate in milliseconds (lower = faster game)
score = 0

# --- High Score Persistence ---
def load_high_score():
    if os.path.exists("highscore.json"):
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0
    else:
        return 0

def save_high_score(value):
    with open("highscore.json", "w") as f:
        json.dump({"high_score": value}, f)

high_score = load_high_score()
colors = []

# Set up the screen canvas layout configuration
screen = turtle.Screen()
screen.title("Lag-Free Retro Snake")
screen.bgcolor("#1A1A24")
screen.setup(width=600, height=600)
screen.tracer(0)  # Stop automatic updates for manual refresh management

# 1. Create the Game Objects
head = turtle.Turtle("square")
head.color("#00FF66")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle("circle")
food.color("#FF3366")
food.penup()
food.goto(0, 100)

segments = []
current_direction = "stop"  # Visual tracking variable to lock fast key inputs

# 2. Scoreboard Setup
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)

def randomColor():
    """Generates a random 6-character hex color string starting with #."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

def update_scoreboard():
    scoreboard.clear()
    scoreboard.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 20, "bold"))

update_scoreboard()

# 3. Input Direction Controls with Lock Guard Prevention
def go_up():
    global current_direction
    if current_direction != "down":
        head.direction = "up"

def go_down():
    global current_direction
    if current_direction != "up":
        head.direction = "down"

def go_left():
    global current_direction
    if current_direction != "right":
        head.direction = "left"

def go_right():
    global current_direction
    if current_direction != "left":
        head.direction = "right"

def Quit():
    screen.bye()

# Bind key inputs
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(Quit, "q")

def reset_game():
    global score, current_direction
    head.goto(0, 0)
    head.direction = "stop"
    current_direction = "stop"
    
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    
    score = 0
    update_scoreboard()

# 4. Main Event Loop Engine Driven by Timer Interrupt Clock Channel
def game_loop():
    global score, high_score, current_direction
    
    if head.direction == "stop":
        screen.update()
        screen.ontimer(game_loop, DELAY)
        return

    current_direction = head.direction

    # Tail movement
    for index in range(len(segments) - 1, 0, -1):
        segments[index].goto(segments[index - 1].xcor(), segments[index - 1].ycor())

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Move head
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

    # Boundary collision
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()
        screen.update()
        screen.ontimer(game_loop, DELAY)
        return

    # Self collision
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()
            screen.update()
            screen.ontimer(game_loop, DELAY)
            return

    # Food collision
    if head.distance(food) < 20:
        food.goto(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)

        new_segment = turtle.Turtle("square")
        new_segment.color(randomColor())
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        update_scoreboard()

    screen.update()
    screen.ontimer(game_loop, DELAY)

# Run the game loop
game_loop()
screen.mainloop()
