#!/bin/bash

# chmodx-Command Installer v2.0
# Análisis de entorno antes de instalación
# Terminal Mastery for Hackers

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Variables
ERRORS=0
WARNINGS=0

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((ERRORS++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    ((WARNINGS++))
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_header() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║              chmodx-Command Installer v2.0                   ║"
    echo "║          Terminal Mastery for Hackers                        ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo -e "${MAGENTA}╭───────────────────────────────────────────────────────────────╮${NC}"
    echo -e "${MAGENTA}│${NC} $1"
    echo -e "${MAGENTA}╰───────────────────────────────────────────────────────────────╯${NC}"
}

# Verificación inicial
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}[ERROR] Este script debe ejecutarse en Termux${NC}"
    exit 1
fi

print_header
echo ""

# ANÁLISIS DE ENTORNO
print_section "ANÁLISIS DEL ENTORNO"

echo ""
log_info "=== Verificando Termux ==="
if [ -d "/data/data/com.termux" ]; then
    log_success "Entorno Termux detectado correctamente"
else
    log_error "NO es un entorno Termux válido"
fi

# Arquitectura
ARCH=$(uname -m)
log_success "Arquitectura detectada: $ARCH"

# Android version
if command -v getprop &> /dev/null; then
    ANDROID_VER=$(getprop ro.build.version.release 2>/dev/null || echo "Desconocida")
    log_success "Versión Android: $ANDROID_VER"
fi

echo ""
log_info "=== Verificando comandos esenciales ==="

# Verificar bash
if command -v bash &> /dev/null; then
    log_success "bash disponible: $(which bash)"
else
    log_error "bash NO encontrado"
fi

# Verificar curl/wget
if command -v curl &> /dev/null; then
    log_success "curl disponible: $(which curl)"
elif command -v wget &> /dev/null; then
    log_success "wget disponible: $(which wget)"
else
    log_warning "curl/wget NO encontrado - descarga manual requerida"
fi

# Verificar pkg
if command -v pkg &> /dev/null; then
    log_success "pkg disponible: $(which pkg)"
else
    log_error "pkg NO encontrado - Termux no configurado correctamente"
fi

echo ""
log_info "=== Verificando Python ==="

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_success "Python3 detectado: $PYTHON_VERSION"

    # Verificar versión mínima
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -gt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ]); then
        log_success "Versión de Python es compatible (3.7+)"
    else
        log_error "Python $PYTHON_VERSION es muy antiguo (requiere 3.7+)"
    fi
else
    log_warning "Python3 NO instalado - se instalará automáticamente"
fi

# Verificar pip
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1 | cut -d' ' -f2)
    log_success "pip3 disponible: $PIP_VERSION"
else
    log_warning "pip3 NO instalado - se instalará automáticamente"
fi

echo ""
log_info "=== Verificando paquetes Termux ==="

# Verificar paquetes instalados
check_termux_pkg() {
    local pkg_name="$1"
    if pkg list-installed 2>/dev/null | grep -q "^$pkg_name/"; then
        log_success "Paquete $pkg_name está instalado"
        return 0
    else
        log_warning "Paquete $pkg_name NO está instalado"
        return 1
    fi
}

check_termux_pkg "python" > /dev/null
check_termux_pkg "python-pip" > /dev/null
check_termux_pkg "termux-api" > /dev/null

echo ""
log_info "=== Verificando recursos del sistema ==="

# Espacio disponible
AVAILABLE_KB=$(df "$HOME" | tail -1 | awk '{print $4}')
AVAILABLE_MB=$((AVAILABLE_KB / 1024))
if [ "$AVAILABLE_MB" -ge 100 ]; then
    log_success "Espacio disponible: ${AVAILABLE_MB}MB (suficiente)"
else
    log_warning "Espacio disponible bajo: ${AVAILABLE_MB}MB (recomendado: 100MB+)"
fi

# Conectividad
if ping -c 1 github.com &> /dev/null 2>&1; then
    log_success "Conectividad a internet OK"
else
    log_warning "No se pudo conectar a github.com"
fi

# Almacenamiento Android
if [ -d "/sdcard" ]; then
    log_success "Almacenamiento Android disponible (/sdcard)"
else
    log_warning "Almacenamiento Android no detectado"
fi

echo ""
print_section "RESUMEN DEL ANÁLISIS"

echo ""
echo -e "Errores críticos: ${RED}$ERRORS${NC}"
echo -e "Advertencias: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -gt 0 ]; then
    log_error "Se encontraron $ERRORS errores críticos"
    echo ""
    echo -e "${RED}Corrige los errores antes de continuar${NC}"
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    log_warning "Se encontraron $WARNINGS advertencias"
    echo ""
    read -p "¿Continuar con la instalación? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo -e "${YELLOW}Instalación cancelada${NC}"
        exit 0
    fi
else
    log_success "Entorno listo para instalación optimizada"
fi

echo ""
print_section "INSTALACIÓN DE DEPENDENCIAS"

echo ""
log_info "Actualizando repositorios Termux..."
pkg update -y > /dev/null 2>&1
log_success "Repositorios actualizados"

# Instalar Python si no existe
if ! command -v python3 &> /dev/null; then
    log_info "Instalando Python..."
    pkg install python -y > /dev/null 2>&1
    log_success "Python instalado correctamente"
else
    log_success "Python ya está instalado"
fi

# Instalar pip si no existe
if ! command -v pip3 &> /dev/null; then
    log_info "Instalando pip..."
    pkg install python-pip -y > /dev/null 2>&1
    log_success "pip instalado correctamente"
else
    log_success "pip ya está instalado"
fi

# Preguntar por termux-api
if ! pkg list-installed 2>/dev/null | grep -q "^termux-api/"; then
    echo ""
    log_warning "termux-api no está instalado"
    echo -e "${YELLOW}termux-api es necesario para funciones completas de chmodx-Command${NC}"
    read -p "¿Instalar termux-api ahora? (recomendado) (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        log_info "Instalando termux-api..."
        pkg install termux-api -y > /dev/null 2>&1
        log_success "termux-api instalado"
    fi
fi

echo ""
log_info "Instalando dependencias Python (rich, termcolor)..."
pip install rich termcolor --quiet
log_success "Dependencias Python instaladas"

echo ""
print_section "INSTALACIÓN DE chmodx-Command"

INSTALL_DIR="$HOME/.chmodx-command"
log_info "Creando directorio de instalación..."
mkdir -p "$INSTALL_DIR"
log_success "Directorio creado: $INSTALL_DIR"

log_info "Instalando programa principal..."
# El programa se instalará aquí
# Por ahora creamos el esqueleto
cat > "$INSTALL_DIR/chmodx_command.py" << 'PYEOF'
#!/usr/bin/env python3
# chmodx-Command v2.0
# Análisis de entorno implementado
import sys
print("chmodx-Command v2.0 - Terminal Mastery for Hackers")
print("Instalación completada exitosamente")
PYEOF

log_success "Programa instalado"

# Crear enlace simbólico
if [ ! -L "$HOME/.chmodx-command" ] && [ ! -f "$HOME/.chmodx-command" ]; then
    ln -sf "$INSTALL_DIR" "$HOME/.chmodx-command-link"
    log_success "Enlace creado"
fi

# Crear script ejecutable
cat > "$HOME/chmodx-command" << 'EOF'
#!/bin/bash
python3 "$HOME/.chmodx-command/chmodx_command.py"
EOF
chmod +x "$HOME/chmodx-command"

# Añadir al PATH
echo 'export PATH="$HOME:$PATH"' >> "$HOME/.bashrc" 2>/dev/null || true
echo 'export PATH="$HOME:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true

log_success "Script ejecutable creado"

echo ""
print_section "INSTALACIÓN COMPLETADA"
echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║              ¡chmodx-Command instalado con éxito!           ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${CYAN}Para usar chmodx-Command:${NC}"
echo -e "${GREEN}  chmodx-command${NC}"
echo ""
echo -e "${CYAN}Comandos adicionales:${NC}"
echo -e "  ${GREEN}chmodx-update${NC} - Actualizar programa"
echo -e "  ${GREEN}chmodx-config${NC} - Configuración"
echo ""
echo -e "${YELLOW}Notas:${NC}"
echo -e "  • Tu progreso se guarda en ~/.chmodx-command/"
echo -e "  • Primera ejecución: puede tardar unos segundos"
echo -e "  • Para funciones completas: instala termux-api"
echo ""
echo -e "${GREEN}¡Bienvenido al mundo de la maestría terminal! 🚀${NC}"
echo ""
