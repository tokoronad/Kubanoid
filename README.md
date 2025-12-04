Cubanoid
Game Overview
Cubanoid is a 2D platformer-shooter hybrid game packaged as a standalone Windows executable (game.exe). Control a cube-shaped character, battle enemies, and utilize various weapons in fast-paced gameplay.

System Requirements
OS: Windows 7/8/10/11 (64-bit)

RAM: 2 GB minimum, 4 GB recommended

Storage: 500 MB available space

Graphics: Any modern integrated or dedicated GPU

Input: Keyboard and mouse required

Installation
Standard Installation
Download the game files

Extract the archive to a folder of your choice

Ensure the folder structure is preserved:

text
your_game_folder/
├── sound/          # Audio files directory
├── images/         # Graphics files directory
├── game.exe        # Main executable file
Portable Version
Simply copy the entire folder to any location (USB drive, cloud storage, etc.) and run game.exe. No installation or registry changes required.

Quick Start
Double-click game.exe

Use the main menu to start playing

No additional software or dependencies needed

File Structure
text
game_folder/
├── game.exe                    # Main executable (PyGame application compiled with PyInstaller)
├── images/                    # All visual assets
│   ├── tiles.png              # Platform textures
│   ├── interface.png          # HUD and interface elements
│   ├── menu.png               # Menu graphics
│   ├── kubmove.png            # Player character animations
│   ├── jump_up.png            # Jump animation frames
│   ├── enemy_fly.png          # Flying enemy sprites
│   ├── enemy_ground.png       # Ground enemy sprites
│   └── [weapon sprites]       # Various weapon graphics
├── sound/                     # Audio assets
│   ├── shoot_shotgun.mp3      # Shotgun firing sound
│   ├── shoot_rifle.mp3        # Rifle firing sound
│   ├── running.wav            # Footstep sounds
│   ├── jump.wav               # Jump sound effect
│   ├── dash.wav               # Dash ability sound
│   ├── rearmed.mp3            # Reload sound
│   ├── menu_button.mp3        # Menu interaction sound
│   └── [music files]          # Background music tracks
└── [optional] saves/          # Save data folder (created automatically)
Controls
Movement
A/D - Move left/right

Left Shift - Sprint

Space - Jump (double jump available)

Q - Dash towards cursor

Wall jumps - Jump while against walls

Combat
Mouse - Aim direction

Left Click - Fire left weapon

Right Click - Fire right weapon

1/2 - Switch weapon loadouts

Menu/Interface
ESC - Pause/Open menu

I - Weapon selection screen

R - Restart (when dead)

F11 - Toggle fullscreen

Game Features
Core Gameplay
Dynamic Platforming: Jump, dash, and wall-jump through levels

Dual-Weapon System: Shotgun and rifle with different characteristics

Enemy Variety: Ground and flying enemies with AI behaviors

Progressive Difficulty: Enemies gain health as you defeat them

Score System: Earn points for defeating enemies

Visual & Audio
Particle Effects: Jump, land, impact, and blood effects

Screen Shake: Weapon feedback and impact effects

Procedural Textures: Platforms auto-texture based on surroundings

Full Soundtrack: Background music with multiple tracks

Sound Effects: Weapon sounds, footsteps, abilities

Technical Features
No Installation Required: Pure executable

Portable: Run from any location

Auto-Save: Progress saved automatically

Config-Free: No configuration files to edit

Troubleshooting
Common Issues
1. Game won't start

Ensure all folders (sound/, images/) are in the same directory as game.exe

Check Windows Defender/firewall isn't blocking the executable

Try running as administrator

2. Missing graphics or sound

Verify all files are present in their respective folders

Files might be blocked by Windows - right-click file → Properties → Unblock

3. Performance issues

Close other applications

Try windowed mode (Alt+Enter)

Update graphics drivers

4. Controls not working

Ensure keyboard/mouse are properly connected

Check for conflicting software (game overlays, etc.)

Try different USB ports

Error Messages
"Missing DLL": Install Microsoft Visual C++ Redistributable

"Access Denied": Run as administrator or check file permissions

"Failed to initialize": Update DirectX or graphics drivers

Security Notes
The executable is compiled Python code using PyInstaller

No malware or spyware included

No internet connection required

All data stays locally on your machine

Save Data
Game saves are stored in:

Windows: %APPDATA%\Cubanoid\ or C:\Users\[Username]\AppData\Roaming\Cubanoid\

Portable mode: saves\ folder next to executable (if enabled)

Uninstallation
Simply delete the game folder. No registry entries or system files are modified.

For Developers
Source Code
If you have the source version (main.py), you can:

Modify game mechanics

Create new levels

Add custom assets

Recompile with: pyinstaller --onefile --windowed main.py

Asset Replacement
You can replace any files in images/ or sound/ folders with your own (maintaining same names and formats).

Modding Support
Level design: Edit the level_map array in the source code

Game balance: Adjust constants like MAX_SPEED, GRAVITY, enemy health

Visuals: Replace PNG files in images/ folder

Credits
Game Engine: PyGame

Packaging: PyInstaller

Programming: [Developer Name/Team]

Assets: [Asset creators or sources]

Support
For issues with the EXE version:

Check the troubleshooting section above

Verify file structure is correct

Ensure your system meets requirements

Contact the developer if problems persist
