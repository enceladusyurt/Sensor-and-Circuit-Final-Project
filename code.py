import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306
import adafruit_adxl34x

# -----------------------------
# Release old displays if needed
# -----------------------------
displayio.release_displays()

# -----------------------------
# Create ONE shared I2C bus
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)

# -----------------------------
# OLED Display Setup
# -----------------------------
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# -----------------------------
# ADXL345 Accelerometer Setup
# -----------------------------
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_tap_detection()

# -----------------------------
# Display Groups Setup
# -----------------------------
main_group = displayio.Group()

# Beat indicator (large, center)
beat_label = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    anchor_point=(0.5, 0.5),
    anchored_position=(64, 28),
    scale=2
)

# Status/feedback label (bottom)
status_label = label.Label(
    terminalio.FONT,
    text="",
    color=0xFFFFFF,
    anchor_point=(0.5, 1),
    anchored_position=(64, 62)
)

main_group.append(beat_label)
main_group.append(status_label)
display.root_group = main_group

# -----------------------------
# Game Settings
# -----------------------------
# Tap window: time allowed to tap after beat appears
TAP_WINDOW_AFTER = 0.3  # 0.3 seconds to react

# Drum patterns: each number is beat interval in seconds
# Slower tempo for better reaction time
PATTERNS = {
    "ROCK": {
        "name": "Rock Beat",
        # Classic 4/4 rock: steady quarter notes
        "beats": [1, 1, 1, 1, 1, 1, 1, 1],
    },
    "MARCH": {
        "name": "March",
        # Marching rhythm: steady but slightly faster
        "beats": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
    },
    "HABANERA": {
        "name": "Habanera",
        # Habanera/Tango rhythm: 1 + 1.5 + 0.5 + 1 beats (1s per beat)
        "beats": [1.0, 1.5, 0.5, 1.0, 1.0, 1.5, 0.5, 1.0],
    },
    "BOSSA": {
        "name": "Bossa Nova",
        # Bossa nova clave-style rhythm
        "beats": [0.9, 0.5, 0.5, 0.9, 0.9, 0.5, 0.5, 0.9],
    },
}

# -----------------------------
# Game State
# -----------------------------
score = 0
total_beats = 0

# -----------------------------
# Helper Functions
# -----------------------------
def update_display():
    try:
        display.refresh()
    except:
        pass

def clear_tap_events():
    """Clear any pending tap events"""
    _ = accelerometer.events["tap"]

def check_tap():
    """Check if tap occurred"""
    return accelerometer.events["tap"]

def show_beat(text, status=""):
    beat_label.text = text
    status_label.text = status
    update_display()

def countdown():
    """Countdown with visual beat preview"""
    for i in [3, 2, 1]:
        show_beat(str(i), "Get ready...")
        time.sleep(0.8)
    show_beat("GO!", "")
    time.sleep(0.4)

def play_pattern(pattern_key):
    """
    Play a rhythm pattern with proper timing.
    Uses a timeline approach: check for taps within window around each beat.
    """
    global score, total_beats
    
    pattern = PATTERNS[pattern_key]
    beats = pattern["beats"]
    
    # Show pattern name
    show_beat(pattern["name"], "")
    time.sleep(1.2)
    
    # Preview: show the rhythm visually first
    show_beat("Watch...", "")
    time.sleep(0.5)
    
    # Visual preview of the rhythm (no tap required)
    for interval in beats:
        show_beat("[O]", "")
        time.sleep(0.15)
        show_beat("[ ]", "")
        time.sleep(interval - 0.15)
    
    time.sleep(0.5)
    show_beat("Your turn!", "")
    time.sleep(0.8)
    
    # Clear any taps from preview phase
    clear_tap_events()
    
    # Now player's turn - same rhythm
    beat_results = []
    
    for i, interval in enumerate(beats):
        total_beats += 1
        beat_num = i + 1
        
        # Show beat number (like watch phase)
        show_beat(f"[{beat_num}]", f"Hit: {score}/{total_beats - 1}" if total_beats > 1 else "TAP!")
        
        # Check for tap within the window
        beat_start = time.monotonic()
        tapped = False
        
        # Wait for tap or timeout
        while (time.monotonic() - beat_start) < TAP_WINDOW_AFTER:
            if check_tap():
                tapped = True
                break
            time.sleep(0.01)
        
        # Record result
        if tapped:
            score += 1
            beat_results.append("O")
        else:
            beat_results.append("X")
        
        # Hide the beat number (like watch phase)
        show_beat("[ ]", f"Hit: {score}/{total_beats}")
        
        # Wait remaining interval time
        elapsed = time.monotonic() - beat_start
        remaining = interval - elapsed
        if remaining > 0:
            # During wait, clear any extra taps
            wait_start = time.monotonic()
            while (time.monotonic() - wait_start) < remaining:
                clear_tap_events()
                time.sleep(0.02)
    
    # Show pattern results
    result_str = " ".join(beat_results)
    hits = beat_results.count("O")
    show_beat(f"{hits}/{len(beats)}", result_str)
    time.sleep(1.5)

def show_final_score():
    """Display final results"""
    percentage = (score / total_beats * 100) if total_beats > 0 else 0
    
    if percentage >= 90:
        rating = "PERFECT!"
    elif percentage >= 70:
        rating = "GREAT!"
    elif percentage >= 50:
        rating = "GOOD"
    else:
        rating = "RETRY?"
    
    show_beat(rating, f"{score}/{total_beats} = {int(percentage)}%")

def select_pattern():
    """Let user select pattern by number of taps"""
    show_beat("SELECT", "1-4 taps")
    time.sleep(0.5)
    
    pattern_keys = list(PATTERNS.keys())
    tap_count = 0
    last_tap_time = time.monotonic()
    
    clear_tap_events()
    
    # Wait for taps, timeout after 2 seconds of no taps
    while True:
        if check_tap():
            tap_count += 1
            last_tap_time = time.monotonic()
            # Show current selection
            idx = min(tap_count, len(pattern_keys)) - 1
            show_beat(str(tap_count), PATTERNS[pattern_keys[idx]]["name"])
        
        # If we have taps and 1.5s passed since last tap, confirm selection
        if tap_count > 0 and (time.monotonic() - last_tap_time) > 1.5:
            break
        
        # Timeout with no taps - default to pattern 1
        if tap_count == 0 and (time.monotonic() - last_tap_time) > 5:
            tap_count = 1
            break
        
        time.sleep(0.02)
    
    # Clamp to valid range
    idx = min(max(tap_count, 1), len(pattern_keys)) - 1
    return pattern_keys[idx]

# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    global score, total_beats
    
    while True:
        # Reset
        score = 0
        total_beats = 0
        
        # Welcome
        show_beat("DRUM", "Tap to start")
        
        # Wait for tap to start
        clear_tap_events()
        while not check_tap():
            time.sleep(0.05)
        
        # Pattern selection
        pattern_key = select_pattern()
        
        # Countdown
        countdown()
        
        # Play the pattern
        play_pattern(pattern_key)
        
        # Final score
        show_final_score()
        time.sleep(3)
        
        # Prompt restart
        show_beat("AGAIN?", "Tap to retry")
        clear_tap_events()
        time.sleep(0.5)
        
        while not check_tap():
            time.sleep(0.05)

# Run
main()
