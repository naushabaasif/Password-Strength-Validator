uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
digits = set("0123456789")
specials = set("@#$!%^&*()_+-=[]{}|;:,.?")

def make_config():
    return {
        "state"  : "q0_No_Upper_No_Digit_No_Special",
        "stack"  : ["Z", "X", "X", "X", "X", "X", "X", "X", "X"],
        "length" : 0,   
        "trace"  : []   
    }

def transition(cfg, char):
    cfg["length"] += 1
    current_state = cfg["state"]
    stack = cfg["stack"]
    trace = cfg["trace"]

    has_upper = ("Has_Upper"   in current_state) or (char in uppercase)
    has_digit = ("Has_Digit"   in current_state) or (char in digits)
    has_special = ("Has_Special" in current_state) or (char in specials)

    upper_part = "Has_Upper"   if has_upper   else "No_Upper"
    digit_part = "Has_Digit"   if has_digit   else "No_Digit"
    special_part = "Has_Special" if has_special else "No_Special"
    cfg["state"] = f"q_{upper_part}_{digit_part}_{special_part}"

    stack_top = stack[-1]
    if stack_top == "X":
        stack.pop()
        trace.append(f"  Read '{char}' -> pop 'X' (length countdown) -> stack: {stack[:]}")
    else:
        trace.append(f"  Read '{char}' -> top is 'Z', length >= 8 already satisfied -> stack: {stack[:]}")

    return cfg

def finalize(cfg):

    state = cfg["state"]
    stack = cfg["stack"]
    trace = cfg["trace"]

    all_type_rules_met = (
        "Has_Upper"   in state and
        "Has_Digit"   in state and
        "Has_Special" in state
    )
    length_rule_met = (stack[-1] == "Z")  

    if all_type_rules_met and length_rule_met:
        stack.pop()  
        trace.append("End of input -> pop 'Z' (bottom marker) -> stack EMPTY -> ACCEPT")
        cfg["state"] = "q_accept"
    else:
        trace.append("  End of input -> unmet rules or stack not empty -> REJECT")
        cfg["state"] = "q_reject"
    return cfg

def get_strength(cfg, state_before_finalize):
    score = 0
    if "Has_Upper" in state_before_finalize: score += 1
    if "Has_Digit" in state_before_finalize: score += 1
    if "Has_Special" in state_before_finalize: score += 1
    if cfg["length"] >= 8:                     score += 1
    strength_labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    return strength_labels[score]

password = input("Enter password: ")
cfg = make_config()

for char in password:
    cfg = transition(cfg, char)

state_before_finalize = cfg["state"]
cfg = finalize(cfg)

print("\n--Stack Tracing --")
for line in cfg["trace"]:
    print(line)

print(f"\nFinal stack : {cfg['stack']}")
print(f"Final state : {cfg['state']}")
print(f"Strength : {get_strength(cfg, state_before_finalize)}")

if cfg["state"] == "q_accept":
    print("Result: ACCEPTED")
else:
    print("Result: REJECTED")
    print("Rules not Met:")
    if "No_Upper"   in state_before_finalize: print("- At least one uppercase letter")
    if "No_Digit"   in state_before_finalize: print("- At least one digit")
    if "No_Special" in state_before_finalize: print("- At least one special character")
    if cfg["length"] < 8:                     print("- Minimum 8 characters")