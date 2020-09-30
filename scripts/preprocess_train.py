import argparse
import re
import sys
import datetime
import tqdm

from sacremoses.tokenize import MosesTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input-file", nargs='?', type=argparse.FileType('r'), default=sys.stdin,  help="filepath of tab separated file src\tmt\tpe or stdin input")
parser.add_argument("-o","--output-prefix", help="filepath prefix without lang extension of the output files")
parser.add_argument("-exts",nargs=3, help="filepath extensions for src, mt, and pe")
parser.add_argument("--keep-music", action='store_true', help="use to keep music symbol ♫♬♪ ")
parser.add_argument("--no-split", action='store_true', help="use to stop splitting at <br>")
parser.add_argument("--remove-begin-hyphens", action='store_true', help="use to remove beginning hyphens")
parser.add_argument("--min-l", default=1, type=int, help="minimum length of each segment in terms of characters")
parser.add_argument("--max-l", default=200, type=int, help="maximum length of each segment in terms of characters")
parser.add_argument("-slang", "--source-language", help="source languge for pre-tokenization using Moses tokenization (e.g. 'en')")
parser.add_argument("-tok", "--tokenize", action="store_true", help="pre-tokenization with moses tokenizer")
parser.add_argument("--output-stdout", action='store_true', help="output as tab-separated similar to the input file instead of 3 files")

args = parser.parse_args()

# opening output files
if args.output_stdout == False:
    args.output_files=[args.output_prefix + '.' + ext for ext in args.exts ]
    fos = [open(fo,'w') for fo in  args.output_files]

tokenizer = None
if args.tokenize:
    assert args.source_language, "--source-language must be set if --tokenize flag is used"
    tokenizer = MosesTokenizer(args.source_language)

def cleanup(s, args=None):
    s = re.sub('<[^>]*>', ' ',s)
    s = s.strip()
    if args:
        if args.remove_begin_hyphens == True and s.startswith('-'):
            s = s[1:]
    s =  re.sub(' +',' ', s.strip())
    return s

for line in tqdm.tqdm(args.input_file):

    line = line.rstrip()

    # standardize <br> tags
    line = re.sub('<\s*br\s*\/*>', '<br>', line, flags=re.IGNORECASE)

    # remove italics 
    line = re.sub('<\s*i/*>', ' ', line, flags=re.IGNORECASE)
    line = re.sub('<\/i>', ' ', line, flags=re.IGNORECASE)

    # remove music symbols
    if args.keep_music == False:
        line = re.sub('[♫♬♪]', '', line)

    src, mt, pe = line.split("\t")
    # splitting based on <br>
    if args.no_split == False:
        src_split = re.split(r'\s*<br>\s*',src)
        mt_split = re.split(r'\s*<br>\s*',mt)
        pe_split = re.split(r'\s*<br>\s*',pe)

    # if the src, mt, and pe does not have the same number of <br>, then do not split it
    if args.no_split == True or not (len(src_split) == len(mt_split) == len(pe_split)):
        # put it back as a single line and as a list
        src_split = [src]
        mt_split = [mt]
        pe_split = [pe]

    # write to file
    for src, mt, pe in zip(src_split, mt_split, pe_split):
        src = cleanup(src, args)
        mt = cleanup(mt, args)
        pe = cleanup(pe, args)

        if len(src) < args.min_l or len(mt) < args.min_l or len(pe) < args.min_l:
            continue

        if len(src) > args.max_l or len(mt) > args.max_l or len(pe) > args.max_l:
            continue

        if tokenizer:
            src = " ".join(tokenizer.tokenize(src, escape=False))
            mt = " ".join(tokenizer.tokenize(mt, escape=False))
            pe = " ".join(tokenizer.tokenize(pe, escape=False))

        if args.output_stdout == False:
            # remove all tags including <br> and write to file
            fos[0].write(src + '\n')
            fos[1].write(mt + '\n')
            fos[2].write(pe + '\n')
        else:
            print("{}\t{}\t{}".format(src,mt,pe))



    
if args.output_stdout == False:
    for fo in fos:
        fo.close()
