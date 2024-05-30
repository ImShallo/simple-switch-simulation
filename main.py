import random
import time
from modules import *
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich import box
import keyboard
from contextlib import contextmanager

# COSTANTS
MAX_PCS = 5
MAX_SIM_SECONDS = 60
MAX_FRAMES = 100
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
        table.add_column("Dispositivi")

    for frame_type in Frame.PRIORITIES.values():
        with beat(10):
            table.add_column(f"Frame {frame_type}")

    with beat(10):
        table.add_column("Totale")
    
    with beat(10):
        table.add_column("Percentuale")

    with beat(10):
        title = "Statistiche Simulazione"
        for i in range(0, len(title)+1):
            with beat(3):
                table.title = title[:i]

        table.title = "[bold][not italic]Statistiche Simulazione[/]"

    with beat(10):
        table.title = "[bold][not italic]📊 Statistiche Simulazione[/]"

    with beat(10):
        table.title = "[bold][not italic]📊 Statistiche Simulazione🔢[/]"

def draw_volume_bar(k_value):
    progress = Progress(
        TextColumn(" [bold yellow]Poco casuale[/bold yellow] "),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn(" [bold yellow]Molto casuale[/bold yellow] "),
        TextColumn("[bold blue]→[/bold blue] per aumentare. [bold blue]←[/bold blue] per diminuire. "
                   "[bold blue]Enter[/bold blue] per confermare.")
    )
    volume_task = progress.add_task("randomness", total=10, completed=k_value)
    return progress, volume_task

def randomness_bar(k_value):
    progress, volume_task = draw_volume_bar(k_value)
    running = True
    
    def on_key_event(event):
        nonlocal k_value, running
        if event.name == 'right' or event.scan_code == 77 and k_value < 10:
            k_value += 1
            progress.update(volume_task, completed=k_value)
        elif event.name == 'left' or event.scan_code == 75 and k_value > 1:
            k_value -= 1
            progress.update(volume_task, completed=k_value)
        elif event.name == 'enter':
            running = False

    keyboard.on_press(on_key_event)

    with Live(progress, refresh_per_second=10, console=console):
        try:
            while running:
                pass
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
    console.print("[bright_black]🤖 Inserisci il tempo di simulazione in secondi ")
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
                console.print(f"[red]⚠️  Attenzione! Limite massimo di tempo superato ([white]{MAX_SIM_SECONDS}[/white] secondi) ")
                with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print("🤖[bright_black italic] Oh coglione, quanto ci vuoi stare qui? [/]🫤") 
                time.sleep(1.5)
                console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
                time.sleep(0.8)

            elif str(e) == "Time must be greater than 0":
                console.print(f"[red]⚠️  Attenzione! Devi inserire un tempo di simulazione superiore a [white]0[/white] secondi ")
                with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                if sim_sec == 0:
                    console.print("🤖[bright_black italic] Ora mi devi spiegare l'utilità della simulazione se metti 0 [/]🫠")
                elif sim_sec < 1:
                    console.print("🤖[bright_black italic] Ti chiamano Dottor Who per caso? [/]🧐") 
                time.sleep(1.5)
                console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
                time.sleep(0.8)

        except ValueError as e:
            console.print(f"[red]⚠️  Attenzione! Devi inserire un numero intero di secondi ")
            with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print("🤖[bright_black italic] Non ti hanno insegnato i numeri interi alle elementari? [/]🤨") 
            time.sleep(1.5)
            console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
            time.sleep(0.8)

        except Exception as e:
            console.print("[red]⚠️  General error, report the issue: [bright_black]", e)
    input_is_valid = False

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print("[bright_black]🤖 Inserisci il numero di PC collegati allo switch ")
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
                console.print(f"[red]⚠️  Attenzione! Limite massimo di PC superato ([white]{MAX_PCS}[/white]) ")
                with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print("🤖[bright_black italic] Ora mi fai incazzare. NON abbiamo switch della nasa!! [/]🙄") 
                time.sleep(1.5)
                console.print("🤖[bright_black italic] Riproviamo... quanti PC vuoi collegare?")
                time.sleep(0.8)
            elif str(e) == "PC number must be greater than 0":
                console.print(f"[red]⚠️  Attenzione! Devi collegare almeno un PC allo switch ")
                with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                    time.sleep(1.5)
                time.sleep(0.5)
                console.print("🤖[bright_black italic] Ma sei scemo!? [/]😡") 
                time.sleep(1.5)
                console.print("🤖[bright_black italic] Riproviamo...  quanti PC vuoi collegare?")
                time.sleep(0.8)

        except ValueError as e:
            console.print(f"[red]⚠️  Attenzione! Devi inserire un numero intero di PC")
            with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print("🤖[bright_black italic] Non ti hanno insegnato i numeri interi alle elementari? [/]🤨") 
            time.sleep(1.5)
            console.print("🤖[bright_black italic] Riproviamo... quanti PC vuoi collegare?")
            time.sleep(0.8)

        except Exception as e:
            console.print("[red]⚠️  General error, report the issue: [bright_black]", e)
    input_is_valid = False

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print("[bright_black]🤖 Inserisci la casualità dell'intervallo dei frame")
    time.sleep(0.8)

    k_value = randomness_bar(5)

    # PC and Switch declaration
    global switch 
    switch = Switch(bufferSize=100)

    for i in range(pc_number):
        new_pc = PC(i+1)
        with console.status(f"[bold black]", spinner_style="yellow"):
            time.sleep(0.8)
        console.print(f"[bright_black]🤖 PC {new_pc.id} collegato allo switch ✅")
        switch.connect_pc(new_pc)

    with console.status("[bold black] Avviando simulazione... 🚀", spinner_style="yellow"):
        time.sleep(1.5)

    original_sim_sec = sim_sec
    with console.status("[bold black] Elaborando i frame... 📶", spinner_style="yellow"):
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
                f"[turquoise4]{formatted_time}[/turquoise4] "
                f"Sono stati inviati [bold yellow]{number_frame} frame {Frame.PRIORITIES[prioritaRandom].lower()}[/bold yellow] al [bold cyan]PC {random_computer.id}")

            switch.process_buffer()


    with console.status("[bold black] Caricando risultati", spinner_style="yellow"):
        time.sleep(1.5)
    time.sleep(0.5)
    console.print("[bright_black bold]Simulazione terminata... 🛑")
    time.sleep(0.8)
    console.print(f"\n[bright_black bold]Nello switch sono stati processati [white]{switch.get_total_frames_processed()}[/white] frame in [white]{original_sim_sec}[/white] secondi")
    time.sleep(0.8)
    console.print(f"[bright_black bold]La grandezza media del buffer dello switch è di [white]{switch.calculate_buffer_average()}[/white] [yellow]frame[/]/[white]s")
    time.sleep(0.8)

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print("[bright_black]\n🤖 Desideri visualizzare le statistiche della simulazione? [bold bright_black](s/n)[/]")
    time.sleep(0.5)
    console.input()
    show_stats = console.input("📊 >> ")

    while show_stats.lower() not in ['s', 'n']:
        console.print(f"[red]⚠️  Attenzione! Devi rispondere con [white]s[/white] o [white]n[/white] ")
        with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
            time.sleep(1.5)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] Sei veramente un rimasto [/]🥱") 
        time.sleep(1.5)
        console.print("🤖[bright_black italic] Riproviamo... vuoi visualizzare le statistiche della simulazione? (s/n)")
        time.sleep(1.2)
        show_stats = console.input("📊 >> ")

    if show_stats.lower() == 's':
        with console.status("", spinner_style="yellow"):
            time.sleep(1.5)
        show_table(static=False)

    with console.status("", spinner_style="yellow"):
        time.sleep(1.5)
    
    
if __name__ == "__main__":
    if debug:
        time.sleep = add_debug(time.sleep)

    with console.status("[bold black]Avvio del programma di simulazione...", spinner_style="yellow"):
        time.sleep(1.5)
    console.print("[bright_black]🤖 Benvenuto nella simulazione switch ")
    time.sleep(1.5)

    while True:
        main()
        console.print("[bright_black]🤖 Desideri eseguire una nuova simulazione? [bold bright_black](s/n)[/]")
        time.sleep(0.5)
        new_sim = console.input("🔄 >> ")

        while new_sim.lower() not in ['s', 'n']:
            console.print(f"[red]⚠️  Attenzione! Devi rispondere con [white]s[/white] o [white]n[/white] ")
            with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
                time.sleep(1.5)
            time.sleep(0.5)
            console.print("🤖[bright_black italic] Dovresti andare a zappare [/]😉") 
            time.sleep(1.5)
            console.print("🤖[bright_black italic] Riproviamo... vuoi eseguire una nuova simulazione? (s/n)")
            time.sleep(0.8)
            new_sim = console.input("🔄 >> ")

        if new_sim.lower() == 'n':
            with console.status("", spinner_style="yellow"):
                time.sleep(1)
            console.print("[bright_black]🤖 Arrivederci... 👋")
            break