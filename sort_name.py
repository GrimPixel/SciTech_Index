from glob import glob
from pathlib import Path
from library import s_get_content_directory, s_get_synonym_separator, s_get_nonsynonym_separator, s_get_coupled_phonetic_writing_system_for_logogram, s_get_principal_locale, ls_get_separated_element, ls_get_separator_for_principal_locale


s_principal_locale = s_get_principal_locale()
ls_separator_for_principal_locale = ls_get_separator_for_principal_locale()

top_path = Path.cwd()
content_path = top_path.joinpath(s_get_content_directory())

def ds_get_entry_with_element_sorted(b_is_synonym, ds_element_by_locale):
	ls_coupled_phonetic_locale = []
	for s_locale, s_element in ds_element_by_locale.items():
		s_language, s_writing_system, s_region = s_locale.split('-')
		if b_is_synonym:
			s_element_separator = s_get_synonym_separator(s_locale, s_element)
		else:
			s_element_separator = s_get_nonsynonym_separator(s_locale, s_element)
		s_coupled_phonetic_writing_system = s_get_coupled_phonetic_writing_system_for_logogram(s_locale)

		if s_coupled_phonetic_writing_system == '':
			ls_element = ls_get_separated_element(s_element_separator, s_element)
			ls_element.sort()
			ds_element_by_locale.update({s_locale: s_element_separator.join(ls_element)})
			continue
		elif s_coupled_phonetic_writing_system == s_writing_system:
			continue

		s_coupled_phonetic_locale = '-'.join([s_language, s_coupled_phonetic_writing_system, s_region])
		s_coupled_phonetic_element = ds_element_by_locale[s_coupled_phonetic_locale]
		if b_is_synonym:
			s_coupled_phonetic_element_separator = s_get_synonym_separator(s_coupled_phonetic_locale, s_coupled_phonetic_element)
		else:
			s_coupled_phonetic_element_separator = s_get_nonsynonym_separator(s_coupled_phonetic_locale, s_coupled_phonetic_element)

		lls_combined_element = []
		ls_element = ls_get_separated_element(s_element_separator, s_element)
		ls_coupled_phonetic_element = ls_get_separated_element(s_coupled_phonetic_element_separator, s_coupled_phonetic_element)
		for i_element_index in range(len(ls_element)):
			lls_combined_element.append([ls_coupled_phonetic_element[i_element_index], ls_element[i_element_index]])
		lls_combined_element.sort()
		lls_combined_element_for_dictionary = []
		ls_element = []
		for ls_combined_element in lls_combined_element:
			ls_element.append(ls_combined_element[1])
		ds_element_by_locale.update({s_locale: s_element_separator.join(ls_element)})
		ls_coupled_phonetic_locale.append(s_coupled_phonetic_locale)

	if ls_coupled_phonetic_locale != []:
		for s_coupled_phonetic_locale in ls_coupled_phonetic_locale:
			if b_is_synonym:
				s_coupled_phonetic_element_separator = s_get_synonym_separator(s_coupled_phonetic_locale, ls_coupled_phonetic_element)
			else:
				s_coupled_phonetic_element_separator = s_get_nonsynonym_separator(s_coupled_phonetic_locale, ls_coupled_phonetic_element)
			ls_coupled_phonetic_element = ds_element_by_locale[s_coupled_phonetic_locale].split(s_coupled_phonetic_element_separator)
			ls_coupled_phonetic_element.sort()

			s_sorted_coupled_phonetic_element = s_coupled_phonetic_element_separator.join(ls_coupled_phonetic_element)
			ds_element_by_locale.update({s_coupled_phonetic_locale: s_sorted_coupled_phonetic_element})
	return ds_element_by_locale

for s_file_path in glob(f'{content_path}/**/*.tsv', recursive=True):
	s_text = Path(s_file_path).read_text().rstrip('\n')
	ls_line = s_text.splitlines()
	s_header = ls_line.pop(0)
	s_sorted_text = s_header + '\n'

	if s_file_path.endswith('_.tsv'):
		ds_subject_by_locale = {}
		if not ls_separator_for_principal_locale[0] in s_file_path[s_file_path.rfind('/')+1:]:
			continue
		for i_line_index in range(len(ls_line)):
			s_locale, s_subject = ls_line[i_line_index].split('\t')
			ds_subject_by_locale.update({s_locale: s_subject})
		ds_subject_by_locale = ds_get_entry_with_element_sorted(True, ds_subject_by_locale)
		for s_locale, s_subject in ds_subject_by_locale.items():
			s_sorted_text += '\t'.join([s_locale, s_subject]) + '\n'
	else:
		ds_concept_by_locale = {}
		ds_prerequisite_by_locale = {}
		for i_line_index in range(len(ls_line)):
			s_locale, s_concept, s_prerequisite = ls_line[i_line_index].split('\t')
			ds_concept_by_locale.update({s_locale: s_concept})
			ds_prerequisite_by_locale.update({s_locale: s_prerequisite})
		ds_concept_by_locale = ds_get_entry_with_element_sorted(True, ds_concept_by_locale)
		ds_prerequisite_by_locale = ds_get_entry_with_element_sorted(False, ds_prerequisite_by_locale)
		for s_locale in ds_concept_by_locale.keys():
			s_sorted_text += s_locale + '\t' + ds_concept_by_locale[s_locale] + '\t' + ds_prerequisite_by_locale[s_locale] + '\n'

	if Path(s_file_path).read_text() != s_sorted_text:
		Path(s_file_path).write_text(s_sorted_text)
 