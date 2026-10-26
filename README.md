# MorphEval-PT

MorphEval-PT is a lightweight framework to assess morphological coherence of LLM tokenizers.

Evaluating the alignment of a token sequence as a morpheme sequence is a challenging task for Brazilian Portuguese, a language with limited resources. MorphEval-PT attempts to partially fill this gap by introducing an evaluation method based on psycholinguistic models of morphological processing. This method assesses how likely sub-word tokenizers can generate morphologically coherent token sequences. 

MorphEval-PT is divided in two components: (i) [dataset](#dataset) and (ii) [evaluation metrics](#evaluation-metrics).

Any tokenizer trained with the Hugging Face [Tokenizers](https://huggingface.co/docs/tokenizers/index) library can be evaluated by MorphEval-PT.

## Dataset

MorphEval-PT uses [MorphyNet](https://github.com/kbatsuren/MorphyNet) as its source and follows the same word-formation splits: derivation and inflection. This separation is required to address the inherited limitations of MorphyNet when computing the metrics. A copy of the original dataset provided by the authors of MorphyNet, along with the processed MorphEval-PT dataset, can be found in the [data](./data/) folder.

See the publications under [Citation](#citation) for details on how MorphyNet was processed to produce the final dataset.

|    Samples   | Derivation | %      | Inflection | %      |
|--------------|-----------:|:-------|-----------:|:-------|
| MorphyNet    |     11,774 |        |    376,341 |        |
| Filtered     |        273 |  2.32% |     76,534 | 20.34% |
| MorphEval-PT |     11,501 | 97.68% |    299,807 | 79.66% |

### MorphEval-PT Examples

#### Inflectional Dataset

| Input Word   | Morpheme Segmentation |
|--------------|:---------------------:|
| infiltrarmos | infiltr \| armos      |
| infiltrados  | infiltr \| ado \| s   |
| infiltradas  | infiltr \| ada \| s   |

#### Derivational Dataset

| Input Word    | Morpheme Segmentation | Type   |
|---------------|:---------------------:|--------|
| multicultural | **multi** \| cultural | prefix |
| amoral        | **a** \| moral        | prefix |
| amoralismo    | amoral \| **ismo**    | suffix |
| adicionar     | adicion \| **ar**     | suffix |
| juramento     | jura \| **mento**     | suffix |


## Evaluation Metrics

MorphEval-PT provides *Precision*, *Recall* and *F1 Score* metrics for each word-formation process.

The evaluation metrics incorporate psycholinguistic models of cognitive word processing. The brain can understand the meaning of words using either the *storage* or *decomposition* routes, similar to how sub-word tokenizers behaves. This behavior is considered on the confusion matrix calculation. If a word is tokenized as a single token, it corresponds to the storage route and is classified as a valid tokenization. Otherwise, if the word is tokenized into sub-word tokens, it is evaluated via the decomposition route, where every possible split is analysed (see the paper under [Citation](#citation) for more details).

### Limitations

As inherited from MorphyNet, the dataset does not contains the complete morpheme segmentation. Only the morphemes related to the word-formation process are identified. The inflectional data may contain one or more suffixes, whereas the derivational data contains a single prefix or suffix. Becouse they do not represent full morpheme segmentation, only the provided morpheme boundaries (borders) are evaluated to avoid skewing the coherence assessment.

**Full Binary Classification:** Not every morpheme boundary is explicitly marked. This can lead to misinterpretations.

- $
    a|moral \rightarrow
    A_1 M_0 O_0 R_0 A_0 L \rightarrow
    [1,0,0,0,0]$
- $
    amoral|ismo \rightarrow
    A_0 M_0 O_0 R_0 A_0 L_1 I_0 S_0 M_0 O \rightarrow
    [0,0,0,0,0,1,0,0,0]$
- $
    infiltr|ada|s \rightarrow
    I_0 N_0 F_0 I_0 L_0 T_1 R_0 A_0 D_0 A_1 S \rightarrow
    [0,0,0,0,0,1,0,0,0,1]$
- $
    re|aver \rightarrow
    R_0 E_1 A_0 V_0 E_0 R \rightarrow
    [0,1,0,0,0]$
    
**Handling dataset limitations:** only the targeted affixes are considered.

- $
    a|moral \rightarrow
    A_1 M_0 O_0 R_0 A_0 L \rightarrow
    [1]$
- $    amoral|ismo \rightarrow
    AMORA L_1 I_0 S_0 M_0 O \rightarrow
    [1,0,0,0]$
- $
    infiltr|ada|s \rightarrow
    INFILT_1 R_0 A_0 D_0 A_1 S \rightarrow
    [1,0,0,0,1]$
- $
    re|aver \rightarrow
    R_0 E_1 AVER \rightarrow
    [0,1]$

### Usage:

```bash
python morpheval.py --derivation --model-name=[MODEL_NAME]
```
or 
```bash
python morpheval.py --inflection --model-name=[MODEL_NAME]
```

**Parameters**

- `--inflection`: Selects the inflectional dataset for evaluation
- `--derivation`: Selects the derivational dataset for evaluation
- `--model-name`: this value is directly passed to [AutoTokenizer.from_pretrained](https://huggingface.co/docs/transformers/main/en/model_doc/auto#transformers.AutoTokenizer.from_pretrained) and can be either a local path or the id of a tokenizer hosted on [huggingface.co](https://huggingface.co/).



## Citation

[Evaluating Portuguese Tokenizers as Morpheme Sequence in Relation to LLM Downstream Performance](https://aclanthology.org/2026.stil-1.21/) (Mello & Finger, STIL 2026)


**Bibtext**

```bibtex
@inproceedings{mello-finger-2026-morpheval-pt,
    title = "
        Evaluating {P}ortuguese Tokenizers as Morpheme Sequence
        in Relation to {LLM} Downstream Performance",
    author = "
        Mello, Guilherme L.  and
        Finger, Marcelo",
    editor = "
        Barbosa, Bryan Khelven da Silva  and
        Paes, Aline  and
        Felippo, Ariani Di",
    booktitle = "
        Proceedings of the 17th {B}razilian Symposium
        in Information and Human Language Technology",
    month = oct,
    year = "2026",
    address = "Cuiab{\'a}, Mato Grosso, Brazil",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.stil-1.21/",
    doi = "10.5753/stil.2026.26562",
    pages = "245--257"
}
```

## License & Attribution

This project uses a dual-licensing structure to ensure that both the software code and the dataset assets are governed by the most appropriate open-source frameworks.

### 1. Software Code (MIT)
All source code, scripts, and transformation logic contained in this repository are licensed under the **MIT License**. 

You are free to use, modify, copy, and distribute the code for both personal and commercial projects, provided the original copyright and permission notice are included. See the main [LICENSE](LICENSE) file in the root directory for the full legal text.

### 2. MorphEval-PT Dataset (CC BY-SA 4.0)

The MorphEval-PT dataset provided in this repository (located in [data/morpheval/](./data/morpheval/)) is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** License. 

Under this license, you are free to share and adapt this modified data for any purpose, even commercially, as long as you provide appropriate attribution and distribute your contributions under the same CC BY-SA 4.0 license.

### 3. MorphyNet Dataset (CC BY-SA 3.0)

The MorphEval-PT data in [data/morpheval/](./data/morpheval/) is a derivative work built upon the following original dataset:

* **Original Dataset Name:** MorphyNet
* **Original Author/Creator:** Khuyagbaatar Batsuren, Gábor Bella, and Fausto Giunchiglia
* **Source Link:** https://github.com/kbatsuren/MorphyNet
* **Original License:** [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/)

*Note: The original, unmodified dataset file is hosted for archival and reproducibility purposes in [data/morphynet/](./data/morphynet/) and remains strictly under its original CC BY-SA 3.0 terms.*
