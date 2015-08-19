import os
import re
import csv


def convert_tags(s, source="C7", target="Penn", delim="_", new_delim="_", csv_path=None):
	"""
	Converts a string with C7 POS tags into one with Penn or Google tags or one in Penn to Google.
	A new delimiter  can be set as well. The conversion table is a reasonable, but incomplete & WIP.
	In case of missing values, the original tag is retained.
	"""
	if csv_path is None:
		csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conversion.csv")
	try:
		with open(csv_path, "r") as handler:
			reader = csv.DictReader(handler, dialect="excel-tab")
			tag_dict = {}
			for r in reader:
				if source == "C7":
					tag_dict[r["C7"]] = {"Penn": r["Penn"], "Google": r["Google"]}
				if source == "Penn":
					tag_dict[r["Penn"]] = {"Google": r["Google"]}
			tags_re = re.compile(r"{}[A-Z0-9]+".format(delim))
			tags = tags_re.findall(s)
			tags = list(set(tags))
			# sorted by size (long to short) so that _NN1 is not matched while replacing _NN 
			tags.sort(key = len, reverse=True)
			for tag in tags:
				key = tag.replace(delim, "")
				try:
					new_tag = "{}{}".format(new_delim, tag_dict[key][target])
					if len(new_tag) == len(new_delim):
						new_tag ="{}{}".format(new_tag, key)
				except KeyError:
					print("Could not find a conversion entry for", key, "from",source," to ",target)
				else:
					s = s.replace(tag, new_tag)
			return s
	except FileNotFoundError:
		print("File not found:", csv_path)
		return None

def run_demo():
	vog_C7 = "Oh_UH freddled_JJ gruntbuggly_RR thy_APPGE micturations_NN2 are_VBR to_II me_PPIO1 \
		 	  As_RG plurdled_JJ gabbleblotchits_NN2 on_II a_AT1 lurgid_JJ bee_NN1 ._."
	vog_Penn = convert_tags(vog_C7, source="C7", target="Penn")
	vog_Google = convert_tags(vog_C7, source="C7", target="Google")
	vog_Penn_Google = convert_tags(vog_Penn, source="Penn", target="Google")
	# conversion vom Penn to C7 not possible, returns unmodified string
	vog_Penn_C7 = convert_tags(vog_Penn, source="Penn", target="C7") 
	print(vog_C7)
	print(vog_Penn)
	print(vog_Google)
	print(vog_Penn_Google)
	print(vog_Penn_C7)  
if __name__ == "__main__":
	run_demo()