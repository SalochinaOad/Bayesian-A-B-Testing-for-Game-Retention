# Bayesian A/B Testing for Game Retention

The goal of this analysis is to determine whether introducing a new in-game level gate ("gate_40") leads to an improvement in user retention compared to the existing gate ("gate_30"). Using data from a mobile game A/B test, the task is to evaluate the effectiveness of the treatment group (gate_40) on Day 1 retention by estimating the probability that users in the treatment group are more likely to return to the game the next day, relative to those in the control group.

### Methodology
Bayesian inference was used to model the retention behavior of users in both control and treatment groups. The following approach was applied:

1. Prior Distributions:
Both group retention probabilities were modeled using uniform Beta(1, 1) priors, reflecting no prior assumptions.

2. Likelihood:
User retention outcomes (binary) were modeled using Bernoulli distributions, conditional on the respective group’s retention probability.

3. Posterior Sampling:
Markov Chain Monte Carlo (MCMC) sampling was performed using PyMC to approximate the posterior distributions of retention probabilities for each group.

4. Probability Estimation:
The final probability, P(p_treatment > p_control), was computed as the proportion of posterior samples where the treatment retention rate exceeded that of the control.

### Findings:
This app calculates the posterior probability that the treatment group (e.g., users shown gate_40) performs better than the control group (gate_30) in terms of retention on day 1.

P(p_treatment > p_control) = 24.00%

This means that, based on the observed data and the Bayesian model, there is only a 24% probability that the treatment outperforms the control. In other words, there's a 76% chance that the control group actually leads to better or equal retention.

This evidence suggests that the new feature version (gate_40) is likely not more effective than the original (gate_30), and adopting it may not improve retention.
