import sys
import alang
import pygame

TAPES_ORIGIN = [340, 80]
EXTRA_TAPE_SQUARES = 10

TAPE_SQUARE_THICK = 4
TAPE_SQUARE_SIZE = 100

BETWEEN_TAPE_SPACE = 80
BETWEEN_SQUARES_SPACE = 3

COLOR_TAPE_SQUARE = (0, 100, 255)
COLOR_TAPE_HEAD = (200, 100, 255)

CAMERA_POS = [0, 0]


def draw_tm_tape(screen, tape_name: str, tape: alang.Tape, origin=(100, 100)):

    min_index = 0
    max_index = 0

    for index in tape.tape:
        min_index = min(min_index, index)
        max_index = max(max_index, index)

    min_index -= EXTRA_TAPE_SQUARES
    max_index += EXTRA_TAPE_SQUARES

    for index in range(min_index, max_index + 1):
        color = COLOR_TAPE_SQUARE if index != tape.head_position \
            else COLOR_TAPE_HEAD

        thick = TAPE_SQUARE_THICK if index != tape.head_position \
            else TAPE_SQUARE_THICK+1
        pygame.draw.rect(screen, color,
                         (origin[0] +
                          index * (TAPE_SQUARE_SIZE + BETWEEN_SQUARES_SPACE) -
                          CAMERA_POS[0],
                          origin[1], TAPE_SQUARE_SIZE, TAPE_SQUARE_SIZE -
                          CAMERA_POS[1]),
                         thick)
    pass


def draw_tm(screen, tm: alang.TuringMachine):
    for i, tape_name in enumerate(tm.tapes):
        draw_tm_tape(screen, tape_name, tm.tapes[tape_name], origin=(
            TAPES_ORIGIN[0], (i) * (TAPE_SQUARE_SIZE + BETWEEN_TAPE_SPACE)
            + TAPES_ORIGIN[1]))


def run():
    global CAMERA_POS
    if len(sys.argv) < 2:
        print("No Turing machine given. "
              "Try `python run_gui example_machines/parity.tm`.")

    tm = alang.TuringMachine.from_file(sys.argv[1])
    pygame.init()

    screen = pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("alangui")

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    CAMERA_POS[0] -= TAPE_SQUARE_SIZE
                if event.key == pygame.K_RIGHT:
                    CAMERA_POS[0] += TAPE_SQUARE_SIZE
                if event.key == pygame.K_c:
                    CAMERA_POS = [0, 0]

        screen.fill((0, 0, 0))

        draw_tm(screen, tm)

        # Flip the display
        pygame.display.flip()

    pygame.quit()
