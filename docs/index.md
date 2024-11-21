# Benchmarks' Benchmark (B~2~)

!!! warning
    You are viewing pre-release benchmark documentation. Please return after the benchmark is made broadly available and do not share this URL.

Large language model (LLM) benchmarks enable system use decisions informed by LLM properties, but benchmarks may be rendered unreliable for real world decision making by a variety of threats to benchmark longevity, correctness, coverage, consistency, and intelligibility. Motivated by emerging LLM safety benchmarks, on whose scores people rely on to make decisions impacting real world safety, this work presents a benchmark for LLM benchmarks inspired by National Institute of Standards and Technology risk management processes. **High scores indicate a reduced likelihood and/or severity of inappropriate reliance on a benchmark.**

## B~2~ Results

!!! warning
    These are filler results pending updates from the benchmarked benchmarks.

{{ read_file('docs/data/table.md') }}

## Scoring Points in B~2~

Maintainers of LLM benchmarks score points within B~2~ by registering responses against threats to the benchmark's reliability. Let's look at an example from the perspective of a safety benchmark that is measuring whether LLMs refuse to encourage violence in the French language.

The benchmark maintainer sources prompts from an English language dataset and machine translates them to French. Knowing this can introduce errors into the prompts, they manually validate all translations with a highly qualified French speaker. Getting credit for this validation activity involves:

**(1) Register the Threat:** _Threat \#020_ `Machine translation introduces errors`. `Severity: 1.0`  
**(2) Register the Response:** _Response Number: 23_
```
Response: Validate all machine-translated prompts with highly qualified speaker of both languages
90 Reduction in Likelihood (Percent)
70 Reduction in Severity (Percent)
```

Now by affirming response number 23 is in place, all benchmark maintainers can score points proportionate to the reduced risk as determined by `likelihood*severity`.

View the complete list of [mitigations](data/risk-response-table.md). Submit a mitigation by [opening a Github issue](https://github.com/ul-dsri/party-paper/issues) or emailing sean.mcgregor-at-ul.org.

## Research Paper

The following are versioned releases of the research paper associated with this work. A snapshot of the paper will be submitted for peer review in May 2025.

[![first page](images/first_page.png){align=right}]( {{ get_latest_pdf_url() }} )

## Paper History

{{ get_latest_pdf_anchor() }}{{ get_pdf_list_from_s3() }}

Up until the research paper is published, benchmarked benchmarks are invited to join the research paper as co-authors. Coauthoring the paper is not required, but is encouraged. You can find the current list of co-authors on the latest paper. Contributions to the research paper are welcome via email (sean.mcgregor-at-ul.org), or on the [Github respository](https://github.com/ul-dsri/party-paper). Please reach out via those means to discuss.

## Independence

- The benchmark benchmark is intended to serve as a guide for producing and adopting best-in-class LLM benchmarks, but this work and its associated scores are not a substitute for learning more about the covered benchmarks and developing an independent sense for their reliability.
- Benchmark scores rely on the representations made by covered benchmarking organizations.
- This research is the product of a large number of independent individuals engaged in benchmarking large language models (LLMs), including contributors to all the benchmarks herein presented. Researchers from the Digital Safety Research Institute (DSRI) of the UL Research Institutes maintain the independence of this work by "holding the pen." DSRI's funding arises from Underwriter's Laboratories more than 100 years of running safety testing and certification and has not received external funding for the production of this work.
