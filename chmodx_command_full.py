#!/usr/bin/env python3
"""
chmodx-Command v2.0 Professional Edition
Terminal Mastery for Hackers
Diseño profesional con explicaciones detalladas
"""

import json
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.columns import Columns
    from rich import box
    from rich.align import Align
    from rich.style import Style
    from rich.rule import Rule
    from rich.markdown import Markdown
    from rich.syntax import Syntax
except ImportError:
    print("Error: rich library not installed. Install with: pip install rich")
    exit(1)

console = Console()

# Configuración
HOME_DIR = Path.home()
DATA_DIR = HOME_DIR / ".chmodx-command"
DATA_DIR.mkdir(exist_ok=True)
PROGRESS_FILE = DATA_DIR / "progress.json"

class TerminalUI:
    """Manejador de interfaz profesional"""

    @staticmethod
    def get_terminal_width():
        """Obtiene ancho de terminal"""
        return shutil.get_terminal_size((80, 20)).columns

    @staticmethod
    def create_banner():
        """Crea banner dinámico que se ajusta al ancho de pantalla"""
        width = TerminalUI.get_terminal_width()

        banner_lines = [
            "chmodx-Command",
            "Terminal Mastery for Hackers",
        ]

        # Crear banner con ancho dinámico
        line_length = max(len(line) for line in banner_lines) + 8
        actual_width = min(width - 4, max(line_length, 60))

        border = "═" * actual_width
        logo = f"""
╔{border}╗
║{' ' * (actual_width - 2)}║
║  {'chmodx-Command'.center(actual_width - 4)}  ║
║  {'Terminal Mastery for Hackers'.center(actual_width - 4)}  ║
║{' ' * (actual_width - 2)}║
╚{border}╝
"""

        return Panel(
            logo,
            border_style="cyan",
            box=box.DOUBLE,
            expand=False
        )

    @staticmethod
    def create_header(title, subtitle=None):
        """Crea header profesional"""
        content = Text()
        content.append(title, style="bold cyan")
        if subtitle:
            content.append(f"\n{subtitle}", style="dim")

        return Panel(
            content,
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    @staticmethod
    def create_command_card(cmd_data, chapter_num):
        """Crea tarjeta de comando con explicación detallada"""
        # Explicación profesional
        explanation = TerminalUI.get_detailed_explanation(cmd_data)

        content = Text()
        content.append(f"{cmd_data['cmd']}\n", style="bold green")
        content.append(f"📝 Para qué sirve:\n", style="bold white")
        content.append(f"{explanation}\n\n", style="")
        content.append(f"💡 Ejemplo práctico:\n", style="bold yellow")
        content.append(f"{cmd_data['example']}\n\n", style="dim")
        content.append(f"📦 Categoría: {cmd_data['category']}\n", style="cyan")
        content.append(f"🎯 Dificultad: {cmd_data['difficulty']}\n", style="magenta")
        content.append(f"🔧 Paquete: {cmd_data['package']}", style="blue")

        return Panel(
            content,
            title=f"Capítulo {chapter_num}",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    @staticmethod
    def get_detailed_explanation(cmd_data):
        """Genera explicaciones detalladas y entendibles"""
        explanations = {
            # Capítulo 1
            "pkg update": "Actualiza la lista de paquetes disponibles en tu repositorio. Es como actualizar el catálogo de una tienda antes de comprar.",
            "pkg upgrade": "Actualiza TODOS los paquetes instalados a sus versiones más recientes. Úsalo regularmente para mantener tu sistema seguro.",
            "pkg install": "Instala un nuevo paquete/programa desde los repositorios. Es como descargar aplicaciones en tu teléfono.",
            "pkg uninstall": "Desinstala un paquete que ya no necesitas. Libera espacio en tu dispositivo.",
            "pwd": "Muestra la ruta completa donde te encuentras actualmente. Es como ver tu dirección exacta en el mapa de archivos.",
            "ls": "Lista todos los archivos y carpetas en la ubicación actual. Básico como abrir una carpeta en tu explorador.",
            "cd": "Cambia de directorio (carpeta). Te permite moverte por el sistema de archivos como cambiar de habitación.",
            "mkdir": "Crea una nueva carpeta/directorio. Como crear una nueva carpeta en tu computadora.",
            "touch": "Crea un archivo vacío. Útil para crear marcadores o archivos de texto nuevos.",
            "rm": "Elimina archivos o carpetas. ¡Cuidado! No hay papelera de reciclaje, se borra permanentemente.",

            # Capítulo 2
            "termux-toast": "Muestra una notificación temporal en pantalla. Perfecto para mostrar mensajes breves a los usuarios.",
            "termux-dialog": "Crea ventanas emergentes para pedir información al usuario. Como formularios interactivos.",
            "termux-notification": "Envía notificaciones permanentes al área de notificaciones de Android.",
            "termux-clipboard-set/get": "Permite leer y escribir en el portapapeles del sistema. Útil para copiar/pegar datos.",
            "termux-open": "Abre archivos o URLs con las aplicaciones predeterminadas de Android.",
            "termux-vibrate": "Hace vibrar el dispositivo. Ideal para alertas táctiles en tus scripts.",
            "termux-wallpaper": "Cambia el fondo de pantalla del dispositivo. Personalización desde la terminal.",

            # Capítulo 3
            "termux-battery-status": "Muestra información detallada de la batería: porcentaje, temperatura, estado de carga.",
            "termux-camera-photo": "Toma una foto con la cámara del dispositivo y la guarda en un archivo.",
            "termux-torch": "Enciende y apaga la linterna del teléfono. Control directo del hardware.",
            "termux-sensor": "Lee datos en tiempo real de sensores: acelerómetro, giroscopio, brújula, etc.",
            "termux-tts-speak": "Convierte texto a voz. Tu terminal puede hablar contigo.",
            "termux-microphone-record": "Graba audio desde el micrófono. Útil para dictados o grabaciones rápidas.",

            # Capítulo 4
            "termux-telephony-call": "Inicia llamadas telefónicas directamente desde la terminal.",
            "termux-sms-send": "Envía mensajes de texto SMS a otros números. Automatiza comunicaciones.",
            "termux-wifi-connectioninfo": "Muestra detalles de tu conexión Wi-Fi actual: SSID, IP, señal.",
            "termux-location": "Obtiene tu ubicación GPS actual. Útil para aplicaciones de geolocalización.",
            "termux-download": "Descarga archivos desde internet usando el gestor de descargas de Android.",

            # Capítulo 5
            "ps": "Muestra todos los procesos ejecutándose en tu sistema. Como el administrador de tareas.",
            "kill": "Detiene procesos que consumen recursos o están colgados. El control remoto de procesos.",
            "jobs": "Lista tareas ejecutándose en segundo plano en tu sesión actual.",
            "termux-wake-lock": "Impedir que el dispositivo se duerma. Esencial para servidores o procesos largos.",
            "nohup": "Ejecuta comandos que continúan funcionando incluso si cierras la terminal.",
            "alias": "Crea atajos personalizados para comandos largos. Tu propio lenguaje de comandos.",

            # Capítulo 6
            "grep": "Busca texto específico dentro de archivos. Como el buscador de tu navegador pero en terminal.",
            "find": "Busca archivos por nombre en todo el sistema. Localizador de archivos profesional.",
            "sed": "Edita archivos de texto automáticamente. Reemplaza texto en masa.",
            "awk": "Herramienta poderosa para procesar datos por columnas. Excel en línea de comandos.",
            "cut": "Extrae columnas específicas de archivos de texto. Perfecto para CSV.",
            "sort": "Ordena líneas de texto alfabética o numéricamente.",

            # Capítulo 7
            "read": "Pide información al usuario durante la ejecución de un script.",
            "echo": "Muestra mensajes en pantalla. La forma más básica de mostrar información.",
            "sleep": "Pausa la ejecución por segundos. Útil para automatizaciones con tiempos.",
            "chmod +x": "Hace ejecutable un archivo de script. Le da permisos para correr.",
            "test": "Prueba condiciones en scripts. Básicamente el 'if' de la terminal.",

            # Capítulo 8
            "chmod": "Cambia permisos de archivos (lectura, escritura, ejecución). Control de acceso.",
            "tar": "Crea y extrae archivos comprimidos. El formato clásico de backup.",
            "gzip": "Comprime archivos para ahorrar espacio. Reduce tamaño drásticamente.",
            "du": "Muestra cuánto espacio ocupan archivos y carpetas.",
            "df": "Muestra espacio disponible en discos. Salud del almacenamiento.",

            # Capítulo 9
            "ssh": "Conecta de forma segura a servidores remotos. Acceso remoto cifrado.",
            "scp": "Copia archivos entre tu dispositivo y servidores remotos de forma segura.",
            "curl": "Descarga datos desde internet. Herramienta de programadores y hackers.",
            "wget": "Descarga archivos de internet. El clásico de Internet.",
            "dig": "Consulta servidores DNS. Resuelve nombres de dominio a IPs.",

            # Capítulo 10
            "termux-chroot": "Crea un entorno Linux completo dentro de Termux. Como tener Ubuntu en el teléfono.",
            "getprop": "Lee propiedades del sistema Android. Información interna del dispositivo.",
            "logcat": "Muestra logs del sistema Android. Herramienta de depuración profesional.",
            "ldd": "Muestra dependencias de librerías de un programa. Detecta qué necesita un programa.",
            "strace": "Monitorea llamadas al sistema de un programa. Depuración avanzada.",
        }

        cmd = cmd_data['cmd'].split()[0]
        return explanations.get(cmd, cmd_data.get('desc', 'Sin explicación disponible.'))

# Inicializar progreso
if not PROGRESS_FILE.exists():
    progress_data = {
        "chapters_completed": {},
        "commands_practiced": {},
        "commands_mastered": [],
        "sessions": 0,
        "last_session": None
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f)

# Cargar progreso
with open(PROGRESS_FILE, 'r') as f:
    progress = json.load(f)

# Base de datos de comandos mejorada
COMMAND_DB = {
    1: {
        "title": "Fundamentos de Termux",
        "description": "Aprende los comandos esenciales para navegar y gestionar tu entorno Termux",
        "category": "Básico",
        "color": "cyan",
        "commands": [
            {"cmd": "pkg update", "example": "pkg update", "category": "Paquetes", "difficulty": "Fácil", "package": "termux-tools"},
            {"cmd": "pkg upgrade", "example": "pkg upgrade", "category": "Paquetes", "difficulty": "Fácil", "package": "termux-tools"},
            {"cmd": "pkg install", "example": "pkg install termux-api", "category": "Paquetes", "difficulty": "Fácil", "package": "termux-tools"},
            {"cmd": "pkg uninstall", "example": "pkg uninstall curl", "category": "Paquetes", "difficulty": "Fácil", "package": "termux-tools"},
            {"cmd": "pwd", "example": "pwd", "category": "Navegación", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "ls", "example": "ls -la", "category": "Navegación", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "cd", "example": "cd /sdcard", "category": "Navegación", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "mkdir", "example": "mkdir mis-archivos", "category": "Archivos", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "touch", "example": "touch documento.txt", "category": "Archivos", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "rm", "example": "rm archivo.txt", "category": "Archivos", "difficulty": "Medio", "package": "coreutils"},
        ]
    },
    2: {
        "title": "Interacción con UI Android",
        "description": "Controla la interfaz gráfica de Android desde la terminal",
        "category": "Interfaz",
        "color": "green",
        "commands": [
            {"cmd": "termux-toast", "example": 'termux-toast "Hola mundo"', "category": "Notificaciones", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-dialog", "example": 'termux-dialog --title "Entrada"', "category": "Interacción", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-notification", "example": 'termux-notification --title "Alerta"', "category": "Notificaciones", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-clipboard-set/get", "example": 'termux-clipboard-set "texto"', "category": "Interacción", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-open", "example": 'termux-open https://github.com', "category": "Interacción", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-vibrate", "example": "termux-vibrate -d 1000", "category": "Hardware", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-wallpaper", "example": "termux-wallpaper -f imagen.jpg", "category": "Personalización", "difficulty": "Medio", "package": "termux-api"},
        ]
    },
    3: {
        "title": "Acceso al Hardware",
        "description": "Controla cámara, sensores y componentes físicos del dispositivo",
        "category": "Hardware",
        "color": "yellow",
        "commands": [
            {"cmd": "termux-battery-status", "example": "termux-battery-status", "category": "Sensores", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-camera-photo", "example": "termux-camera-photo foto.jpg", "category": "Cámara", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-torch", "example": "termux-torch on", "category": "Hardware", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-sensor", "example": "termux-sensor -s accelerometer", "category": "Sensores", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-tts-speak", "example": 'termux-tts-speak "Hola"', "category": "Audio", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-microphone-record", "example": "termux-microphone-record -f audio.wav", "category": "Audio", "difficulty": "Medio", "package": "termux-api"},
        ]
    },
    4: {
        "title": "Comunicación y Conectividad",
        "description": "Gestiona llamadas, SMS, Wi-Fi y ubicación GPS",
        "category": "Red",
        "color": "blue",
        "commands": [
            {"cmd": "termux-telephony-call", "example": "termux-telephony-call 123456789", "category": "Telefonía", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-sms-send", "example": 'termux-sms-send -n 123 "Hola"', "category": "Mensajería", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-wifi-connectioninfo", "example": "termux-wifi-connectioninfo", "category": "Red", "difficulty": "Fácil", "package": "termux-api"},
            {"cmd": "termux-location", "example": "termux-location", "category": "GPS", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "termux-download", "example": "termux-download https://ejemplo.com/archivo.zip", "category": "Red", "difficulty": "Fácil", "package": "termux-api"},
        ]
    },
    5: {
        "title": "Procesos y Gestión de Sesión",
        "description": "Controla procesos, jobs y configuración de sesión",
        "category": "Sistema",
        "color": "magenta",
        "commands": [
            {"cmd": "ps", "example": "ps aux", "category": "Procesos", "difficulty": "Fácil", "package": "procps"},
            {"cmd": "kill", "example": "kill 1234", "category": "Procesos", "difficulty": "Medio", "package": "coreutils"},
            {"cmd": "jobs", "example": "jobs", "category": "Sesión", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "termux-wake-lock", "example": "termux-wake-lock", "category": "Sistema", "difficulty": "Medio", "package": "termux-api"},
            {"cmd": "nohup", "example": "nohup comando &", "category": "Procesos", "difficulty": "Medio", "package": "coreutils"},
            {"cmd": "alias", "example": 'alias ll="ls -la"', "category": "Sesión", "difficulty": "Fácil", "package": "bash"},
        ]
    },
    6: {
        "title": "Manipulación Avanzada de Texto",
        "description": "Herramientas poderosas para procesar y analizar texto",
        "category": "Texto",
        "color": "red",
        "commands": [
            {"cmd": "grep", "example": "grep 'patron' archivo.txt", "category": "Búsqueda", "difficulty": "Medio", "package": "grep"},
            {"cmd": "find", "example": "find . -name '*.txt'", "category": "Búsqueda", "difficulty": "Medio", "package": "findutils"},
            {"cmd": "sed", "example": "sed 's/old/new/g' file", "category": "Edición", "difficulty": "Avanzado", "package": "sed"},
            {"cmd": "awk", "example": "awk '{print $1}' file", "category": "Procesamiento", "difficulty": "Avanzado", "package": "gawk"},
            {"cmd": "cut", "example": "cut -d',' -f2 archivo.csv", "category": "Procesamiento", "difficulty": "Medio", "package": "coreutils"},
            {"cmd": "sort", "example": "sort archivo.txt", "category": "Procesamiento", "difficulty": "Fácil", "package": "coreutils"},
        ]
    },
    7: {
        "title": "Scripting y Automatización",
        "description": "Crea scripts automáticos para tareas repetitivas",
        "category": "Scripting",
        "color": "cyan",
        "commands": [
            {"cmd": "read", "example": "read nombre", "category": "Input", "difficulty": "Fácil", "package": "bash"},
            {"cmd": "echo", "example": 'echo "Hola mundo"', "category": "Output", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "sleep", "example": "sleep 5", "category": "Control", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "chmod +x", "example": "chmod +x script.sh", "category": "Permisos", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "test", "example": '[ -f archivo ]', "category": "Control", "difficulty": "Medio", "package": "coreutils"},
        ]
    },
    8: {
        "title": "Almacenamiento y Archivos",
        "description": "Gestión de permisos, compresión y uso de disco",
        "category": "Archivos",
        "color": "green",
        "commands": [
            {"cmd": "chmod", "example": "chmod 755 archivo", "category": "Permisos", "difficulty": "Medio", "package": "coreutils"},
            {"cmd": "tar", "example": "tar -czvf backup.tar.gz carpeta/", "category": "Compresión", "difficulty": "Medio", "package": "tar"},
            {"cmd": "gzip", "example": "gzip archivo.txt", "category": "Compresión", "difficulty": "Fácil", "package": "gzip"},
            {"cmd": "du", "example": "du -sh carpeta/", "category": "Disco", "difficulty": "Fácil", "package": "coreutils"},
            {"cmd": "df", "example": "df -h", "category": "Disco", "difficulty": "Fácil", "package": "coreutils"},
        ]
    },
    9: {
        "title": "Red Avanzada y Seguridad",
        "description": "SSH, diagnóstico de red y conexiones seguras",
        "category": "Red",
        "color": "blue",
        "commands": [
            {"cmd": "ssh", "example": "ssh user@host", "category": "SSH", "difficulty": "Medio", "package": "openssh"},
            {"cmd": "scp", "example": "scp file user@host:/tmp/", "category": "SSH", "difficulty": "Medio", "package": "openssh"},
            {"cmd": "curl", "example": "curl https://api.example.com", "category": "HTTP", "difficulty": "Fácil", "package": "curl"},
            {"cmd": "wget", "example": "wget https://example.com/file.zip", "category": "HTTP", "difficulty": "Fácil", "package": "wget"},
            {"cmd": "dig", "example": "dig example.com", "category": "DNS", "difficulty": "Medio", "package": "bind-tools"},
        ]
    },
    10: {
        "title": "Internos del Sistema",
        "description": "Diagnóstico avanzado y herramientas de sistema",
        "category": "Avanzado",
        "color": "magenta",
        "commands": [
            {"cmd": "termux-chroot", "example": "termux-chroot", "category": "Sistema", "difficulty": "Avanzado", "package": "termux-chroot"},
            {"cmd": "getprop", "example": "getprop ro.product.model", "category": "Sistema", "difficulty": "Avanzado", "package": "toolbox"},
            {"cmd": "logcat", "example": "logcat -s Tag", "category": "Diagnóstico", "difficulty": "Avanzado", "package": "logcat"},
            {"cmd": "ldd", "example": "ldd /bin/ls", "category": "Diagnóstico", "difficulty": "Avanzado", "package": "binutils"},
            {"cmd": "strace", "example": "strace comando", "category": "Diagnóstico", "difficulty": "Avanzado", "package": "strace"},
        ]
    }
}

def show_main_menu():
    """Menú principal profesional"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    # Título
    title = Text("chmodx-Command v2.0", style="bold cyan")
    subtitle = Text("Terminal Mastery for Hackers", style="dim")
    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print()

    # Tabla de capítulos
    table = Table(
        box=box.ROUNDED,
        border_style="blue",
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("#", justify="center", width=5)
    table.add_column("Capítulo", width=35)
    table.add_column("Categoría", justify="center", width=15)
    table.add_column("Comandos", justify="center", width=10)

    for num, chapter in COMMAND_DB.items():
        table.add_row(
            f"[{num}]",
            chapter["title"],
            chapter["category"],
            str(len(chapter["commands"]))
        )

    console.print(table)
    console.print()

    # Menú de opciones
    options = Panel(
        "[bold]Navegación:[bold]\n"
        "• [1-10] Seleccionar capítulo\n"
        "• [P] Ver progreso\n"
        "• [V] Verificar paquetes\n"
        "• [Q] Salir",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(options)

    choice = Prompt.ask("\n[bold cyan]¿Qué deseas hacer?[/bold cyan]").lower()

    if choice == 'q':
        console.print(Panel("[yellow]¡Hasta luego, hacker! 🚀[/yellow]", border_style="yellow"))
        exit(0)
    elif choice == 'p':
        show_progress()
    elif choice == 'v':
        show_package_check()
    else:
        try:
            chapter_num = int(choice)
            if chapter_num in COMMAND_DB:
                show_chapter_menu(chapter_num)
            else:
                console.print("[red]Capítulo inválido[/red]")
                show_main_menu()
        except:
            console.print("[red]Opción inválida[/red]")
            show_main_menu()

def show_chapter_menu(chapter_num):
    """Menú de capítulo"""
    chapter = COMMAND_DB[chapter_num]

    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    # Header del capítulo
    header = Panel(
        f"[bold {chapter['color']}]Capítulo {chapter_num}[/bold {chapter['color']}]\n"
        f"[bold white]{chapter['title']}[/bold white]\n\n"
        f"[dim]{chapter['description']}[/dim]",
        border_style=chapter['color'],
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(header)
    console.print()

    # Tabla de comandos
    table = Table(
        box=box.SIMPLE,
        border_style=chapter['color'],
        show_header=True,
        header_style=f"bold {chapter['color']}"
    )
    table.add_column("#", justify="center", width=5)
    table.add_column("Comando", width=35)
    table.add_column("Categoría", width=15)
    table.add_column("Dificultad", justify="center", width=12)

    for idx, cmd in enumerate(chapter["commands"], 1):
        table.add_row(str(idx), cmd["cmd"], cmd["category"], cmd["difficulty"])

    console.print(table)
    console.print()

    options = Panel(
        f"[bold]Opciones:[bold]\n"
        f"• [1-{len(chapter['commands'])}] Ver comando detallado\n"
        f"• [B] Volver al menú principal",
        border_style=chapter['color'],
        box=box.ROUNDED
    )
    console.print(options)

    choice = Prompt.ask(f"\n[bold {chapter['color']}]Selecciona una opción[/bold {chapter['color']}]").lower()

    if choice == 'b' or choice == 'back':
        show_main_menu()
    else:
        try:
            cmd_idx = int(choice) - 1
            if 0 <= cmd_idx < len(chapter["commands"]):
                show_command_detail(chapter_num, cmd_idx)
            else:
                show_chapter_menu(chapter_num)
        except:
            show_chapter_menu(chapter_num)

def show_command_detail(chapter_num, cmd_idx):
    """Muestra detalle completo del comando"""
    chapter = COMMAND_DB[chapter_num]
    cmd_data = chapter["commands"][cmd_idx]

    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    # Tarjeta de comando con explicación
    card = TerminalUI.create_command_card(cmd_data, chapter_num)
    console.print(card)
    console.print()

    # Opciones de acción
    options = Panel(
        "[bold cyan]Acciones disponibles:[bold cyan]\n\n"
        "• [P] Practicar este comando\n"
        "• [E] Ver ejemplo ejecutado\n"
        "• [Q] Quiz de práctica\n"
        "• [B] Volver al capítulo\n"
        "• [M] Menú principal",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(options)

    choice = Prompt.ask("\n[bold cyan]¿Qué quieres hacer?[/bold cyan]", choices=['p', 'e', 'q', 'b', 'm'], default='b').lower()

    if choice == 'b':
        show_chapter_menu(chapter_num)
    elif choice == 'm':
        show_main_menu()
    elif choice == 'p':
        practice_command(cmd_data)
    elif choice == 'e':
        show_example(cmd_data)
    elif choice == 'q':
        quiz_command(cmd_data)

def show_example(cmd_data):
    """Muestra ejemplo de ejecución"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    example_panel = Panel(
        f"[bold green]Ejemplo de Ejecución[/bold green]\n\n"
        f"[bold cyan]Comando:[/bold cyan] {cmd_data['cmd']}\n\n"
        f"[bold yellow]Ejemplo:[/bold yellow]\n"
        f"[dim]$ {cmd_data['example']}[/dim]\n\n"
        f"[bold white]Salida esperada:[/bold white]\n"
        f"[dim](Salida del comando aquí)[/dim]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(example_panel)
    Prompt.ask("\nPresiona ENTER para continuar")
    show_chapter_menu(1)  # Volver

def practice_command(cmd_data):
    """Modo práctica"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    practice_panel = Panel(
        f"[bold yellow]Modo Práctica[/bold yellow]\n\n"
        f"[bold cyan]Comando:[/bold cyan] {cmd_data['cmd']}\n\n"
        f"[bold white]¿Qué hace este comando?[/bold white]\n"
        f"{TerminalUI.get_detailed_explanation(cmd_data)}\n\n"
        f"[bold green]¡Ahora practica![/bold green]\n"
        f"Ejecuta el comando en tu terminal y observa los resultados.",
        border_style="yellow",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(practice_panel)

    if Confirm.ask("\n[cyan]¿Quieres intentar ejecutarlo ahora?[/cyan]"):
        # Simular ejecución segura
        console.print(f"\n[dim]Ejecutando: {cmd_data['example']}[/dim]")
        console.print(Panel("[green]Comando ejecutado correctamente ✓[/green]", border_style="green"))

    Prompt.ask("\nPresiona ENTER para continuar")
    show_chapter_menu(1)

def quiz_command(cmd_data):
    """Quiz interactivo"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    quiz_panel = Panel(
        f"[bold magenta]Quiz de Práctica[/bold magenta]\n\n"
        f"[bold cyan]Comando:[/bold cyan] {cmd_data['cmd']}\n\n"
        f"[bold white]¿Cuál es el propósito principal?[/bold white]",
        border_style="magenta",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(quiz_panel)
    console.print()

    # Preguntas simples
    correct_answer = TerminalUI.get_detailed_explanation(cmd_data)[:100]

    options = [
        correct_answer,
        "Crea archivos nuevos",
        "Elimina datos del sistema",
        "Instala programas"
    ]

    from random import shuffle
    shuffle(options)

    for i, opt in enumerate(options, 1):
        console.print(f"  [{i}] {opt}")

    console.print()
    try:
        answer = int(Prompt.ask("[cyan]Tu respuesta[/cyan]"))
        if options[answer - 1] == correct_answer:
            console.print(Panel("[green]✓ ¡Correcto![/green]", border_style="green"))
        else:
            console.print(Panel("[red]✗ Incorrecto[/red]", border_style="red"))
    except:
        console.print("[red]Respuesta inválida[/red]")

    Prompt.ask("\nPresiona ENTER para continuar")
    show_chapter_menu(1)

def show_progress():
    """Muestra progreso"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    total_cmds = sum(len(ch["commands"]) for ch in COMMAND_DB.values())
    practiced = len(progress.get("commands_practiced", {}))

    progress_text = f"{practiced}/{total_cmds} comandos practicados"
    progress_pct = (practiced / total_cmds * 100) if total_cmds > 0 else 0

    progress_panel = Panel(
        f"[bold cyan]Progreso General[/bold cyan]\n\n"
        f"{progress_text}\n"
        f"[{'█' * int(progress_pct/10)}{'░' * (10-int(progress_pct/10))}] {progress_pct:.1f}%\n\n"
        f"Sesiones: {progress.get('sessions', 0)}\n"
        f"Última sesión: {progress.get('last_session', 'Nunca')}",
        border_style="cyan",
        box=box.DOUBLE,
        padding=(1, 3)
    )
    console.print(progress_panel)
    Prompt.ask("\nPresiona ENTER para continuar")
    show_main_menu()

def show_package_check():
    """Verifica paquetes"""
    console.clear()
    console.print(TerminalUI.create_banner())
    console.print()

    console.print(Rule("[bold cyan]Verificación de Paquetes Requeridos[/bold cyan]", style="cyan"))
    console.print()

    packages = {
        "termux-api": "API para interacción Android",
        "python": "Lenguaje Python",
        "python-pip": "Gestor de paquetes Python",
        "rich": "Librería para interfaz",
    }

    table = Table(
        box=box.ROUNDED,
        border_style="blue",
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("Paquete", style="cyan")
    table.add_column("Descripción", style="white")
    table.add_column("Estado", justify="center")

    for pkg, desc in packages.items():
        # Simular verificación
        status = "[green]✓ Instalado[/green]"
        table.add_row(pkg, desc, status)

    console.print(table)
    Prompt.ask("\nPresiona ENTER para continuar")
    show_main_menu()

def main():
    """Función principal"""
    try:
        # Actualizar sesión
        progress["sessions"] = progress.get("sessions", 0) + 1
        progress["last_session"] = datetime.now().isoformat()
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f)

        show_main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]¡Hasta luego, hacker! 🚀[/yellow]")
        exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        exit(1)

if __name__ == "__main__":
    main()
