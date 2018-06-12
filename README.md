# What is this about

A tutorial project for using [Juman++](https://github.com/ku-nlp/jumanpp) as a general text processing tool.

This tutorial implements something like a [T9](https://en.wikipedia.org/wiki/T9_(predictive_text)) with a small variation. 
What would happen if you input everything without spaces.

## Prerequisites

* Unix-like environment
* C++14-compatible compiler
* CMake 3.1 or later
* Python 3 or later

## How to build

```bash
git clone --recursive https://github.com/eiennohito/jumanpp-t9.git
cd jumanpp-t9
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j jumanpp_tool jumanpp_t9
```

You should get a src/jumanpp_t9 binary.

# Tutorial

Let's try to use Juman++ to solve T9 without spaces.
The goal of this tutorial is to demonstrate how to make morphological analyzers using Juman++.

## Introduction: What was T9

T9 was popular before the smartphones have came and everyone started to use QWERTY on their touch screens.
However, dumbphones did not have a touchscreen.
Instead they had only had 4x3 keyboard like this one (picture credit to Wikipedia).

![Phone Keyboard](https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Telephone-keypad2.svg/200px-Telephone-keypad2.svg.png)

T9 had a great idea: what if we will press the keys for each letter only once and 
select matching words by using the context.
For example, a to input "hello" you would type "43556".
0 was used for spaces and 1 for punctuation.

But if you provide spaces it is relatively easy to guess the correct word. 
But how would we do if there were no spaces.
For example, the previous sentence would be inputted as: 28846996853933643843739373667722371.
In this case, we would need to segment digits into "words" and select words corresponding to those digits simultaniously.

This is what morphological analyzers for languages with continuous scripts (like Japanese or Chinese) have to do.
They segment continuous text into tokens (morphemes) and tag them with additional information like lemmas (base forms)
and parts of speech.

Juman++ is a modern morphological analyzer for continuous languages.
And we will try to use it to solve T9 without spaces. 

## Juman++ Structure 

To build an analyzer using Juman++ we would need to prepare some things, namely

1. Dictionary,
1. Analysis Spec,
1. Driver Program.

## Dictionary

The analysis dictionary defines words which our analyzer would be able to accept.
Words can define other fields, like parts of speech. 
Dictionary should be supplied in the CSV format.

Let's create a dictionary that would have at least

* 9-pad number representation
* English original spelling

Let's use [Universal Dependencies](http://universaldependencies.org/) project for creating the dictionary.
It provides annotated text corpora in many languages; and we will use the annotation information later,
for improving our model.

Let's download the UD corpora.

```bash
wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2515/ud-treebanks-v2.1.tgz
tar xf ud-treebanks-v2.1.tgz
```

Inside there will be a lot of folders starting with `UD_`.
We will use `UD_English`.
It should have these files:
```
LICENSE.txt
README.md
en-ud-dev.conllu
en-ud-dev.txt
en-ud-test.conllu
en-ud-test.txt
en-ud-train.conllu
en-ud-train.txt
stats.xml
```

Let's first make a training corpus using [conversion script](scripts/conll2minicorpus.py).
From the jumanpp-t9 root directory execute: 
```
python3 scripts/conll2minicorpus.py <path to UD dir>/UD_English/en-ud-train.conllu > build/ud_en.train.corpus
```

The file will contain lines like
```
3766,from
843,the
27,ap
26637,comes
8447,this
78679,story
1,:
EOS
```

Each line will correspond to a single word in the sentence; EOS marks the end of sentence.
Let's repeat the conversion for dev and test parts as well:
```bash
python3 scripts/conll2minicorpus.py <path to UD dir>/UD_English/en-ud-dev.conllu > build/ud_en.dev.corpus
python3 scripts/conll2minicorpus.py <path to UD dir>/UD_English/en-ud-test.conllu > build/ud_en.test.corpus
```

And now let's compile the dictionary itself using [another python script](scripts/minicorpus2minidic.py).
```bash
python3 scripts/conll2minicorpus.py build/ud_en.*.corpus > build/ud_en.dic
```

It will contains like: 
```
227623,abroad
22787859,abruptly
2273623,absence
227368,absent
227368464,absenting
22765883,absolute
```

## Analysis Spec

Analysis Spec defines the dictionary format,
features used for scoring
and the structure of the loss function.

A [minimal dictionary spec](src/jumanpp_t9_nano.spec) would be something like

```
field 1 surface string trie_index
field 2 english string

ngram [surface, english]

train loss surface 1, english 1
```


First two lines define a dictionary definition.
This spec uses only two fields, but 
the actual CSV can contain more fields, but only first two will be used.
A column #1 would be called "surface", have string type and a trie-based index
for *surface* lookup would be built over this field.
A column #2 would be called "english" and have string type.

A single unigram feature, which uses both content of surface and english fields
would be used for path scoring.
Finally, the loss would use both fields with the equal weight of 1.

The creation of a trained model is done in two steps.

1. We build a binary dictionary from a spec and dictionary csv.
1. We train model weights using a binary dictionary and corpus, producing an analysis model.

Let's do this!

```bash
cd build
./jumanpp/src/core/tool/jumanpp_tool index \
    --spec ../src/jumanpp_t9_nano.spec \
    --dict-file build/ud_en.dic \
    --output nano.seed
../scripts/train.sh ./jumanpp/src/core/tool/jumanpp_tool nano.seed build/ud_en.dev.corpus dev.nano.model
```

You can also try to train a model with `build/ud_en.train.corpus`,
but the training will use around 6GB or RAM.

## Driver Program

Finally, we need a program which will do the actual analysis.
While the training and dictionary preparation could be done
with generalized tools, 
Juman++ does not provide a generalized analysis tool
because of two reasons: output formats and statically generated feature processing code.

I have already implemented a [very simple driver program](src/jumanpp_t9.cc)
for our case.

Let's test our trained model:

```bash
# There is a tester.py script which converts English text to digits
# and forward them into the driver program itself.
python3 ../scripts/tester.py ./src/jumanpp_t9 dev.nano.model
```

Ok, let's test it!

```
this model works
84476633596757
8447	this
66335	model
96757	works

and sometimes it does not
263766384637483637668
263	and
7663	roof
84	vi
63748	merit
3637	does
668	not
```

So, our model already works for some inputs, but not for everything.
Let's improve on it.

## Improving the spec

The current model uses only a single unigram feature template,
which is obviously very naive.
Let's add some other templates so the ngram feature section will look like:

```
ngram [surface]
ngram [english]
ngram [surface, english]

ngram [surface][surface]
ngram [english][english]
ngram [surface, english][surface, english]

ngram [english][english][english]
```

Now we have three unigram, three bigram and one trigram feature templates.

Let's retrain our model with the new spec:

```bash
./jumanpp/src/core/tool/jumanpp_tool index \
    --spec ../src/jumanpp_t9_mini.spec \
    --dict-file build/ud_en.dic \
    --output mini.seed
../scripts/train.sh ./jumanpp/src/core/tool/jumanpp_tool mini.seed build/ud_en.dev.corpus dev.mini.model
```

Notice that the loss became much smaller than with the "nano" model.
"And sometimes it does not" should be restored correctly this time.