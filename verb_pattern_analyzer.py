import spacy
import nltk
from nltk.corpus import wordnet

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def analyze_paragraph(paragraph):
    # Process the paragraph with spaCy
    doc = nlp(paragraph)
    
    results = []
    
    for sent in doc.sents:
        for i, token in enumerate(sent):
            if token.pos_ == "VERB":
                pattern, preposition = identify_verb_pattern(sent[i:])
                if pattern:
                    results.append({
                        "pattern": pattern,
                        "preposition": preposition,
                        "meaning": "Meaning not provided in this version."
                    })
    
    # Format the results
    formatted_results = []
    for result in results:
        formatted_results.append(f"-> verb pattern: {result['pattern']}\n   -> preposition: {result['preposition']}\n   -> Meaning: {result['meaning']}")
    
    return f"Paragraph: {paragraph}\n\n" + "\n\n".join(formatted_results)

def identify_verb_pattern(tokens):
    verb = tokens[0].lemma_
    pattern = f"to {verb}"
    preposition = "N/A"
    
    for token in tokens[1:4]:  # Look at up to 3 tokens after the verb
        if token.pos_ == "ADP":  # Check if the token is a preposition
            pattern += f" {token.text}"
            preposition = token.text
            break
        elif token.pos_ in ["PART", "ADV"]:  # Include particles and adverbs (for phrasal verbs)
            pattern += f" {token.text}"
        else:
            break  # Stop if we encounter any other part of speech
    
    return pattern, preposition

def get_verb_meaning(pattern):
    # Remove "to " from the beginning of the pattern
    verb = pattern[3:]
    
    # Try to get the meaning from WordNet
    synsets = wordnet.synsets(verb, pos=wordnet.VERB)
    if synsets:
        return synsets[0].definition()
    else:
        return "Meaning not found in the dictionary."
