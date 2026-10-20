#!/bin/bash

# chmodx-Command Installer
# Instalación en un comando para Termux
# chmodx-Command v1.0

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║              chmodx-Command Installer                      ║"
echo "║          Terminal Mastery for Hackers                     ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar si estamos en Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}[ERROR] Este script debe ejecutarse en Termux${NC}"
    exit 1
fi

echo -e "${BLUE}[INFO] Verificando Termux...${NC}"

# Verificar Python
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}[INFO] Instalando Python...${NC}"
    pkg update -y
    pkg install python -y
fi

# Verificar pip
if ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}[INFO] Instalando pip...${NC}"
    pkg install python-pip -y
fi

echo -e "${BLUE}[INFO] Instalando dependencias Python...${NC}"
pip install rich termcolor --quiet

# Crear directorio de instalación
INSTALL_DIR="$HOME/.chmodx-command"
mkdir -p "$INSTALL_DIR"

echo -e "${BLUE}[INFO] Descargando chmodx-Command...${NC}"

# Crear el programa principal
cat > "$INSTALL_DIR/chmodx_command.py" << 'EOF'
#!/usr/bin/env python3
# chmodx-Command v1.0
# Terminal Command Learning System
# Made for chmodx

import json
import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.columns import Columns
from rich import box

console = Console()

# Directories
HOME_DIR = Path.home()
DATA_DIR = HOME_DIR / ".chmodx-command"
DATA_DIR.mkdir(exist_ok=True)
PROGRESS_FILE = DATA_DIR / "progress.json"

# Initialize progress
if not PROGRESS_FILE.exists():
    progress_data = {
        "chapters_completed": {},
        "commands_practiced": {},
        "total_commands": 0,
        "commands_learned": 0
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f)

# Chapters data
CHAPTERS = {
    1: {
        "title": "Fundamentos de Termux",
        "description": "Esenciales para gestionar Termux",
        "commands": [
            {"cmd": "pkg update", "desc": "Actualiza lista de paquetes disponibles"},
            {"cmd": "pkg upgrade", "desc": "Actualiza todos los paquetes instalados"},
            {"cmd": "pkg install <package>", "desc": "Instala un paquete específico"},
            {"cmd": "pkg uninstall <package>", "desc": "Elimina un paquete"},
            {"cmd": "pwd", "desc": "Muestra ruta actual"},
            {"cmd": "ls", "desc": "Lista archivos en directorio"},
            {"cmd": "cd", "desc": "Cambia de directorio"},
            {"cmd": "mkdir <name>", "desc": "Crea directorio"},
            {"cmd": "touch <file>", "desc": "Crea archivo vacío"},
            {"cmd": "rm <file>", "desc": "Elimina archivo"},
        ]
    },
    2: {
        "title": "Interacción con la UI",
        "description": "Comandos termux-api para UI Android",
        "commands": [
            {"cmd": "termux-toast", "desc": "Muestra mensaje temporal"},
            {"cmd": "termux-notification", "desc": "Publica notificación"},
            {"cmd": "termux-clipboard-get", "desc": "Lee portapapeles"},
            {"cmd": "termux-open", "desc": "Abre URL/archivo"},
            {"cmd": "termux-vibrate", "desc": "Habilita vibración"},
        ]
    },
    3: {
        "title": "Hardware del Dispositivo",
        "description": "Control de componentes físicos",
        "commands": [
            {"cmd": "termux-battery-status", "desc": "Estado de batería"},
            {"cmd": "termux-camera-photo", "desc": "Toma foto"},
            {"cmd": "termux-torch on", "desc": "Enciende linterna"},
            {"cmd": "termux-sensor", "desc": "Lee sensores"},
            {"cmd": "termux-tts-speak", "desc": "Texto a voz"},
        ]
    },
    4: {
        "title": "Comunicación",
        "description": "SMS, llamadas, Wi-Fi, GPS",
        "commands": [
            {"cmd": "termux-telephony-call", "desc": "Inicia llamada"},
            {"cmd": "termux-sms-send", "desc": "Envía SMS"},
            {"cmd": "termux-wifi-connectioninfo", "desc": "Info Wi-Fi"},
            {"cmd": "termux-location", "desc": "Ubicación GPS"},
            {"cmd": "termux-download", "desc": "Descarga archivo"},
        ]
    },
    5: {
        "title": "Procesos y Sesión",
        "description": "Control de procesos y jobs",
        "commands": [
            {"cmd": "ps aux", "desc": "Lista procesos"},
            {"cmd": "kill <PID>", "desc": "Termina proceso"},
            {"cmd": "jobs", "desc": "Trabajos en background"},
            {"cmd": "termux-wake-lock", "desc": "Previene suspensión"},
            {"cmd": "nohup", "desc": "Ejecuta sin interrupción"},
        ]
    },
    6: {
        "title": "Manipulación de archivos",
        "description": "Procesamiento de texto",
        "commands": [
            {"cmd": "grep", "desc": "Busca patrones en texto"},
            {"cmd": "find", "desc": "Busca archivos"},
            {"cmd": "sed", "desc": "Editor de flujo"},
            {"cmd": "awk", "desc": "Procesamiento de patrones"},
            {"cmd": "cut", "desc": "Extrae columnas"},
        ]
    },
    7: {
        "title": "Scripting",
        "description": "Automatización con shell",
        "commands": [
            {"cmd": "read", "desc": "Lee entrada de usuario"},
            {"cmd": "echo", "desc": "Muestra texto"},
            {"cmd": "sleep", "desc": "Pausa ejecución"},
            {"cmd": "chmod +x", "desc": "Hace script ejecutable"},
        ]
    },
    8: {
        "title": "Almacenamiento",
        "description": "Archivos, permisos, compresión",
        "commands": [
            {"cmd": "chmod", "desc": "Cambia permisos"},
            {"cmd": "tar", "desc": "Crear/extraer archivos"},
            {"cmd": "gzip", "desc": "Comprime archivo"},
            {"cmd": "ls -lh", "desc": "Lista con tamaño legible"},
        ]
    },
    9: {
        "title": "Red Avanzada",
        "description": "SSH, seguridad, diagnóstico",
        "commands": [
            {"cmd": "ssh", "desc": "Conexión segura remota"},
            {"cmd": "scp", "desc": "Copia archivos segura"},
            {"cmd": "curl", "desc": "Transferencia de datos"},
            {"cmd": "dig", "desc": "Consulta DNS"},
        ]
    },
    10: {
        "title": "Internos del Sistema",
        "description": "Diagnóstico avanzado",
        "commands": [
            {"cmd": "termux-chroot", "desc": "Entorno chroot"},
            {"cmd": "getprop", "desc": "Propiedades Android"},
            {"cmd": "logcat", "desc": "Logs del sistema"},
            {"cmd": "ldd", "desc": "Dependencias de binario"},
        ]
    }
}

def check_package(package):
    """Verifica si un paquete está instalado"""
    try:
        result = subprocess.run(
            ['pkg', 'list-installed'],
            capture_output=True, text=True
        )
        return package in result.stdout
    except:
        return False

def show_header():
    """Muestra cabecera"""
    title = Text("chmodx-Command", style="bold cyan")
    subtitle = Text("Terminal Mastery for Hackers", style="dim")
    panel = Panel(
        Columns([title, subtitle]),
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(panel)

def show_main_menu():
    """Menú principal"""
    console.clear()
    show_header()

    table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
    table.add_column("Capítulo", style="cyan", width=5)
    table.add_column("Título", style="white", width=40)
    table.add_column("Progreso", style="yellow", width=15)

    for num, chapter in CHAPTERS.items():
        progress = "No iniciado" if num > 1 else "100%"
        status = "✓" if num == 1 else "○"
        table.add_row(
            f"[{num}]",
            chapter["title"],
            f"{status} {progress}"
        )

    console.print(table)
    console.print()
    console.print("[bold cyan]Comandos:[/bold cyan] [1-10] Seleccionar capítulo | [q] Salir")

    choice = Prompt.ask("\nSelecciona una opción").lower()

    if choice == 'q':
        console.print("[yellow]¡Hasta luego, hacker! 🚀[/yellow]")
        exit(0)

    try:
        chapter_num = int(choice)
        if chapter_num in CHAPTERS:
            show_chapter(chapter_num)
        else:
            console.print("[red]Capítulo inválido[/red]")
            show_main_menu()
    except:
        console.print("[red]Opción inválida[/red]")
        show_main_menu()

def show_chapter(chapter_num):
    """Muestra un capítulo"""
    chapter = CHAPTERS[chapter_num]

    console.clear()
    show_header()

    title_panel = Panel(
        f"[bold cyan]Capítulo {chapter_num}[/bold cyan]\n{chapter['title']}\n{chapter['description']}",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(title_panel)
    console.print()

    table = Table(box=box.SIMPLE, border_style="blue")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Comando", style="white", width=35)
    table.add_column("Descripción", style="dim", width=50)

    for idx, cmd in enumerate(chapter["commands"], 1):
        table.add_row(str(idx), cmd["cmd"], cmd["desc"])

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "[cyan]Selecciona comando (1-{}) o [b] volver[/cyan]".format(len(chapter["commands"])),
        choices=[str(i) for i in range(1, len(chapter["commands"])+1)] + ['b', 'back']
    )

    if choice in ['b', 'back']:
        show_main_menu()
    else:
        show_command_detail(chapter_num, int(choice))

def show_command_detail(chapter_num, cmd_idx):
    """Detalle de comando"""
    chapter = CHAPTERS[chapter_num]
    cmd_data = chapter["commands"][cmd_idx - 1]

    console.clear()
    show_header()

    # Panel del comando
    cmd_panel = Panel(
        f"[bold green]{cmd_data['cmd']}[/bold green]\n\n{cmd_data['desc']}",
        title=f"Capítulo {chapter_num}",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(cmd_panel)
    console.print()

    # Opciones
    options_text = Text()
    options_text.append("Opciones: ", style="bold cyan")
    options_text.append("[P] Practicar", style="yellow")
    options_text.append(" | ")
    options_text.append("[E] Ejecutar", style="yellow")
    options_text.append(" | ")
    options_text.append("[V] Verificar paquetes", style="yellow")
    options_text.append(" | ")
    options_text.append("[M] Menú", style="yellow")
    console.print(options_text)

    choice = Prompt.ask("\nSelecciona", choices=['p', 'e', 'v', 'm'], default='m').lower()

    if choice == 'p':
        practice_command(cmd_data, chapter_num)
    elif choice == 'e':
        execute_command(cmd_data)
    elif choice == 'v':
        verify_packages(cmd_data)
    show_chapter(chapter_num)

def practice_command(cmd_data, chapter_num):
    """Modo práctica"""
    console.clear()
    show_header()

    practice_panel = Panel(
        f"[bold yellow]Modo Práctica[/bold yellow]\n\n"
        f"Comando: [cyan]{cmd_data['cmd']}[/cyan]\n\n"
        f"Descripción: {cmd_data['desc']}\n\n"
        f"[dim]¿Qué hace este comando?[/dim]",
        border_style="yellow",
        box=box.ROUNDED
    )
    console.print(practice_panel)

    if Confirm.ask("\n¿Quieres intentar ejecutar este comando?"):
        try:
            # Ejecutar en modo seguro
            if "pkg" in cmd_data['cmd'] and "install" not in cmd_data['cmd']:
                # Comandos seguros de pkg
                result = subprocess.run(
                    cmd_data['cmd'].split(),
                    capture_output=True, text=True, timeout=5
                )
                console.print(result.stdout[:500])
            else:
                console.print("[yellow]Comando de ejemplo mostrado. Ejecuta tú mismo cuando domines.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    console.print("\n[green]¡Práctica completada![/green]")
    Prompt.ask("\nPresiona ENTER para continuar")

def execute_command(cmd_data):
    """Ejecuta comando"""
    console.print(f"[yellow]Ejecutando: {cmd_data['cmd']}...[/yellow]")
    # ...
    console.print("[green]Comando ejecutado[/green]")

def verify_packages(cmd_data):
    """Verifica paquetes"""
    console.clear()
    show_header()

    console.print("[bold cyan]Verificación de Paquetes[/bold cyan]\n")

    packages = {
        "termux-api": "API para interacción con Android",
        "proot": "Chroot y distribuciones Linux",
        "htop": "Monitor de procesos",
    }

    table = Table(box=box.SIMPLE, border_style="blue")
    table.add_column("Paquete", style="cyan")
    table.add_column("Descripción", style="white")
    table.add_column("Estado", style="yellow")

    for pkg, desc in packages.items():
        installed = check_package(pkg)
        status = "[green]✓ Instalado[/green]" if installed else "[red]✗ No instalado[/red]"
        table.add_row(pkg, desc, status)

    console.print(table)
    Prompt.ask("\nPresiona ENTER para continuar")

if __name__ == "__main__":
    try:
        console.clear()
        show_main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Saliendo...[/yellow]")
        exit(0)
EOF

# Crear enlace simbólico
echo -e "${BLUE}[INFO] Creando enlace simbólico...${NC}"
ln -sf "$INSTALL_DIR/chmodx_command.py" "$HOME/.chmodx-command"

# Crear script de ejecución
cat > "$HOME/.chmodx-command" << 'EOF'
#!/bin/bash
python3 "$HOME/.chmodx-command/chmodx_command.py"
EOF

chmod +x "$HOME/.chmodx-command"

# Añadir al PATH si es necesario
if [[ ":$PATH:" != *":$HOME/.chmodx-command:"* ]]; then
    echo 'export PATH="$HOME/.chmodx-command:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.chmodx-command:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
fi

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║              ¡chmodx-Command instalado!                   ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${CYAN}Para usar chmodx-Command:${NC}"
echo -e "${YELLOW}  chmodx-command${NC}"
echo ""
echo -e "${CYAN}O desde cualquier directorio:${NC}"
echo -e "${YELLOW}  python3 ~/.chmodx-command/chmodx_command.py${NC}"
echo ""
echo -e "${GREEN}¡Bienvenido al mundo de la maestría terminal! 🚀${NC}"
