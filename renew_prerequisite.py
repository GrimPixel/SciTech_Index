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

top_path = Path.cwd()
dd_all_locale_entry_by_file_path = {}
for s_file_name in glob(f'{top_path}/**/*.tsv', recursive=True):
	if s_file_name.endswith('_.tsv'):
		continue
	ls_line = Path(s_file_name).read_text().splitlines()
	ls_line.pop(0)
	d_locale_entry = {}
	for s_line in ls_line:
		print(s_line.split('\t'))
		print(s_file_name)
		s_locale_code, s_locale_concept, s_locale_prerequisite = s_line.split('\t')
		d_locale_entry[s_locale_code] = [s_locale_concept, s_locale_prerequisite]
	dd_all_locale_entry_by_file_path[s_file_name] = d_locale_entry
print(dd_all_locale_entry_by_file_path)

'''
d_all_entry_line_by_subject = {}
lls_all_entry_line = []

for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	if s_file_path.endswith('_.tsv'):
		continue
	s_text = Path(s_file_path).read_text()
	ls_file_text_in_line = s_text.splitlines()
	s_header = ls_file_text_in_line.pop(0)

	s_file_name = s_file_path[s_file_path.rfind('/')+1:]
	for s_line in ls_file_text_in_line:
		if s_file_name in d_all_entry_line_by_subject.keys():
			d_all_entry_line_by_subject[s_file_name] += s_line
		else:
			d_all_entry_line_by_subject[s_file_name] = s_header
		d_all_entry_line_by_subject[s_file_name] +=  '\n'

for s_file_path in glob(f'{top_path}/**/*.tsv', recursive=True):
	if s_file_path.endswith('_.tsv'):
		continue

	s_text = Path(s_file_path).read_text()
	s_file_name = s_file_path[s_file_path.rfind('/')+1:]
	if s_text == d_all_entry_line_by_subject[s_file_name]:
		continue

	ls_file_text_in_line = s_text.splitlines()
	s_header = ls_file_text_in_line.pop(0)
	for s_line in ls_file_text_in_line:
		if s_writing_system in ['Arab', 'Aran']:
			if len(ls_entry) == 2:
				s_sort_item = s_subject
			else:
				s_sort_item = s_concept + s_prerequisite
			if '⁏' in s_sort_item:
				return '⁏ '
			else:
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
		else:
			return '; '
'''
