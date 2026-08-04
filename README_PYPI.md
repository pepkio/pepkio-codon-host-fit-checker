# pepkio-codon-host-fit-checker

A Python client and CLI for evaluating sequence-level host compatibility, Codon Adaptation Index (CAI), rare codon bottlenecks, and GC composition profiles across major expression hosts.

# What It Does

`pepkio-codon-host-fit-checker` provides Python bindings and a command-line interface to evaluate host expression suitability for heterologous genes. It quantifies the Codon Adaptation Index (CAI), pinpoints local rare codon clusters ($w_i < 0.15$), profiles positional GC distributions ($GC_1, GC_2, GC_3$), and flags translational obstacles across bacterial (*E. coli*, *B. subtilis*), yeast (*S. cerevisiae*, *P. pastoris*), insect (*Sf9*), and mammalian (CHO, HEK293) expression systems.

# Features

- **Multi-Host Compatibility Profiling**: Evaluates nucleotide sequences against reference codon usage tables for *E. coli* (K-12 & BL21(DE3)), *S. cerevisiae*, *P. pastoris*, CHO, HEK293, *Sf9*, and *B. subtilis*.
- **Codon Adaptation Index (CAI)**: Calculates geometric mean CAI scores relative to host-specific high-expression reference gene sets.
- **Rare Codon & Bottleneck Mapping**: Highlights codons with host frequency $< 15\%$ and flags tandem rare codon clusters that trigger ribosomal pausing or translation stalling.
- **Positional GC & Regional Composition**: Computes overall GC content alongside position-specific ($GC_1, GC_2, GC_3$) and sliding-window regional GC metrics to detect destabilizing composition spikes.
- **Translational Signal Screening**: Detects internal prokaryotic ribosome binding sites (Shine-Dalgarno-like sequences), eukaryotic cryptic splice donor/acceptor sites, and out-of-frame stop codons.
- **Side-by-Side Comparison Matrix**: Compares candidate gene compatibility across multiple expression hosts simultaneously in a unified matrix format.
- **Python API & CLI**: Offers synchronous and asynchronous execution in Python alongside a CLI producing structured JSON output for pipeline integration.

# Installation

Install the package via `pip`:

```bash
pip install pepkio-codon-host-fit-checker
```

# Quick Example

```python
from pepkio_codon_host_fit_checker import PepkioClient

with PepkioClient() as client:
    # Evaluate sequence compatibility across bacterial and mammalian expression hosts
    result = client.run({
        "tab": "matrix",
        "sequence": "ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAG",
        "host_ids": ["e_coli_k12", "s_cerevisiae", "cho_cell"]
    })

    print("Status:", result.status)
    print("Host Compatibility Results:", result.result)
```

# Typical Use Cases

- **Expression Host Organism Selection**: Compare codon adaptation metrics across bacterial (*E. coli*), yeast (*P. pastoris*), and mammalian (CHO) systems prior to cloning to identify optimal host compatibility.
- **Gene Synthesis Pre-Flight Auditing**: Audit codon-optimized constructs from commercial synthesis vendors to verify the elimination of rare codon bottlenecks without introducing secondary structures or cryptic splice sites.
- **Troubleshooting Expression Yield Drops**: Diagnose protein yield drops or truncated expression products by mapping host-specific rare codon clusters in heterologous genes.
- **Dual-Host Vector Optimization**: Assess sequence suitability for shuttle vector constructs intended for initial expansion in *E. coli* followed by functional expression in eukaryotic hosts.
- **Metabolic Pathway & Operon Balancing**: Profile translational efficiency across multi-gene synthetic operons to prevent host cell metabolic strain and resource competition.

# Scientific Background

Heterologous protein expression efficiency is closely tied to how well a target sequence matches the host organism's tRNA pool and codon usage preferences. The Codon Adaptation Index (CAI) quantifies this bias by measuring the geometric mean of relative adaptiveness values ($w_i$) for all codons relative to a reference set of highly expressed genes. However, global CAI scores alone can mask localized rare codon clusters (codons with relative adaptiveness $w_i < 0.15$ or host frequency $< 15\%$) that induce ribosomal stalling, co-translational misfolding, or premature termination. Additionally, extreme regional GC composition imbalances ($GC_1, GC_2, GC_3$) and unwanted sequence signals like internal Shine-Dalgarno motifs or cryptic splice sites can severely impair mRNA stability and translation yield.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/codon-host-fit-checker

The web application provides visual codon frequency heatmaps, interactive host comparison matrices, downloadable worksheets, and shareable permalinks.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-codon-host-fit-checker

Web Application: https://www.pepkio.com/tools/codon-host-fit-checker

Source and issue tracker: https://github.com/pepkio/pepkio-codon-host-fit-checker

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

* codon host fit checker
* codon adaptation index
* CAI calculator
* rare codon finder
* codon usage bias
* tRNA adaptation index
* GC content analyzer
* position specific GC
* GC1 GC2 GC3
* heterologous expression
* recombinant protein expression
* gene synthesis optimization
* host expression compatibility
* E. coli expression checker
* yeast codon adaptation
* CHO host fitness
* Pichia pastoris expression
* HEK293 codon usage
* Sf9 insect cell expression
* Bacillus subtilis expression
* Shine Dalgarno motif finder
* cryptic splice site detector
* ribosomal pausing predictor
* synthetic biology tools
* bioinformatics python client
* evaluate codon adaptation index in python
* host specific rare codon bottleneck detection
* multi host codon compatibility matrix comparison
* optimize nucleotide sequence for heterologous protein yield
* detect translational obstacles in synthetic constructs
* pre flight audit for gene synthesis orders
* dual host shuttle vector sequence analysis
* positional GC composition profiling for recombinant genes
* troubleshoot protein expression yield drops in e coli
* compare mammalian yeast and bacterial expression hosts
* automated codon host fit checker python api
* programmatic codon bias calculation command line tool
* co translational protein folding rare codon analysis
