from glob import glob
from pathlib import Path
from library import s_get_principal_locale, ls_get_all_locale

s_principal_locale = s_get_principal_locale()
ls_all_locale = ls_get_all_locale()

top_path = Path.cwd()
for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	ls_line = Path(s_file_path).read_text().splitlines()
	s_header = ls_line.pop(0)

	ls_updated_entry = []
	for s_locale in ls_all_locale:
		for s_line in ls_line:
			if s_locale == s_line[:s_line.find('\t')]:
				ls_updated_entry.append(s_line)
				break
		else:
			ls_updated_entry.append(s_locale + '\t'*s_header.count('\t'))
	ls_updated_entry.sort()

	s_updated_text = s_header + '\n'
	for s_entry_line in ls_updated_entry:
		s_updated_text += s_entry_line + '\n'

	if s_updated_text != Path(s_file_path).read_text():
		Path(s_file_path).write_text(s_updated_text)
