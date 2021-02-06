import sys
import alang
import pygame

TAPES_ORIGIN = [340, 80]
EXTRA_TAPE_SQUARES = 10

TAPE_SQUARE_THICK = 4
TAPE_SQUARE_SIZE = 100

BETWEEN_TAPE_SPACE = 110
BETWEEN_SQUARES_SPACE = 3

COLOR_TAPE_SQUARE = (0, 100, 255)
COLOR_TAPE_HEAD = (200, 100, 255)

CAMERA_POS = [0, 0]

MAIN_FONT_SIZE = 32
MAIN_FONT = None
MAIN_FONT_BIGGER_SIZE = 72
MAIN_FONT_BIGGER = None

TAPE_NAME_COLOR = (0, 255, 0)
ALPHABET_COLOR = (220, 220, 220)

tapes_names_rendered = {}
alphabet_rendered = {}


def draw_tm_tape(screen, tape_name: str, tape: alang.Tape, origin=(100, 100)):
    global tapes_names_rendered, alphabet_rendered

    min_index = 0
    max_index = 0

    for index in tape.tape:
        min_index = min(min_index, index)
        max_index = max(max_index, index)

    min_index -= EXTRA_TAPE_SQUARES
    max_index += EXTRA_TAPE_SQUARES

    if tape_name not in tapes_names_rendered:
        tapes_names_rendered[tape_name] = MAIN_FONT.render(f"Tape: `{tape_name}`", True, TAPE_NAME_COLOR)

    screen.blit(tapes_names_rendered[tape_name], (10, origin[1] - 30))

    for index in range(min_index, max_index + 1):
        color = COLOR_TAPE_SQUARE if index != tape.head_position else COLOR_TAPE_HEAD

        thick = TAPE_SQUARE_THICK if index != tape.head_position else TAPE_SQUARE_THICK + 1

        tape_square_rect = [
            origin[0] + index * (TAPE_SQUARE_SIZE + BETWEEN_SQUARES_SPACE) - CAMERA_POS[0],
            origin[1] - CAMERA_POS[1],
            TAPE_SQUARE_SIZE,
            TAPE_SQUARE_SIZE,
        ]

        if index in tape.tape:
            if tape.tape[index]:
                symbol = tape.tape[index]
                if symbol not in alphabet_rendered:
                    alphabet_rendered[symbol] = MAIN_FONT_BIGGER.render(f"{symbol}", True, ALPHABET_COLOR)

                symbol_pos = tape_square_rect[:2]
                symbol_pos[0] += tape_square_rect[2] / 2 - alphabet_rendered[symbol].get_size()[0] / 2
                symbol_pos[1] += tape_square_rect[3] / 2 - alphabet_rendered[symbol].get_size()[1] / 2

                screen.blit(alphabet_rendered[symbol], symbol_pos)

        pygame.draw.rect(screen, color, tape_square_rect, thick)
    pass


def draw_tm(screen, tm: alang.TuringMachine):
    for i, tape_name in enumerate(tm.tapes):
        draw_tm_tape(
            screen,
            tape_name,
            tm.tapes[tape_name],
            origin=(
                TAPES_ORIGIN[0],
                (i) * (TAPE_SQUARE_SIZE + BETWEEN_TAPE_SPACE) + TAPES_ORIGIN[1],
            ),
        )


def input_tapes(tm):
    for tape_name in tm.tapes:
        print(f"Input for tape `{tape_name}`:")
        in_ = input()
        tm.init_tape(tape_name, list(in_))
    print("System ready!")


def run():
    global CAMERA_POS, MAIN_FONT, MAIN_FONT_BIGGER
    if len(sys.argv) < 2:
        print("No Turing machine given. " "Try `python run_gui example_machines/parity.tm`.")

    tm = alang.TuringMachine.from_file(sys.argv[1])

    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            tm.tapes[tm.tape_order[i - 2]].init_tape(list(sys.argv[i]))

    pygame.init()

    screen = pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("alangui")

    MAIN_FONT = pygame.font.SysFont(None, MAIN_FONT_SIZE)
    MAIN_FONT_BIGGER = pygame.font.SysFont(None, MAIN_FONT_BIGGER_SIZE)

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
                if event.key == pygame.K_r:
                    tm.reset()
                if event.key == pygame.K_i:
                    input_tapes(tm)
                if event.key == pygame.K_n:
                    tm.step()

        screen.fill((0, 0, 0))

        draw_tm(screen, tm)
        # Flip the display
        pygame.display.flip()

    pygame.quit()
