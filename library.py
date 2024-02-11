def ls_get_all_locale():
	return '''
arb-Arab-ZZ
cmn-Hans-CN
cmn-Latn-CN
dan-Latn-DK
deu-Latn-DE
eng-Latn-US
fin-Latn-FI
fra-Latn-FR
heb-Hebr-IL
hin-Deva-IN
ita-Latn-IT
jpn-Hrkt-JP
jpn-Jpan-JP
kor-Hang-KR
kor-Kore-KR
nld-Latn-NL
nob-Latn-NO
pes-Aran-IR
por-Latn-PT
rus-Cyrl-RU
swe-Latn-SE
spa-Latn-ES
tur-Latn-TR
zxx-Zmth-ZZ
'''.strip('\n').split('\n')

def s_get_principal_locale():
	return 'eng-Latn-US'

def ls_get_separator_for_principal_locale():
	return [', ', '; ']

def s_get_subject_header():
	return 'locale\tsubject'

def s_get_concept_header():
	return 'locale\tconcept\tprerequisite'

def s_get_content_directory():
	return 'content'

def s_get_synonym_separator(s_locale, s_text):
	s_language, s_writing_system, s_region = s_locale.split('-')
	if s_writing_system in ['Arab', 'Aran']:
		return '، '
	elif s_writing_system == 'Bamu':
		return '꛵ '
	elif s_writing_system in ['Bopo', 'Hanb', 'Hani', 'Hans', 'Hant', 'Hrkt']:
		if '，' in s_text:
			return '，'
		return '、'
	elif s_writing_system == 'Ethi':
		return '፣ '
	elif s_writing_system == 'Hmng':
		return '𖬹 '
	elif s_writing_system == 'Lisu':
		return '꓾ '
	elif s_writing_system == 'Medf':
		return '𖺗 '
	elif s_writing_system == 'Mong':
		if '᠈' in s_text:
			return '᠈ '
		return '᠂ '
	elif s_writing_system == 'Newa':
		return '𑑍 '
	elif s_writing_system == 'Nkoo':
		return '߸ '
	elif s_writing_system == 'Sgnw':
		return '𝪇 '
	elif s_writing_system == 'Tibt':
		return '༔ '
	elif s_writing_system == 'Vaii':
		return '꘍ '
	return ', '

def s_get_nonsynonym_separator(s_locale, s_text):
	s_language, s_writing_system, s_region = s_locale.split('-')
	if s_writing_system in ['Arab', 'Aran']:
		if '⁏' in s_text:
			return '⁏ '
		return '؛ '
	elif s_writing_system == 'Armn':
		return '․ '
	elif s_writing_system == 'Bamu':
		return '꛶ '
	elif s_writing_system in ['Bopo', 'Hanb', 'Hani', 'Hans', 'Hant', 'Hrkt', 'Jpan']:
		return '；'
	elif s_writing_system == 'Grek':
		return '· '
	elif s_writing_system == 'Ethi':
		return '፤ '
	elif s_writing_system == 'Sgnw':
		return '𝪉'
	return '; '

def s_get_coupled_phonetic_writing_system_for_logogram(s_locale):
	s_language, s_writing_system, s_region = s_locale.split('-')
	if s_language in ['cdo', 'cjy', 'cmn', 'cpx', 'cnp', 'csp', 'czh', 'czo', 'gan', 'hak', 'hsn', 'mnp', 'nan', 'wuu', 'yue']:
		if s_region == 'TW' and s_language == 'cmn':
			return 'Bopo'
		return 'Latn'
	elif s_language in ['ams', 'jpn', 'kzg', 'mvi', 'okn', 'tkn', 'rvn', 'ryu', 'rys', 'xug', 'yoi', 'yox']:
		return 'Hrkt'
	elif s_language in ['jje', 'kor']:
		return 'Hang'
	elif s_language == 'vie':
		return 'Latn'
	return ''

def ls_get_separated_element(s_separator, s_entry):
	if '｛' in s_entry:
		s_escapement = ['｛', '｝']
	else:
		s_escapement = ['{', '}']
	
	ls_text = s_entry.split(s_separator)
	ls_entry = []
	b_escape = False
	for s_text in ls_text:
		if b_escape:
			ls_entry[-1] += s_separator + s_text
		else:
			ls_entry.append(s_text)

		if s_escapement[0] in s_text:
			b_escape = True
		elif s_escapement[1] in s_text:
			b_escape = False
	return ls_entry
