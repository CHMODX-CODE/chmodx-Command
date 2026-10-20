#!/usr/bin/env python3
"""
chmodx-Command v1.0
Terminal Mastery for Hackers
Made for chmodx

Programa educativo interactivo para aprender comandos de Termux
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.columns import Columns
    from rich import box
    from rich.align import Align
    from rich.style import Style
    from rich.live import Live
except ImportError:
    print("Error: rich library not installed. Install with: pip install rich")
    sys.exit(1)

console = Console()

# Configuración
HOME_DIR = Path.home()
DATA_DIR = HOME_DIR / ".chmodx-command"
DATA_DIR.mkdir(exist_ok=True)
PROGRESS_FILE = DATA_DIR / "progress.json"
LOG_FILE = DATA_DIR / "activity.log"

class ProgressTracker:
    """Gestor de progreso del usuario"""

    def __init__(self):
        self.data = self.load()

    def load(self):
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            "chapters_completed": {},
            "commands_practiced": {},
            "commands_mastered": [],
            "total_commands": 0,
            "commands_learned": 0,
            "sessions": 0,
            "last_session": None,
            "started_at": datetime.now().isoformat()
        }

    def save(self):
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def log_activity(self, activity):
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {activity}\n")

    def update_chapter_progress(self, chapter_num, progress):
        self.data["chapters_completed"][str(chapter_num)] = progress
        self.save()

    def mark_command_practiced(self, command):
        self.data["commands_practiced"][command] = datetime.now().isoformat()
        self.save()

# Inicializar tracker
tracker = ProgressTracker()

# Base de datos de comandos
COMMAND_DATABASE = {
    1: {
        "title": "Fundamentos de Termux",
        "description": "Esenciales para gestionar el entorno Termux",
        "category": "Básico",
        "commands": [
            {
                "cmd": "pkg update",
                "example": "pkg update",
                "desc": "Actualiza lista de paquetes disponibles",
                "category": "Paquetes",
                "difficulty": "Fácil",
                "package": "termux-tools"
            },
            {
                "cmd": "pkg upgrade",
                "example": "pkg upgrade",
                "desc": "Actualiza todos los paquetes instalados",
                "category": "Paquetes",
                "difficulty": "Fácil",
                "package": "termux-tools"
            },
            {
                "cmd": "pkg install",
                "example": "pkg install termux-api",
                "desc": "Instala paquete específico",
                "category": "Paquetes",
                "difficulty": "Fácil",
                "package": "termux-tools"
            },
            {
                "cmd": "pkg uninstall",
                "example": "pkg uninstall curl",
                "desc": "Elimina paquete",
                "category": "Paquetes",
                "difficulty": "Fácil",
                "package": "termux-tools"
            },
            {
                "cmd": "pwd",
                "example": "pwd",
                "desc": "Muestra directorio actual",
                "category": "Navegación",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "ls",
                "example": "ls -la",
                "desc": "Lista archivos y directorios",
                "category": "Navegación",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "cd",
                "example": "cd /sdcard",
                "desc": "Cambia directorio",
                "category": "Navegación",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "mkdir",
                "example": "mkdir nueva_carpeta",
                "desc": "Crea directorio",
                "category": "Archivos",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "touch",
                "example": "touch archivo.txt",
                "desc": "Crea archivo vacío",
                "category": "Archivos",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "rm",
                "example": "rm archivo.txt",
                "desc": "Elimina archivo",
                "category": "Archivos",
                "difficulty": "Medio",
                "package": "coreutils"
            },
        ]
    },
    2: {
        "title": "Interacción con la UI Android",
        "description": "Comandos termux-api para interactuar con Android",
        "category": "UI",
        "commands": [
            {
                "cmd": "termux-toast",
                "example": 'termux-toast "Hola mundo"',
                "desc": "Muestra mensaje temporal (toast)",
                "category": "Notificaciones",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-dialog",
                "example": 'termux-dialog --title "Título"',
                "desc": "Crea diálogo para entrada de usuario",
                "category": "Interacción",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-notification",
                "example": 'termux-notification --title "Alerta"',
                "desc": "Publica notificación Android",
                "category": "Notificaciones",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-clipboard-set/get",
                "example": 'termux-clipboard-set "texto"',
                "desc": "Lee/Escribe portapapeles",
                "category": "Interacción",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-open",
                "example": 'termux-open https://github.com',
                "desc": "Abre URL o archivo",
                "category": "Interacción",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-vibrate",
                "example": "termux-vibrate -d 1000",
                "desc": "Activa vibrador del dispositivo",
                "category": "Hardware",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-wallpaper",
                "example": "termux-wallpaper -f imagen.jpg",
                "desc": "Cambia wallpaper del dispositivo",
                "category": "Personalización",
                "difficulty": "Medio",
                "package": "termux-api"
            },
        ]
    },
    3: {
        "title": "Acceso al Hardware",
        "description": "Control de cámara, sensores y componentes físicos",
        "category": "Hardware",
        "commands": [
            {
                "cmd": "termux-battery-status",
                "example": "termux-battery-status",
                "desc": "Estado de batería en JSON",
                "category": "Sensores",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-camera-photo",
                "example": "termux-camera-photo -c 0 foto.jpg",
                "desc": "Toma foto con cámara",
                "category": "Cámara",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-torch",
                "example": "termux-torch on",
                "desc": "Controla linterna",
                "category": "Hardware",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-sensor",
                "example": "termux-sensor -s accelerometer",
                "desc": "Lee datos de sensores",
                "category": "Sensores",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-tts-speak",
                "example": 'termux-tts-speak "Hola"',
                "desc": "Texto a voz",
                "category": "Audio",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-microphone-record",
                "example": "termux-microphone-record -f audio.wav -l 5",
                "desc": "Graba audio de micrófono",
                "category": "Audio",
                "difficulty": "Medio",
                "package": "termux-api"
            },
        ]
    },
    4: {
        "title": "Comunicación y Conectividad",
        "description": "SMS, llamadas, Wi-Fi y GPS",
        "category": "Red",
        "commands": [
            {
                "cmd": "termux-telephony-call",
                "example": "termux-telephony-call 123456789",
                "desc": "Inicia llamada telefónica",
                "category": "Telefonía",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-sms-send",
                "example": 'termux-sms-send -n 123456789 "Hola"',
                "desc": "Envía SMS",
                "category": "Mensajería",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-wifi-connectioninfo",
                "example": "termux-wifi-connectioninfo",
                "desc": "Información Wi-Fi actual",
                "category": "Red",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
            {
                "cmd": "termux-location",
                "example": "termux-location",
                "desc": "Ubicación GPS actual",
                "category": "GPS",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "termux-download",
                "example": "termux-download https://example.com/file.zip",
                "desc": "Descarga archivo",
                "category": "Red",
                "difficulty": "Fácil",
                "package": "termux-api"
            },
        ]
    },
    5: {
        "title": "Procesos y Gestión de Sesión",
        "description": "Control de procesos, jobs y configuración",
        "category": "Sistema",
        "commands": [
            {
                "cmd": "ps",
                "example": "ps aux",
                "desc": "Lista procesos en ejecución",
                "category": "Procesos",
                "difficulty": "Fácil",
                "package": "procps"
            },
            {
                "cmd": "kill",
                "example": "kill 1234",
                "desc": "Termina proceso por PID",
                "category": "Procesos",
                "difficulty": "Medio",
                "package": "coreutils"
            },
            {
                "cmd": "jobs",
                "example": "jobs",
                "desc": "Muestra jobs en background",
                "category": "Sesión",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "termux-wake-lock",
                "example": "termux-wake-lock",
                "desc": "Previene suspensión del dispositivo",
                "category": "Sistema",
                "difficulty": "Medio",
                "package": "termux-api"
            },
            {
                "cmd": "nohup",
                "example": "nohup command &",
                "desc": "Ejecuta comando ignorando hangup",
                "category": "Procesos",
                "difficulty": "Medio",
                "package": "coreutils"
            },
            {
                "cmd": "alias",
                "example": 'alias ll="ls -la"',
                "desc": "Crea atajos de comando",
                "category": "Sesión",
                "difficulty": "Fácil",
                "package": "bash"
            },
        ]
    },
    6: {
        "title": "Manipulación Avanzada de Texto",
        "description": "grep, sed, awk y procesamiento de datos",
        "category": "Texto",
        "commands": [
            {
                "cmd": "grep",
                "example": "grep 'patron' archivo.txt",
                "desc": "Busca patrones en texto",
                "category": "Búsqueda",
                "difficulty": "Medio",
                "package": "grep"
            },
            {
                "cmd": "find",
                "example": "find . -name '*.txt'",
                "desc": "Busca archivos por nombre",
                "category": "Búsqueda",
                "difficulty": "Medio",
                "package": "findutils"
            },
            {
                "cmd": "sed",
                "example": "sed 's/old/new/g' file",
                "desc": "Editor de flujo para texto",
                "category": "Edición",
                "difficulty": "Avanzado",
                "package": "sed"
            },
            {
                "cmd": "awk",
                "example": "awk '{print $1}' file",
                "desc": "Procesamiento de patrones",
                "category": "Procesamiento",
                "difficulty": "Avanzado",
                "package": "gawk"
            },
            {
                "cmd": "cut",
                "example": "cut -d',' -f2 archivo.csv",
                "desc": "Extrae columnas de texto",
                "category": "Procesamiento",
                "difficulty": "Medio",
                "package": "coreutils"
            },
            {
                "cmd": "sort",
                "example": "sort archivo.txt",
                "desc": "Ordena líneas de texto",
                "category": "Procesamiento",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
        ]
    },
    7: {
        "title": "Scripting y Automatización",
        "description": "Creación de scripts shell automáticos",
        "category": "Scripting",
        "commands": [
            {
                "cmd": "read",
                "example": "read nombre",
                "desc": "Lee entrada del usuario",
                "category": "Input",
                "difficulty": "Fácil",
                "package": "bash"
            },
            {
                "cmd": "echo",
                "example": 'echo "Hola mundo"',
                "desc": "Muestra texto en terminal",
                "category": "Output",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "sleep",
                "example": "sleep 5",
                "desc": "Pausa ejecución del script",
                "category": "Control",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "chmod +x",
                "example": "chmod +x script.sh",
                "desc": "Hace script ejecutable",
                "category": "Permisos",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "test",
                "example": '[ -f archivo ]',
                "desc": "Evalúa condiciones",
                "category": "Control",
                "difficulty": "Medio",
                "package": "coreutils"
            },
        ]
    },
    8: {
        "title": "Almacenamiento y Archivos",
        "description": "Permisos, compresión y gestión de archivos",
        "category": "Archivos",
        "commands": [
            {
                "cmd": "chmod",
                "example": "chmod 755 archivo",
                "desc": "Cambia permisos de archivo",
                "category": "Permisos",
                "difficulty": "Medio",
                "package": "coreutils"
            },
            {
                "cmd": "tar",
                "example": "tar -czvf backup.tar.gz carpeta/",
                "desc": "Crea/extrae archivos comprimidos",
                "category": "Compresión",
                "difficulty": "Medio",
                "package": "tar"
            },
            {
                "cmd": "gzip",
                "example": "gzip archivo.txt",
                "desc": "Comprime archivos",
                "category": "Compresión",
                "difficulty": "Fácil",
                "package": "gzip"
            },
            {
                "cmd": "du",
                "example": "du -sh carpeta/",
                "desc": "Muestra uso de disco",
                "category": "Disco",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
            {
                "cmd": "df",
                "example": "df -h",
                "desc": "Espacio disponible en discos",
                "category": "Disco",
                "difficulty": "Fácil",
                "package": "coreutils"
            },
        ]
    },
    9: {
        "title": "Red Avanzada y Seguridad",
        "description": "SSH, SFTP, diagnóstico de red",
        "category": "Red",
        "commands": [
            {
                "cmd": "ssh",
                "example": "ssh user@host",
                "desc": "Conexión segura remota",
                "category": "SSH",
                "difficulty": "Medio",
                "package": "openssh"
            },
            {
                "cmd": "scp",
                "example": "scp local.txt user@host:/tmp/",
                "desc": "Copia archivos segura",
                "category": "SSH",
                "difficulty": "Medio",
                "package": "openssh"
            },
            {
                "cmd": "curl",
                "example": "curl https://api.example.com",
                "desc": "Transferencia de datos HTTP",
                "category": "HTTP",
                "difficulty": "Fácil",
                "package": "curl"
            },
            {
                "cmd": "wget",
                "example": "wget https://example.com/file.zip",
                "desc": "Descarga archivos de internet",
                "category": "HTTP",
                "difficulty": "Fácil",
                "package": "wget"
            },
            {
                "cmd": "dig",
                "example": "dig example.com",
                "desc": "Consulta DNS",
                "category": "DNS",
                "difficulty": "Medio",
                "package": "bind-tools"
            },
        ]
    },
    10: {
        "title": "Internos del Sistema",
        "description": "Diagnóstico avanzado y configuración",
        "category": "Avanzado",
        "commands": [
            {
                "cmd": "termux-chroot",
                "example": "termux-chroot",
                "desc": "Entorno chroot tradicional",
                "category": "Sistema",
                "difficulty": "Avanzado",
                "package": "termux-chroot"
            },
            {
                "cmd": "getprop",
                "example": "getprop ro.product.model",
                "desc": "Propiedades del sistema Android",
                "category": "Sistema",
                "difficulty": "Avanzado",
                "package": "toolbox"
            },
            {
                "cmd": "logcat",
                "example": "logcat -s Tag",
                "desc": "Logs del sistema Android",
                "category": "Diagnóstico",
                "difficulty": "Avanzado",
                "package": "logcat"
            },
            {
                "cmd": "ldd",
                "example": "ldd /bin/ls",
                "desc": "Dependencias de librerías",
                "category": "Diagnóstico",
                "difficulty": "Avanzado",
                "package": "binutils"
            },
            {
                "cmd": "strace",
                "example": "strace comando",
                "desc": "Traza llamadas al sistema",
                "category": "Diagnóstico",
                "difficulty": "Avanzado",
                "package": "strace"
            },
        ]
    }
}

def check_package_installed(package_name):
    """Verifica si un paquete está instalado"""
    try:
        result = subprocess.run(
            ['pkg', 'list-installed'],
            capture_output=True, text=True, timeout=5
        )
        return package_name in result.stdout.lower() or \
               any(package_name.lower() in line.lower() for line in result.stdout.split('\n'))
    except:
        return False

def show_ascii_art():
    """Muestra arte ASCII del logo"""
    art = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         ██████╗██╗  ██╗███╗   ███╗ ██████╗ ███████╗██╗  ██╗   ║
    ║        ██╔════╝██║  ██║████╗ ████║██╔════╝ ██╔════╝██║  ██║   ║
    ║        ██║     ███████║██╔████╔██║██║  ███╗█████╗  ███████║   ║
    ║        ██║     ██╔══██║██║╚██╔╝██║██║   ██║██╔══╝  ██╔══██║   ║
    ║        ╚██████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝███████╗██║  ██║   ║
    ║         ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ║
    ║                                                              ║
    ║                    Terminal Mastery                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(art, style="bold cyan")

def show_main_menu():
    """Menú principal"""
    console.clear()
    show_ascii_art()

    # Título
    title = Text("chmodx-Command v1.0", style="bold cyan")
    subtitle = Text("Terminal Mastery for Hackers", style="dim")
    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print()

    # Tabla de capítulos
    table = Table(box=box.ROUNDED, border_style="blue", show_header=True)
    table.add_column("Cap", style="cyan", justify="center", width=6)
    table.add_column("Capítulo", style="white", width=35)
    table.add_column("Categoría", style="yellow", width=18)
    table.add_column("Comandos", style="green", justify="center", width=10)

    for num, chapter in COMMAND_DATABASE.items():
        completed = tracker.data.get("chapters_completed", {}).get(str(num), 0)
        cmd_count = len(chapter["commands"])
        table.add_row(
            f"[{num}]",
            chapter["title"],
            chapter["category"],
            f"{cmd_count}"
        )

    console.print(table)
    console.print()

    # Opciones
    options = Panel(
        "[bold cyan]Opciones:[/bold cyan]\n"
        "• Selecciona un capítulo (1-10)\n"
        "• [P] Progreso\n"
        "• [V] Verificar paquetes\n"
        "• [Q] Salir",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(options)

    choice = Prompt.ask("\n[bold cyan]Selecciona una opción[/bold cyan]").lower()

    if choice == 'q':
        console.print(Panel("[yellow]¡Hasta luego, hacker! 🚀[/yellow]", border_style="yellow"))
        exit(0)
    elif choice == 'p':
        show_progress()
    elif choice == 'v':
        show_package_verification()
    else:
        try:
            chapter_num = int(choice)
            if chapter_num in COMMAND_DATABASE:
                show_chapter_menu(chapter_num)
            else:
                console.print("[red]Capítulo inválido[/red]")
                show_main_menu()
        except:
            console.print("[red]Opción inválida[/red]")
            show_main_menu()

def show_progress():
    """Muestra progreso del usuario"""
    console.clear()
    show_ascii_art()

    total_cmds = sum(len(ch["commands"]) for ch in COMMAND_DATABASE.values())
    practiced = len(tracker.data.get("commands_practiced", {}))

    progress_text = f"{practiced}/{total_cmds} comandos practicados"
    progress_pct = (practiced / total_cmds * 100) if total_cmds > 0 else 0

    progress_panel = Panel(
        f"[bold cyan]Progreso General[/bold cyan]\n\n"
        f"{progress_text}\n"
        f"[{progress_pct:.1f}% completado]\n\n"
        f"Sesiones: {tracker.data.get('sessions', 0)}\n"
        f"Última sesión: {tracker.data.get('last_session', 'Nunca')}",
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(progress_panel)
    console.print()

    Prompt.ask("Presiona ENTER para continuar")
    show_main_menu()

def show_package_verification():
    """Verificador de paquetes"""
    console.clear()
    show_ascii_art()

    console.print(Panel("[bold cyan]Verificación de Paquetes Requeridos[/bold cyan]", border_style="cyan"))
    console.print()

    packages_needed = {
        "termux-api": "API para interacción Android",
        "proot": "Chroot y distribuciones Linux",
        "openssh": "SSH y SFTP",
        "curl": "Transferencia HTTP",
        "wget": "Descargas",
        "jq": "Procesamiento JSON",
        "python": "Este programa",
    }

    table = Table(box=box.ROUNDED, border_style="blue")
    table.add_column("Paquete", style="cyan", width=20)
    table.add_column("Descripción", style="white", width=40)
    table.add_column("Estado", style="yellow", width=15)

    missing = []
    for pkg, desc in packages_needed.items():
        installed = check_package_installed(pkg)
        status = "[green]✓ Instalado[/green]" if installed else "[red]✗ Falta[/red]"
        if not installed:
            missing.append(pkg)
        table.add_row(pkg, desc, status)

    console.print(table)
    console.print()

    if missing:
        console.print(Panel(
            f"[yellow]Paquetes faltantes: {', '.join(missing)}[/yellow]\n\n"
            f"Instalar con: pkg install {' '.join(missing)}",
            border_style="yellow"
        ))

    Prompt.ask("\nPresiona ENTER para continuar")
    show_main_menu()

def show_chapter_menu(chapter_num):
    """Menú de capítulo"""
    chapter = COMMAND_DATABASE[chapter_num]

    console.clear()
    show_ascii_art()

    # Header del capítulo
    header = Panel(
        f"[bold cyan]Capítulo {chapter_num}[/bold cyan]\n"
        f"[bold white]{chapter['title']}[/bold white]\n\n"
        f"[dim]{chapter['description']}[/dim]",
        border_style="green",
        box=box.DOUBLE,
        expand=False
    )
    console.print(header)
    console.print()

    # Lista de comandos
    table = Table(box=box.SIMPLE, border_style="blue", show_header=True)
    table.add_column("#", style="cyan", justify="center", width=4)
    table.add_column("Comando", style="white", width=35)
    table.add_column("Categoría", style="yellow", width=15)
    table.add_column("Dificultad", style="magenta", width=12)

    for idx, cmd in enumerate(chapter["commands"], 1):
        practiced = "✓" if cmd["cmd"] in tracker.data.get("commands_practiced", {}) else "○"
        table.add_row(
            f"{idx} {practiced}",
            cmd["cmd"],
            cmd["category"],
            cmd["difficulty"]
        )

    console.print(table)
    console.print()

    # Opciones
    console.print("[bold cyan]Opciones:[/bold cyan] [1-{}] Ver comando | [b] Volver | [p] Práctica".format(
        len(chapter["commands"])
    ))

    choice = Prompt.ask("\nSelecciona").lower()

    if choice == 'b':
        show_main_menu()
    elif choice == 'p':
        practice_mode(chapter_num)
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
    """Detalles de un comando específico"""
    chapter = COMMAND_DATABASE[chapter_num]
    cmd = chapter["commands"][cmd_idx]

    console.clear()
    show_ascii_art()

    # Panel de comando
    cmd_panel = Panel(
        f"[bold green]{cmd['cmd']}[/bold green]\n\n"
        f"[white]{cmd['desc']}[/white]\n\n"
        f"[cyan]Ejemplo:[/cyan] {cmd['example']}\n\n"
        f"[yellow]Categoría:[/yellow] {cmd['category']}\n"
        f"[yellow]Dificultad:[/yellow] {cmd['difficulty']}\n"
        f"[yellow]Paquete:[/yellow] {cmd['package']}",
        title=f"Capítulo {chapter_num} - Comando {cmd_idx + 1}",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(cmd_panel)
    console.print()

    # Verificar paquete
    pkg_installed = check_package_installed(cmd["package"])
    if not pkg_installed:
        console.print(Panel(
            f"[yellow]⚠ Paquete requerido no instalado[/yellow]\n"
            f"Ejecuta: [cyan]pkg install {cmd['package']}[/cyan]",
            border_style="yellow"
        ))
        console.print()

    # Menú de acciones
    actions = Panel(
        "[bold cyan]Acciones disponibles:[/bold cyan]\n\n"
        "• [P] Práctica interactiva\n"
        "• [E] Ejecutar comando\n"
        "• [Q] Quiz del comando\n"
        "• [M] Menú anterior\n"
        "• [B] Volver al menú principal",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(actions)

    choice = Prompt.ask("\n[bold cyan]Selecciona acción[/bold cyan]", choices=['p', 'e', 'q', 'm', 'b'], default='m').lower()

    if choice == 'p':
        practice_command(cmd, chapter_num)
    elif choice == 'e':
        execute_command(cmd)
    elif choice == 'q':
        quiz_command(cmd)
    elif choice == 'b':
        show_main_menu()
    else:
        show_chapter_menu(chapter_num)

def practice_command(cmd, chapter_num):
    """Modo práctica de comando"""
    console.clear()
    show_ascii_art()

    practice_panel = Panel(
        f"[bold yellow]Modo Práctica[/bold yellow]\n\n"
        f"[bold cyan]Comando:[/bold cyan] {cmd['cmd']}\n\n"
        f"[bold white]Descripción:[/bold white] {cmd['desc']}\n\n"
        f"[bold cyan]Ejemplo:[/bold cyan] {cmd['example']}\n\n"
        f"[dim]¿Qué hace este comando exactamente?[/dim]",
        border_style="yellow",
        box=box.DOUBLE
    )
    console.print(practice_panel)
    console.print()

    if Confirm.ask("[cyan]¿Quieres intentar ejecutarlo?[/cyan]"):
        try:
            console.print(f"\n[dim]Ejecutando: {cmd['cmd']}...[/dim]")
            # Simulación segura
            if cmd['cmd'] in ['pwd', 'ls', 'termux-battery-status']:
                result = subprocess.run(
                    cmd['cmd'].split(),
                    capture_output=True, text=True, timeout=5
                )
                console.print(Panel(result.stdout[:500], border_style="green"))
            else:
                console.print(Panel(
                    "[yellow]Comando no ejecutado en modo sandbox[/yellow]\n"
                    "[dim]Ejecuta manualmente cuando domines el comando[/dim]",
                    border_style="yellow"
                ))

            tracker.mark_command_practiced(cmd['cmd'])
            console.print("\n[green]✓ Comando practicado[/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    Prompt.ask("\nPresiona ENTER para continuar")

def execute_command(cmd):
    """Ejecuta un comando"""
    console.print(f"\n[yellow]⚠ Ejecutando: {cmd['cmd']}[/yellow]")
    console.print(f"[dim]Ejemplo: {cmd['example']}[/dim]")
    console.print("[yellow]El comando se ejecutará en tu terminal[/yellow]")
    Prompt.ask("\nPresiona ENTER para continuar")

def quiz_command(cmd):
    """Quiz de comando"""
    console.clear()
    show_ascii_art()

    quiz_panel = Panel(
        f"[bold magenta]Quiz Rápido[/bold magenta]\n\n"
        f"[bold cyan]Comando:[/bold cyan] {cmd['cmd']}\n\n"
        f"[dim]¿Cuál es la descripción correcta?[/dim]",
        border_style="magenta",
        box=box.DOUBLE
    )
    console.print(quiz_panel)
    console.print()

    # Pregunta simple
    options = [
        cmd['desc'],
        "Crea un archivo nuevo",
        "Elimina archivos permanentemente",
        "Muestra permisos del sistema"
    ]

    from random import shuffle
    shuffle(options)

    for i, opt in enumerate(options, 1):
        console.print(f"  [{i}] {opt}")

    console.print()
    try:
        answer = int(Prompt.ask("Tu respuesta"))
        if options[answer - 1] == cmd['desc']:
            console.print(Panel("[green]✓ ¡Correcto![/green]", border_style="green"))
        else:
            console.print(Panel("[red]✗ Incorrecto[/red]\nRespuesta correcta: " + cmd['desc'], border_style="red"))
    except:
        console.print("[red]Respuesta inválida[/red]")

    Prompt.ask("\nPresiona ENTER para continuar")

def practice_mode(chapter_num):
    """Modo práctica general del capítulo"""
    chapter = COMMAND_DATABASE[chapter_num]

    console.clear()
    show_ascii_art()

    mode_panel = Panel(
        f"[bold yellow]Modo Práctica - Capítulo {chapter_num}[/bold yellow]\n\n"
        f"{chapter['title']}\n\n"
        f"Selecciona comandos para practicar",
        border_style="yellow",
        box=box.DOUBLE
    )
    console.print(mode_panel)
    console.print()

    # Mostrar comandos no practicados
    table = Table(box=box.SIMPLE, border_style="yellow")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Comando", style="white", width=35)
    table.add_column("Estado", style="yellow", width=12)

    for idx, cmd in enumerate(chapter["commands"], 1):
        practiced = "✓ Practicado" if cmd["cmd"] in tracker.data.get("commands_practiced", {}) else "○ Pendiente"
        table.add_row(str(idx), cmd["cmd"], practiced)

    console.print(table)
    console.print()

    choice = Prompt.ask("[cyan]Selecciona comando a practicar[/cyan]")
    if choice.lower() == 'b':
        show_chapter_menu(chapter_num)
    else:
        try:
            cmd_idx = int(choice) - 1
            if 0 <= cmd_idx < len(chapter["commands"]):
                practice_command(chapter["commands"][cmd_idx], chapter_num)
            else:
                practice_mode(chapter_num)
        except:
            practice_mode(chapter_num)

def main():
    """Función principal"""
    try:
        # Actualizar sesión
        tracker.data["sessions"] = tracker.data.get("sessions", 0) + 1
        tracker.data["last_session"] = datetime.now().isoformat()
        tracker.save()

        # Inicio
        show_main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Saliendo... ¡Hasta luego![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
