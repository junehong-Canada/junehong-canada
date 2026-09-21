---
title: "Traditional Algorithms vs. Edge AI Models: Choosing the Right Approach at the Edge"
description: "Not every problem on a microcontroller needs a neural network. A practical framework for deciding between threshold rules, classical DSP, and quantized ML models at the extreme edge."
date: "2026-09-21"
author: "June Hong"
tags: [Edge AI, Physical AI, Embedded Systems, Machine Learning]
---

## Introduction

Every few weeks I get asked some version of the same question: *"Should this run as a neural network, or can a simple threshold do the job?"*

It's a fair question, and on a microcontroller the answer has real consequences — flash budget, inference latency, power draw, and whether you can explain to a safety auditor exactly why the system made the decision it made. This post is the decision framework I actually use when architecting sensor-driven firmware for industrial safety systems: when to reach for a classical algorithm, when to reach for a quantized model, and when the right answer is both.

## What "Traditional" Means at the Edge

"Traditional algorithm" isn't a dismissal — it covers a wide, well-understood toolbox:

- **Threshold and hysteresis logic** — the workhorse of alarm systems. Fixed or slowly-adapting limits with debounce to avoid chatter.
- **Finite state machines** — deterministic transitions between known operating modes.
- **Classical DSP** — moving averages, FFT-based frequency analysis, Kalman filters for sensor fusion.
- **PID and control-loop math** — well-characterized, decades of tooling, easy to simulate before deployment.

These share three properties that matter enormously in industrial firmware: they are **deterministic**, **cheap to run**, and **easy to certify** — you can write down exactly why the system tripped, which matters when the output drives a fire suppression relay.

## What "Edge AI" Means Here

By Edge AI I mean models small enough to run directly on the MCU doing the sensing — not "AI in the cloud, edge just forwards data." On something like an ESP32-WROVER-E, that typically means:

- **Quantized TensorFlow Lite Micro models** — INT8 weights, a few hundred KB of arena, running in single-digit milliseconds per inference.
- **Small recurrent or convolutional architectures** (GRUs, 1D-CNNs) — suited to time-series sensor windows rather than single readings.
- **On-device feature extraction** feeding a lightweight classifier, rather than raw streams feeding a large model.

The appeal isn't "AI is smarter." It's that some failure signatures genuinely don't reduce to a clean threshold — a bearing that's *beginning* to fail doesn't cross a fixed vibration limit, it develops a shape over time that a model can learn and a human can't easily hand-code.

## The Comparison

| Dimension | Traditional Algorithm | Edge AI Model |
|---|---|---|
| Latency | Microseconds to low milliseconds | Milliseconds (quantized, MCU-class) |
| Memory footprint | Bytes to a few KB | Tens of KB to low MB (arena + weights) |
| Power draw | Minimal | Higher, but still edge-viable when quantized |
| Explainability | Fully traceable — "X exceeded Y for Z seconds" | Post-hoc at best; hard to certify a "why" |
| Handles novel/gradual patterns | Poorly — requires a human to define the rule | Well — learns shape from labeled data |
| Development cost | Low, fast to iterate and simulate | Higher — needs a labeled dataset and a training pipeline |
| Behavior under sensor noise/drift | Brittle unless carefully tuned | More robust if trained on representative noise |
| Regulatory/safety review | Straightforward | Requires additional validation evidence |

Neither column wins outright. The table is a set of trade-offs to weigh against what the system actually has to do.

## A Practical Decision Framework

I use four questions, roughly in this order:

1. **Does a human domain expert already know the rule?** If a fire-safety engineer can tell you "smoke obscuration above X% for more than Y seconds is unsafe," that's a threshold, not a model. Don't spend a training pipeline re-deriving knowledge you already have.
2. **Does the failure mode drive a safety-critical action?** If the output directly triggers suppression, shutdown, or an alarm relay, I default to deterministic logic for the *decision*, even if a model contributes a *signal* upstream of it.
3. **Is the pattern gradual, multivariate, or hard to hand-specify?** Bearing wear, motor imbalance, slow refrigerant leaks — these develop across several correlated channels over time. That's the model's home turf.
4. **What's the cost of a false negative vs. a false positive, and can you afford the model's calibration overhead to tune that trade-off?** Rules are easy to make conservative. Models need a labeled dataset that actually represents your failure distribution, which is often the real cost, not the inference itself.

## The Answer Is Usually Both

In practice, the systems I've shipped don't pick one column — they split responsibilities across a hard boundary. On a dual-core ESP32 industrial gateway, that looks like:

- **The deterministic core** owns protocol polling, safety thresholds, and anything that has to happen on a guaranteed schedule — Modbus/BACnet polling, hard alarm limits, watchdog-safe isolation.
- **The inference core** runs a quantized model against a rolling window of sensor features, purely to *flag anomalies for attention* — it never has direct authority over a suppression action.
- Rules still gate the final decision. The model's job is to catch the failure mode the rule-writer didn't think to encode, and hand it to a human — or to a rule — with enough lead time to matter.

That separation is what makes the AI half auditable: you can point to the exact rule that triggered an action, while still benefiting from a model that's watching for the pattern nobody wrote a threshold for.

## Guardrails: Protecting Against a Wrong Model Decision in Critical Cases

Deciding a problem genuinely needs a model is only half the job. The other half is making sure a wrong prediction never becomes a safety incident. On systems where the output drives a suppression relay, a shutdown, or anything else with real consequences, I treat the model as an **advisor, never the sole authority** — and I enforce that with specific guardrails, not good intentions:

- **Keep a deterministic hard limit as the final veto.** The model can raise or lower confidence, but a hard-coded, provable safety limit still has independent authority to trigger — and to block a model-driven action that would violate it. If the model says "safe" but the hard limit says the reading is out of range, the hard limit wins.
- **Require a confidence threshold, and define what happens below it.** Don't act on a raw class label — act on "class X with confidence ≥ N." Below that threshold, the system doesn't guess; it falls back to the traditional algorithm or escalates for review.
- **Demand temporal consistency, not a single inference.** A single high-confidence frame can be a sensor glitch. Require the model to agree across several consecutive windows (an N-of-M pattern) before a critical action fires — the same debounce principle a threshold system already uses, applied to model output.
- **Bound the action, not just the confidence.** Whatever the model outputs, clamp the resulting action to a physically plausible envelope. A model shouldn't be able to command a state the hardware or the safety case never anticipated.
- **Validate the input before you trust the output.** Detect out-of-range sensor values, stuck sensors, and inputs far outside the training distribution before they reach the model. A model asked to classify garbage will confidently classify garbage.
- **Choose a fail-safe default, deliberately.** Decide in advance what happens on model timeout, crash, or low confidence — and make that default the safe state, not "do nothing."
- **Log every decision with its inputs.** You lose the traceability of an if/else chain the moment you add a model, so you have to build it back: log the feature vector, confidence, and final action for every trip so a failure can be reconstructed.
- **Ship new models in shadow mode first.** Before a model gets authority over a critical action, run it in parallel with the existing deterministic system, logging what it *would* have done without acting on it. Compare the two before cutting over.
- **Monitor for drift after deployment.** A model validated on last year's sensor data can quietly degrade as hardware ages or conditions shift. Track prediction confidence and agreement with the deterministic layer over time — a slow decline is a signal to retrain, not a mystery to explain later.

| Guardrail | Failure Mode It Prevents |
|---|---|
| Deterministic veto | Model overrides a known, provable safety limit |
| Confidence threshold + fallback | Low-confidence guess treated as a certain decision |
| N-of-M temporal consistency | Single noisy frame triggers a critical action |
| Bounded action envelope | Model commands a physically implausible or unsafe state |
| Input validation / OOD detection | Model confidently misclassifies a faulty sensor reading |
| Fail-safe default | Timeout or crash silently falls back to "do nothing" |
| Decision logging | A wrong call can't be reconstructed or audited afterward |
| Shadow-mode rollout | An unproven model gets authority on day one |
| Drift monitoring | A model that degrades in production goes unnoticed |

None of this makes the model itself explainable. It makes the **system around the model** accountable — which is the actual requirement in a safety review. A model that's wrong 2% of the time is fine if the rest of the architecture is built to catch that 2% before it ever reaches the relay.

## Conclusion

The question isn't "rules or AI." It's "what does each part of this system actually need to guarantee, and which tool gives me that guarantee at the lowest cost." Deterministic logic stays the backbone of anything safety-critical. Edge AI earns its place specifically where the failure signature is too gradual, too multivariate, or too novel for a human to hand-write a clean rule — and it earns that place *alongside* the rules, not instead of them.
