# Copyright 2023 The Bojax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Alias for acquisition functions."""

import math

from jax import numpy as jnp
from jax import scipy

from bojax._src.optimization.acquisitions.base import Acquisition
from bojax._src.prediction.processes.base import Process
from bojax._src.typing import Array, Numeric
from bojax._src.util import compose


def scale_improvement(loc: Array, scale: Array, best: Numeric) -> Array:
  return (loc - best) / scale


def log_probability_of_improvement(
  best: Numeric, process: Process
) -> Acquisition:
  """
  The Log Probability of Improvement acquisition function.

  Logarithm of the probability of improvement over the best function value observed so far.

  `logPI(x) = log(P(y >= best_f)), y ~ f(x)`

  Args:
    best: The best function value observed so far.
    process: A gaussian posterior.

  Returns:
    The corresponding `Acquisition`.
  """

  def acquisition(candidates: Array, **kwargs) -> Array:
    loc, cov = process(candidates)
    scale = jnp.vectorize(compose(jnp.sqrt, jnp.diag), signature='(k,k)->(k)')(
      cov
    )
    x = scale_improvement(loc, scale, best)
    return scipy.stats.norm.logcdf(x)

  return acquisition


def log_expected_improvement(best: Numeric, process: Process) -> Acquisition:
  """
  The Log Expected Improvement acquisition function.

  Logarithm of the expected improvement over the best function value observed so far.

  `LogEI(x) = log(E(max(f(x) - best_f, 0))),`

  where the expectation is taken over the value of stochastic function `f` at `x`.

  References:
    Ament, Sebastian, et al. "Unexpected improvements to expected improvement for bayesian optimization."
    arXiv preprint arXiv:2310.20708 (2023).

  Args:
    best: The best function value observed so far.
    process: A gaussian posterior.

  Returns:
    The corresponding `Acquisition`.
  """

  _log2 = math.log(2)
  _neg_inv_sqrt_eps = -1e6
  _neg_inv_sqrt2 = -(2**-0.5)
  _log_sqrt_pi_div_2 = math.log(math.pi / 2) / 2

  def log1mexp(x):
    return jnp.where(-_log2 < x, jnp.log(jnp.expm1(-x)), jnp.log1p(jnp.exp(-x)))

  def erfcx(x):
    return jnp.exp(x**2) * scipy.special.erfc(x)

  def log_ei_eps(x):
    return log1mexp(
      jnp.log(erfcx(_neg_inv_sqrt2 * x) * jnp.abs(x)) + _log_sqrt_pi_div_2
    )

  def log_ei_upper(x):
    return jnp.log(scipy.stats.norm.pdf(x) + x * scipy.stats.norm.cdf(x))

  def log_ei_lower(x):
    return jnp.log(jnp.abs(x)) * -2

  def log_ei(x):
    bound = -1
    x_upper = jnp.where(x < bound, bound, x)
    x_lower = jnp.where(x > bound, bound, x)
    x_eps = jnp.where(x < _neg_inv_sqrt_eps, _neg_inv_sqrt_eps, x_lower)

    return jnp.where(
      x > bound,
      log_ei_upper(x_upper),
      scipy.stats.norm.logpdf(x)
      + jnp.where(
        x > _neg_inv_sqrt_eps, log_ei_eps(x_eps), log_ei_lower(x_lower)
      ),
    )

  def acquisition(candidates: Array, **kwargs) -> Array:
    loc, cov = process(candidates)
    scale = jnp.vectorize(compose(jnp.sqrt, jnp.diag), signature='(k,k)->(k)')(
      cov
    )
    x = scale_improvement(loc, scale, best)
    return log_ei(x)

  return acquisition


def upper_confidence_bound(beta: Numeric, process: Process) -> Acquisition:
  """
  The Upper Confidence Bound (UBC) acquisition function.

  Upper confidence bound comprises of the posterior mean plus an additional term:
  the posterior standard deviation weighted by a trade-off parameter, `beta`.

  `UCB(x) = loc(x) + sqrt(beta) * scale(x)`

  Args:
    beta: The mean and covariance trade-off parameter.
    process: A gaussian posterior.

  Returns:
    The corresponding `Acquisition`.
  """

  def acquisition(candidates: Array, **kwargs) -> Array:
    loc, cov = process(candidates)
    scale = jnp.vectorize(compose(jnp.sqrt, jnp.diag), signature='(k,k)->(k)')(
      cov
    )
    return loc + jnp.sqrt(beta) * scale

  return acquisition
