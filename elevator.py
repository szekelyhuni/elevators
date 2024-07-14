import tkinter as tk
from tkinter import messagebox

class Floor:
    def __init__(self, number):
        self.number = number
        self.call_up = False
        self.call_down = False
    
    def call_elevator(self, direction):
        if direction == 'up':
            self.call_up = True
        elif direction == 'down':
            self.call_down = True

class Elevator:
    def __init__(self, name, current_floor):
        self.name = name
        self.current_floor = current_floor
        self.target_floor = None
        self.state = 'idle'  # states: 'idle', 'moving_up', 'moving_down', 'door_open'
    
    def move_to_floor(self, target_floor):
        self.target_floor = target_floor
        if target_floor > self.current_floor:
            self.state = 'moving_up'
        elif target_floor < self.current_floor:
            self.state = 'moving_down'
        else:
            self.state = 'door_open'
    
    def update_state(self):
        if self.state == 'moving_up':
            while self.current_floor != self.target_floor:
                self.current_floor += 1
                print(f"Elevator {self.name} moving up to floor {self.current_floor}")
            if self.current_floor == self.target_floor:
                self.state = 'door_open'
                print(f"Elevator {self.name} opening door")
        elif self.state == 'moving_down':
            while self.current_floor != self.target_floor:
                self.current_floor -= 1
                print(f"Elevator {self.name} moving down to floor {self.current_floor}")
            if self.current_floor == self.target_floor:
                self.state = 'door_open'
                print(f"Elevator {self.name} opening door")
        elif self.state == 'door_open':
            self.state = 'idle'
            self.target_floor = None

class ElevatorControlSystem:
    def __init__(self):
        self.elevators = [Elevator('A', 0), Elevator('B', 6)]
        self.floors = [Floor(i) for i in range(7)]
    
    def assign_elevator(self, floor, direction):
        closest_elevator = None
        min_distance = float('inf')
        for elevator in self.elevators:
            distance = abs(elevator.current_floor - floor)
            if distance < min_distance:
                min_distance = distance
                closest_elevator = elevator
            elif distance == min_distance:
                if elevator.current_floor < closest_elevator.current_floor:
                    closest_elevator = elevator
        
        closest_elevator.move_to_floor(floor)
        self.floors[floor].call_elevator(direction)
        return closest_elevator
    
    def update_system(self):
        for elevator in self.elevators:
            elevator.update_state()
    
    def display_elevator_positions(self):
        positions = []
        for elevator in self.elevators:
            positions.append(f"Elevator {elevator.name} is on floor {elevator.current_floor}")
        return positions

def call_elevator():
    global assigned_elevator
    try:
        floor = int(floor_entry.get())
        if floor < 0 or floor > 6:
            raise ValueError("Floor must be between 0 and 6")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return

    direction = direction_var.get()
    
    assigned_elevator = control_system.assign_elevator(floor, direction)
    control_system.update_system()
    update_positions()
    
    result_label.config(text=f"Elevator {assigned_elevator.name} called to floor {floor}")

def go_to_floor():
    global assigned_elevator
    if assigned_elevator is None:
        messagebox.showerror("Error", "You must call an elevator first!")
        return
    
    try:
        destination_floor = int(destination_entry.get())
        if destination_floor < 0 or destination_floor > 6:
            raise ValueError("Floor must be between 0 and 6")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return
    
    assigned_elevator.move_to_floor(destination_floor)
    control_system.update_system()
    update_positions()

def update_positions():
    positions = control_system.display_elevator_positions()
    positions_text = "\n".join(positions)
    positions_label.config(text=positions_text)

control_system = ElevatorControlSystem()
assigned_elevator = None

root = tk.Tk()
root.title("Elevator Control System")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Current floor:").grid(row=0, column=0)
floor_entry = tk.Entry(frame)
floor_entry.grid(row=0, column=1)

direction_var = tk.StringVar(value="up")
tk.Radiobutton(frame, text="Up", variable=direction_var, value="up").grid(row=1, column=0)
tk.Radiobutton(frame, text="Down", variable=direction_var, value="down").grid(row=1, column=1)

call_button = tk.Button(frame, text="Call Elevator", command=call_elevator)
call_button.grid(row=2, columnspan=2, pady=10)

tk.Label(frame, text="Destination Floor:").grid(row=3, column=0)
destination_entry = tk.Entry(frame)
destination_entry.grid(row=3, column=1)

go_button = tk.Button(frame, text="Go to Floor", command=go_to_floor)
go_button.grid(row=4, columnspan=2, pady=10)

result_label = tk.Label(frame, text="")
result_label.grid(row=5, columnspan=2, pady=10)

positions_label = tk.Label(root, text="")
positions_label.pack(pady=10)

update_positions()

root.mainloop()
