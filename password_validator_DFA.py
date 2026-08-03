uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
digits = set("0123456789")
specials = set("@#$!%^&*()_+-=[]{}|;:,.?")

def get_start_state():
    return "Len0_NoU_NoD_NoS"

def transition(state, char):
    
    current_len = int(state.split('_')[0].replace("Len", ""))
    has_u = "HasU" in state
    has_d = "HasD" in state
    has_s = "HasS" in state

    if current_len < 8:
        next_len = current_len + 1
    else:
        next_len = 8

    if char in uppercase: has_u = True
    if char in digits:    has_d = True
    if char in specials:  has_s = True

    u_part = "HasU" if has_u else "NoU"
    d_part = "HasD" if has_d else "NoD"
    s_part = "HasS" if has_s else "NoS"
    return f"Len{next_len}_{u_part}_{d_part}_{s_part}"

def is_accepted(state):
    return state == "Len8_HasU_HasD_HasS"

def get_strength(state):
    current_len = int(state.split('_')[0].replace("Len", ""))
    
    score = sum(["HasU" in state,"HasD" in state,"HasS" in state,current_len >= 8])
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    return labels[score]

password = input("Enter password: ")
state = get_start_state()

for char in password:
    state = transition(state, char)

print("Final DFA State:", state)
print("Strength:", get_strength(state))

if is_accepted(state):
    print("ACCEPTED")
else:
    print("REJECTED")
    print("Missing rules:")
    if "NoU" in state: print("  - At least one uppercase letter")
    if "NoD" in state: print("  - At least one digit")
    if "NoS" in state: print("  - At least one special character")
    current_len = int(state.split('_')[0].replace("Len", ""))
    if current_len < 8: print("  - Minimum 8 characters")