# README

# Drum Master - Rhythm Game

A 90s-era style handheld electronic rhythm game inspired by classics like Bop It and Brain Warp. Built with ESP32 microcontroller and CircuitPython.

---

## Table of Contents

- [Overview](about:blank#overview)
- [How to Play](about:blank#how-to-play)
- [Game Features](about:blank#game-features)
- [Hardware Components](about:blank#hardware-components)
- [Wiring Diagram](about:blank#wiring-diagram)
- [Enclosure Design](about:blank#enclosure-design)
- [File Structure](about:blank#file-structure)

---

## Overview

**Drum Master** is a rhythm-based game where players must match drum beats by touching pads or tilting the device. The game features 3 difficulty levels, for each difficulty levels 12 progressive levels, and multiple input methods to keep players engaged.

The game starts with an animated drum startup sequence, then guides players through increasingly challenging rhythm patterns. Players must hit the correct drum at the right time to progress through all levels.

---

## How to Play

### Starting the Game

1. **Power On**: Flip the power switch to turn on the device
2. **Startup Animation**: Watch the animated drum sequence (10 seconds)
3. **Calibration**: Keep hands off touch pads and hold device still for sensor calibration
4. **Press Button**: Press the rotary encoder button to start

### Selecting Difficulty

Use the **rotary encoder** to select difficulty:
- **EASY**: Slower rhythms, more forgiving timing
- **MEDIUM**: Moderate speed, tighter timing
- **HARD**: Fast rhythms, precise timing required

Press the rotary encoder **button** to confirm your selection.

### Game Stages

The game has **12 levels** divided into 3 stages:

| Stage | Levels | Input Method | Description |
| --- | --- | --- | --- |
| **Know the Beat** | 1-4 | Any Touch Pad | Touch any pad when prompted |
| **Feel the Rhythm** | 5-8 | Left/Right Touch | Touch the correct pad (Left or Right) |
| **Move to Play** | 9-12 | IMU Tilt | Tilt the drumstick Left or Right |

### Gameplay Flow

1. **Watch Phase**: Observe the rhythm pattern displayed on screen
    - `[O]` appears briefly for each beat
    - Pay attention to the timing between beats
2. **Your Turn Phase**: Reproduce the rhythm
    - Numbers `[1]` `[2]` `[3]`… appear to guide you
    - Touch/tilt within the time window to score a hit
    - **Green LED** = Hit! ✓
    - **Red LED** = Miss! ✗
3. **Level Complete**: View your accuracy percentage
4. **Next Level**: Prepare for the next challenge

### Winning and Losing

- **Win**: Complete all 12 levels
    - Final score and rating displayed
    - Victory sound plays
- **Game Over**: Miss 6 consecutive beats
    - “GAME OVER! 6 MISSES!” displayed
    - Fail sound plays

### Scoring System

| Rating | Accuracy |
| --- | --- |
| PERFECT! | 90%+ |
| EXCELLENT! | 80-89% |
| GREAT! | 70-79% |
| GOOD | 60-69% |
| OK | 50-59% |
| KEEP TRYING | Below 50% |

### Restarting

After game ends, press the rotary button to play again (no need to power cycle).

---

## Game Features

### Rhythm Patterns by Difficulty

### EASY Difficulty

| Level | Pattern | Description |
| --- | --- | --- |
| 1, 5, 9 | **March** | Steady 4/4 beat (0.9s intervals) |
| 2, 6, 10 | **Waltz** | 3/4 time signature |
| 3, 7, 11 | **Swing** | Syncopated jazz feel |
| 4, 8, 12 | **Simple** | Basic quarter notes |

### MEDIUM Difficulty

| Level | Pattern | Description |
| --- | --- | --- |
| 1, 5, 9 | **Rock** | Driving rock beat |
| 2, 6, 10 | **Funk** | Groovy syncopation |
| 3, 7, 11 | **Habanera** | Cuban tango rhythm (1-1.5-0.5-1) |
| 4, 8, 12 | **Latin** | Energetic Latin feel |

### HARD Difficulty

| Level | Pattern | Description |
| --- | --- | --- |
| 1, 5, 9 | **Jazz** | Complex jazz timing |
| 2, 6, 10 | **Groove** | Tight funk groove |
| 3, 7, 11 | **Blast** | Fast-paced beats |
| 4, 8, 12 | **Chaos** | Unpredictable rhythms |

### Visual Feedback

- **OLED Display**: Shows game state, prompts, and scores
- **NeoPixel LED**:
    - Green = Successful hit
    - Red = Missed beat
    - Animation effects during startup

### Audio Feedback

- **Game Start Sound**: Short melody when each level begins
- **Victory Sound**: Ascending C-E-G-C arpeggio
- **Fail Sound**: Descending melody

### Sensor Calibration

At startup, the game automatically calibrates:
- **Touch Sensors**: Establishes baseline readings for accurate touch detection
- **Accelerometer**: Records neutral position for accurate tilt detection

---

## Hardware Components

### Required Components (Provided)

| Component | Model | Purpose |
| --- | --- | --- |
| Microcontroller | Xiao ESP32-C3 | Main processing unit |
| OLED Display | SSD1306 128x64 | Game display |
| Accelerometer | ADXL345 | Tilt detection (Levels 9-12) |
| Rotary Encoder | Standard with button | Menu navigation & selection |
| NeoPixel LED | WS2812B | Visual feedback |
| Battery | 3.7V LiPo | Portable power |
| Power Switch | SPST Toggle | On/Off control |

### Additional Components (Added)

| Component | Model | Purpose | Pin |
| --- | --- | --- | --- |
| **Touch Pad Left** | Copper pad + 1.2MΩ resistor | Left drum input | A0 |
| **Touch Pad Right** | Copper pad + 1.2MΩ resistor | Right drum input | A1 |
| **Piezo Buzzer** | KSSG1203-42 (Passive) | Audio feedback | D2 |

### Touch Pad Construction

The touch pads are custom-made using:
- Copper tape or copper sheet (conductive surface)
- 1MΩ pull-down resistor (between analog pin and GND)
- Wire connection to analog input pins

**How it works**: When finger touches the copper pad, body capacitance changes the analog reading. The game detects this change relative to the calibrated baseline.

---

## Wiring Diagram

### Pin Connections

```
Xiao ESP32-C3 Pinout:
┌─────────────────────────────────┐
│  [USB-C]                        │
│                                 │
│  D0/A0 ──── Touch Pad Left      │
│  D1/A1 ──── Touch Pad Right     │
│  D2    ──── Buzzer (+)          │
│  D3    ──── (unused)            │
│  D4/SDA ─┬─ OLED SDA            │
│          └─ ADXL345 SDA         │
│  D5/SCL ─┬─ OLED SCL            │
│          └─ ADXL345 SCL         │
│  D6    ──── NeoPixel Data       │
│  D7    ──── Rotary Button       │
│  D8    ──── (unused)            │
│  D9    ──── Rotary CLK          │
│  D10   ──── Rotary DT           │
│                                 │
│  3V3   ──── VCC (all sensors)   │
│  GND   ──── GND (all sensors)   │
│                                 │
│  BAT+  ──── Switch ──── LiPo +  │
│  BAT-  ──── LiPo -              │
└─────────────────────────────────┘
```

### I2C Bus (Shared)

Both OLED and ADXL345 share the I2C bus:
- **SDA**: D4 (GPIO4)
- **SCL**: D5 (GPIO5)
- **OLED Address**: 0x3C
- **ADXL345 Address**: 0x53

### Power Circuit

```
LiPo Battery (+) ──── On/Off Switch ──── BAT+ (Xiao)
LiPo Battery (-) ──────────────────────── BAT- (Xiao)
```

---

## Enclosure Design

The enclosure consists of two main parts: the **Drumstick** (controller) and the **Main Housing** (drum pad unit).

### Design Philosophy

The design is inspired by **MIDI drum pads**, creating a familiar and intuitive interface for rhythm game interaction. The layout prioritizes ergonomics and accessibility, with all interactive components facing upward for easy operation.

### Drumstick Design

The drumstick serves as a motion controller for IMU-based levels (9-12).

| Feature | Description |
| --- | --- |
| **IMU Mounting** | ADXL345 accelerometer fixed to the rear end with screws |
| **Flat Surface** | One side is flat (not round) allowing the drumstick to rest stably on a table |
| **Calibration Position** | Flat side down on table during startup calibration ensures consistent baseline readings |

### Main Housing (Drum Pad Unit)

### Materials

| Part | Material | Reason |
| --- | --- | --- |
| **Main Body** | PLA (3D Printed) | Durable, easy to print, non-yellow color |
| **Top Cover** | Transparent PLA | Allows NeoPixel light to shine through |

### Component Mounting

| Component | Mounting Method |
| --- | --- |
| Rotary Encoder | Through-hole mount, secured by its own nut |
| On/Off Switch | Through-hole mount |
| Touch Pads (×2) | Self-adhesive copper sheets attached to top surface |
| OLED Display | Screw-mounted to frame |
| NeoPixel LED | Internal mount, light visible through transparent cover |
| ESP32 + Perfboard | Internal mount on standoffs |
| LiPo Battery | Internal compartment |
| Buzzer | Internal mount |

### Access & Maintenance

| Feature | Implementation |
| --- | --- |
| **USB Access** | Slot on the side of enclosure for Type-C connector |
| **Easy Open** | Magnetic attachment between top cover and base |
| **Electronics Access** | Remove top cover to access all internal components |
| **Removable Components** | All hardware connected via female headers on perfboard |

### Design Considerations

1. **Ergonomics**: All interactive elements (touch pads, OLED, rotary encoder, switch) face upward for comfortable tabletop play
2. **Visual Feedback**: Transparent top cover ensures NeoPixel LED feedback is clearly visible during gameplay
3. **Stability**: Flat base allows the unit to sit securely on any surface
4. **Portability**: Compact design with internal battery for wireless gameplay
5. **Maintainability**: Magnetic closure allows quick access to electronics without tools
6. **Constraint Compliance**:
    - No yellow PLA used
    - No solderless breadboard (perfboard with female headers)
    - All components easily removable

---

## File Structure

```
Final/
├── README.md                 # This file
├── code.py       # Main game code
├── lib/                      # CircuitPython libraries
│   ├── adafruit_adxl34x.mpy
│   ├── adafruit_bus_device/
│   ├── adafruit_display_text/
│   ├── adafruit_displayio_ssd1306.mpy
│   ├── i2cdisplaybus.mpy
│   └── neopixel.mpy
├── diagrams/                 # Wiring diagrams
    ├── system_diagram.png
    └── circuit_diagram.png

```
