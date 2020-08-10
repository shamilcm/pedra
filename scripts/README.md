## Scripts to Process Datasets

### Training

Training datasets were preprocessed using `preprocess_train.py` scripts to split lines as `<br>` tags, remove other HTML tags, music symbols, and leading hyphens to resemble normal sentences on which BERT had been trained on. Only triplets where the src, mt, and pe  with number of characters in the range [1,200] are kept.

Example:
```
DATADIR=/path/to/data
paste $DATADIR/train.{src,mt,pe} | python3 preprocess_train.py -o $DATADIR/train.prepro -exts src mt pe --remove-begin-hyphens
paste $DATADIR/dev.{src,mt,pe} | python3 preprocess_train.py -o $DATADIR/dev.prepro -exts src mt pe --remove-begin-hyphens
```

To pass to OpenNMT-APE, `src` and `mt` files must be separated by `[SEP]` token after tokenization following the steps in the README in the OpenNMT-APE [repository](https://github.com/deep-spin/OpenNMT-APE).

### Decoding

During decoding, the input is preprocessed to follow training data pattern such as removing `<i>` tags, split at `<br>` tags, remove heading hyphens, and music symbols. These changes are kept track of a `codes` file that will be used to revert these changes during preprocessing.

Example:
```
python3 preprocess_decode.py -i $DATADIR/test.src $DATADIR/test.mt -odir inputs/
```

This will create the preprocessed input files `test.src.pre` and `test.mt.pre`, and the codes file `codes.test.mt` that tracks preprocessing operations within the `inputs/` directory.

After passing the `test.src.pre` and `test.mt.pre` to the APE system, and obtaining the output, say `outputs/test.ape.out`, use the following command to detokenize (Moses+WordPiece) and post-process the output (with target langauge German `de`)
```
python3 postprocess_decode.py  -i outputs/test.ape.out -tlang de -c inputs/codes.dev.nopre.mt
```

This will create the file `outputs/test.ape.out.post` that is the final post-processed output.
