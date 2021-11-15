import math
import os

# number of models SHOULD be odd to achieve a majority
main_path = './prediction/'
prediction_files_path = ['bert-base-cased_bal_post.tsv',
                         'allenai_scibert_scivocab_uncased_bal_post.tsv',
                         'microsoft_BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext_bal_post.tsv',
                         'allenai_biomed_roberta_base_bal_post.tsv',
                         'bert-large-cased_bal_post.tsv'
                         ]
output_file_path = './prediction/ensemble_bert-base-large_scibert_pubmedbert_biomed_bal_newpred_post.tsv'

majority = math.ceil(len(prediction_files_path)/2)
all_pmids = set()
candidates = {}


def get_voting(prediction_files_path):
    with open(prediction_files_path) as pred_file:
        pred_txt = pred_file.read().split('\n')
    for line in pred_txt:
        if line.strip() == '':
            continue
        part = line.split('\t')
        if part[0] not in candidates:
            candidates[part[0]] = {}
        if line.strip() not in candidates[part[0]]:
            candidates[part[0]][line.strip()] = 0
        candidates[part[0]][line.strip()] += 1


for pred_path in prediction_files_path:
    get_voting(main_path + pred_path)

ensemble_majority_txt = ''
for pmid, predictions in candidates.items():
    for line, count in predictions.items():
        if count >= majority:
            ensemble_majority_txt += '{}\n'.format(line)
            all_pmids.add(pmid)

with open(output_file_path, 'w') as output_file:
    output_file.write(ensemble_majority_txt)

# generating file with all the PMIDs with prediction, needed for evaluation in the challenge
pmid_output_path = os.path.splitext(output_file_path)[0] + '_pmids.txt'
pmids_output_txt = ''
for p in all_pmids:
    pmids_output_txt += '{}\n'.format(p)
pmids_output_txt = pmids_output_txt.strip()

with open(pmid_output_path, 'w') as pmid_output_file:
    pmid_output_file.write(pmids_output_txt)
