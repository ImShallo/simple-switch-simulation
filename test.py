import random
import time
from modules import *
from datetime import datetime
from rich.console import Console


# Console declaration
console = Console()

console.print("[bright_black]🤖 Benvenuto nella simulazione switch ")
console.print("[bright_black]🤖 Inserisci il tempo di simulazione in secondi ")
secondi = int(console.input("🕒 >> "))

while secondi > 60:
    console.print("[red]⚠️  Attenzione! Limite massimo di tempo superato [white](60[/white] secondi) ")
    with console.status("[bold black]Elaborando la cazzata che hai digitato...", spinner_style="yellow"):
        time.sleep(2)
    time.sleep(0.5)
    console.print("🤖[bright_black italic] Oh coglione, quanto ci vuoi stare qui?") 
    time.sleep(2)
    console.print("🤖[bright_black italic] Riproviamo... quanto vuoi che duri questa simulazione?")
    time.sleep(0.8)
    secondi = int(console.input("🕒 >> "))


# PC and Switch declaration
pc1 = PC("1")
pc2 = PC("2")
switch = Switch(pc1, pc2, bufferSize=100)

secondi_simulazione = secondi
with console.status("[bold black] Elaborando i frame... 📶", spinner_style="yellow"):
    inizio = time.time()
    while secondi > 0:
        random_computer = random.choice([pc1, pc2])
        prioritaRandom = random.choice(list(Frame.PRIORITIES.keys()))
        frame = random.randint(1, 50)

        now = datetime.now()
        formatted_time = now.strftime("[%H:%M:%S]")

        time.sleep(0.5)
        secondi -= 0.5

        for _ in range(frame):
            newFrame = Frame(random_computer, prioritaRandom)
            switch.add_to_buffer(newFrame)

        console.print(
            f"[turquoise4]{formatted_time}[/turquoise4] "
            f"Sono stati inviati [bold yellow]{frame} frame {Frame.PRIORITIES[prioritaRandom].lower()}[/bold yellow] al [bold cyan]PC {random_computer.id}")

        switch.process_buffer()


    console.print(f"\n[bright_black bold]Sono stati processati [white]{switch.get_total_frames_processed()}[/white] frame in [white]{secondi_simulazione}[/white] secondi")
    console.print(f"[bright_black bold]La grandezza media del buffer è: [white]{switch.calculate_buffer_average()}[/white] [yellow]frame")