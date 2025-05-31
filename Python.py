
import time
import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
        __import__(package)



import_or_install('keyboard')
import keyboard
import_or_install('pynput')
from pynput.mouse import Button, Controller
import_or_install('threading')
import threading
import_or_install('pyserial')
import serial
import serial.serialutil
import serial.tools.list_ports

import pip





Running = True
Repeating = False
repeat_thread = None
repeat_flag = False

# Place these globally (at the top)
last_pwm_toggle_time = 0
turn_key_state = False  # False = released, True = pressed
turn_key = None
 
last_toggle_was_press = None

On = False

port = None
arduino = None

last_pwm_time = 0
accel_pwm = {
    'last_toggle': time.time(),
    'pressing': False,
    'key': 'w',
    'strength': 0,
    'cycle_time': 0.05  # Total cycle time (in seconds)
}


print("\n\nType letters to press them. Type 'quit' or 'exit' to stop.")

def repeat_key_action(key, press_duration, repeat_count):
    global repeat_flag
    repeat_flag = True
    if repeat_count == -999:
        while True:
            if not repeat_flag:
                break
            keyboard.press(key)
            #print(f"Pressed: {key}")
            time.sleep(press_duration)
            keyboard.release(key)

    else:
        for _ in range(repeat_count):
            if not repeat_flag:
                break
            keyboard.press(key)
            #print(f"Pressed: {key}")
            time.sleep(press_duration)
            keyboard.release(key)

    print("Stopped repeating.")

# Stop function (for ESC key)
def stop_repeat():
    global repeat_flag
    repeat_flag = False
    print("Repeat stopped with ESC.")

def toggle_repeat(key, press_duration, repeat_count):
    global Repeating, repeat_thread, repeat_flag
    if not Repeating:
        #print("Starting repeat...")
        repeat_thread = threading.Thread(target=repeat_key_action, args=(key, press_duration, repeat_count))
        repeat_thread.start()
        Repeating = True
    else:
        #print("Stopping repeat...")
        repeat_flag = False
        Repeating = False


# Set up the serial connection (Update 'COM3' or '/dev/ttyUSB0' for your system)
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description or "USB-SERIAL" in port.description:
            return port.device  # e.g., 'COM6'
    return None

def read_arduino():
    try:
        data = arduino.readline().decode('utf-8').strip()
        return data if data else None
    except:
        return None

keyboard.add_hotkey('esc', stop_repeat)  # ESC to stop infinite loops


while Running:
    input_command = input("\n\nWhat Command you would like? \ntry: \n R1- repeat the junction of leters (e.g. im here) \n R2 - R1 but leter by leter (e.g. i m space h e r e) \n M1 - mouse buttons \n M2 - mouse buttons \n CC - when you press the active combo it start pressing the key \n V - Simulator Mode (need arduino and some phericals) \n") # Include "space" as a word, not just a character

    if "quit" in input_command.lower() or "exit" in input_command.lower():
        Running = False
        break

    elif "R1" in input_command:
        try:
            input_text = input("What key(s) do you want to press repeatedly?\n") # Include "space" as a word, not just a character
            repeat_count = int(input("How many times should each key be pressed?a\n"))
            press_duration = float(input("How long to hold each key? (in seconds)\n"))
        except ValueError:
            print("Invalid number. Try again.")
            continue


        for _ in range(repeat_count):
            for char in input_text:
                try:
                    keyboard.press(char)
                    print(f"Pressed: {char}")
                    time.sleep(press_duration)
                    keyboard.release(char)

                except ValueError:
                    print("Invalid number. Try again.")
                    continue

    elif "R2" in input_command:
        try:
            input_text = input("write all leters you would like! (e.g. w a s space d -> was d)\n")  # Include "space" as a word, not just a character
            repeat_count = int(input("How many times should each key be pressed?\n"))
            press_duration = float(input("How long to hold each key? (in seconds)\n"))
            start_duration = float(input("How long to start? (in seconds)\n"))
            time.sleep(start_duration)
            keys = input_text.split()   # Splits into ['w', 'a', 's', 'space', 'd']
        
        except ValueError:
            print("Invalid number. Try again.\n")
            continue
        
        for _ in range(repeat_count):
            for key in keys:
                try:
                    keyboard.press(key)
                    print(f"Pressed: {key}")
                    time.sleep(press_duration)
                    keyboard.release(key)
                    
                except ValueError:
                    print("Invalid number. Try again.\n")

    elif "M1" in input_command or "M2" in input_command:
        try:
            input_text = input("Try 'left' or 'right' or 'middle' to chose the mouse botton \n")
            repeat_count = int(input("How many times should each key be pressed?\n"))
            press_duration = float(input("How long to hold each key? (in seconds)\n"))
            if "M2" in input_command:
                start_duration = float(input("How long to start? (in seconds)\n"))
                time.sleep(start_duration)

        except ValueError:
            print("Invalid number. Try again.\n")
            continue

        for _ in range(repeat_count):
            if "left" in input_text or "L" in input_text or "l" in input_text:
                Controller().click(Button.left, 1)

            if "right" in input_text or "R" in input_text or "r" in input_text:
                Controller().click(Button.right, 1)

            if "mid" in input_text or "middle" in input_text or "m" in input_text or "M" in input_text:
                Controller().click(Button.middle, 1)


            time.sleep(press_duration)
    
    elif "CC" in input_command or "cc" in input_command:
        try:
            #hotkey = input("Enter the hotkey combination (e.g. ctrl+alt+h):\n").lower()
            input("redy to set a hotkey?")
            while True:
                time.sleep(1)
                print("Press the hotkey combination now: \n")
                hotkey = keyboard.read_hotkey(suppress=True)
                time.sleep(0.3)# Small delay to avoid leftover keypresses
                confirmation = input(f"do you want ({hotkey}) to be hotkey? (y/n)").strip().lower()
                if "y" in confirmation or "Y" in confirmation:
                    break
                else:
                    keyboard.read_hotkey(clear=True)
                    continue

            #input("redy to set a auto clickable key?")
            while True:
                time.sleep(1)
                repeat_key = input("Press the key you want to repeat now: \n").lower()
                confirmation = input(f"do you want ({repeat_key}) to be auto clickable? (y/n)").strip().lower()
                if "y" in confirmation or "Y" in confirmation:
                    break
                else:
                    continue

            repeat_count = int(input("How many times to press the key? (-999 = infinite)\n"))
            press_duration = float(input("How long to hold each key? (in seconds) \n'if you put infinite times do NOT put duration of 0 or lower than 0.01 it will become unstable and you will not be able to stop it'\n")) 
            if press_duration == -999:
                press_duration = 0.001
        except ValueError:
            print("Invalid input. Try again.\n")
            continue

        # Bind toggle to the hotkey
        keyboard.add_hotkey(hotkey, lambda: toggle_repeat(repeat_key, press_duration, repeat_count))
        print(f"Hotkey '{hotkey}' will toggle repeating key '{repeat_key}'")

    elif "V" in input_command or "v" in input_command:

        ports = serial.tools.list_ports.comports()
        for Port in ports:
            print(f"Port: {Port.device}, Description: {Port.description}")
            port = Port.device
        
        if arduino == None:
            arduino = serial.Serial(port, 9600, timeout=0.1)
            print(arduino)
        On = True

        while On:
            try:
                value = read_arduino()
                line = arduino.readline().decode('utf-8').strip()
            except serial.serialutil.PortNotOpenError:
                print("Arduino Port Not Found!\nPlug the arduino into USB port!\n")
                arduino = None
                On = False
                break

            if not line:
                #print(f"line: {line}")
                continue
            
            else:
                # Parse the line
                parts = line.split(',')
                data = {}
                for part in parts:
                    if ':' in part:
                        key, val = part.split(':', 1)
                        data[key.strip()] = int(val.strip())

                #volante
                #print(data)
                
                if data.get('V'):  # volante pin (A0)
                    Turn = data.get('V')
                    print(f"Turn: {Turn}")

                    if Turn is None or Turn == 0:
                        Turn = 1

                    center = 512
                    now = time.time()

                    keyboard.release('a')
                    keyboard.release('d')

                    if Turn >= center + 20:
                        turn_key = 'a'
                        # Normalize strength between 0 and 1
                        strength = min((Turn - (center + 20)) / (center - 20), 1)
                    elif Turn <= center - 20:
                        turn_key = 'd'
                        strength = min(((center - 20) - Turn) / (center - 20), 1)
                    else:
                        turn_key = None

                    base_press = 0.5
                    max_press = 0
                    release_duration = 0  # fixed short release time

                    if turn_key:
                        press_duration = base_press + (max_press - base_press) * strength*2

                        elapsed = now - last_pwm_toggle_time

                        if turn_key_state:  # currently pressed
                            if elapsed >= press_duration:
                                keyboard.release(turn_key)
                                turn_key_state = False
                                last_pwm_toggle_time = now
                        else:  # currently released
                            if elapsed >= release_duration:
                                keyboard.press(turn_key)
                                turn_key_state = True
                                last_pwm_toggle_time = now
 
                if data.get('W'):  # accelerator pin (A1)
                    Accelerate = data.get('W')
                    print(f"Accelerate: {Accelerate}")

                    if Accelerate is None or Accelerate == 0:
                        Accelerate = 0

                    now = time.time()

                    accel_key = accel_pwm['key']  # e.g., 'w'

                    # Normalize strength between 0 and 1
                    strength = max(min(Accelerate / 1023.0, 2.0), 0.0)

                    base_press = 0.8
                    max_press = 0
                    release_duration = 0  # short fixed release time

                    if strength > 0.0000001:
                        press_duration = base_press + (max_press - base_press) * strength
                        #print(f"press_duration: {press_duration}")

                        elapsed = now - accel_pwm['last_toggle']

                        if accel_pwm['pressing']:  # currently pressed
                            if elapsed >= press_duration:
                                keyboard.release(accel_key)
                                accel_pwm['pressing'] = False
                                accel_pwm['last_toggle'] = now
                        else:  # currently released
                            if elapsed >= release_duration:
                                keyboard.press(accel_key)
                                accel_pwm['pressing'] = True
                                accel_pwm['last_toggle'] = now
                    else:
                        if accel_pwm['pressing']:
                            keyboard.release(accel_key)
                            accel_pwm['pressing'] = False

                if data.get('Shift'): #mudanças pin(5)
                    Shift = data.get('Shift')
                    if Shift is not None and Shift is not 0:
                        print(f"mudanças: {Shift}")
                        keyboard.press('shift')
                    else:
                        keyboard.release('shift')

                if data.get('S'): #breaker pin(6)
                    BValue = data.get('S')
                    if BValue is not None and BValue is not 0:
                        print(f"s: {BValue}")
                        keyboard.press('s')
                    else:
                        keyboard.release('s')

                if data.get('H'): #Horn pin(7)
                    Horn = data.get('H')
                    if Horn is not None and Horn is not 0: 
                        print(f"Horn: {Horn}")
                        keyboard.press('h')
                    else:
                        keyboard.release('h')

                if data.get('IO'): #Horn pin(4)
                    BValue4 = data.get('IO')
                    if BValue4 is not None and BValue4 is not 0: 
                        print(f"IO: {BValue4}")
                        if BValue4:
                            data.clear()
                            print(f"data: {data}")
                            On = False

    else:
        print("Invalid command. Try again.\n")
        continue    



