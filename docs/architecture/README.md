# Architecture Diagrams

**DATSCI7030 — Causal Event-Driven Market Impact Modelling** · Version 1.1

---

## Diagram Index

| File | What it shows | Status |
|------|---------------|--------|
| `ml_project_map.svg` | 5-phase ML project overview (data → features → ARIMA → XGBoost → validation) | ✅ Current |
| `full_system_architecture.svg` | 13-phase master blueprint: all data sources, processing, NLP, causal inference, modelling, results | ✅ Current |
| `data_pipeline_architecture.svg` | Compact 5-stage pipeline: sources → scrapers → raw → event catalogue → analysis branches | ✅ Current |
| `causal_dag_dowhy.svg` | Causal DAG (Directed Acyclic Graph) — DoWhy structural causal model with confounders, treatment, mediators, outcome, and 4-step estimation pipeline | ✅ Current — **new** |
| `datsci7030_project_structure.svg` | Full project directory tree with purpose annotations for every folder and file | ✅ Current — **new** |
| `hybrid_model.svg` | Dual-layer hybrid model: ARIMA (Layer 1) + FinBERT NLP (Layer 2) → combined feature vector → XGBoost + logistic classifier | ✅ Current |
| `arima_pipeline.svg` | 6-stage ARIMA intervention analysis pipeline: event catalogue → window definition → ARIMA fit → intervention specification → abnormal return measurement → significance testing | ✅ Current |
| `car_formula.svg` | Annotated CAR formula reference: CARₑₐ(t₁,t₂) = Σ(Rₜₐ − E[Rₜₐ]) with all index and term definitions | ✅ Current |
| `intervention_equation.svg` | Annotated intervention equation: Yₜ = ωIₜ/(1−δB) + ARIMA noise — pulse vs step intervention shapes | ✅ Current |
| `phase5_validation_pipeline.svg` | Validation pipeline: temporal split → out-of-sample testing → benchmark comparison → SHAP → report/dashboard | ✅ Current |
| `project_structure.svg` | **Deprecated** — superseded by `datsci7030_project_structure.svg` | ⚠️ Old — references `govfin/` structure |

---

## Diagram Relationships

```
ml_project_map.svg          ← start here: project overview
    │
    ├── data_pipeline_architecture.svg   ← zoom into data flow
    ├── full_system_architecture.svg     ← full 13-phase detail
    │
    ├── causal_dag_dowhy.svg             ← causal inference layer (DoWhy)
    ├── hybrid_model.svg                 ← ARIMA + FinBERT combination
    │
    ├── arima_pipeline.svg              ← ARIMA methodology detail
    ├── intervention_equation.svg       ← ARIMA maths reference
    ├── car_formula.svg                 ← CAR maths reference
    │
    ├── phase5_validation_pipeline.svg  ← evaluation & reporting
    └── datsci7030_project_structure.svg ← codebase layout
```

---

## Notes

- `.ipynb_checkpoints/` in this folder is a Jupyter artefact — already in `.gitignore`, safe to ignore
- `.DS_Store` files are macOS artefacts — already in `.gitignore`
- All diagrams are SVG (scalable, no resolution loss in dissertation PDF export)
- To embed in dissertation: use `<img>` tag or insert via Word's Insert → Pictures
