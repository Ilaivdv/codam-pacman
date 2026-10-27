*This project has been created as part of the 42 curriculum by yafu, ivan-der.*

# Pacman (42 Curriculum)

## Description
This project is an interdisciplinary implementation of the classic **Pac-Man** arcade game, built in Python using `Pygame`. The main goal of this project is to model dynamic game states, complex ghost behavior/pathfinding, real-time input handling, and automated maze parsing within a modular, maintainable software architecture.

Key features include:
- Multiple ghost state machines (Scatter, Chase, Frightened).
- Procedural/dynamic maze loading and scaling via the given `Mazegenerator` package.
- Highscore tracking, custom settings configuration, and level management.

---

## Instructions

### Prerequisites
- Python `3.12+`
- Package manager: [`uv`](https://github.com/astral-sh/uv)

### Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ilaivdv/codam-pacman.git
   cd codam-pacman
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the game:**
   ```bash
   make
   # Or
   python3 pac-man.py config.json
   ```

---

## Configuration

The project reads settings from `config.json`. If the file is missing or corrupted, standard default values are automatically generated and applied.

### Configuration(default)
```json
  {
    'highscore_filename': "highscore.json",
    "level": 10,
    "width": 15,
    "height": 15,
    'lives': 3, 'pacgum': 42,
    'points_per_pacgum': 10,
    'points_per_super_pacgum': 50,
    'points_per_ghost': 200,
    'seed': 42,
    'level_max_time': 90
                }
```

---

## Highscore Section

### Implementation Details
The highscore system reads and writes scores to a local persistent file (`~/.local/share/highscore.json`). Scores are updated immediately upon game completion or failure. In the game, only top 10 records are displayed.

### Design Choice
We chose an explicit file-backed JSON over in-memory storage to ensure data retains integrity across sessions without requiring external database dependencies. If the file doesn't exist, the program will create one empty file.

---

## Maze Generation

This project integrates the `A-Maze-ing` maze generation package.

- **Parsing & Visuals:** The output grid array from `mazegenerator-2.0.2-py3-none-any` is mapped dynamically to grid coordinates, scaling pacgums, walls, and spawn points based on window boundaries.
- **Pathfinding Graph:** Grid nodes are converted into an adjacency matrix / node graph used by ghost AI algorithms (A* search ).

---

## Implementation Summary(not sure needed)

- **Engine & Loop:** .
- **Entity Management:** 
- **Pathfinding:** 

---

## General Software Architecture

```text
src/
├── level/            # 
      └── entities/     
├── ui/               # UI elements, clickable, non-clickable
    ├── overlay/      # UI interface that overlay on current screen
    └── screens/      # UI interface that occupies the whole screen
└── utils/            # 
```

- **Modular Coupling:** 
- **State Machine:** 

---

## Project Management

This project was developed iteratively using GitHub Projects:
- **Task Tracking & Roadmap:** Tasks were organized into feature branches, code reviews, and issue tracking.
- **Documentation:** Project management artifacts, gantt charts, and sprint logs are located in the root directory [`process_track.md`].

---

## Resources & AI Disclosure

### References
- [Pygame Documentation](https://pyg.am/docs/)
- [The Pac-Man Dossier (Jamey Pittman)](https://pacman.holenet.info/)
- [Creating Start Menu in Pygame](https://www.geeksforgeeks.org/python/creating-start-menu-in-pygame/)
- [Pygame tutorial](https://www.geeksforgeeks.org/python/pygame-tutorial/)


### AI Usage Disclosure
In accordance with 42 curriculum guidelines, AI assistance was utilized for README scaffolding.
