# Pokemon Stadium 2 Modding Tool

## Introduction

This tool is a python-based modding tool for Pokemon Stadium 2

Pokemon Stadium 2 must be uncompressed and in Big Endian Format, as well as the USA version, to use this file.

All the offsets have been calculated for your convenience.

## Features

Currently support features:

Rental Pass Editing.

Version 1.1.1

## Known Bugs and Issues

None currently

## Installation

### Prerequisites

A Pokemon Stadium 2 rom file, named baserom.z64 (n64 or any other 64 rom file will not work!). This rom file must be in big endian format and uncompressed.

Python 3.14 or above (for running python in command prompt).

A text editor.

Your imagination.

### Install

Make sure you have Python 3.14 first.

Download the zip file of the github repo, and extract it anywhere on your system.

Copy your rom file to this folder. Rename it to baserom.n64 if needed (if it's not an n64 file, renaming isn't enough, you need to convert it with a proper converter!)

## How to use

Open command prompt.

```cd /d``` into your directory where you downloaded or placed the extracted zip file.

```cd``` into ```"Rental Editing Tools"```

### Rental Pokemon Editing

The following terminal code will dump the rental roster to a text file for convenient editing.

#### Dumping the Text Files 

To extract the following rental battle formats:

for Little Cup, type ```python little_cup_dump_to_text_file```. It will output the text file little_cup_rental_pokemon.txt in the same folder.

for Poke Cup, type ```python poke_cup_dump_to_text_file```. It will output the text file poke_cup_rental_pokemon.txt in the same folder.

for Prime Cup, type ```python prime_cup_dump_to_text_file```. It will output the text file prime_cup_rental_pokemon.txt in the same folder.

#### Editing the Rental Pokemon Text Files

The Rental Pokemon must be typed in readable format.

For example, ```Pikachu``` will be typed exactly as is: ```Pikachu```.

Mr. Mime will be typed exactly as is: ```Mr. Mime```

Farfetch'd will be typed exactly as is: ```Farfetch'd```

The only exceptions are the Nidorans, which will be typed as: ```Nidoran Male``` and ```Nidoran Female```

For moves, type exactly as is:

For example, Hyper Beam will be typed as is: ```Hyper Beam```

Double-Edge will be typed as is: ```Double-Edge```

Happiness ranges from 0 to 255

Stat Exps range from 0 to 65535

DVs range from 0 to 15

#### Importing back to the game.

To import rental pokemon text files back into the game, use the following code:

for Little Cup, type ```python little_cup_import_to_game```

for Poke Cup, type ```python poke_cup_import_to_game```

for Prime Cup, type ```python prime_cup_import_to_game```

This will import the edited file back into the game.

It will create a new file called baserom_modified.z64. This has your edits.

NOTE: You do not need to recompile or fix checksums if your playing/testing on emulator.

#### Importing another file on top of your edit

By default, this program will keep importing baserom.z64 to create baserom_modified.z64.


Go into the Rental Editing Tools folder.

To add more changed to the modified rom, change this line in the python scripts (```little_cup_import_to_game```, ```poke_cup_import_to_game```, and ```prime_cup_import_to_game```):

```        if f.lower() == 'baserom.z64':```

to

```        if f.lower() == 'modified_baserom.z64':```

This will retain your mods and add a new change to the already modded game.


#### Dumping a text file from your modified rom as an editable document.


By default, this program will only dump a text file from the original rom (baserom.z64)

To dump a file from a modified rom (like baserom_modified.z64), you'll need to change a parameter in the python script.

Go into the Rental Editing Tools folder.

In the desired ```dump_to_text_file.py``` python scripts (```little_cup_dump_to_text_file.py```, ```poke_cup_dump_to_text_file.py```, or ```prime_cup_dump_to_text_file.py```), replace:

```        if f.lower() == 'baserom.z64':```

with

```        if f.lower() == 'modified_baserom.z64':```

#### Reverting changes.

To revert all changes (in case you messed up), just delete your baserom_modified.z64 and append back on to of the baserom.z64

If you changed the included python scripts to match your new modified rom, and need to use the original rom, replace in the ```_cup_dump_to_text_file.py``` python scripts (```little_cup_dump_to_text_file.py```, ```poke_cup_dump_to_text_file.py```, or ```prime_cup_dump_to_text_file.py```) and ```_cup_import_to_game```python scripts (```little_cup_import_to_game```, ```poke_cup_import_to_game```, and ```prime_cup_import_to_game```):

```        if f.lower() == 'modified_baserom.z64':```

with

```        if f.lower() == 'baserom.z64':```