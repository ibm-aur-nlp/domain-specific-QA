# domain-specific-QA
Extracting six domain-specific QA datasets from MS MARCO

## To generate 6 domain specific QA datasets from MS MARCO

Please use Python 2.7 environment.

Download [MS MARCO Reading Comprehension v2.1 training set](http://www.msmarco.org/dataset.aspx)  
`pip install json argparse`   
`git clone https://github.com/ibm-aur-nlp/domain-specific-QA.git`  
`cd <YOUR_CLONE_PATH>/domain-specific-QA`  
`python extract_domain_specific_samples.py --marco <YOUR_MARCO_DOWNLOAD_PATH>/train_v2.1.json --out_dir <YOUR_OUTPUT_PATH> --lookup_table lookup_table.json`

In `<YOUR_OUTPUT_PATH>`, you should see json files of format `squad.<DOMAIN>.<SPLIT>.json`. The statistics of the 6 domain specific QA datasets is:  

| Domain | Total | Train |  Dev  |  Test |
|  :---  | :---: | :---: | :---: | :---: |
| music | 3,596 | 2,517 | 539 | 540 |
| biomedical | 31,620 | 22,134 | 4,743 | 4,743 |
| film | 5,032 | 3,522 | 755 | 755 |
| finance | 9,700 | 6,790 | 1,455 | 1,455 |
| law | 4,436 | 3,105 | 665 | 666 |
| computing | 4,316 | 3,021 | 647 | 648 |
