import random
import time
from modules import *
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich import box
import msvcrt
import json
from contextlib import contextmanager


# COSTANTS
MAX_PCS = 5
MAX_SIM_SECONDS = 60
MAX_FRAMES = 200
MIN_FRAMES = 1

# Debug mode
debug = False

# Console declaration
console = Console()

def add_debug(func):
    def wrapper(*args, **kwargs):
        if not debug:
            return func(*args, **kwargs)
    return wrapper

@contextmanager
def beat(length: int = 1):
    yield
    time.sleep(length * 0.02)

def add_columns():
    with beat(10):
        table.add_column(locale["devices"])

    for frame_type in Frame.PRIORITIES.values():
        with beat(10):
            table.add_column(f"Frame {frame_type}")

    with beat(10):
        table.add_column(locale["total"])
    
    with beat(10):
        table.add_column(locale["percentage"])

    with beat(10):
        title = locale["table_title"]
        for i in range(0, len(title)+1):
            with beat(3):
                table.title = title[:i]

        table.title = f"[bold][not italic]{locale['table_title']}[/]"

    with beat(10):
        table.title = f"[bold][not italic]📊 {locale['table_title']}[/]"

    with beat(10):
        table.title = f"[bold][not italic]📊 {locale['table_title']}🔢[/]"

def draw_volume_bar(k_value):
    progress = Progress(
        TextColumn(locale["randomness_low"]),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn(locale["randomness_high"]),
        TextColumn(locale["randomness_instructions"])
    )
    volume_task = progress.add_task("randomness", total=10, completed=k_value)
    return progress, volume_task

def randomness_bar(k_value):
    progress, volume_task = draw_volume_bar(k_value)
    running = True

    with Live(progress, refresh_per_second=10, console=console):
        try:
            while running:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\x00' or key == b'\xe0':
                        key = msvcrt.getch() 
                        if key == b'M' and k_value < 10:  
                            k_value += 1
                            progress.update(volume_task, completed=k_value)
                        elif key == b'K' and k_value > 1: 
                            k_value -= 1
                            progress.update(volume_task, completed=k_value)
                    elif key == b'\r': 
                        running = False
                time.sleep(0.01) 
        except KeyboardInterrupt:
            pass
    return k_value

def generate_frames(k_value):
    middle = MAX_FRAMES // 2
    lower = middle - (k_value * 10 / 2)
    upper = middle + (k_value * 10 / 2)
    return random.SystemRandom().randint(lower, upper) + MIN_FRAMES

def populate_table_data():
    table_data = []

    for pc in switch.listPCs:
        new_row = [f"PC {pc.id}"]

        for value in pc.get_frames_type_count().values():
            new_row.append(str(value))

        total_frames = pc.totalFramesReceived()
        total_frames_percentage = round(total_frames / switch.get_total_frames_processed() * 100)

        new_row.append(str(total_frames))
        new_row.append(str(total_frames_percentage) + '%')

        table_data.append(new_row)
    
    for row in table_data:
        with beat(10):
            table.add_row(*row)

def change_table_style():
    with beat(10):
        table.columns[0].justify = "center"
    for i in range(1, len(table.columns)):
        with beat(10):
            table.columns[i].justify = "right"
        
    with beat(10):
        table.columns[0].header_style = "bright_cyan"
        table.columns[0].style = "bright_cyan"

    for i in Frame.PRIORITIES:
        with beat(10):
            table.columns[i+1].header_style = "bright_yellow"
            table.columns[i+1].style = "bright_yellow"

    with beat(10):
        table.columns[-2].header_style = "white"
        table.columns[-2].style = "white"

    with beat(10):
        table.columns[-1].header_style = "spring_green3"
        table.columns[-1].style = "spring_green3"

def show_table(static = True): 
    global table
    table = Table(box=box.SIMPLE)
    if static:
        add_columns()
        populate_table_data()
        console.print(table)
    else:
        with Live(table, console=console, refresh_per_second=20):
            add_columns()
            populate_table_data()
            change_table_style()

            with beat(10):
                table.box = box.ROUNDED

def main():
    console.print(locale["input_time"])
    time.sleep(1.2)

    input_is_valid = False

    while not input_is_valid:
        try:
            sim_sec = int(console.input("🕒 >> "))

            if sim_sec > MAX_SIM_SECONDS:
                raise CustomException.NotInRangeError("Time limit exceeded")
            elif sim_sec < 1:
                raise CustomException.NotInRangeError("Time must be greater than 0")
            else: 
                input_is_valid = True

        except CustomException.NotInRangeError as e:
            if str(e) == "Time limit exceeded":
                console.print(locale["error_time_limit_exceeded"].format(MAX_SIM_SECONDS=MAX_SIM_SECONDS))
                with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print(locale["robot_time_limit_exceeded"]) 
                time.sleep(1.5)
                console.print(locale["robot_retry_time_limit_exceeded"])
                time.sleep(0.8)

            elif str(e) == "Time must be greater than 0":
                console.print(locale["error_time_must_be_greater_than_0"])
                with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                if sim_sec == 0:
                    console.print(locale["robot_time_equals_0"])
                elif sim_sec < 1:
                    console.print(locale["robot_time_less_than_1"]) 
                time.sleep(1.5)
                console.print(locale["robot_retry_time_limit_exceeded"])
                time.sleep(0.8)

        except ValueError as e:
            console.print(locale["error_time_must_be_integer"])
            with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print(locale["robot_time_must_be_integer"]) 
            time.sleep(1.5)
            console.print(locale["robot_retry_time_limit_exceeded"])
            time.sleep(0.8)

        except Exception as e:
            console.print(locale["error_general"], e)
    input_is_valid = False

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print(locale["input_pc_number"])
    time.sleep(0.8)

    while not input_is_valid:
        try:
            pc_number = int(console.input("💻 >> "))

            if pc_number > MAX_PCS:
                raise CustomException.NotInRangeError("PC limit exceeded")
            elif pc_number < 1:
                raise CustomException.NotInRangeError("PC number must be greater than 0")
            else:
                input_is_valid = True
        
        except CustomException.NotInRangeError as e:
            if str(e) == "PC limit exceeded":
                console.print(locale["error_pc_limit_exceeded"].format(MAX_PCS=MAX_PCS))
                with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print(locale["robot_pc_limit_exceeded"]) 
                time.sleep(1.5)
                console.print(locale["robot_retry_pc_limit_exceeded"])
                time.sleep(0.8)
            elif str(e) == "PC number must be greater than 0":
                console.print(locale["error_pc_must_be_greater_than_0"])
                with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print(locale["robot_pc_must_be_greater_than_0"]) 
                time.sleep(1.5)
                console.print(locale["robot_retry_pc_limit_exceeded"])
                time.sleep(0.8)

        except ValueError as e:
            console.print(locale["error_pc_must_be_integer"])
            with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print(locale["robot_pc_must_be_integer"]) 
            time.sleep(1.5)
            console.print(locale["robot_retry_pc_limit_exceeded"])
            time.sleep(0.8)

        except Exception as e:
            console.print(locale["error_general"], e)
    input_is_valid = False

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print(locale["input_randomness"])
    time.sleep(0.8)

    k_value = randomness_bar(5)

    # PC and Switch declaration
    global switch 
    switch = Switch(bufferSize=MAX_FRAMES)

    for i in range(pc_number):
        new_pc = PC(i+1)
        with console.status("", spinner_style="yellow"):
            time.sleep(0.8)
        console.print(locale["pc_connected"].format(pc_id=i+1))
        switch.connect_pc(new_pc)

    with console.status(locale["starting_simulation"], spinner_style="yellow"):
        time.sleep(1.5)

    original_sim_sec = sim_sec
    with console.status(locale["frame_processing"], spinner_style="yellow"):
        while sim_sec > 0:
            random_computer = random.SystemRandom().choice(switch.listPCs)
            prioritaRandom = random.SystemRandom().choice(list(Frame.PRIORITIES.keys()))

            if sim_sec > (original_sim_sec//2):
                number_frame = generate_frames(k_value)
                waiting_time = 1
            else:
                number_frame = generate_frames(k_value)
                waiting_time = 0.5

            time.sleep(waiting_time)
            sim_sec -= waiting_time

            now = datetime.now()
            formatted_time = now.strftime("[%H:%M:%S]")
            
            for _ in range(number_frame):
                newFrame = Frame(random_computer, prioritaRandom)
                switch.add_to_buffer(newFrame)

            console.print(
                f"[turquoise4]{formatted_time}[/turquoise4] ",
                locale["frame_sent"].format(number_frame=number_frame, pc_id=random_computer.id, frame_type=Frame.PRIORITIES[prioritaRandom].lower()))

            switch.process_buffer()


    with console.status(locale["loading_results"], spinner_style="yellow"):
        time.sleep(1.5)
    time.sleep(0.5)
    console.print(locale["simulation_ended"])
    time.sleep(0.8)
    console.print(locale["total_frames_processed"].format(total_frames=switch.get_total_frames_processed(), total_seconds=original_sim_sec))
    time.sleep(0.8)
    console.print(locale["frames_per_second"].format(frames_per_second=(switch.get_total_frames_processed()) / original_sim_sec))
    time.sleep(0.8)

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print(locale["input_show_stats"])
    time.sleep(0.5)
    show_stats = console.input("📊 >> ")

    while show_stats.lower() not in ['y', 's', 'n']:
        console.print(locale["error_input"])
        with console.status(locale["processing_nonsense"], spinner_style="yellow"):
            time.sleep(1.5)
        time.sleep(0.5)
        console.print(locale["robot_error_input"]) 
        time.sleep(1.5)
        console.print(locale["robot_retry_show_stats"])
        time.sleep(1.2)
        show_stats = console.input("📊 >> ")

    if show_stats.lower() == 's' or show_stats.lower() == 'y':
        with console.status("", spinner_style="yellow"):
            time.sleep(1.5)
        show_table(static=False)

    with console.status("", spinner_style="yellow"):
        time.sleep(1.5)
    
if __name__ == "__main__":
    if debug:
        time.sleep = add_debug(time.sleep)

    with console.status("[bold black] Starting up...", spinner_style="yellow"):
        time.sleep(1.5)
    console.print("[bright_black]🤖 Welcome to the Simple Switch Simulation")
    time.sleep(1.5)

    console.print("[bright_black]🤖 Please, select your language (en/it)")
    time.sleep(0.5)
    
    language = console.input("🌐 >> ")
    while language.lower() not in ['en', 'it']:
        console.print(f"[red]⚠️  Attention! You must choose between [white]en[/white] and [white]it[/white]")
        with console.status("[bold black]Processing the nonsense you typed...", spinner_style="yellow"):
            time.sleep(1.5)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] You should go dig [/]😉") 
        time.sleep(1.5)
        console.print("🤖[bright_black italic] Let's try again... please, select your language (en/it)")
        time.sleep(0.8)
        language = console.input("🌐 >> ")

    with open(f"locales/{language}.json", "r", encoding="utf8") as file:
        locale = json.load(file)

    while True:
        main()
        console.print(locale["new_sim"])
        time.sleep(0.5)
        new_sim = console.input("🔄 >> ")

        while new_sim.lower() not in ['y', 's', 'n']:
            console.print(locale["error_input"])
            with console.status(locale["processing_nonsense"], spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print(locale["robot_error_input"]) 
            time.sleep(1.5)
            console.print(locale["robot_retry_new_sim"])
            time.sleep(0.8)
            new_sim = console.input("🔄 >> ")

        if new_sim.lower() == 'n':
            with console.status("", spinner_style="yellow"):
                time.sleep(1)
            console.print(locale["goodbye"])
            break