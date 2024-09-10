import csv
import re

# Charger les correspondances depuis le fichier CSV
def load_key_mappings(file, source, result):
	key_mappings = {}
	with open(file, mode='r', newline='') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if len(row) == 2:
				key1, key2 = row
				key_mappings[key1.strip()] = key2.strip()
	print("Mappings chargés :")
	return key_mappings

# Traduire les touches en utilisant les mappings
def TradPyMgp(keys, source, result):
	file = 'translate.csv'
	key_mappings = load_key_mappings(file, source, result)

	translated_keys = []
	startKey= ""
	for key in keys:
		key = key.strip()
		if source == 'pynput_key' and result == 'Code': # source == 'Code' and result == 'pynput_key':
			# Pour les traductions directes
			translated_key = key_mappings.get(key, "Touche non trouvée")
		elif source == 'Code' and result == 'pynput_key':
			for item in keys:
				match = re.search(r"bindedkey=([A-Za-z])", key)
			if match:

				startKey = match.group(1)
				print(startKey)

			inverse_mappings = {v: k for k, v in key_mappings.items()}
			translated_key = ['','']
		# Trouve la première correspondance si plusieurs résultats
			prefix_suffix = extract_prefix(key)
			print(prefix_suffix)
			if prefix_suffix:
				prefix, suffix = prefix_suffix
				translated_key[0] = inverse_mappings.get(prefix)
				# startKey = inverse_mappings.get('bindedkey=')
				if translated_key[0] == None :
					translated_key[0]=prefix
				else :
					translated_key[0]= translated_key[0].replace('_r', '_l')
				translated_key[1] = suffix

					# try : 
					# 	translated_key[0].replace('_r','_l')
					# except :
				 # 		pass
		else:
			translated_key = "Source ou résultat non reconnu"
		
		translated_keys.append(translated_key)
		print(f'{key}: {translated_key}')
	if startKey is not None:
		return translated_keys, suffix, startKey
	else : 
		return translated_keys, suffix

def extract_prefix(key):
	# Motif regex pour trouver le préfixe 'SHIFT', 'CTRL', ou 'ALT' suivi de 'UP' ou 'DOWN'
	patternSpeChar = r'^(SHIFT|CTRL|ALT)(UP|DOWN)$'
	
	# Recherche une correspondance
	matchSpeChar = re.match(patternSpeChar, key)

	patternChar = r'^([a-z])\s+(down|up)$'
	matchChar = re.match(patternChar, key)

	patternDelay = r'^(\d+)\s(D)$'
	matchDelay = re.match(patternDelay,key)

	if matchSpeChar:
		# Retourne le préfixe et le suffixe comme un tuple
		return matchSpeChar.group(1), matchSpeChar.group(2)
	elif matchChar : 
	# Retourne None si aucune correspondance
		return matchChar.group(1), matchChar.group(2)
	elif matchDelay :
		return matchDelay.group(1), matchDelay.group(2)

	return None

# Exemple d'utilisation
# keys = ['SHIFTDOWN', 'CTRLUP', 'e down', '120 D']
# source = 'Code'
# result = 'pynput_key'
# TradPyMgp(keys, source, result)
