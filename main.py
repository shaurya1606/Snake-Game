# NOTE: On Windows, run 'pip install windows-curses' before running this script.
import curses
from random import randint

def main(stdscr):
    curses.curs_set(0)
    height, width = 20, 60
    max_y, max_x = stdscr.getmaxyx()
    if max_y < height or max_x < width:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Terminal too small! Resize to at least {width}x{height}.")
        stdscr.refresh()
        stdscr.getch()
        return
    win = curses.newwin(height, width, 0, 0)
    win.keypad(1)
    win.timeout(100)

    # Initial snake position and other settings
    snk_x = width // 4
    snk_y = height // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [randint(1, height - 2), randint(1, width - 2)]
    win.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        # Calculate the new head of the snake
        head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            head[0] += 1
        if key == curses.KEY_UP:
            head[0] -= 1
        if key == curses.KEY_LEFT:
            head[1] -= 1
        if key == curses.KEY_RIGHT:
            head[1] += 1

        # Check for collisions (borders or self)
        if (
            head[0] in [0, height-1] or
            head[1] in [0, width-1] or
            head in snake
        ):
            break

        snake.insert(0, head)

        # Check if snake has eaten the food
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    randint(1, height - 2),
                    randint(1, width - 2)
                ]
                food = nf if nf not in snake else None
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove last segment of snake
            last = snake.pop()
            win.addch(last[0], last[1], ' ')

        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    stdscr.clear()
    stdscr.addstr(0, 0, "Game Over! Final Score: {}".format(score))
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)