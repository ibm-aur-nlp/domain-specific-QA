# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json
import argparse
import os

parser = argparse.ArgumentParser(description='Extract extractive domains specific questions answering samples from MS MARCO')
parser.add_argument('--marco', help='path to MS MARCO training set')
parser.add_argument('--out_dir', help='path to save domain specific datasets')
parser.add_argument('--lookup_table', help='path to the lookup table')
args = parser.parse_args()

# Load lookup table
# {query_id: {domain:str, split:str}}
with open(args.lookup_table, 'r') as fp:
    domain_table = json.load(fp)

# Load MS MARCO training set
with open(args.marco, 'r') as fp:
    marco = json.load(fp)
    rev_query_id = dict()
    for query_id in marco['query']:
        rev_query_id[marco['query_id'][query_id]] = query_id

domains = {'finance': {'train': [], 'dev': [], 'test': []},
           'law': {'train': [], 'dev': [], 'test': []},
           'music': {'train': [], 'dev': [], 'test': []},
           'film': {'train': [], 'dev': [], 'test': []},
           'biomedical': {'train': [], 'dev': [], 'test': []},
           'computing': {'train': [], 'dev': [], 'test': []}}

# Convert extractive domain specific samples into the SQUAD format
for domain in domain_table:
    for split in domain_table[domain]:
        for id in domain_table[domain][split]:
            qid, pid = map(int, id.split('_'))
            query_id = rev_query_id[qid]
            context = marco['passages'][query_id][pid]['passage_text'].strip()
            datum = None
            for answer in marco['answers'][query_id]:
                answer = answer.strip()
                if len(answer) > 0:
                    # Find answer position
                    answer_start = context.lower().find(answer.lower())
                    if answer_start >= 0:
                        answer = context[answer_start:answer_start + len(answer)]
                        if datum is None:
                            # Create a QA sample in SQUAD format
                            datum = {
                                'paragraphs': [{
                                    'context': context,
                                    'qas': [{
                                        'answers': [{'answer_start': answer_start, 'text': answer}],
                                        'question': marco['query'][query_id],
                                        'id': id
                                    }]
                                }]
                            }
                        else:  # Handle multiple-answers case
                            datum['paragraphs'][0]['qas'][0]['answers'].append(
                                {'answer_start': answer_start,
                                 'text': answer}
                            )
            domains[domain][split].append(datum)

# Save
if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)
for domain in domains:
    for split in domains[domain]:
        with open(os.path.join(args.out_dir, 'squad.%s.%s.json' % (domain, split)), 'w') as fp:
            json.dump({'data': domains[domain][split]}, fp)
