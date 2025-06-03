# keyboardMouseActivity
Track keyboard and mouse activity in real time using aw-watcher-input in Activity Watch.

- keyboardMouseActivity0.py and keyboardMouseActivity2.py weren't outputting what I intended so I attempted to correct them in a 'hacky' kind of way in keyboardMouseActivity1.py and keyboardMouseActivity3.py respectively and they work better but I'm guessing not the direction I want to go in the long run.
- keyboardMouseActivity0.py is a simplified first major attempt
- keyboardMouseActivity1.py is a revised (perhaps unclean) first major attempt
- keyboardMouseActivity2.py is a simplified second major attempt
- keyboardMouseActivity3.py is a revised (perhaps unclean) second major attempt

- I created a simple script, wcOutput, to count character differences between test files before and after testing each program. The test files are all the same before testing each program. But I also had to manually count keystrokes to navigate the test files and add this to the character count output of the script after testing each program since these aren't counted by the script. I then compare this data to the output of the program running. Each test file is edited by me for the length of the interval while the program is running. I used a timer set to 2 or 3 mins. depending on how many test files and my original thoughts were to use the file called test for small amounts of typing, test2 for typing at a simulated coding speed, and test3 for typing sentences continuously.
