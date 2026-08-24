# Pokemon Stats dumper and importer (Unfinished!)

This is all coded and ready. It imports correctly and can dump the imported stats as well correctly.

It does not work properly as intended. Project64 enters a fatal infinite loop and throws an error message, and closes.

I suspect there's some kind of checksum or checker:

1) Checks to see if the stats match another addresses' values (directly with values) (I found that some pokemon don't have duplicate stats in hexadecimal.)

2) Uses a checksum or anti-modification code that checks the stats against a checksum hash.

We need to disable the checksum checker or anti-modification code by either bypassing it or setting it to true/false to bypass the check.

## Order of usage:

1. Rename your rom "baserom.z64". Convert to z64 with a tool if not z64 and make it Big Endian format with another tool.

2. Place the baserom.z64 into the sibling folder "Rom_Folder".

3. Open command prompt.

4. cd into your downloaded github repository.

5. cd into "Pokemon Stat Editing Tools"

6. run python dump_master_table.py first.

7. run python dump_pokemon_stats_to_text_file.py

8. Edit your pokemon in the dumped text file located in the sibling folder "Editing". It will be called "pokemon_stadium_2_stat_sheet.txt"

9. Run python pokemon_stats_importer.py

10. Open your favorite emulator and run the modified rom file ("baserom_modified.z64")