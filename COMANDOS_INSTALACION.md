# 📦 Comandos de Instalación - chmodx-Command

## Instalación en 1 Comando (Recomendado)

Ejecuta este comando en Termux:

```bash
curl -fsSL https://raw.githubusercontent.com/usuario/chmodx-Command/main/install.sh | bash
```

## Alternativas de Instalación

### Opción 1: Con wget
```bash
wget -O install.sh https://raw.githubusercontent.com/usuario/chmodx-Command/main/install.sh
bash install.sh
```

### Opción 2: Git clone
```bash
git clone https://github.com/usuario/chmodx-Command.git
cd chmodx-Command
bash install.sh
```

### Opción 3: Instalación manual
```bash
# Descargar
wget https://github.com/usuario/chmodx-Command/archive/main.zip
unzip main.zip

# Instalar dependencias Python
pip install rich termcolor

# Ejecutar
python3 chmodx-command/chmodx_command_full.py
```

## Uso después de instalar

```bash
chmodx-command
```

## Comandos útiles

```bash
# Actualizar el programa
bash ~/.chmodx-command/update.sh

# Ver progreso
cat ~/.chmodx-command/progress.json

# Reinstalar
rm -rf ~/.chmodx-command && bash install.sh
```

## Requisitos

- Termux instalado
- Python 3.7 o superior
- Conexión a internet (primera instalación)
- Espacio de almacenamiento: ~50MB

## Soporte

Si tienes problemas:
1. Verifica que Python esté instalado: `python3 --version`
2. Verifica conexión a internet
3. Ejecuta el instalador con permisos: `bash install.sh`
