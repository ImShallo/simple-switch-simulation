import random
import time
from modules import *
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from contextlib import contextmanager

# COSTANTS
MAX_PCS = 5
MAX_SIM_SECONDS = 60
MAX_FRAMES = 50

# Debug mode
debug = False

# Console declaration
console = Console()
table = Table()

def add_debug(func):
    def wrapper(*args, **kwargs):
        if not debug:
            return func(*args, **kwargs)
    return wrapper

@contextmanager
def beat(length: int = 1):
    yield
    time.sleep(length * 0.05)

def add_columns(table):
    with beat(10):
        table.add_column("Dispositivi")

    for frame_type in Frame.PRIORITIES.values():
        with beat(10):
            table.add_column(f"Frame {frame_type}")

    with beat(10):
        table.add_column("Totale")
    
    with beat(10):
        table.add_column("Percentuale")

def populate_table_data(switch):
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

def show_table(static = True):  
    if static:
        add_columns(table)
        populate_table_data(switch)
        console.print(table)
    else:
        with Live(table, console=console, refresh_per_second=10):
            add_columns(table)
            populate_table_data(switch)



def main():
    with console.status("[bold black]Avvio del programma di simulazione...", spinner_style="yellow"):
        time.sleep(2)
    console.print("[bright_black]🤖 Benvenuto nella simulazione switch ")
    time.sleep(1.5)
    console.print("[bright_black]🤖 Inserisci il tempo di simulazione in secondi ")
    time.sleep(1.2)
    secondi = int(console.input("🕒 >> "))

    while secondi > MAX_SIM_SECONDS:
        console.print(f"[red]⚠️  Attenzione! Limite massimo di tempo superato ([white]{MAX_SIM_SECONDS}[/white] secondi) ")
        with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
            time.sleep(2)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] Oh coglione, quanto ci vuoi stare qui? [/]🫤") 
        time.sleep(2)
        console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
        time.sleep(0.8)
        secondi = int(console.input("🕒 >> "))

    while secondi < 1:
        console.print(f"[red]⚠️  Attenzione! Devi inserire un tempo di simulazione superiore a 0 secondi ")
        with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
            time.sleep(2)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] Ti chiamano Dottor Who per caso? [/]🧐") 
        time.sleep(2)
        console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
        time.sleep(0.8)
        secondi = int(console.input("🕒 >> "))

    with console.status("", spinner_style="yellow"):
        time.sleep(1)
    console.print("[bright_black]🤖 Inserisci il numero di PC collegati allo switch ")
    time.sleep(0.8)
    pc_number = int(console.input("💻 >> "))

    while pc_number > MAX_PCS:
        console.print(f"[red]⚠️  Attenzione! Limite massimo di PC superato ([white]{MAX_PCS}[/white]) ")
        with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
            time.sleep(2)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] Ora mi fai incazzare. NON abbiamo switch della nasa!! [/]🙄") 
        time.sleep(2)
        console.print("🤖[bright_black italic] Riproviamo... quanti PC vuoi collegare?")
        time.sleep(0.8)
        pc_number = int(console.input("💻 >> "))

    while pc_number < 1:
        console.print(f"[red]⚠️  Attenzione! Devi collegare almeno un PC allo switch ")
        with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
            time.sleep(2)
        time.sleep(0.5)
        console.print("🤖[bright_black italic] Ma sei scemo!? [/]😡") 
        time.sleep(2)
        console.print("🤖[bright_black italic] Riproviamo...  quanti PC vuoi collegare?")
        time.sleep(0.8)
        pc_number = int(console.input("💻 >> "))

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
        time.sleep(3)

    secondi_simulazione = secondi
    with console.status("[bold black] Elaborando i frame... 📶", spinner_style="yellow"):
        while secondi > 0:
            random_computer = random.SystemRandom().choice(switch.listPCs)
            prioritaRandom = random.SystemRandom().choice(list(Frame.PRIORITIES.keys()))

            if secondi > (secondi_simulazione//2):
                frame = random.SystemRandom().randint(MAX_FRAMES//2, MAX_FRAMES)
                waiting_time = 1
            else:
                frame = random.SystemRandom().randint(1, MAX_FRAMES//3)
                waiting_time = 0.5

            time.sleep(waiting_time)
            secondi -= waiting_time

            now = datetime.now()
            formatted_time = now.strftime("[%H:%M:%S]")
            
            for _ in range(frame):
                newFrame = Frame(random_computer, prioritaRandom)
                switch.add_to_buffer(newFrame)

            console.print(
                f"[turquoise4]{formatted_time}[/turquoise4] "
                f"Sono stati inviati [bold yellow]{frame} frame {Frame.PRIORITIES[prioritaRandom].lower()}[/bold yellow] al [bold cyan]PC {random_computer.id}")

            switch.process_buffer()


    with console.status("[bold black] Caricando risultati", spinner_style="yellow"):
        time.sleep(2)
    time.sleep(0.5)
    console.print("[bright_black bold]Simulazione terminata... 🛑")
    time.sleep(0.8)
    console.print(f"\n[bright_black bold]Nello switch sono stati processati [white]{switch.get_total_frames_processed()}[/white] frame in [white]{secondi_simulazione}[/white] secondi")
    time.sleep(0.8)
    console.print(f"[bright_black bold]La grandezza media del buffer dello switch è di [white]{switch.calculate_buffer_average()}[/white] [yellow]frame[/]/[white]s")
    
    

if __name__ == "__main__":
    if debug:
        time.sleep = add_debug(time.sleep)

    main()
    show_table(static=False)
    
