Basic Setup/Basic Usage of Snips on Raspberry
-

/Install an assistant:
* sam install assistant
* choose the one you want
* you'll find it located in /var/lib/snips/skills/

Testing, if assistant is running correctly
* sudo systemctl stop snips-skill-server
* snips-skill-server -vvv

=> This will show potential errors during launch of assistant, e.g. missing libraries or wrong indentations

Running the assistant and checking for runtime errors
* sam watch (will print what's going on during the execution of a snips command to the command line)

=> if it says sth like: "didn't respond in a timely manner" then there is a runtime error in your code


Checking which error occured
* sam service log snips-skill-server (will show you what happened during execution of your program)
* sudo tail -f /var/log/syslog (more or less the same, just on system level)
