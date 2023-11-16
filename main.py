# Note: I took many snippets of code off of StackOverflow, so... thanks. (And github copilot)
# PSA: This code is terrible (also unreadable), and probably the least efficient way to do this. But it gets the job done, which is the only thing I care about. (And the fact that I wrote it)

from bs4 import BeautifulSoup, SoupStrainer, Tag
import cchardet
import json


def get_key(val):
    for key, value in concepts.items():
        if val == value:
            return key

    return "key doesn't exist"


def is_cjk(character):
    """"
    Checks whether character is CJK.

        >>> is_cjk(u'\u33fe')
        True
        >>> is_cjk(u'\uFE5F')
        False

    :param character: The character that needs to be checked.
    :type character: char
    :return: bool
    """
    return any([start <= ord(character) <= end for start, end in
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
                 (63744, 64255), (65072, 65103), (65381, 65500),
                 (131072, 196607)]
                ])

def check_text(sib: Tag):
    for char in sib.text.strip():
        if is_cjk(char):
            return True
    return False

def check_text_examples(sib: Tag):
    for char in sib.text.strip():
        if is_cjk(char):
            return True
    return False

with open ("djtguide.github.io/grammar/masterreference.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, 'lxml')

concepts = {}

for td in soup.find_all("td"):
    if td.a:
        if "https" in td.a.get('href'):
            concepts[td.text.strip()] = td.a.get('href').strip()
            continue
        concepts[td.text.strip()] = td.a.get('href').strip()

explanations = []

for element in concepts:
    if "https" in concepts[element]:
        explanations.append(None)
        continue
    if "#" in concepts[element]:
        with open("djtguide.github.io/grammar/" + concepts[element].split("#")[0], encoding="utf8") as fp:
            soup = BeautifulSoup(fp, 'lxml')
            
            for h2 in soup.find_all("h2", {"class": "donnaconcept"}):
                next_sibling = h2.find_next_sibling("p")
                if h2.text.strip() == element:
                    if next_sibling is not None:
                        if "➡" in next_sibling.text.strip():
                            explanations.append({next_sibling.a.text.strip(): "https://djtguide.github.io/grammar/donnatoki/" + next_sibling.a.get('href')})
                            break

                        if check_text(next_sibling) is False:
                            explanations.append(next_sibling.text.strip())
                            break
                        else:
                            explanations.append(next_sibling.find_next_sibling().text.strip())
                            break
                    else:
                        explanations.append(None)
                        break

        continue
    with open("djtguide.github.io/grammar/" + concepts[element], encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'lxml')

    table = soup.find("table", {"class": "dojgtab"})
    if table is not None:
        text = table.find('td').text.strip()

        if table.find('td').find_next_sibling("td") is not None:
            # add to explanations list
            explanations.append({table.find('td').find_next_sibling("td").text.strip(): table.find('td').text.strip()})
        else:
            explanations.append(table.find('td').text.strip())
    else:
        explanations.append(None)

related_expressions = []

for element in concepts:
    if "https" in concepts[element]:
        related_expressions.append(None)
        continue
    if "#" in concepts[element]:
        related_expressions.append(None)
        continue
    with open("djtguide.github.io/grammar/" + concepts[element], encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'lxml')

    table = soup.find("table", {"class": "dojgtab"})
    if table is not None:
        text = table.find('td').text.strip()

        if table.find('tr').find_next_sibling("tr") is not None:
            if table.find('tr').find_next_sibling("tr").td is not None:
                related_expressions.append(table.find('tr').find_next_sibling("tr").td.text.strip())
            else:
                related_expressions.append(None)
        else:
            related_expressions.append(None)
    else:
        related_expressions.append(None)


examples = []

for element in concepts:
    if "https" in concepts[element]:
        examples.append(None)
        continue
    if "#" in concepts[element]:
        with open("djtguide.github.io/grammar/" + concepts[element].split("#")[0], encoding="utf8") as fp:
            soup = BeautifulSoup(fp, 'lxml')


            for h2 in soup.find_all("h2", {"class": "donnaconcept"}):
                next_sibling = h2.find_next_sibling("p")
                if h2.text.strip() == element:

                    if next_sibling is not None:
                        if "➡" in next_sibling.text.strip():

                            examples.append(None)
                            break

                        if check_text_examples(next_sibling) is False:
                            definitions = []
                            for p in next_sibling.find_next_sibling("div").find_all(["p", "dd"]):
                                if '\n' in p.text.strip():
                                    definitions.append(p.text.strip().partition('\n')[0])
                                    continue
                                definitions.append(p.text.strip())

                            examples.append(definitions)
                            break
                        else:
                            defs = []
                            next_next_sibling = next_sibling.find_next_sibling()
                            for p in next_next_sibling.find_next_sibling("div").find_all(["p", "dd"]):
                                if '\n' in p.text.strip():
                                    defs.append(p.text.strip().partition('\n')[0])
                                    continue
                                defs.append(p.text.strip())

                            examples.append(defs)
                            break
                    else:
                        examples.append(None)
                        break

        continue
    with open("djtguide.github.io/grammar/" + concepts[element], encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'lxml')


    h4 = soup.find("h4", string="Key Sentences")
    if h4 is None:
        examples.append(None)
        continue

    hr = h4.find_next_sibling("hr", {"class": "dotted"})

    elements = []
    for element in h4.next_elements:
        if element == hr:
            break

        if element.name == "p":
            elements.append(element.text.strip())

    examples.append(elements)

    # {Definition: Explanation}, {Definition: Explanation}, {Name: Link}
    #
    # Name: [
    #   {Definition: Explanation}, Explanation, {Name: Link} 0 X
    #   {Related Expression: [{Name: Link}, {Name: Link}]} 1 X
    #   {Example Sentences: [{Sentence: Translation}, {Sentence: Translation}, Sentence]} 2
    #   Link 3
    # ]
    #

dictionary = {}
print(len(concepts), len(explanations), len(related_expressions), len(examples))
for i in range(len(concepts)):
    link = concepts.get(list(concepts.keys())[i])
    if "https" in link:
        dictionary[get_key(link)] = [
            None,
            None,
            None,
            link,
        ]
        continue
    else:
        dictionary[get_key(link)] = [
            explanations[i],
            related_expressions[i],
            examples[i],
            "https://djtguide.github.io/grammar/" + link,
        ]

json_object = json.dumps(dictionary, ensure_ascii=False, indent=4)

with open("grammardict.json", "w", encoding="utf8") as fp:
    fp.write(json_object)
