from collections import OrderedDict

# TODO: Allow this method to be run from any working directory.

file = open("include/rapidstring.h", "r+")
contents = file.read()
file.seek(0)
lines = [line for line in file]

# A dictionary of module name keys mapped to an array of line numbers.
modules = OrderedDict()

# Constants.
CENTER_MODULE_OFFSET = 3
COMMENT_OFFSET = 2
MODULE_LINES = 9
BASE_TOC_LINES = 3
TOC_LINE = " *       TABLE OF CONTENTS\n"
TOC_HEADER = "/*\n" + TOC_LINE + " *\n"

current_toc_begin = lines.index(TOC_LINE) - 1
current_toc = ""
current_toc_lines = -1
for i in range(current_toc_begin, len(lines)):
	current_toc += lines[i]

	if lines[i] == " */\n":
		current_toc += "\n"
		current_toc_lines = i - current_toc_begin + 1
		break

for i, line in enumerate(lines):
	if line == "/*\n" and lines[i + 1].startswith(" * ="):
		module_line = lines[i + CENTER_MODULE_OFFSET]
		name = module_line[COMMENT_OFFSET:].strip();
		line_number = i + MODULE_LINES

		if name in modules:
			modules[name].append(line_number)
		else:
			modules[name] = [line_number]

toc_lines = BASE_TOC_LINES + len(modules) * 2
for key, values in modules.items():
	toc_lines += len(values)

toc_diff = current_toc_lines - toc_lines
toc = TOC_HEADER
pos = 1

def toc_elem(name, val):
	return " * - " + name + ":\tline " + str(val - toc_diff) + "\n"

for key, values in modules.items():
	toc += " * " + str(pos) + ". " + key + "\n"
	toc_sub_elems = ["Declarations", "Definitions"]

	for i, val in enumerate(values):
		toc += toc_elem(toc_sub_elems[i], val)

	toc += " *\n"
	pos += 1

toc = toc[:-3]
toc += " */\n\n"

file.seek(0)
file.write(contents.replace(current_toc, toc))
file.truncate()
