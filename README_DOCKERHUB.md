# Pepkio Codon Host Fit Checker

Container image bundling the Codon Host Fit Checker CLI to assess Codon Adaptation Index (CAI), detect translational bottlenecks, and evaluate multi-host expression compatibility via the Pepkio API.

# What It Does

The image runs `pepkio-codon-host-fit-checker`, a client for the Pepkio Codon Host Fit Checker REST API. It evaluates candidate coding sequences across model expression hosts (such as *E. coli*, *S. cerevisiae*, *P. pastoris*, CHO, HEK293, *Sf9*, and *B. subtilis*) by computing global Codon Adaptation Index (CAI) values, identifying rare codon bottlenecks, and profiling position-specific GC content ($GC_1, GC_2, GC_3$).

Typical workflows include screening synthetic gene constructs across multiple expression hosts before ordering synthesis, diagnosing translation arrest and low yields in recombinant protein purification, auditing commercial codon optimization outputs, and balancing multi-gene metabolic pathways. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Multi-host codon adaptation profiling across bacterial, yeast, insect, and mammalian hosts
- Geometric mean Codon Adaptation Index (CAI) calculation relative to host reference sets
- Identification of rare codon bottlenecks ($w_i < 0.15$) and tandem pausing clusters
- Positional GC analysis ($GC_{\text{total}}, GC_1, GC_2, GC_3$) and regional composition tracking
- Detection of problematic translational signals such as internal Shine-Dalgarno motifs and cryptic splice sites
- Pre-configured manifest examples (`gfp_matrix`, `short_inspector`)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/codon-host-fit-checker:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/codon-host-fit-checker:0.1.0 \
  pepkio-codon-host-fit-checker run --example gfp_matrix
```

Manifest only (no API key):

```bash
docker run --rm pepkio/codon-host-fit-checker:0.1.0 \
  pepkio-codon-host-fit-checker manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/codon-host-fit-checker:0.1.0 \
  pepkio-codon-host-fit-checker run --input-json \
  '{"tab":"matrix","sequence":"ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA","host_ids":["e_coli_k12","cho","human_hek293","pichia_pastoris"]}'
```

# Typical Use Cases

- Comparing codon adaptation metrics across bacterial (*E. coli*), yeast (*P. pastoris*), and mammalian (CHO) systems prior to cloning
- Screening recombinant protein sequences for translation-limiting rare codon clusters
- Auditing gene synthesis candidates for unwanted internal regulatory sequences and extreme GC bias
- Containerized pre-flight validation in automated bioinformatics and synthetic biology pipelines

# Scientific Background

In recombinant protein expression, heterologous gene sequences often encounter translation efficiency bottlenecks due to differences in host tRNA abundance and codon bias. The Codon Adaptation Index (CAI) measures the relative adaptiveness of a coding sequence compared to a reference set of highly expressed host genes. Identifying localized clusters of rare codons ($w_i < 0.15$) and extreme GC fluctuations is essential for avoiding ribosome stalling, truncated products, and mRNA instability.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/codon-host-fit-checker

The web UI provides interactive multi-host comparison heatmaps, rare codon distribution charts, positional GC graphs, and shareable run permalinks.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-codon-host-fit-checker

Web Application: https://www.pepkio.com/tools/codon-host-fit-checker

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

A semantic, AI-native version of this document in the K2F format is available at https://k2f.dev (https://k2f.dev/v/ce242ab877606a40fa8cad2b09453c363fbcde232535827a6f98c74e6075580a)
