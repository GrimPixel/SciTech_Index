from glob import glob
from pathlib import Path
from library import s_get_content_directory


lls_all_nonempty_line = []
top_path = Path.cwd()
content_path = top_path.joinpath(s_get_content_directory())
for s_file_path in glob(f'{content_path}/**/*.tsv', recursive=True):
	ls_line = Path(s_file_path).read_text().splitlines()
	ls_line.pop(0)
	for s_line in ls_line:
		if s_file_path.endswith('_.tsv'):
			if s_line.endswith('\t'*2):
				continue
		else:
			if s_line.endswith('\t'*3):
				continue
		if s_line.startswith('zxx-Zmth-ZZ'):
			continue
		lls_all_nonempty_line.append([s_line, s_file_path])

lls_all_nonempty_line.sort()
s_element = lls_all_nonempty_line[0][0].split('\t')[1]
for i_entry_index in range(len(lls_all_nonempty_line)-1):
	s_next_element = lls_all_nonempty_line[i_entry_index+1][0].split('\t')[1]

	if s_element != '' and s_element == s_next_element:
		print(lls_all_nonempty_line[i_entry_index][0])
		print(lls_all_nonempty_line[i_entry_index][1])
		print(lls_all_nonempty_line[i_entry_index+1][1])
		print()
	s_element = s_next_element
