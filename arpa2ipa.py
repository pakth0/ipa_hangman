_MAP_ARPA_IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ","AW": "aʊ",
                "AX": "ə", "AXR": "ɚ", "AY": "aɪ", "EH": "ɛ", "ER": "ɝ",
                "EY": "eɪ", "IH": "ɪ", "IX": "ɨ", "IY": "i", "OW": "oʊ",
                "OY": "ɔɪ", "UH": "ʊ", "UW": "u", "UX": "ʉ", "B": "b",
                "CH": "tʃ", "D": "d", "DH": "ð", "DX": "ɾ", "EL": "l̩",
                "EM": "m̩", "EN": "n̩", "F": "f", "G": "ɡ", "HH": "h",
                "H": "h", "JH": "dʒ", "K": "k", "L": "l", "M": "m",
                "N": "n", "NG": "ŋ", "NX": "ɾ̃", "P": "p", "Q": "ʔ",
                "R": "ɹ", "S": "s", "SH": "ʃ", "T": "t", "TH": "θ",
                "V": "v", "W": "w", "WH": "ʍ", "Y": "j", "Z": "z",
                "ZH": "ʒ"}

_MAP_ARPA_AUX = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "-": "-",   "!": "!", "+": "+",
    "/": "/",   "#": "#", ":": ":"}

def arpa2ipa(tag, mapping=_MAP_ARPA_IPA, aux_map=_MAP_ARPA_AUX):
  """
  function definition:
  --> takes an Arpabet tag and maps into IPA
  stress is shown as a superscript

  >>> arpa2ipa("AA", _MAP_ARPA_IPA, _MAP_ARPA_AUX)
  "ɑ"
  >>> arpa2ipa("IY0", _MAP_ARPA_IPA, _MAP_ARPA_AUX)
  "i⁰"
  """
  if tag[-1] in aux_map:
    assert tag[:-1] in mapping, f"Unexpected arpabet: {tag[:-1]}"
    return mapping[tag[:-1]] + aux_map[tag[-1]]
  else:
    assert tag in mapping, f"Unexpected arpabet: {tag}"
    return mapping[tag]