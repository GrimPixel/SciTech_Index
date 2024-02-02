from glob import glob
from pathlib import Path
from library import s_get_principal_locale, s_get_synonym_separator, s_get_subject_header, ls_get_all_locale, ls_get_separated_item


s_principal_locale = s_get_principal_locale()
ls_all_locale = ls_get_all_locale()
s_text = s_get_subject_header() + '\n'
for s_locale in ls_all_locale:
	s_text += s_locale + '\t\n'

top_path = Path.cwd()
for s_directory_path in glob(f'{top_path}/**/*/', recursive=True):
	if '__pycache__' in s_directory_path:
		continue
	s_subject = s_directory_path[s_directory_path.rstrip('/').rfind('/')+1:].rstrip('/')
	s_synonym_separator = s_get_synonym_separator(s_principal_locale, s_subject)

	if s_synonym_separator in s_subject:
		ls_subject = ls_get_separated_item(s_synonym_separator, s_subject)
		for i_subject_index in range(len(ls_subject)):
			ls_subject[i_subject_index] = '_' + ls_subject[i_subject_index] + '_'
		s_subject = s_synonym_separator.join(ls_subject)
	else:
		s_subject = '_' + s_subject + '_'

	s_file_name = s_subject + '.tsv'
	file_path = Path(s_directory_path).joinpath(s_file_name)
	if not file_path.is_file():
		print(file_path)
		file_path.write_text(s_text.replace(s_principal_locale + '\t', s_principal_locale + '\t' + s_subject, 1))
