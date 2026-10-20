# Configuración de GitHub para chmodx-Command

## 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `chmodx-Command`
3. Descripción: `Terminal Mastery for Hackers - Programa educativo para aprender comandos de Termux`
4. Público
5. Crear repositorio

## 2. Estructura de archivos

Subir estos archivos al repositorio:

```
chmodx-Command/
├── install.sh                   # Instalador principal
├── chmodx_command_full.py       # Programa principal Python
├── requirements.txt             # Dependencias Python
├── README.md                    # Documentación principal
├── INSTALL.md                   # Instrucciones de instalación
├── COMANDOS_INSTALACION.md      # Comandos rápidos
├── GITHUB_SETUP.md              # Este archivo
└── LICENSE                      # Licencia MIT
```

## 3. Archivos necesarios

### install.sh
```bash
#!/bin/bash
# chmodx-Command Installer
# ...
```

### chmodx_command_full.py
El programa completo Python con Rich UI

## 4. Comando de instalación final

Una vez subido a GitHub con tu usuario:

```bash
curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/chmodx-Command/main/install.sh | bash
```

## 5. Reemplazos necesarios

Antes de hacer commit, reemplaza:
- `tu-usuario` → Tu usuario de GitHub
- `usuario` → Tu usuario de GitHub
- Rutas según tu estructura

## 6. README con badges

Añadir a README.md:

```markdown
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
```

## 7. Configurar GitHub Pages (opcional)

Para documentación web:
1. Settings → Pages
2. Source: main branch
3. Folder: /docs

## 8. Comando de prueba

Probar la instalación:
```bash
curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/chmodx-Command/main/install.sh | bash
```

## 9. Promoción

Compartir el comando de instalación:
```bash
curl -fsSL https://raw.githubusercontent.com/TU_USUARIO/chmodx-Command/main/install.sh | bash
```

## 10. Mantenimiento

Actualizar versión:
- Incrementar versión en código
- Actualizar changelog
- Hacer tag release
- Push a GitHub
