import turtle
from turtle import Turtle, Screen
import random

# Create Screen

window = Screen()
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)

window.register_shape('ship1.gif')
window.register_shape('alien4.gif')

# Set Score

score = 0

score_board = Turtle()
score_board.speed(0)
score_board.color('white')
score_board.penup()
score_board.setposition(-290, 280)
score_total = f"Score: {score}"
game_over = f"Score: {score}            GAME OVER!"
score_board.write(score_total, False, align="left", font=('arial', 18, 'normal'))
score_board.hideturtle()

# Create Ship

ship = Turtle()
ship.shape('ship1.gif')
ship.penup()
ship.speed(0)
ship.setposition(0, -250)

# Create Laser

laser = Turtle()
laser.color("white")
laser.shape("circle")
laser.shapesize(0.2, 0.2)
laser.penup()
laser.speed(0)
laser.hideturtle()
laser_speed = 1
laser_state = 'ready'

# Create Enemy Fire

torpedo = turtle.Turtle()
torpedo.color('yellow')
torpedo.speed(6)
torpedo.up()
torpedo.shape('square')
torpedo.shapesize(0.15, 0.6)
torpedo.lt(90)
torpedo.goto(1000, 1000)
torpedo_state = 'ready'


# Move Ship

def move_left():
    x = ship.xcor()
    x -= 15
    if x < -350:
        x = -350
    ship.setx(x)


def move_right():
    x = ship.xcor()
    x += 15
    if x > 350:
        x = 350
    ship.setx(x)


def shoot():
    global laser_state
    if laser_state == "ready":
        laser_state = "fire"
        x = ship.xcor()
        y = ship.ycor()
        laser.setposition(x, y + 15)
        laser.showturtle()


def enemy_laser():
    global torpedo_state
    for a in aliens:
        x = random.random()
        if x < 0.2 and torpedo_state == 'ready':
            torpedo_state = 'fire'
            torpedo.goto(a.xcor(), a.ycor() - 20)


def collision(t1, t2):
    if t1.distance(t2) < 20:
        return True
    else:
        return False


# Create multiple aliens

aliens = []

x_list = [-260, -210, -160, -110, -60, -10, 40, 90, 140]
y_list = [250, 200, 150]

alien_speed = 0.08

for i in x_list:
    for j in y_list:
        alien = turtle.Turtle()
        alien.color('red')
        alien.s = 'alien4.gif'
        alien.shape(alien.s)
        alien.up()
        alien.speed(0)
        alien.goto(i, j)
        alien.dx = alien_speed
        aliens.append(alien)

window.listen()
window.onkeypress(move_right, 'Right')
window.onkeypress(move_left, 'Left')
window.onkey(shoot, "space")

# Game Loop
game_on = True
while game_on:
    window.update()
    enemy_laser()
    if len(aliens) == 0:
        score_board.clear()
        score_board.write(game_over, False, align="left", font=('arial', 18, 'normal'))
        game_on = False
        break

    # Alien Movement
    for alien in aliens:

        x = alien.xcor()
        x += alien_speed
        alien.setx(x)

        if alien.xcor() > 300:
            for a in aliens:
                y = a.ycor()
                y -= 40
                a.sety(y)
            alien_speed *= -1

        if alien.xcor() < -300:
            for a in aliens:
                y = a.ycor()
                y -= 40
                a.sety(y)
            alien_speed *= -1

        if collision(laser, alien):
            laser.hideturtle()
            laser_state = "ready"
            laser.goto(1000, 1000)
            alien.goto(1000, 1000)
            aliens.remove(alien)
            score += 1
            score_total = f"Score: {score}"
            score_board.clear()
            score_board.write(score_total, False, align="left", font=('arial', 18, 'normal'))

        if collision(ship, alien):
            ship.hideturtle()
            alien.hideturtle()
            game_over = f"Score: {score}            GAME OVER!"
            score_board.clear()
            score_board.write(game_over, False, align="left", font=('arial', 18, 'normal'))
            game_on = False
            break

        if collision(ship, torpedo):
            ship.hideturtle()
            torpedo.hideturtle()
            game_over = f"Score: {score}            GAME OVER!"
            score_board.clear()
            score_board.write(game_over, False, align="left", font=('arial', 18, 'normal'))
            game_on = False
            break

    if torpedo_state == 'fire':  # Random fire from the enemies
        if torpedo.ycor() >= -280:
            torpedo.sety(torpedo.ycor() - .40)
        else:
            torpedo.goto(1000, 1000)
            torpedo_state = 'ready'

    # Fire Laser
    if laser_state == "fire":
        y = laser.ycor()
        y += laser_speed
        laser.sety(y)

    if laser.ycor() > 300:
        laser.hideturtle()
        laser_state = "ready"

window.exitonclick()
