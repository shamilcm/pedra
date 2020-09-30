import argparse
import re
import os,sys

from sacremoses.tokenize import MosesTokenizer
from sacremoses.normalize import MosesPunctNormalizer

def cleanup(s):
    """
    remove all other html tags and extra spaces
    """
    s = re.sub('<[^>]*>', ' ', s)
    s = s.strip()
    s =  re.sub(' +',' ', s.strip())
    return s

def preprocess(src_file, mt_file, output_dir, tokenize_lang=None):
    """
        pre-process input file before post-editing
        split at <br> and remove <i> tags and music symbols.
        store everything in a codes file in output_dir

        Args:
            src_file: src_file of the translation to be preprocessed
            mt_file: output of the mt system file to be preprocessed
            output_dir: output directory to output the preprocessed files and codes file

    """

    punct_normalizer = MosesPunctNormalizer()

    # set tokenizer
    tokenizer = None
    if tokenize_lang:
        tokenizer = MosesTokenizer(lang=tokenize_lang)

    code_file = output_dir+'/codes.'+os.path.basename(mt_file)
    src_out_file = output_dir+'/'+os.path.basename(src_file)+'.pre'
    mt_out_file = output_dir+'/'+os.path.basename(mt_file)+'.pre'
    with open(src_out_file,'w') as fosrc, open(mt_out_file,'w') as fomt, open(code_file,'w') as fcodes, open(src_file) as fsrc, open(mt_file) as fmt:
        idx=0
        for src,mt in zip(fsrc,fmt):
            src, mt = src.strip(), mt.strip()
            

            idx+=1
            
            # standardize br tags
            src = re.sub('<\s*br\s*\/*>', '<br>', src, flags=re.IGNORECASE)
            mt = re.sub('<\s*br\s*\/*>', '<br>', mt, flags=re.IGNORECASE)


            # if number of <br> is same, split and save it as multiple lines
            src_split = re.split(r'\s*<br>\s*',src)
            mt_split = re.split(r'\s*<br>\s*',mt)

            # if the src, mt, do not have the same number of <br>, then do not split it
            if not (len(src_split) == len(mt_split)):
                src_split = [src]
                mt_split = [mt]
                


            for src_part, mt_part in zip(src_split, mt_split):
                code = "{}\t".format(idx)

                # check if they start with the hyphen
                has_hyphen = False
                if src_part.startswith('-'):
                    has_hyphen = True
                    src_part = src_part[1:].lstrip()

                if mt_part.startswith('-'):
                    has_hyphen = True
                    mt_part = mt_part[1:].lstrip()

                # check if they start with the music symbol
                music_syms = ('♫','♬','♪')
                has_music = False
                if re.search(r'\s*[{}]\s*'.format(''.join(music_syms)), src_part):
                    has_music = True
                    src_part = re.sub(r'\s*[{}]\s*'.format(''.join(music_syms)), '', src_part)

                #if mt_part.startswith(music_syms) or mt_part.endswith(music_syms):
                if re.search(r'\s*[{}]\s*'.format(''.join(music_syms)), mt_part):                
                    has_music = True
                    mt_part = re.sub(r'\s*[{}]\s*'.format(''.join(music_syms)), '', mt_part)

                # check if it has enclosing italics tags. otherwise leave it as it is
                itag = '<i>'
                eitag = '</i>'
                has_itag = False
                if src_part.startswith(itag) or src_part.endswith(eitag):
                    has_itag = True

                if mt_part.startswith(itag) or mt_part.endswith(eitag):
                    has_itag = True


                #if re.match(r'^<i>[^<]*</i>$', src_part):
                if has_hyphen == True:
                    code += 'HYPHENBEGIN\t'
                if has_music == True:
                    code += 'MUSIC\t'
                if has_itag == True:
                    code += 'ITALICTAGS\t'

                src_part = punct_normalizer.normalize(cleanup(src_part))
                mt_part = punct_normalizer.normalize(cleanup(mt_part))

                if tokenizer:
                    src_part = " ".join(tokenizer.tokenize(src_part, escape=False))
                    mt_part = " ".join(tokenizer.tokenize(mt_part, escape=False))

                fosrc.write(src_part.strip()+'\n')
                fomt.write(mt_part.strip()+'\n')
                fcodes.write("{}\n".format(code))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input-files", nargs=2, required=True, help="paths to src and mt files")
    parser.add_argument("-slang", "--source-language", help="source languge for pre-tokenization using Moses tokenization (e.g. 'en')")
    parser.add_argument("-tok", "--tokenize", action="store_true", help="pre-tokenization with moses tokenizer")
    parser.add_argument("-odir","--output-dir", required=True, help="directory to output processed file along with history of operation codes to post process")
    args = parser.parse_args()

    if args.tokenize:
        assert args.source_language, "--source-language must be set if --tokenize flag is used"

    preprocess(src_file=args.input_files[0], mt_file=args.input_files[1], output_dir=args.output_dir, tokenize_lang=args.source_language)

if __name__ == "__main__":
    main()


