import tkinter as tk
import time
import threading

uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
digits    = set("0123456789")
specials  = set("@#$!%^&*()_+-=[]{}|;:,.?")

class PDAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA Password Validator")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f2f5")

        title = tk.Label(root, text="PDA Password Validator", font=("Arial", 16, "bold"), bg="#f0f2f5")
        title.pack(pady=10)

        input_frame = tk.Frame(root, bg="#f0f2f5")
        input_frame.pack(pady=10)
        
        lbl = tk.Label(input_frame, text="Enter Password:", font=("Arial", 11), bg="#f0f2f5")
        lbl.pack(side=tk.LEFT, padx=5)
        
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        self.btn_run = tk.Button(input_frame, text="Simulate PDA", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=self.start_simulation)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        display_frame = tk.Frame(root, bg="#f0f2f5")
        display_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.info_frame = tk.LabelFrame(display_frame, text=" PDA Finite Control ", font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        self.info_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)

        self.lbl_char = tk.Label(self.info_frame, text="Current Char: None", font=("Arial", 12), bg="white")
        self.lbl_char.pack(anchor="w", pady=5)

        self.lbl_state = tk.Label(self.info_frame, text="State: q0_No_Upper_No_Digit_No_Special", font=("Arial", 10), bg="white", fg="blue", wraplength=220, justify="left")
        self.lbl_state.pack(anchor="w", pady=5)

        self.lbl_result = tk.Label(self.info_frame, text="Result: Waiting...", font=("Arial", 14, "bold"), bg="white", fg="gray")
        self.lbl_result.pack(anchor="w", pady=20)

        self.stack_frame = tk.LabelFrame(display_frame, text=" PDA Stack (LIFO) ", font=("Arial", 11, "bold"), bg="white", padx=20, pady=10)
        self.stack_frame.pack(side=tk.RIGHT, padx=20, fill=tk.BOTH, expand=True)

        self.stack_listbox = tk.Listbox(self.stack_frame, font=("Arial", 14, "bold"), width=10, height=10, justify="center")
        self.stack_listbox.pack(pady=5)
  
        self.update_stack_view(["Z", "X", "X", "X", "X", "X", "X", "X", "X"])

    def update_stack_view(self, stack_list):
        self.stack_listbox.delete(0, tk.END)

        for item in reversed(stack_list):
            self.stack_listbox.insert(tk.END, item)
            if item == "X":
                self.stack_listbox.itemconfig(tk.END, {'fg': '#e91e63'}) 
            elif item == "Z":
                self.stack_listbox.itemconfig(tk.END, {'fg': '#9c27b0'}) 

    def start_simulation(self):
        password = self.password_entry.get()
        if not password:
            return
        
        self.btn_run.config(state=tk.DISABLED)
        self.lbl_result.config(text="Processing...", fg="orange")
        
        threading.Thread(target=self.run_pda, args=(password,), daemon=True).start()

    def run_pda(self, password):

        state = "q0_No_Upper_No_Digit_No_Special"
        stack = ["Z", "X", "X", "X", "X", "X", "X", "X", "X"]
        length = 0

        self.lbl_state.config(text=f"State: {state}")
        self.update_stack_view(stack)
        time.sleep(1.2) 

        for char in password:
            length += 1
            
            has_upper = ("Has_Upper" in state) or (char in uppercase)
            has_digit = ("Has_Digit" in state) or (char in digits)
            has_special = ("Has_Special" in state) or (char in specials)

            upper_part   = "Has_Upper"   if has_upper   else "No_Upper"
            digit_part   = "Has_Digit"   if has_digit   else "No_Digit"
            special_part = "Has_Special" if has_special else "No_Special"
            state = f"q_{upper_part}_{digit_part}_{special_part}"

            stack_top = stack[-1]
            if stack_top == "X":
                stack.pop()

            self.lbl_char.config(text=f"Current Char: '{char}'")
            self.lbl_state.config(text=f"State: {state}")
            self.update_stack_view(stack)
            
            time.sleep(0.8) 

        self.lbl_char.config(text="Current Char: None (End of Input)")
        time.sleep(1.0)

        all_type_rules_met = ("Has_Upper" in state and "Has_Digit" in state and "Has_Special" in state)
        length_rule_met = (stack[-1] == "Z")

        if all_type_rules_met and length_rule_met:
            stack.pop() 
            self.update_stack_view(stack)
            self.lbl_state.config(text="State: q_accept")
            self.lbl_result.config(text="Result: ACCEPTED ", fg="green")
        else:
            self.lbl_state.config(text="State: q_reject")
            self.lbl_result.config(text="Result: REJECTED ", fg="red")

        self.btn_run.config(state=tk.NORMAL)

if __name__ == "__main__": 
    root = tk.Tk()
    app = PDAGUI(root)
    root.mainloop()