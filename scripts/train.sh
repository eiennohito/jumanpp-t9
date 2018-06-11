#!/usr/bin/env bash

JUMANPP_TOOL="$1"
SEED_MODEL="$2"
CORPUS="$3"
OUTPUT_MODEL="$4"

NTHREADS="${NTHREADS:-4}"
EPOCHS="${EPOCHS:-10}"
ITERS="${ITERS:-5}"
MODEL_SIZE="${MODEL_SIZE:-22}"
LOC_BEAM="${LOC_BEAM:-4}"

set -x

"$JUMANPP_TOOL" train \
    --model-input="$SEED_MODEL" \
    --model-output="$OUTPUT_MODEL" \
    --corpus="$CORPUS" \
    --csv-corpus-format \
    --size="$MODEL_SIZE" \
    --beam="$LOC_BEAM" \
    --threads="${NTHREADS}" \
    --max-batch-iters="$ITERS" --max-epochs="$EPOCHS" --epsilon=1e-7 \
    --batch="100000" \
    --gb-left-min=4 --gb-left-max=4 \
    --gb-right-min=4 --gb-right-max=4 \
    --gb-rcheck-min=1 --gb-rcheck-max=1 \
    --gb-first-full
