# AI Compute, by Function

*Photon Mountain substance. How each piece of the compute stack contributes to intelligence, grouped by what it does. Reframed from the Colorado AI seed on 2026-07-06 (PT-5); product statuses searched that day (see source block). Companion to `photonics_why_and_how.md`, which carries the corridor's photonics case in full.*

## How intelligence is produced (the one-paragraph version)

A modern AI model "thinks" by doing enormous amounts of one operation: matrix multiplication. Training builds the model by running that math across vast data. It is the compute-hungry phase. Inference runs the finished model to answer a prompt, lighter but still the same math. Producing intelligence means doing that math fast, feeding it data, holding the model in memory, and wiring many chips together so they act as one brain. Each function below plays one role in that chain.

**The chain, compressed:** the CPU directs the work and feeds the data. The GPU or TPU does the math that is the thinking. Memory holds the model. The interconnect ties many chips into one brain. Integration packs them tightly, and the AI data center houses it all at scale. Photonics makes the math and the connections faster and cooler. That is the corridor's layer.

## What the columns mean

- **What it contributes to intelligence:** the one thing this component adds to producing AI.
- **Used in:** where it shows up in the AI lifecycle. One of four values only: **Training** (building the model), **Inference** (running the finished model), **Both**, or **Separate track** (outside the training and inference pipeline).

---

## 1. Do the thinking (the compute)

The AI math happens here. The matrix multiplication these chips run *is* the model's thinking.

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **GPU** | Runs the parallel matrix math that *is* the model's thinking. More power means bigger, smarter models, trained faster. | Both |
| **TPU** | The same math on a chip built only for AI, so more performance per watt and per dollar. | Both |
| **Photonic processor** (emerging) | Will do that same math with light at far lower energy, so more intelligence per watt. An inference-first bet for the back half of the decade, not a near-term certainty. | Inference |

## 2. Direct the work (control)

Orchestrates everything and keeps the accelerators fed.

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **CPU** | Runs the system and feeds data to the accelerators. It does no AI math itself, but nothing runs without it. | Both |

## 3. Hold the knowledge (memory)

Stores what the model knows and what it is working on.

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **Memory** (RAM, HBM) | Holds the model's weights (its learned knowledge) and the data in flight. Bigger, faster memory means bigger models and longer context, and it is often the real bottleneck. | Both |

## 4. Connect the brains (interconnect)

Wires many chips into one brain. This is the layer where light wins first, and the corridor's materials companies sell into it (see `photonics_why_and_how.md`).

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **Interconnect** (NVLink, optical and co-packaged optics) | Links chips so thousands act as one giant brain. Frontier models are too big for one chip, so link speed sets how large a model you can build. Matters most in training. | Both |

## 5. Pack it together (integration)

Combines compute and memory in one tight package to cut the data-movement penalty, which raises usable intelligence per watt and per rack.

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **SoC** (System on a Chip) | Puts compute and memory on one module so data travels less, more usable compute per watt (Apple M-series). | Both |
| **Superchip** | Fuses a CPU and GPU(s) plus memory into one module for the same payoff at data-center scale. Nvidia Grace Blackwell ships today. Vera Rubin is announced, targeting early 2027. | Both |
| **APU** (Accelerated Processing Unit) | Puts CPU and GPU on one package for tighter integration and higher efficiency (AMD MI300A). | Both |

## 6. House it at scale (facilities)

Where thousands of the above combine, with power and cooling, to train and serve frontier AI. Energy is the binding constraint at this layer, which is why the corridor's energy-for-compute work matters (see `energy_why_and_how.md`).

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **AI data center** | Combines thousands of chips, memory, interconnect, power, and cooling. Facility scale roughly sets the scale of intelligence you can build. | Both |
| **AI supercomputer** | One very large, tightly-linked cluster aimed at the largest models. | Training |

## 7. A separate track (quantum)

A different computing paradigm, not part of today's neural-network AI math. Photon Mountain claims only the light-based slice: quantum optics research and the photonic-integrated-circuit fab in Arvada, which serves quantum and classical photonics alike. The broader quantum story (materials discovery, the statewide quantum economy) belongs to the Colorado AI project, not this one.

| Component | What it contributes to intelligence | Used in |
|---|---|---|
| **QPU** | The quantum processor (qubits), a different paradigm, not the matrix math AI runs on today. | Separate track |

## Training vs inference, in plain terms

- **Training** is the heaviest-demand phase: the most chips, memory, interconnect, and power. This is what the frontier labs race on.
- **Inference** is lighter per query but runs constantly at huge volume. It is where efficiency per watt matters most, and so where photonics makes its compute bet.

## Where the corridor plugs in

Two layers are the live opportunity. **Photonics** sits at the "connect the brains" layer today, where optical interconnects are the surest near-term win, and at the "do the thinking" layer tomorrow, where photonic compute is emerging. **Energy for compute** is what makes the "house it at scale" layer possible, because the facilities are limited by power more than by anything else. The full cases, with sources and honesty guardrails, are `photonics_why_and_how.md` and `energy_why_and_how.md`.

## Internal honesty guardrails

1. **The photonic processor row stays emerging.** It is an inference-first bet for the back half of the decade, not a shipping product at scale. Never move it to the present tense.
2. **Quantum stays a separate track.** It is not part of today's AI math, and this project claims only its light-based slice. Do not blend the QPU row into the AI pipeline.
3. **Product examples carry their real status.** Grace Blackwell ships today. Vera Rubin is announced, with first deployments targeted for early 2027, per Nvidia customer announcements. Update examples when the facts move.

## Sources (searched and verified 2026-07-06)

- Nvidia Vera Rubin platform: unveiled 2026, pairing Rubin GPUs with the Vera CPU. Initial deployments are targeted for the first quarter of 2027, per Nvidia customer announcements (Digi Power X 8-K, June 2026).
- Component roles (CPU, GPU, TPU, memory, interconnect, SoC, APU): stable, widely documented product categories; examples per vendor documentation (Apple, Nvidia, AMD).
- Photonic processor status and the interconnect-first timeline: sourced in `photonics_why_and_how.md` (searched 2026-07-06).
