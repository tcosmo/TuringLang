import sys
import alang
import pygame

TAPES_ORIGIN = [140, 40]
EXTRA_TAPE_SQUARES = 10

TAPE_SQUARE_THICK = 4
TAPE_SQUARE_SIZE = 100

BETWEEN_TAPE_SPACE = 90
BETWEEN_SQUARES_SPACE = 3

COLOR_TAPE_SQUARE = (0, 100, 255)
COLOR_TAPE_HEAD = (200, 100, 255)

CAMERA_POS = [0, 0]

MAIN_FONT_SIZE = 32
MAIN_FONT = None

MAIN_FONT_BIGGER_SIZE = 72
MAIN_FONT_BIGGER = None

MAIN_FONT_A_BIT_BIGGER_SIZE = 42
MAIN_FONT_A_BIT_BIGGER = None

BACKGROUND_NON_EMPTY_SQUARE = (53, 53, 53)
TAPE_NAME_COLOR = (0, 255, 0)
ALPHABET_COLOR = (220, 220, 220)
MACHINE_INFO_COLOR = (0, 255, 0)
ERROR_MSG_COLOR = (255, 50, 50)

COLOR_INSTR_SELECTED = (255, 140, 0)

MACHINE_TEXT_ORIGIN_X = 50
SPECIAL_MSG_X = 600

LINE_HEIGHT = 35

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
                pygame.draw.rect(screen, BACKGROUND_NON_EMPTY_SQUARE, tape_square_rect)
                symbol = tape.tape[index]
                if symbol not in alphabet_rendered:
                    alphabet_rendered[symbol] = MAIN_FONT_BIGGER.render(f"{symbol}", True, ALPHABET_COLOR)

                symbol_pos = tape_square_rect[:2]
                symbol_pos[0] += tape_square_rect[2] / 2 - alphabet_rendered[symbol].get_size()[0] / 2
                symbol_pos[1] += tape_square_rect[3] / 2 - alphabet_rendered[symbol].get_size()[1] / 2

                screen.blit(alphabet_rendered[symbol], symbol_pos)

        pygame.draw.rect(screen, color, tape_square_rect, thick)
    pass


machine_text = {}


def draw_tm(screen, tm: alang.TuringMachine):
    global machine_text

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

    if len(machine_text) == 0:
        machine_text["machine"] = MAIN_FONT.render(f"Machine: `{tm.name}`", True, MACHINE_INFO_COLOR)
        machine_text["instructions"] = MAIN_FONT.render(4 * " " + f"Instructions:", True, MACHINE_INFO_COLOR)
        machine_text["instructions_name"] = []
        for instr in tm.instructions:
            colored_text = []
            colored_text.append(MAIN_FONT.render(8 * " " + f"- `{instr.name}`", True, MACHINE_INFO_COLOR))
            colored_text.append(
                MAIN_FONT_A_BIT_BIGGER.render(12 * " " + f"- `{instr.name}`", True, COLOR_INSTR_SELECTED)
            )

            machine_text["instructions_name"].append(colored_text)

    pos_machine_text = [MACHINE_TEXT_ORIGIN_X, len(tm.tapes) * (TAPE_SQUARE_SIZE + BETWEEN_TAPE_SPACE) - 20]
    screen.blit(
        machine_text["machine"],
        pos_machine_text,
    )

    screen.blit(
        machine_text["instructions"],
        [pos_machine_text[0], pos_machine_text[1] + LINE_HEIGHT],
    )

    for i, instr_name in enumerate(machine_text["instructions_name"]):
        screen.blit(
            instr_name[i == tm.instruction_pointer],
            [pos_machine_text[0], pos_machine_text[1] + LINE_HEIGHT * (i + 2)],
        )


def input_tapes(tm):
    for tape_name in tm.tapes:
        print(f"Input for tape `{tape_name}`:")
        in_ = input()
        tm.init_tape(tape_name, list(in_))
    print("System ready!")


def input_tapes_from_argv(tm: alang.TuringMachine):
    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            tm.tapes[tm.tape_order[i - 2]].init_tape(list(sys.argv[i]))


def run():
    global CAMERA_POS, MAIN_FONT, MAIN_FONT_BIGGER, MAIN_FONT_A_BIT_BIGGER
    if len(sys.argv) < 2:
        print("No Turing machine given. " "Try `python run_gui example_machines/parity.tm`.")

    machine_ill_formed = False
    try:
        tm = alang.TuringMachine.from_file(sys.argv[1])
    except alang.TMSpecificationError as e:
        print("\nFATAL: " + str(e))
        machine_ill_formed = True

    if not machine_ill_formed:
        input_tapes_from_argv(tm)

    machine_halted = False

    pygame.init()

    screen = pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("alangui")
    pygame.key.set_repeat(200)

    MAIN_FONT = pygame.font.SysFont(None, MAIN_FONT_SIZE)
    MAIN_FONT_BIGGER = pygame.font.SysFont(None, MAIN_FONT_BIGGER_SIZE)
    MAIN_FONT_A_BIT_BIGGER = pygame.font.SysFont(None, MAIN_FONT_A_BIT_BIGGER_SIZE)

    special_messages = {}
    special_messages["ill_formed"] = MAIN_FONT_BIGGER.render("Machine ill formed", True, ERROR_MSG_COLOR)
    special_messages["runtime_error"] = MAIN_FONT_BIGGER.render("Runtime error", True, ERROR_MSG_COLOR)
    special_messages["halt"] = MAIN_FONT_BIGGER.render("Machine has halted", True, (255, 255, 255))

    if not machine_ill_formed:
        special_msg_pos = [SPECIAL_MSG_X, len(tm.tapes) * (TAPE_SQUARE_SIZE + BETWEEN_TAPE_SPACE) + 50]
    else:
        special_msg_pos = [
            (screen.get_size()[0] - special_messages["halt"].get_size()[0]) / 2,
            (screen.get_size()[1] - special_messages["halt"].get_size()[1]) / 2,
        ]

    runtime_error = False

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

                if not machine_ill_formed:
                    if event.key == pygame.K_r:
                        tm.reset()
                        runtime_error = False
                        machine_halted = False
                        input_tapes_from_argv(tm)
                    if event.key == pygame.K_i:
                        tm.reset()
                        runtime_error = False
                        machine_halted = False
                        input_tapes(tm)
                    if event.key == pygame.K_n and not runtime_error:
                        try:
                            tm.step()
                        except alang.TMRuntimeError as e:
                            print("\nFATAL: " + str(e))
                            runtime_error = True
                        except alang.TMHalt as e:
                            print("\n" + str(e))
                            machine_halted = True

        screen.fill((0, 0, 0))

        if not machine_ill_formed:
            draw_tm(screen, tm)

        if machine_ill_formed:
            screen.blit(special_messages["ill_formed"], special_msg_pos)
        elif runtime_error:
            screen.blit(special_messages["runtime_error"], special_msg_pos)
        elif machine_halted:
            screen.blit(special_messages["halt"], special_msg_pos)

        # Flip the display
        pygame.display.flip()

    pygame.quit()
