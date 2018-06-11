# A Juman++ Analysis Spec for T9 (without spaces)

# Dictionary fields
field 1 surface string trie_index
field 2 english string
# we share string storage of english and lemma fields
field 3 lemma string storage english
field 4 ud_pos string
field 5 ptb_pos1 string
field 6 ptb_pos2 string
field 7 ptb_pos3 string

# unk word handler: a basic one which will assign X to output
unk any_char template row 1: single family_anything surface to [english,lemma]

# analysis features

# unigrams
ngram [english]
ngram [lemma]
ngram [ud_pos]
ngram [ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ud_pos, ptb_pos2, ptb_pos3]
ngram [surface, english]
ngram [english, ud_pos, ptb_pos3]

# bigrams
ngram [english][english]
ngram [lemma][lemma]
ngram [ud_pos][ud_pos]
ngram [ptb_pos1][ptb_pos1]
ngram [ptb_pos1][ptb_pos1, ptb_pos2]
ngram [ptb_pos1][ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ptb_pos1][ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ptb_pos1, ptb_pos2][ptb_pos1]
ngram [ptb_pos1, ptb_pos2][ptb_pos1, ptb_pos2]
ngram [ptb_pos1, ptb_pos2][ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ptb_pos1, ptb_pos2][ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ptb_pos1]
ngram [ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ptb_pos1, ptb_pos2]
ngram [ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]

ngram [english, ud_pos][english, ud_pos]
ngram [english, ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][english, ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]

# trigrams
ngram [english][english][english]
ngram [english, ud_pos][english, ud_pos][english, ud_pos]
ngram [english, ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][english, ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][english, ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]
ngram [ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ud_pos, ptb_pos1, ptb_pos2, ptb_pos3][ud_pos, ptb_pos1, ptb_pos2, ptb_pos3]

# train loss
train loss
    surface 1,
    english 1,
    lemma 1,
    ud_pos 1,
    ptb_pos1 1,
    ptb_pos2 1,
    ptb_pos3 1
