# Instrucciones de Instalación - chmodx-Command

## Instalación con un solo comando

Ejecuta este comando en tu Termux:

```bash
curl -fsSL https://raw.githubusercontent.com/CHMODX-CODE/chmodx-Command/main/install.sh | bash
```

## Instalación manual paso a paso

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/chmodx-Command.git
cd chmodx-Command
```

2. **Ejecutar el instalador**
```bash
bash install.sh
```

3. **Verificar instalación**
```bash
chmodx-command
```

## Requisitos previos

El instalador automáticamente verifica e instala:
- Python 3.7+
- pip
- Paquetes Python: rich, termcolor

## Ubicación de instalación

El programa se instala en:
- `~/.chmodx-command/chmodx_command.py` (código principal)
- `~/.chmodx-command` (ejecutable)

## Actualización

Para actualizar a la última versión:
```bash
bash ~/.chmodx-command/update.sh
```

O re-ejecuta el instalador:
```bash
curl -fsSL https://raw.githubusercontent.com/tu-usuario/chmodx-Command/main/install.sh | bash
```

## Desinstalación

```bash
rm -rf ~/.chmodx-command
```

## Soporte

Para problemas o preguntas, abre un issue en GitHub.
