from glob import glob
from pathlib import Path


s_locale_file = 'locale.txt'

ls_locale = Path(s_locale_file).read_text().splitlines()
for i_locale_index in range(len(ls_locale)):
	s_locale = ls_locale[i_locale_index]
	if s_locale.startswith(' '):
		s_principal_locale = s_locale.lstrip(' ')
		ls_locale[i_locale_index] = s_principal_locale
		break

def s_get_prerequisite_separator():
	if s_writing_system in ['Arab', 'Aran']:
		if '⁏' in s_line:
			return '⁏ '
		return '؛ '
	elif s_writing_system == 'Armn':
		return '․ '
	elif s_writing_system == 'Bamu':
		return '꛶ '
	elif s_writing_system in ['Bopo', 'Hani', 'Hans', 'Hant', 'Jpan']:
		return '；'
	elif s_writing_system == 'Grek':
		return '· '
	elif s_writing_system == 'Ethi':
		return '፤ '
	elif s_writing_system == 'Sgnw':
		return '𝪉'
	return '; '

ddls_all_entry_by_locale_by_concept = {}
top_path = Path.cwd()
for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	if s_file_path.endswith('_.tsv'):
		continue
	s_file_text = Path(s_file_path).read_text()
	ls_line = s_file_text.splitlines()
	s_header = ls_line.pop(0)
	for s_line in ls_line:
		if not s_line.startswith(s_principal_locale + '\t'):
			continue
		s_principal_locale, s_concept_in_principal_locale, s_prerequisite_in_principal_locale = s_line.split('\t')
		s_language, s_writing_system, s_region = s_locale.split('-')
		s_prerequisite_separator = s_get_prerequisite_separator()
		ls_prerequisite_in_principal_locale = s_prerequisite_in_principal_locale.split(s_prerequisite_separator)
		break
	ddls_all_entry_by_locale_by_concept[s_concept_in_principal_locale] = {}

	for s_line in ls_line:
		s_locale, s_concept, s_prerequisite = s_line.split('\t')
		s_language, s_writing_system, s_region = s_locale.split('-')
		if [s_concept, s_prerequisite] == ['', '']:
			continue
		ddls_all_entry_by_locale_by_concept[s_concept_in_principal_locale].update({s_locale: [s_concept, s_prerequisite]})

for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	if s_file_path.endswith('_.tsv'):
		continue
	s_file_text = Path(s_file_path).read_text()
	ls_line = s_file_text.splitlines()
	s_header = ls_line.pop(0)

	s_concept_in_principal_locale = s_file_path[s_file_path.rfind('/')+1:].removesuffix('.tsv')
	s_writing_system = s_principal_locale.split('-')[1]
	s_prerequisite_separator_for_principal_locale = s_get_prerequisite_separator()
	s_prerequisite_in_principal_locale = ddls_all_entry_by_locale_by_concept[s_concept_in_principal_locale][s_principal_locale][1]
	ls_prerequisite_in_principal_locale = s_prerequisite_in_principal_locale.split(s_prerequisite_separator_for_principal_locale)

	for i_line_index in range(len(ls_line)):
		s_locale, s_concept, s_prerequisite = ls_line[i_line_index].split('\t')
		if s_locale == s_principal_locale:
			continue
		if s_locale == 'zxx-Zmth-ZZ':
			ls_line[i_line_index] = '\t'.join([s_locale, s_concept, ''])
			continue
		s_writing_system = s_locale.split('-')[1]
		s_prerequisite_separator = s_get_prerequisite_separator()
		ls_prerequisite = []
		for s_prerequisite_in_principal_locale in ls_prerequisite_in_principal_locale:
			if s_prerequisite_in_principal_locale in ddls_all_entry_by_locale_by_concept.keys() and \
					s_locale in ddls_all_entry_by_locale_by_concept[s_prerequisite_in_principal_locale].keys():
				s_prerequisite = ddls_all_entry_by_locale_by_concept[s_prerequisite_in_principal_locale][s_locale][0]
				ls_prerequisite.append(s_prerequisite)
			else:
				ls_prerequisite.append('')
		ls_line[i_line_index] = '\t'.join([s_locale, s_concept, s_prerequisite_separator.join(ls_prerequisite)])
	s_header = 'locale	concept	prerequisite\n'
	if s_file_text != s_header + '\n' + '\n'.join(ls_line) + '\n':
		Path(s_file_path).write_text(s_header + '\n'.join(ls_line) + '\n')
