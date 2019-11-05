# domain-specific-QA
Extracting six domain-specific QA datasets from MS MARCO

# To generate 6 domain specific QA datasets from MS MARCO

Please use Python 2.7 environment.

Download [MS MARCO Reading Comprehension v2.1 training set](http://www.msmarco.org/dataset.aspx)  
`pip install json argparse`   
`git clone https://github.com/ibm-aur-nlp/domain-specific-QA.git`  
`cd <YOUR_CLONE_DIR>/domain-specific-QA`  
`python extract_domain_specific_samples.py --marco <YOUR_MARCO_DOWNLOAD_PATH>/train_v2.1.json --out_dir <YOUR_OUTPUT_PATH> --lookup_table lookup_table.json`
