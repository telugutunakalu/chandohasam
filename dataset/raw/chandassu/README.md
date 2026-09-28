# Kaggle Chandassu dataset (raw copy)

`Chandassu_Dataset.csv` is an unmodified copy of the Kaggle dataset
[boddusripavan111/chandassu](https://www.kaggle.com/datasets/boddusripavan111/chandassu) by Boddu
Sri Pavan and Boddu Swathi Sree. It contains 4,651 padyams from 28 satakams in 8 metres, with texts
from [andhrabharati.com](https://andhrabharati.com/). The dataset page declares the
[MIT License](https://opensource.org/license/mit); the authors' code is at
[BodduSriPavan-111/chandassu](https://github.com/BodduSriPavan-111/chandassu).

Please cite the authors' paper when using this data:

```bibtex
@misc{pavan2025computationalsociallinguisticstelugu,
  title={Computational Social Linguistics for Telugu Cultural Preservation: Novel Algorithms for Chandassu Metrical Pattern Recognition},
  author={Boddu Sri Pavan and Boddu Swathi Sree},
  year={2025},
  eprint={2510.01233}
}
```

`import_report.json` is written by `meter_engine/scripts/import_chandassu.py` when it builds
`dataset/chandassu.json` from the CSV. It records which CSV rows became which record. It also lists
every dropped row, with the reason and the record it matched: either a duplicate within the file,
or a poem already in `bhagavatam.json`, `vemana.json` or `kuchimanchi_timmakavi.json`.
