# Benchmarks' Benchmark (B~2~)

!!! warning
    You are viewing pre-release benchmark documentation. This benchmark of LLM benchmark reliability is not currently reliable.

If you are viewing this, you are likely a benchmark author that has graciously agreed to score their benchmark with B~2~. The process should be quick and painless. We recommend reading the "about" section below, then reading proceeding to the [questionnaire](questionnaire).

## About ##

Large language model (LLM) benchmarks enable system use decisions informed by LLM properties, but benchmarks may be rendered unreliable for real world decision making by a variety of threats to benchmark longevity, correctness, coverage, consistency, and intelligibility. Motivated by emerging LLM safety benchmarks, on whose scores people rely on to make decisions impacting real world safety, this work presents a benchmark for LLM benchmarks inspired by National Institute of Standards and Technology risk management processes. **High scores indicate a reduced likelihood and/or severity of inappropriate reliance on a benchmark.**

## Scoring Points in B~2~

Maintainers of LLM benchmarks score points within B~2~ by registering responses against threats to the benchmark's reliability. Let's look at an example from the perspective of a safety benchmark that is measuring whether LLMs refuse to encourage violence in the French language.

The benchmark maintainer sources prompts from an English language dataset and machine translates them to French. Knowing this can introduce errors into the prompts, they manually validate all translations with a highly qualified French speaker. Getting credit for this validation activity involves:

**(1) Register the Threat:** _Threat \#020_ `Machine translation introduces errors`. `Severity: 1.0` `Likelihood: 1.0`  
**(2) Register the Response:**
```
Response 23: Validate all machine-translated prompts with highly qualified speaker of both languages
90 Reduction in Likelihood (Percent)
70 Reduction in Severity (Percent)
```

Now by affirming response number 23 is in place, all benchmark maintainers can score points proportionate to the reduced risk as determined by `likelihood*severity` (post response) - `likelihood*severity` (before). So response 23 provides `(0.1*0.3) - (1.0*1.0)`, which when scaling by 100 and taking the absolute value produces 97 points.

Now all other benchmarks can similarly score these points by either affirming they have response 23 in place. Alternatively, they can also register their own response, such as,

**(2) Register the Response:**
```
Response 24: Do not translate any prompts. Source prompts exclusively within the target languages.
100 Reduction in Likelihood (Percent)
0 Reduction in Severity (Percent)
```

Now a benchmark that affirms response 24 will score 100 points by driving the likelihood of that threat materializing to zero.

You can view the complete list of [mitigations](data/risk-response-table.md) and submit new mitigations by [opening a Github issue](https://github.com/ul-dsri/party-paper/issues) or emailing sean.mcgregor-at-ul.org.

## Research Paper

The following are versioned releases of the research paper associated with this work. A snapshot of the paper will be submitted for peer review in May 2025. All benchmark authors scoring their benchmarks with B~2~ will be invited, but not expected, to collaborate on the research paper.

[![first page](images/first_page.png){align=right}]( {{ get_latest_pdf_url() }} )

## Paper History

{{ get_latest_pdf_anchor() }}{{ get_pdf_list_from_s3() }}

You can find the current list of co-authors on the latest paper. Contributions to the research paper are welcome via email (sean.mcgregor-at-ul.org), or on the [Github respository](https://github.com/ul-dsri/party-paper). Please reach out via those means to discuss.

## Independence

- The benchmark benchmark is intended to serve as a guide for producing and adopting best-in-class LLM benchmarks, but this work and its associated scores are not a substitute for learning more about the covered benchmarks and developing an independent sense for their reliability.
- Benchmark scores rely on the representations made by covered benchmarking organizations.
- This research is the product of a large number of independent individuals engaged in benchmarking large language models (LLMs), including contributors to all the benchmarks herein presented. Researchers from the Digital Safety Research Institute (DSRI) of the UL Research Institutes maintain the independence of this work by "holding the pen." DSRI's funding arises from Underwriter's Laboratories more than 100 years of running safety testing and certification and has not received external funding for the production of this work.
