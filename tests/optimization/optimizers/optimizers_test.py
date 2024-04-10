from operator import itemgetter

from absl.testing import absltest, parameterized
from jax import numpy as jnp
from jax import random

from boax.optimization import optimizers


class OptimizersTest(parameterized.TestCase):
  def test_batch(self):
    key = random.key(0)
    num_samples, num_restarts, q, d = 100, 10, 3, 1

    initializer = lambda k, x, _, n: random.choice(k, x, (n,))
    solver = lambda fun, _, c: (c, fun(c))

    acqf = itemgetter((..., 0, 0))
    bounds = jnp.array([[-1.0, 1.0]])

    next_x, next_a = optimizers.batch(initializer, solver)(
      key,
      acqf,
      bounds,
      q,
      num_samples,
      num_restarts,
    )

    self.assertEqual(next_x.shape, (q, d))
    self.assertEqual(next_a.shape, ())

  def test_sequential(self):
    key = random.key(0)
    num_samples, num_restarts, q, d = 100, 10, 3, 1

    initializer = lambda k, x, _, n: random.choice(k, x, (n,))
    solver = lambda fun, _, c: (c, fun(c))

    acqf = itemgetter((..., 0, 0))
    bounds = jnp.array([[-1.0, 1.0]])

    next_x, next_a = optimizers.sequential(initializer, solver)(
      key,
      acqf,
      bounds,
      q,
      num_samples,
      num_restarts,
    )

    self.assertEqual(next_x.shape, (q, d))
    self.assertEqual(next_a.shape, (q,))


if __name__ == '__main__':
  absltest.main()
