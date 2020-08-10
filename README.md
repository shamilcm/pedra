## Post-editing Datasets by Rakuten  (PEDRa)

PEDRa contains publicly available neural machine translation post-editing datasets in the subtitle domain created by [Rakuten Institute of Technology](https://rit.rakuten.co.jp/). The datasets are released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License ([CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). 

#### Datasets

1. **SubEdits** (English-German 160k triplets): A human-annnoated post-editing dataset of neural machine translation outputs, compiled from in-house NMT outputs and human post-edits of subtitles form [Rakuten Viki](https://www.viki.com/). Details about dataset collection and preprocessing can be found in the [paper](https://arxiv.com/pdf/XXX.XXXX).

2. **SubEscape** (English-German, 5.6m triplets): An artificial post-editing dataset created by translating OpenSubtitles2016 corpus [Lison and Tiedemann, 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/947_Paper.pdf) collected from [www.opensubtitles.org/] using the in-house NMT system used for SubEdits and the references used as synthetic post-edits following the procedure used to compile eSCAPE ([Negri et al., 2018](https://www.aclweb.org/anthology/L18-1004.pdf)).


#### License
The scripts provided in the repository are licensed under MIT License (see LICENSE.md)
The datasets are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

#### Citation
If you use this dataset, please cite the following paper
```
@inproceedings{chollampatt2020pedra,
    title = "Can Automatic Post-editing Improve NMT?",
    author = "Chollampatt, Shamil  and
      Susanto, Raymond  and
      Tan, Liling and
      Ewa Szymanska",
    booktitle = "arXiv",
    year = "2020",
}
```
