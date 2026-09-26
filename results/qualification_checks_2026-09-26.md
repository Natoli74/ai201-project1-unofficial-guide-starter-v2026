# Qualification checks

- Produced by: `tools/qualification_checks.py::main`
- Rounds: 3
- Corpus: `city_guides`

| Criterion | Round 1 | Round 2 | Round 3 |
|---|---:|---:|---:|
| 3. Gate refusal | 5 of 5 | 5 of 5 | 5 of 5 |
| 4. Chunk integrity | 100% | 100% | 100% |
| 5. Distance gap | 0.317-0.632 / 0.829-0.903 | 0.317-0.632 / 0.829-0.903 | 0.317-0.632 / 0.829-0.903 |

Criterion 3 is repeated as a deterministic gate check. Criterion 4
is repeated against all generated chunks. Criterion 5 is repeated
against all ten recorded distance measurements.
