import random
from time import time,sleep
import tkinter as tk
from threading import Thread

# Define IoT Device Classes
class SmartDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False

    def toggle_status(self):
        self.status = not self.status

class SmartLight(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, brightness):
        self.brightness = brightness

    def set_random_brightness(self):
         self.set_brightness(random.randint(0, 100))

class Thermostat(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 20

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_random_temperature(self):
         self.set_temperature(random.randint(10, 30))

class SecurityCamera(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.motion_detected = False

    def detect_motion(self):
        self.motion_detected = random.choice([True, False])

# Automation System and Rule Classes
class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.rules = []
        self.status = False

    def add_device(self, device):
        self.devices.append(device)


    def add_rule(self, rule):
        self.rules.append(rule)



    def execute_rules(self):
        for rule in self.rules:
            rule.apply(self.devices)

class AutomationRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def apply(self, devices):
        if self.condition(devices):
            self.action(devices)


# GUI Dashboard Class
class Dashboard:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Smart Home IoT Simulator")
        self.labels = []
        self.automation_on = False

        self.realAutomation_on = False

        self.automation_text = tk.StringVar()
        self.automation_text.set("Random automation: {}".format("ON" if self.automation_on else "OFF"))

        self.light_button_texts = []

        self.lastMovementTime = {}


        self.device_listbox = tk.Listbox(root, width=50)
        self.device_listbox.pack()

        self.create_device_controls()
        self.create_rule_controls()

        self.update_device_list()
        self.update_thread = Thread(target=self.simulation_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        self.automation_btn = tk.Button(self.root, textvariable=self.automation_text, command=lambda: self.toggle_random())
        self.automation_btn.pack()

    def toggle_random(self):
        self.automation_on = not self.automation_on
        self.automation_text.set("Random automation: {}".format("ON" if self.automation_on else "OFF"))

    def create_device_controls(self):
        # Create controls for each device
        for i, device in enumerate(self.system.devices):

            deviceStatusString = tk.StringVar()
            deviceStatusString.set("ON" if device.status else "OFF")

            if isinstance(device, SmartLight):
                self.create_light_controls(device)
                self.create_light_control_Random(device)

                var_str = tk.StringVar()
                var_str.set("{} - {}%".format(device.device_id, device.brightness))

                self.light_button_texts.append({'device': device, 'text': deviceStatusString})


                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, textvariable=deviceStatusString, command=lambda device=device,text = deviceStatusString : self.toggle_helper(device,text)).pack()
                tmp_label.pack()
            elif isinstance(device, Thermostat):

                self.create_thermostat_controls(device)
                self.create_thermostat_control_Random(device)

                var_str = tk.StringVar()
                var_str.set("{} - {}-C".format(device.device_id, device.temperature))
                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, textvariable=deviceStatusString, command=lambda device=device,text = deviceStatusString: self.toggle_helper(device,text)).pack()
                tmp_label.pack()
            elif isinstance(device, SecurityCamera):
                self.create_camera_controls(device)
                var_str = tk.StringVar()
                var_str.set("{} - Motion: {}".format(device.device_id, 'YES' if device.motion_detected else 'NO'))
                tmp_label = tk.Label(self.root, textvariable=var_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': var_str,
                    'device': device
                })
                tk.Button(self.root, textvariable=deviceStatusString, command=lambda device=device,text = deviceStatusString: self.toggle_helper(device,text)).pack()
                tmp_label.pack()

    def toggle_helper(self, device,text):
        device.toggle_status()
        text.set("ON" if device.status else "OFF")

    def update_values(self):
        for tmp_label in self.labels:
            device = tmp_label['device']
            if isinstance(device, SmartLight):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.brightness}%" if device.status else "(OFF)"))
            elif isinstance(device, Thermostat):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.temperature}C" if device.status else "(OFF)"))
            elif isinstance(device, SecurityCamera):
                tmp_label['label'].set("{} - Motion: {}".format(device.device_id, ('YES' if device.motion_detected else 'NO')  if device.status else "(OFF)"))

        for objects in self.light_button_texts:
             device = objects['device']
             text_var = objects['text']
             text_var.set("ON" if device.status else "OFF")


    def create_light_controls(self, light):
        # Create controls for a smart light
        label = tk.Label(self.root, text=f"{light.device_id} Brightness")
        label.pack()
        brightness_slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", command=lambda value, light=light: self.set_brightness(light, value))
        brightness_slider.pack()


    def create_thermostat_controls(self, thermostat):
        # Create controls for a thermostat
        label = tk.Label(self.root, text=f"{thermostat.device_id} Temperature")
        label.pack()
        temperature_slider = tk.Scale(self.root, from_=10, to=30, orient="horizontal", command=lambda value, thermostat=thermostat: self.set_temperature(thermostat, value))
        temperature_slider.pack()

    def create_light_control_Random(self,light):
        label = tk.Label(self.root, text=f"{light.device_id} Random Brightness")
        label.pack()
        random_light_button = tk.Button(self.root, text="Random Brightness", command=lambda light=light: light.set_random_brightness())

        random_light_button.pack()

    def create_thermostat_control_Random(self,thermostat):
        label = tk.Label(self.root, text=f"{thermostat.device_id} Random Temperature")
        label.pack()
        random_light_button = tk.Button(self.root, text="Random Temperature", command=lambda thermostat=thermostat: thermostat.set_random_temperature())

        random_light_button.pack()

    def create_camera_controls(self, camera):
        # Create controls for a security camera
        label = tk.Label(self.root, text=f"{camera.device_id} Motion Detection")
        label.pack()
        motion_button = tk.Button(self.root, text="Random Detect Motion", command=lambda camera=camera: self.detect_motion(camera))

        motion_button.pack()

    def create_rule_controls(self):
        # Create controls for automation rules
        automationStatusString = tk.StringVar()
        automationStatusString.set("ON" if self.realAutomation_on else "OFF")

        rule_label = tk.Label(self.root, text="Automation Rule: Turn on lights when motion is detected")
        rule_label.pack()
        rule_button = tk.Button(self.root, textvariable=automationStatusString, command= lambda text=automationStatusString : self.toggle_automation_rule(text))
        rule_button.pack()

    def update_device_list(self):
        self.device_listbox.delete(0, tk.END)
        for device in self.system.devices:
            self.device_listbox.insert(tk.END, f"{device.device_id}: {type(device).__name__} Status: {'On' if device.status else 'Off'}")

    def simulation_loop(self):
        while True:
            current_time = time()

            if self.automation_on:
                self.system.execute_rules()
                randomize_device_states(self.system.devices)

            if self.realAutomation_on:
                self.system.execute_rules()

            for device in self.system.devices:
                if isinstance(device, SmartLight) and device.device_id in self.lastMovementTime:
                    if current_time - self.lastMovementTime[device.device_id] > 5:
                        device.status = False

            self.update_values()
            self.update_device_list()
            sleep(1)  # Simulate updates every 1 seconds

    def set_brightness(self, light, brightness):
        light.set_brightness(int(brightness))

    def set_temperature(self, thermostat, temperature):
        thermostat.set_temperature(int(temperature))

    def detect_motion(self, camera):
        camera.detect_motion()



    def toggle_automation_rule(self,text):
        if not self.realAutomation_on:
            self.realAutomation_on = True
            def motion_detected(devices):
                for device in devices:
                    if isinstance(device, SecurityCamera) and device.motion_detected:
                        #print(f"Motion detected by {device.device_id}")
                        return True
                return False

            def turn_on_lights(devices):
               # print("Turning on lights...")
                current_time = time()
                for device in devices:
                    if isinstance(device, SmartLight):
                        device.status = True
                        device.set_brightness(50)
                        self.lastMovementTime[device.device_id] = current_time

            rule = AutomationRule(motion_detected, turn_on_lights)
            self.system.add_rule(rule)

        else :
            self.realAutomation_on = False
            self.system.rules = []

        text.set("ON" if self.realAutomation_on else "OFF")

    def create_automation_rule(self):
        def motion_detected(devices):
            for device in devices:
                if isinstance(device, SecurityCamera) and device.motion_detected:
                    return True
            return False

        def turn_on_lights(devices):
            for device in devices:
                if isinstance(device, SmartLight):
                    device.status = True


        rule = AutomationRule(motion_detected, turn_on_lights)
        self.system.add_rule(rule)

# Randomization mechanism
def randomize_device_states(devices):
    for device in devices:
        if not device.status:
            continue

        if isinstance(device, SmartLight):
            device.set_brightness(random.randint(0, 100))
        elif isinstance(device, Thermostat):
            device.set_temperature(random.randint(18, 25))
        elif isinstance(device, SecurityCamera):
            device.detect_motion()

# Main function to initialize and run the simulation
if __name__ == "__main__":
    # Create IoT Devices
    light1 = SmartLight("Living Room Light")
    light2 = SmartLight("Living Room 2 Light")
    thermostat1 = Thermostat("Living Room Thermostat")
    camera1 = SecurityCamera("Front Door Camera")

    # Create Automation System
    automation_system = AutomationSystem()
    automation_system.add_device(light1)
    automation_system.add_device(light2)
    automation_system.add_device(thermostat1)
    automation_system.add_device(camera1)

    # Create GUI Dashboard
    root = tk.Tk()
    dashboard = Dashboard(root, automation_system)
    root.mainloop()
