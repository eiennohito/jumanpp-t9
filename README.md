# What is this about

A tutorial project for using [Juman++](https://github.com/ku-nlp/jumanpp) as a general text processing tool.

This tutorial implements a variation of [T9](https://en.wikipedia.org/wiki/T9_(predictive_text)) with a small variation. 
What would happen if you input everything without spaces.

# How to build

```bash
git clone  --recursive https://github.com/eiennohito/jumanpp-t9.git
cd jumanpp-t9
mkdir build
cd build
cmake ..
make -j
```

You should get a src/jumanpp_t9 binary.