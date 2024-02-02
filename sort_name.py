from glob import glob
from pathlib import Path
from library import s_get_synonym_separator, s_get_nonsynonym_separator, s_get_writing_system_for_ideograph, s_get_principal_locale, ls_get_separator_for_principal_locale


s_principal_locale = s_get_principal_locale()

top_path = Path.cwd()

for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	s_writing_system = s_principal_locale.split('-')[1]

	s_principal_locale_synonym_separator = ls_get_separator_for_principal_locale()
	if s_file_path[s_file_path.rfind('/')+1:].count(s_principal_locale_synonym_separator) == 0:
		continue
	ls_line = Path(s_file_path).read_text().splitlines()
	s_header = ls_line.pop(0)

	if s_file_path.endswith('_.tsv'):
		if not s_principal_locale_synonym_separator[0] in s_file_path[s_file_path.rfind('/')+1:]:
			continue
		for i_line_index in range(len(ls_line)):
			s_locale, s_subject = ls_line[i_line_index].split('\t')
			s_language, s_writing_system, s_region = s_locale.split('-')
			s_subject_separator = s_get_synonym_separator(s_locale, ls_line[i_line_index])

		s_phonetic_writing_system_for_ideograph = s_get_phonetic_writing_system_for_ideograph(s_locale)
		if s_phonetic_writing_system_for_ideograph == '':
			ls_subject = s_subject.split(s_subject_separator)
			ls_subject.sort()
			ls_line[i_line_index] = '\t'.join([s_locale, s_subject])
			