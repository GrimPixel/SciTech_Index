from glob import glob
from pathlib import Path
from library import s_get_nonsynonym_separator, s_get_principal_locale


s_export_directory = 'Markdown'

s_principal_locale = s_get_principal_locale()

top_path = Path.cwd()
top_path.joinpath(s_export_directory).mkdir(exist_ok=True)
for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	ls_line = Path(s_file_path).read_text().splitlines()
	s_header = '|' + ls_line.pop(0).replace('\t', '|') + '|\n|' + '-|'*(ls_line[0].count('\t')+1) + '\n'

	s_text = s_header
	if s_file_path.endswith('_.tsv'):
		for s_line in ls_line:
			s_text += '|' + s_line.replace('\t', '|') + '|\n'
	else:
		for s_line in ls_line:
			s_locale, s_concept, s_prerequisite = s_line.split('\t')
			if s_locale != s_principal_locale or s_prerequisite == '':
				s_text += '|' + s_line.replace('\t', '|') + '|\n'
				continue

			s_nonsynonym_separator = s_get_nonsynonym_separator(s_locale, s_line)
			ls_prerequisite = s_prerequisite.split(s_nonsynonym_separator)
			for i_prerequisite_index in range(len(ls_prerequisite)):
				ls_prerequisite[i_prerequisite_index] = '[[' + ls_prerequisite[i_prerequisite_index] + ']]'
			s_prerequisite_with_bracket = s_nonsynonym_separator.join(ls_prerequisite)
			s_text += '|' + s_line[:s_line.rfind('\t')].replace('\t', '|') + '|' + s_prerequisite_with_bracket + '|\n'

	s_export_subdirectory = top_path.joinpath(s_export_directory + s_file_path.removeprefix(str(top_path)).removesuffix(s_file_path[s_file_path.rfind('/'):]))
	Path(s_export_subdirectory).mkdir(parents=True, exist_ok=True)
	export_file_path = top_path.joinpath(s_export_directory + s_file_path.removeprefix(str(top_path)).removesuffix('.tsv') + '.md')
	export_file_path.write_text(s_text)
