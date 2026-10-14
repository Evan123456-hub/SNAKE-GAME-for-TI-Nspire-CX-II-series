import random
import time
import ti_draw
import ti_system


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
GRID_X = 20
GRID_Y = 40
CELL_SIZE = 14
GRID_WIDTH = 20
GRID_HEIGHT = 12
STEP_DELAY = 0.20

BLACK = (20, 24, 28)
BOARD_COLOR = (35, 43, 48)
WHITE = (240, 240, 240)
GREEN = (80, 220, 100)
PURPLE = (180, 90, 230)
RED = (255, 90, 80)


def draw_text(x, y, text, color):
    ti_draw.set_color(color[0], color[1], color[2])
    ti_draw.draw_text(x, y, text)


def draw_cell(cell, color):
    x = GRID_X + cell[0] * CELL_SIZE
    y = GRID_Y + cell[1] * CELL_SIZE
    ti_draw.set_color(color[0], color[1], color[2])
    ti_draw.fill_rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)


def draw_score(score):
    ti_draw.set_color(BLACK[0], BLACK[1], BLACK[2])
    ti_draw.fill_rect(GRID_X, 210, 180, 28)
    draw_text(GRID_X, 222, "SNAKE   SCORE: " + str(score), WHITE)


def draw_game(snake, food, score):
    ti_draw.clear()
    ti_draw.set_window(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    ti_draw.set_color(BLACK[0], BLACK[1], BLACK[2])
    ti_draw.fill_rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_score(score)

    ti_draw.set_color(BOARD_COLOR[0], BOARD_COLOR[1], BOARD_COLOR[2])
    ti_draw.fill_rect(
        GRID_X, GRID_Y, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE
    )
    draw_cell(food, RED)
    draw_cell(snake[0], PURPLE)
    for part in snake[1:]:
        draw_cell(part, GREEN)


def draw_step(old_head, new_head, old_tail, food, growing, score):
    if not growing:
        draw_cell(old_tail, BOARD_COLOR)
    draw_cell(old_head, GREEN)
    draw_cell(new_head, PURPLE)
    if growing:
        draw_cell(food, RED)
        draw_score(score)


def draw_message(title, subtitle):
    ti_draw.clear()
    ti_draw.set_window(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    ti_draw.set_color(BLACK[0], BLACK[1], BLACK[2])
    ti_draw.fill_rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_text(112, 162, title, GREEN)
    draw_text(57, 128, subtitle, WHITE)
    draw_text(70, 90, "ENTER: continue", WHITE)
    draw_text(88, 66, "ESC: quit", WHITE)


def choose_food(snake):
    free_cells = []
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = (x, y)
            if cell not in snake:
                free_cells.append(cell)
    if not free_cells:
        return None
    return free_cells[random.randrange(len(free_cells))]


def play_game():
    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2
    snake = [
        (center_x, center_y),
        (center_x - 1, center_y),
        (center_x - 2, center_y),
    ]
    direction = (0, 0)
    next_direction = direction
    food = choose_food(snake)
    score = 0
    last_step = time.time()
    draw_game(snake, food, score)

    while True:
        key = ti_system.get_key()
        if key == "esc":
            return score, False, True
        if key == "up" and direction != (0, -1):
            next_direction = (0, 1)
        elif key == "down" and direction != (0, 1):
            next_direction = (0, -1)
        elif key == "left" and direction != (1, 0):
            next_direction = (-1, 0)
        elif key == "right" and direction != (-1, 0):
            next_direction = (1, 0)

        now = time.time()
        if next_direction != (0, 0) and now - last_step >= STEP_DELAY:
            direction = next_direction
            head = snake[0]
            new_head = (
                (head[0] + direction[0]) % GRID_WIDTH,
                (head[1] + direction[1]) % GRID_HEIGHT,
            )
            growing = new_head == food

            hit_body = new_head in snake and (growing or new_head != snake[-1])
            if hit_body:
                return score, False, False

            old_tail = snake[-1]
            snake.insert(0, new_head)
            if growing:
                score += 1
                food = choose_food(snake)
                if food is None:
                    return score, True, False
            else:
                snake.pop()

            draw_step(head, new_head, old_tail, food, growing, score)
            last_step = now

        time.sleep(0.03)


def wait_for_enter():
    while True:
        key = ti_system.get_key()
        if key == "enter":
            return True
        if key == "esc":
            return False
        time.sleep(0.05)


def main():
    while True:
        draw_message("SNAKE", "ARROWS: start/move")
        if not wait_for_enter():
            break

        score, won, quit_game = play_game()
        if quit_game:
            break
        if won:
            draw_message("YOU WIN!", "SCORE: " + str(score))
        else:
            draw_message("GAME OVER", "SCORE: " + str(score))
        if not wait_for_enter():
            break


main()
