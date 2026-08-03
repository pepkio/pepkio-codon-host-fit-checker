# pepkio-codon-host-fit-checker

Python client for the Pepkio [codon-host-fit-checker](https://www.pepkio.com/tools/codon-host-fit-checker) tool.

## Installation

```bash
pip install pepkio-codon-host-fit-checker
```

## Usage

### Python API

```python
from pepkio_codon_host_fit_checker import PepkioClient

client = PepkioClient(api_key="your_api_key")

# Get manifest
manifest = client.get_manifest()

# Run tool
result = client.run(
    input_data={
        "tab": "matrix",
        "sequence": "ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA",
        "host_ids": ["e_coli_k12", "cho", "human_hek293"],
    }
)
print(result.status)
print(result.result)
```

### CLI

```bash
# Get manifest
pepkio-codon-host-fit-checker manifest

# Run example from manifest
pepkio-codon-host-fit-checker run --example gfp_matrix

# Run with JSON input
pepkio-codon-host-fit-checker run --input-json '{"tab":"matrix","sequence":"ATGGCC","host_ids":["e_coli_k12"]}'
```
