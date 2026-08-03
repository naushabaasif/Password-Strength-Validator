# Password Strength Validator using Automata Theory

A Python-based password validation system that demonstrates the practical implementation of **Deterministic Finite Automata (DFA)** and **Pushdown Automata (PDA)**. The project validates password strength according to predefined security rules while illustrating automata state transitions and stack operations through both console-based simulations and an interactive graphical interface.

> Developed as a course project for **Finite Automata & Formal Languages** at **SZABIST**.

---

## Overview

This project applies concepts from **Automata Theory** to solve a real-world problem: password validation.

The system consists of three implementations:

- **Deterministic Finite Automaton (DFA)** for password validation using finite state transitions.
- **Pushdown Automaton (PDA)** for password validation using stack-based computation.
- **Tkinter GUI Simulation** that visually demonstrates PDA state transitions and stack operations.

The project bridges theoretical concepts from Formal Languages with practical software implementation.

---

## Automata Concepts Used

This project demonstrates the implementation of:

- Deterministic Finite Automata (DFA)
- Pushdown Automata (PDA)
- State Transitions
- Stack Operations (LIFO)
- Acceptance and Rejection States
- Formal Language Theory
- Password Validation using Automata Models

---

## Password Validation Rules

A password is accepted only if it satisfies all of the following conditions:

- Minimum length of **8 characters**
- Contains at least **one uppercase letter**
- Contains at least **one digit**
- Contains at least **one special character**

Accepted special characters include:

```
@ # $ ! % ^ & * ( ) _ + - = [ ] { } | ; : , . ?
```

---

## Project Components

### 1. DFA Password Validator

The DFA implementation validates passwords by transitioning through states that represent whether each password rule has been satisfied.

Features:

- State-based password validation
- Password strength classification
- Displays final DFA state
- Reports missing validation rules

---

### 2. PDA Password Validator

The PDA implementation validates passwords using stack operations.

Features:

- Stack-based length verification
- State transition tracing
- Stack operation logging
- Acceptance based on final state and stack contents
- Password strength evaluation

---

### 3. PDA GUI Simulator

An interactive graphical application developed using **Tkinter**.

Features:

- Real-time state transitions
- Live stack visualization
- Character-by-character simulation
- Acceptance and rejection display
- Educational demonstration of PDA execution

---

## Technologies Used

- Python 3
- Tkinter
- Python Standard Library

---

## Project Structure

```text
Password-Strength-Validator/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── password_validator_DFA.py
├── password_validator_PDA.py
├── Password_validator_PDA_GUI.py
│
├── Project_Proposal.pdf
├── Project_Report.pdf
│
└── screenshots/
    ├── gui-home.png
    ├── simulation.png
    ├── accepted.png
    ├── rejected.png
    ├── dfa-console.png
    └── pda-console.png
```

---

## How to Run

### Clone the repository

```bash
git clone https://github.com/yourusername/Password-Strength-Validator.git
```

### Navigate to the project

```bash
cd Password-Strength-Validator
```

### Run the DFA Validator

```bash
python dfa_password_validator.py
```

### Run the PDA Validator

```bash
python pda_password_validator.py
```

### Launch the GUI Simulator

```bash
python pda_gui_simulator.py
```

---

## Application Screenshots

Below are sample outputs demonstrating the DFA, PDA, and GUI implementations.

### GUI Home Screen

![GUI Home](screenshots/gui-home.png)

### PDA Simulation

![Simulation](screenshots/simulation.png)

### Accepted Password

![Accepted](screenshots/accepted.png)

### Rejected Password

![Rejected](screenshots/rejected.png)

### DFA Console Output

![DFA Console](screenshots/dfa-console.png)

### PDA Console Output

![PDA Console](screenshots/pda-console.png)

---

## Learning Outcomes

This project demonstrates practical implementation of:

- Deterministic Finite Automata
- Pushdown Automata
- Formal Languages
- State Machine Design
- Stack-Based Computation
- Password Validation Algorithms
- GUI Development with Tkinter
- Python Programming
- Algorithm Design

---

## Future Improvements

Potential enhancements include:

- Support for lowercase character validation
- Password entropy analysis
- Animated state transition diagrams
- Export validation reports
- Enhanced GUI visualization
- Multiple password policy configurations
- Integration with authentication systems

---

## Project Documentation

The repository also includes:

### Project Proposal

Contains:

- Initial project idea
- Problem statement
- Automata selection
- Proposed implementation
- Real-world application

### Project Report

Contains:

- System design
- DFA implementation
- PDA implementation
- GUI implementation
- Comparison between DFA and PDA
- Testing and results
- Conclusion

---

## Authors

**Naushaba Asif**  
4th Semester Computer Science Student  
SZABIST Karachi

**Rohban Tariq**  
4th Semester Computer Science Student  
SZABIST Karachi

---

## License

This project was developed for educational purposes as part of the **Finite Automata & Formal Languages** course at **SZABIST**.
