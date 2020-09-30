import argparse
import re
import os,sys

from sacremoses.tokenize import MosesDetokenizer

def postprocess(ape_file, codes_file, detokenizer=None):
    """
        post-process the output file of the post-editing system
        by making use of the codes file.

        Args:
            ape_file: post-edited output of the system
            codes_file: created during pre-processing that keeps track of <br> and symbols
    """
    def detokenize(s, detokenizer):
        """ helper function to detokenize """
        return detokenizer.detokenize(re.sub(" ##", "", s).split())

    ape_out_file = ape_file +'.post'
    with open(ape_out_file,'w') as foape, open(ape_file) as fape, open(codes_file) as fcodes:
        idx = 0
        for ape, code in zip(fape, fcodes):
            ape = ape.strip()
            if detokenizer is not None:
                ape = detokenize(ape, detokenizer)
            pieces = code.strip().split('\t')
            orig_idx = int(pieces[0])
            tags = [] if len(pieces) == 1 else pieces[1:]
            if orig_idx != idx  : 
                if idx!=0: foape.write('\n') #except for first line, add a new line to any new lne
                idx += 1
            else:
                foape.write(' <br> ')

            if "MUSIC" in tags:
                ape = "♫ {} ♫".format(ape)
 
            if "ITALICTAGS" in tags:
                ape = "<i> {} </i>".format(ape)
            
            if "HYPHENBEGIN" in tags:
                ape = "- {}".format(ape)
           
            # removing spaces around hyphens due to BERT tokenizer split
            ape = re.sub(r"([^>.?]) - ([^<])", r"\1-\2", ape)

            foape.write(ape)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input-pe-file", required=True, help="output of the pe system to be post processed")
    parser.add_argument("-tlang","--target-language", dest="target_language", help="required for detokenization")
    parser.add_argument("-detok", "--detokenize", action="store_true", help="do detokenization (-tlang is necessary)")
    parser.add_argument("-c","--codes-file", required=True, help="codes file used to post process the output")
    args = parser.parse_args()
    
    detokenizer=None
    if args.detokenize == True:
        assert (
            args.target_language is not None
        ), "--target-language is required for detokenization"
        detokenizer = MosesDetokenizer(lang=args.target_language)

 
    postprocess(ape_file=args.input_pe_file, codes_file=args.codes_file, detokenizer=detokenizer)

if __name__ == "__main__":
    main()


