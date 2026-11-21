# 🔐 Password Strength Validator

A password validator implemented **twice** using formal computation models — once as a **Deterministic Finite Automaton (DFA)** and once as a **Pushdown Automaton (PDA)** — plus a live **Tkinter GUI** that animates the PDA's finite control and stack in real time as it consumes a password character by character.

Most password validators are five lines of regex. This one is deliberately built the hard way: as a state machine whose states, transition function, and acceptance condition are designed from first principles, to demonstrate how security policy enforcement maps onto formal language theory.

> Built for a Theory of Automata & Formal Languages course — but engineered like a project meant to be read by more than a grader.

---

## Why this project is more than a class assignment

- **Two different computational models solving the same problem** — and reasoning explicitly about *why* each one is shaped the way it is (state-space design vs. stack-based memory).
- **State-space engineering**: the DFA's state space isn't ad hoc — it's a deliberate cross-product of length (0–8) × three boolean type-flags, justified as `9 × 8 = 72` states, with an explicit argument for *why* a DFA can't just "count" length with an integer.
- **Stack-based algorithm design**: the PDA offloads length-tracking onto a stack instead of the finite control, and accepts by the classical **empty-stack** convention rather than a designated final state.
- **Concurrent GUI programming**: the visualizer runs the simulation on a background thread (`threading`) so the Tkinter main loop never freezes during the animated step-by-step trace — a real, non-trivial UI engineering detail, not just "add a button."
- **Self-aware engineering**: see [Known Limitations](#known-limitations--next-steps) below. Knowing where your own model's abstraction leaks is part of the skill.

---

## The problem being modeled

A password is accepted only if it satisfies **all four** conditions simultaneously:

| # | Rule | Alphabet |
|---|------|----------|
| 1 | At least one uppercase letter | `Σ_upper = {A–Z}` |
| 2 | At least one digit | `Σ_digit = {0–9}` |
| 3 | At least one special character | `Σ_special = {!,@,#,$,...}` |
| 4 | Minimum length of 8 characters | — |

This is a **conjunction of independent conditions**, which is exactly the kind of requirement that gets messy to reason about informally but maps cleanly onto a finite-state model — each state *is* a snapshot of "which conditions are currently satisfied."

---

## Model 1 — Deterministic Finite Automaton (DFA)

**Formal definition:** `(Q, Σ, δ, q0, F)`

The core design insight: a DFA has no external memory, so it can't hold an arbitrary integer counter for password length. Length has to be tracked *by moving through states*, and — critically — that only stays finite if the counter is **capped**. Once the count hits 8, it stops advancing (`j = i+1 if i < 8, else j = 8`), which is what keeps `Q` a genuinely finite set instead of growing per input.

- **State space:** `Q` = length steps `(0..8)` × 3 boolean type-flags → `9 × 8 = 72` states
- **State encoding:** a live string token, e.g. `Len3_HasU_NoD_NoS`
- **Transition function:** `δ(Len_i_Flags, char) → Len_j_UpdatedFlags`
- **Accept state:** exactly `Len8_HasU_HasD_HasS`
- **Bonus feature:** the implementation goes further than raw accept/reject — it derives a **strength score** (`Very Weak → Very Strong`) from how many of the four conditions are currently met, and on rejection it reports *which specific rules* failed.

```python
def transition(state, char):
    current_len = int(state.split('_')[0].replace("Len", ""))
    has_u = "HasU" in state
    has_d = "HasD" in state
    has_s = "HasS" in state

    next_len = current_len + 1 if current_len < 8 else 8

    if char in uppercase: has_u = True
    if char in digits:    has_d = True
    if char in specials:  has_s = True

    return f"Len{next_len}_{'HasU' if has_u else 'NoU'}_{'HasD' if has_d else 'NoD'}_{'HasS' if has_s else 'NoS'}"
```

---

## Model 2 — Pushdown Automaton (PDA)

**Formal definition:** `(Q, Σ, Γ, δ, q0, Z0, F)`

The design goal here was to actually *use* the extra memory a PDA gets over a DFA, instead of just re-solving the DFA problem with more moving parts. So the two concerns are split cleanly:

- **Character-type tracking** (upper/digit/special) stays in the **finite control** — that part of the problem is genuinely regular, so it belongs in states.
- **Length tracking** moves onto the **stack**, `Γ = {X, Z}` — the part of the problem that's naturally about *counting*, which is the PDA's whole reason for existing.

**Mechanics:**
1. The stack is pre-loaded: `[Z, X, X, X, X, X, X, X, X]` (8 length-counter tokens over a bottom marker).
2. Every character read pops one `X`, only if `X` is on top — the read head only ever looks at `stack[-1]`, respecting the LIFO constraint properly instead of cheating by indexing into the stack.
3. If input runs past 8 characters, the top is already `Z`, so the machine safely stops popping instead of erroring.
4. **Acceptance by empty stack**: after the last character, if all three type-flags are satisfied *and* the stack top is `Z`, the final `Z` is popped — stack becomes `[]`, and *that emptiness itself* is the accept signal, rather than landing in a designated final state.

```python
def finalize(cfg):
    all_type_rules_met = ("Has_Upper" in cfg["state"] and "Has_Digit" in cfg["state"] and "Has_Special" in cfg["state"])
    length_rule_met = (cfg["stack"][-1] == "Z")

    if all_type_rules_met and length_rule_met:
        cfg["stack"].pop()          # pop the bottom marker -> stack is now empty
        cfg["state"] = "q_accept"   # acceptance by EMPTY STACK, not a final state
    else:
        cfg["state"] = "q_reject"
    return cfg
```

---

## Model 3 — Live GUI Simulator

A Tkinter dashboard that makes the PDA's internal configuration observable instead of theoretical:

- **Finite Control panel** — renders the live state string as it updates on every character read.
- **Stack panel** — a vertical `Listbox` that mirrors the actual Python list in memory, with the pink `X` length-tokens visibly popping off to expose the purple `Z` bottom marker underneath.
- **Non-blocking animation** — the step-by-step trace runs on a background `threading.Thread`, so `time.sleep()` calls between steps animate the process without freezing the Tkinter main loop.

```python
def start_simulation(self):
    password = self.password_entry.get()
    self.btn_run.config(state=tk.DISABLED)
    threading.Thread(target=self.run_pda, args=(password,), daemon=True).start()
```

---

## DFA vs. PDA — side by side

| | DFA | PDA |
|---|---|---|
| **Type tracking** | Encoded in the state string | Encoded in the state string |
| **Length tracking** | Explicit states `Len0 → Len8` | Stack pop per character |
| **Acceptance** | Reaching state `Len8_HasU_HasD_HasS` | Emptying the stack `[]` |
| **Computational class** | Regular language | Context-free (by construction — see limitations) |
| **Memory model** | Fixed 72-state matrix | Stack-based, LIFO-constrained |

---

## Known Limitations & Next Steps

Being upfront about this rather than glossing over it:

- **The PDA's stack is currently capped at 8 tokens**, mirroring the DFA's length cap rather than exploiting the PDA's real advantage — a true unbounded stack. A natural extension: push one `X` per character with no ceiling, and check length by whether the stack depth is `≥ 8` at the end, which would actually demonstrate context-free-style unbounded counting instead of a relabeled DFA.
- **The GUI currently only visualizes the PDA**, not the DFA — a side-by-side dual visualization would make the state-space size difference (72 fixed states vs. a growing stack) visually obvious.
- **No persistent history** — could log each run to compare validator behavior across many passwords.

---

## Tech Stack

- **Python 3** — core logic for both automata
- **Tkinter** — GUI framework
- **threading** — non-blocking animated simulation

## Project Structure

```
password-strength-validator/
├── password_validator_DFA.py       # DFA implementation (console)
├── password_validator_PDA.py       # PDA implementation (console)
├── Password_validator_PDA_GUI.py             # Tkinter live visualizer
└── README.md
```

## Running it

```bash
# Console versions
python password_validator_DFA.py
python password_validator_PDA.py

# GUI visualizer
python Password_validator_PDA_GUI.py
```

---

## Background

Coursework project for **Theory of Automata & Formal Languages**, BSCS.

**Contributors:** Naushaba Asif - 2412485· Rohban Tariq - 2412488
4th Semester - SZABIST Karachi
