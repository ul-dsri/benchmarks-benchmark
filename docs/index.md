# Benchmarks' Benchmark (B~2~)

!!! warning
    You are viewing pre-release benchmark documentation. Please return after the benchmark is made broadly available and do not share this URL.

Large language model (LLM) benchmarks enable system use decisions informed by LLM properties, but benchmarks may be rendered unreliable for real world decision making by a variety of threats to benchmark longevity, correctness, coverage, consistency, and intelligibility. Motivated by emerging LLM safety benchmarks, on whose scores people rely on to make decisions impacting real world safety, this work presents a benchmark for LLM benchmarks inspired by National Institute of Standards and Technology risk management processes. High scores indicate a reduced likelihood and/or severity of inappropriate reliance on a benchmark.

## B~2~ Results

!!! warning
    These are filler results pending updates from the benchmarked benchmarks.

{{ read_file('docs/data/table.md') }}

## Threat Registry
There are many threats to reliability of benchmarks. For example,

**Threat \#020:** `Machine translation introduces errors`

View the complete list of [threats](data/threat-registry-table.md). Submit a threat by opening a [Github issue](https://github.com/ul-dsri/party-paper/issues) or emailing sean.mcgregor-at-ul.org.

## Responses and Mitigations
Benchmarks score points by mitigating threats to benchmark reliability. For example,

**Response Number:** 23
```
Response: Validate all machine-translated prompts with highly qualified speaker of both languages
90 Reduction in Likelihood (Percent)
70 Reduction in Severity (Percent)
```

View the complete list of [mitigations](data/risk-response-table.md). Submit a mitigation by [opening a Github issue](https://github.com/ul-dsri/party-paper/issues) or emailing sean.mcgregor-at-ul.org.

## Research Paper

The following are versioned releases of the research paper associated with this work. A snapshot of the paper will be submitted for peer review in May 2025.

[![first page](images/first_page.png){align=right}]( {{ get_latest_pdf_url() }} )

Current paper as of {{ current_date() }}.

## Paper History

{{ get_latest_pdf_anchor() }}{{ get_pdf_list_from_s3() }}

Contributions to the research paper are welcome via email (sean.mcgregor-at-ul.org), or on the [Github respository](https://github.com/ul-dsri/party-paper). Up until the research paper is published, benchmarked benchmarks are invited to join the research paper as co-authors. You can find the current list of co-authors on the latest paper.

## Independence

- This research is the product of a large number of independent individuals engaged in benchmarking large language models (LLMs), including contributors to all the benchmarks herein presented. Researchers from the Digital Safety Research Institute (DSRI) of the UL Research Institutes maintain the independence of this work by "holding the pen" on the work. DSRI's funding arises from Underwriter's Laboratories more than 100 years of running safety testing and certification and has not received external funding for the production of this work.
- **Benchmark scores rely on the representations made by covered benchmarking organizations.**
- The benchmark benchmark is intended to serve as a guide for producing and adopting best-in-class LLM benchmarks, but this work and its associated scores are not a substitute for learning more about the covered benchmarks and developing an independent sense for their reliability.

