# 🗣️ TTS VoiceTxt — Linux TTS Application

> Una aplicación de escritorio moderna para convertir texto a voz, diseñada específicamente para Linux y preparada para su distribución mediante Flatpak.

---

Este proyecto es una **reescritura completa y un rediseño arquitectónico** basado en el trabajo inicial de [schr-0dinger/edge_tts_gui](https://github.com/schr-0dinger/edge_tts_gui).

Agradecemos enormemente a **schr-0dinger** por la idea original y el punto de partida que motivó esta nueva versión.

---

## 🚀 Motivo de la reescritura

Aunque la aplicación original era funcional, presentaba problemas de arquitectura que causaban **bloqueos en la interfaz (freezing)** durante la generación de audio, y su estructura monolítica dificultaba su mantenimiento y empaquetado para Linux.

Esta nueva versión soluciona esos problemas e introduce una **arquitectura modular desde cero**.

---

## ✨ Características principales

| Característica                    | Descripción                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **🖥️ Interfaz Qt6/PySide6**      | Integración nativa con escritorios Linux modernos (como KDE Plasma).                                               |
| **⚡ Cero bloqueos**               | Uso de `QThread` y señales asíncronas para mantener la interfaz siempre responsiva.                                |
| **🧩 Arquitectura de Motores**    | Abstracción del motor TTS (`BaseTTSEngine`) que permite añadir futuros motores locales sin reescribir la interfaz. |
| **🎙️ Gestión de Voces Mejorada** | Filtrado por idioma, región y género de forma dinámica.                                                            |
| **📂 Importar y Exportar**        | Soporte para importar archivos `.txt` y guardar el audio generado en MP3.                                          |
| **📦 Preparado para Flatpak**     | Estructura de directorios y configuración pensada para cumplir con los estándares XDG de Linux.                    |
| **🎮 Detección de Hardware**      | Preparación para identificar GPUs (AMD/NVIDIA) para futuras aceleraciones de modelos locales.                      |

---

## 🏗️ Arquitectura

El proyecto se divide en **capas estrictamente separadas**:

```text
┌──────────────────────────────┐
│       GUI (PySide6)          │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│          Controller          │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│   TTS Worker                 │
│   QThread + asyncio          │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│         TTS Engine           │
│ Edge TTS / Futuros motores   │
│           locales            │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│       Audio Player           │
│        QtMultimedia          │
└──────────────────────────────┘
```

---

## 🛠️ Instalación — Modo Desarrollo

Actualmente, la aplicación está en **fase de desarrollo activo**.

Para ejecutarla en tu máquina Linux:

### 1. Clona el repositorio

```bash
git clone https://github.com/danny123uwu/edge_tts_gui_VoiceTxt.git

cd edge_tts_gui_VoiceTxt
```

### 2. Crea un entorno virtual y actívalo

```bash
python -m venv venv

source venv/bin/activate
```

> En `fish`:
>
> ```fish
> source venv/bin/activate.fish
> ```

### 3. Instala las dependencias

```bash
pip install PySide6 edge-tts
```

### 4. Ejecuta la aplicación

```bash
python main.py
```

---

## 🗺️ Hoja de ruta — Roadmap

### 🔹 Fase 1–3

* Análisis
* Arquitectura
* Core TTS (Edge TTS)

### 🔹 Fase 4–6

* GUI en PySide6
* Concurrencia
* Reproductor de Audio

### 🔹 Fase 7.1

* Mejora en UI
* Importar TXT
* Filtrado de voces

### 🔹 Fase 7.2

* Persistencia de configuración
* XDG dirs

### 🔹 Fase 8

* Detección de Hardware
* CPU/GPU

### 🔹 Fase 10

* Integración de Motores TTS Locales
* Modelos

### 🔹 Fase 12

* Empaquetado definitivo en Flatpak

---

<div align="center">

**TTS VoiceTxt — Linux TTS Application**

</div>
