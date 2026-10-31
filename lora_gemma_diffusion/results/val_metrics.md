# Validation diagnostics: base vs adapters

120 E6 val poems (data/val.pt), loss on the poem positions (nats per Gemma token), fixed noise, no self-conditioning. Integrated = mean over t = 1/8 … 1 (an ELBO-like summary of our objective, not the model's own NELBO). T0 = the same prompt with an empty bhāvam line.

| measure | base | runs/lora-48k/lora_step_3000.pt | runs/lora-48k/lora.pt |
|---|---|---|---|
| integrated T1 | 4.1006 | 2.6004 | 2.5532 |
| T1 at t 0.25 | 1.9102 | 0.8323 | 0.7951 |
| T0 − T1 at t 0.25 | +0.1690 | +0.2017 | +0.2124 |
| T1 at t 0.5 | 3.4480 | 1.9125 | 1.8601 |
| T0 − T1 at t 0.5 | +0.4633 | +0.3777 | +0.4121 |
| T1 at t 0.75 | 5.3244 | 3.5561 | 3.4910 |
| T0 − T1 at t 0.75 | +1.0506 | +0.4321 | +0.5037 |
| T1 at t 1.0 | 7.6785 | 5.5640 | 5.5300 |
| T0 − T1 at t 1.0 | +0.1914 | +0.4309 | +0.5044 |

Per metre (T1, t = 0.5):

| metre | poems | base | runs/lora-48k/lora_step_3000.pt | runs/lora-48k/lora.pt |
|---|---|---|---|---|
| ataveladi | 8 | 3.466 | 1.927 | 1.853 |
| champakamala | 4 | 3.331 | 1.944 | 1.912 |
| kandamu | 46 | 3.473 | 1.867 | 1.809 |
| mattakokilamu | 2 | 3.822 | 2.300 | 2.221 |
| mattebhavikriditamu | 18 | 3.507 | 1.959 | 1.916 |
| sardulavikriditamu | 7 | 3.514 | 1.814 | 1.754 |
| seesamu | 21 | 3.295 | 1.912 | 1.866 |
| tetagiti | 2 | 3.049 | 1.722 | 1.802 |
| utpalamala | 12 | 3.526 | 2.023 | 1.961 |
