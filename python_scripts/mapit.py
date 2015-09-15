# Launches a map in the browser using an address from the command line or clipboard.

import webbrowser, sys, pyperclip
if len(sys.argv) > 1:
	# Get adress from command line.
	address = ' '.join(sys.argv[1:])
else:
	#
	address = pyperclip.paste()

# Open the address.
webbrowser.open('https://www.google.com/maps/place/' + address)
