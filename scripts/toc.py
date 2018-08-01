from collections import OrderedDict

# TODO: Allow this method to be run from any working directory.
# TODO: Don't require this to be ran twice if a section is removed.

file = open('include/rapidstring.h', 'r+')
contents = file.read()
lines = [line for line in file]

# A dictionary of module name keys mapped to an array of line numbers.
modules = OrderedDict()

# Constants.
CENTER_MODULE_OFFSET = 3
COMMENT_OFFSET = 2
MODULE_LINES = 9
TOC_HEADER = "/*\n *       TABLE OF CONTENTS\n *\n"

for i, line in enumerate(lines):
	if line.startswith('/*') and lines[i + 1].startswith(' * ='):
		module_line = lines[i + CENTER_MODULE_OFFSET]
		name = module_line[COMMENT_OFFSET:].strip();
		line_number = i + MODULE_LINES

		if name in modules:
			module[name].append(line_number)
		else:
			module[name] = [line_number]

toc = TOC_HEADER
pos = 1

for key, values in elems.items():
	toc += ' * ' + str(pos) + '. ' + key + '\n'
	toc_sub_elems = ['Declarations', 'Definitions']
	for i, val in values:
		toc += ' * - ' + toc_sub_elems[i] + ':\t' + str(val) + '\n'

	toc += ' *\n'
	pos += 1

toc = toc[:-3]
toc += " */\n\n"

file.seek(contents.find(TOC_HEADER))
file.write(toc)
