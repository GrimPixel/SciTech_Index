from glob import glob
from pathlib import Path
from library import s_get_content_directory


ls_file_path_with_mismatching_field = []
top_path = Path.cwd()
content_path = top_path.joinpath(s_get_content_directory())
for s_file_path in glob(f'{content_path}/**/*.tsv', recursive=True):
	ls_line = Path(s_file_path).read_text().splitlines()
	ls_line.pop(0)
	for s_line in ls_line:
		if s_line == '' or s_file_path in ls_file_path_with_mismatching_field:
			continue
		if s_file_path.endswith('_.tsv'):
			if s_line.count('\t') != 1:
				ls_file_path_with_mismatching_field.append(s_file_path)
		else:
			if s_line.count('\t') != 2:
				ls_file_path_with_mismatching_field.append(s_file_path)

if ls_file_path_with_mismatching_field != []:
	for s_file_path_with_mismatching_field in ls_file_path_with_mismatching_field:
		print(s_file_path_with_mismatching_field)
