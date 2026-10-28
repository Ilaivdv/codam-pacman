## Team Organization

Team planning went very smoothly for this project. 
We first decided who will work on what part of the game, we split the work as follows:

- Yawen
    + UI System (menus, overlays, notifications, etc.)
    + Score handling
    + Config and highscore parsing
- Ilai
    + Level & Gameplay (maze creation, game loop, players, ghosts, etc.)
    + Game structure/system
    + Art & Assets
    + Executable game build

Tasks we worked on in collaboration were general project planning and structure, deciding on using a kanban board 
utilizing Github issues and pull requests with a trunk-based workflow ensuring no conflicts or broken merges. 
Development went very smoothly and no unexpected problem arose.

## Game structure
When deciding on game structure, Other game engines were studied to see what works for them. 
Eventually we decided to implement something similar to the Godot game engine and their Node-based process tree, 
structuring our game as a tree of objects which can dynamically be moved around, inserted and removed made working 
on features hassle-free becuase it meant working on features could be done completely seperate from each other without causing conflicts.

### Assets

Assets were made using Aseprite and animations were hand-drawn and the fonts were found from [Google Fonts](https://fonts.google.com/)
