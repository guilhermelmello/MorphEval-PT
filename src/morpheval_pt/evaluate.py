"""
Morphological Coherence Evaluation Script.

Computes Precision, Recall and F1 Measures based on MorphEval-PT dataset.
The metrics can be computed as complete and affixes segmentation. The
affixes segmentation also considers a full word as a possible correct
segmentation as it allows its meaning to emerge from a single token.
"""

import csv

from transformers import AutoTokenizer


def _generate_predicted_positions(tokenizer, word):
    '''Convert the tokenizer segments into a sequence of boundary positions.'''
    unk_id = tokenizer.unk_token_id
    tokenized = tokenizer(
        word,
        return_offsets_mapping=True,
        add_special_tokens=False,
    )

    # unknown words
    if unk_id in tokenized['input_ids']:
        print(f'>>> {word}')

    offsets = tokenized['offset_mapping']
    splits = [o[0] for o in offsets[1:]]
    return splits


def _generate_target_positions(tokens: list[str]):
    '''Convert the MorphEval-PT segmentation in a sequence of boundary positions.'''
    if len(tokens) == 1:
        return []

    position = len(tokens[0])
    positions = [position]
    for token in tokens[1:-1]:
        position += len(token)
        positions.append(position)

    return positions


def _compute_confusion_matrix(target, predicted, is_suffix=True):
    '''Confusion Matrix Statistics.'''
    # considers a single word (no predicted split) as a true positive case
    if len(predicted) == 0:
        return 1, 0, 0  # tp, fp, fn

    t_index = 0
    p_index = 0

    tp = 0
    fp = 0
    fn = 0

    if is_suffix:
        # skip predictions that are not suffixes
        while p_index < len(predicted) and target[0] > predicted[p_index]:
            p_index += 1
    else:
        # remove predictions that are not prefixes
        while len(predicted) > 0 and predicted[-1] > target[-1]:
            predicted.pop()

    # while both target and predicted have splits
    while t_index < len(target) and p_index < len(predicted):
        t = target[t_index]
        p = predicted[p_index]

        if t < p:       # false negative
            fn += 1
            t_index += 1
            continue

        if p < t :      # false positive
            fp += 1
            p_index += 1
            continue

        # p == t : true positive
        tp += 1
        t_index += 1
        p_index += 1

    # process remaining false negatives
    while t_index < len(target):
        fn += 1
        t_index += 1

    # process remaining false positives
    while p_index < len(predicted):
        fp += 1
        p_index += 1

    return tp, fp, fn


def evaluate(dataset_path, model_name):
    '''Morphologic Coherence Metrics'''
    print(f"{model_name} ========")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    words = 0
    sw = 0
    tp = 0  # true positive
    fp = 0  # false positive
    fn = 0  # false negative

    # for line in samples:
    with open(dataset_path, 'r', encoding='utf-8') as dataset_file:
        input_reader = csv.reader(dataset_file, delimiter='\t')
        for line in input_reader:
            words += 1
            word = line[0]
            target = line[1]
            is_suffix = True if len(line) == 2 else True if line[2] == 'suffix' else False

            t_tokens = target.split('|')
            t_positions = _generate_target_positions(t_tokens)
            p_positions = _generate_predicted_positions(tokenizer, word)

            # predicted as a single word
            if len(p_positions) == 0:
                sw += 1

            _tp, _fp, _fn = _compute_confusion_matrix(t_positions, p_positions, is_suffix=is_suffix)

            tp += _tp
            fp += _fp
            fn += _fn

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall  / (precision + recall)

    print(f"Precision: {100 * precision:.2f}%")
    print(f"Recall: {100 * recall:.2f}%")
    print(f"F1: {100 * f1:.2f}%")
    print(f"Single Words: {100 * sw / words:.2f}% ({sw}/{words})")
