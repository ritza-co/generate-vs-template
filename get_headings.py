import requests
import re
import urllib.parse
import json

import time
import random
from collections import defaultdict
import string

def get_auto_suggestions(searchterm):
    autocomplete_url = "http://suggestqueries.google.com/complete/search?&output=toolbar&gl=us&hl=en&q="
    enc = urllib.parse.quote(searchterm)
    autocomplete_url += searchterm
    xml_response = requests.get(autocomplete_url).text
    suggestion_search = re.findall(r'data="(.+?)"', xml_response)
    suggestions = []
    for match in suggestion_search:
        suggestions.append(match)
    return suggestions

def clean_suggestions(suggestions, searchterm):
    cleaned = []
    for suggestion in suggestions:
        if len(cleaned) >= 5:
            break
        if suggestion.count("vs") > 1:
            continue
        if suggestion.count(searchterm) > 1:
            continue
        if any([x in suggestion for x in cleaned]):
            continue
        try:
            suggestion = suggestion.split(searchterm + " vs")[1]
            if suggestion:
                cleaned.append(suggestion.strip())
        except Exception as e:
            print(e)
            continue
    return cleaned


def get_top_comparisons(term):
    term = term.lower()
    headings = []
    comparisons = clean_suggestions(get_auto_suggestions(f"{term} vs "), term)
    title = ' vs. '.join(comparisons)
    title = term + ' vs. ' + title

    d = defaultdict(list)
    for comp in comparisons:
        nc = clean_suggestions(get_auto_suggestions(comp + " vs "), comp)

        for n in nc:
            if n in comparisons:
                d[comp].append(n)

    seen = set()
    for c in comparisons:
        pair = sorted([term, c])
        seen.add((pair[0], pair[1]))
        headings.append((pair[0].title(), pair[1]))

    for l1_alt in d:
        for l2_alt in d[l1_alt]:
            pair = sorted([l1_alt, l2_alt])
            t = pair[0], pair[1]
            if t in seen:
                continue
            seen.add(t)
            headings.append((t[0].title(), t[1]))
    return title, headings


def generate_doc(title, headings):
    doc_url = "https://script.google.com/macros/s/AKfycbwmlNF-9OU1-iYPzf1KWTpJJc0q01fH1FMAdLkUHtL__22vgKs/exec?title="

    doc_url += urllib.parse.quote(title)

    for i, letter in enumerate(string.ascii_lowercase[:15]):
        if i < len(headings):
            doc_url += f"&{letter}1={urllib.parse.quote(headings[i])}"
        else:
            doc_url += f"&{letter}1={urllib.parse.quote(' ')}"

    return(doc_url)