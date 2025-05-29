import keyboard
from pynput.mouse import Button, Controller
import threading
import time
import serial
import serial.tools.list_ports


Running = True
Repeating = False
repeat_thread = None
repeat_flag = False

On = False

port = None

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
    input_command = input("\n\nWhat Command you would like? \ntry: \n R1- repeat the junction of leters (e.g. im here) \n R2 - R1 but leter by leter (e.g. i m space h e r e) \n M1 - mouse buttons \n M2 - mouse buttons \n CC - when you press the active combo it start pressing the key \n") # Include "space" as a word, not just a character

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
            print(f"port: {Port.device}")
        
        
        arduino = serial.Serial(port, 9600, timeout=0.1)
        On = True

        while On:

            value = read_arduino()
            line = arduino.readline().decode('utf-8').strip()
            if not line:
                print(f"line: {line}")
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
                if data.get('V'): #volante pin(A0)
                    Turn = data.get('V')
                    print(f"Turn: {Turn}")
                    if Turn is None:
                        Turn = 1
                    if Turn is not None:
                        center = 512
                        now = time.time()

                        if Turn >= center+20:
                            turn_key = 'd'
                            turn_strength = (Turn - center) / 512  # Normalize between 0 and ~1
                            pwm_interval = max(0.02, 0.2 * (1 - turn_strength))  # Higher value = slower tapping

                        elif Turn < center-20:
                            turn_key = 'a'
                            turn_strength = (center - Turn) / 512
                            pwm_interval = max(0.02, 0.2 * (1 - turn_strength))

                        else:
                            turn_key = None  # No steering

                        # If enough time passed since last PWM tap
                        if turn_key and now - last_pwm_time > pwm_interval:
                            keyboard.press(turn_key)
                            keyboard.release(turn_key)
                            last_pwm_time = now

                if data.get('W'): #accelerator pin(A1)
                    Accelerate = data.get('W')
                    print(f"Accelerate: {Accelerate}")
                    if Accelerate is not None:
                        accel_pwm['strength'] = max(min(Accelerate / 1023.0, 2.0), 0.0)  # Normalize to [0.0, 1.0]

                    now = time.time()
                    elapsed = now - accel_pwm['last_toggle']
                    press_time = accel_pwm['strength'] * accel_pwm['cycle_time']
                    rest_time = accel_pwm['cycle_time'] - press_time

                    if accel_pwm['strength'] > 0.05:
                        if accel_pwm['pressing'] and elapsed >= press_time:
                            keyboard.release(accel_pwm['key'])
                            accel_pwm['pressing'] = False
                            accel_pwm['last_toggle'] = now
                        elif not accel_pwm['pressing'] and elapsed >= rest_time:
                            keyboard.press(accel_pwm['key'])
                            accel_pwm['pressing'] = True
                            accel_pwm['last_toggle'] = now
                    else:
                        if accel_pwm['pressing']:
                            keyboard.release(accel_pwm['key'])
                            accel_pwm['pressing'] = False

                if data.get('S'): #breaker pin(6)
                    BValue = data.get('S')
                    if BValue is not None:
                        print(f"BValue: {BValue}")
                        keyboard.press('s')
                    else:
                        keyboard.release('s')

                if data.get('Shift'): #mudanças pin(5)
                    BValue2 = data.get('Shift')
                    if BValue2 is not None:
                        print(f"mudanças: {BValue2}")
                        if BValue2 > 0:
                            keyboard.press('shift')
                        else:
                            keyboard.release('shift')

                if data.get('H'): #Horn pin(7)
                    BValue3 = data.get('H')
                    if BValue3 is not None: 
                        print(f"Horn: {BValue3}")
                        if BValue3 > 0:
                            keyboard.press('h')
                        else:
                            keyboard.release('h')

                if data.get('IO'): #Horn pin(4)
                    BValue4 = data.get('IO')
                    if BValue4 is not None: 
                        #print(f"IO: {BValue4}")
                        if BValue4:
                            On = False

    else:
        print("Invalid command. Try again.\n")
        continue    

