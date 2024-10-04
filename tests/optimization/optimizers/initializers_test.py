from operator import itemgetter

from absl.testing import absltest, parameterized
from chex import assert_shape
from jax import random

from boax.core import samplers
from boax.optimization import optimizers
from boax.utils.typing import PRNGKey


class InitializersTest(parameterized.TestCase):
  @parameterized.parameters(
    {"key": random.key(0), "s": 10, "n": 5, "q": 3, "d": 1},
  )
  def test_q_batch(self, key: PRNGKey, s: int, n: int, q: int, d: int):
    fun = itemgetter((..., 0, 0))
    sampler = samplers.halton_uniform()

    initializer = optimizers.initializers.q_batch(
      fun,
      sampler,
      q,
      s,
      n,
    )

    result = initializer(key)

    assert_shape(result, (n, q, d))

  @parameterized.parameters(
    {"key": random.key(0), "s": 10, "n": 5, "q": 3, "d": 1},
  )
  def test_q_nonnegative(self, key: PRNGKey, s: int, n: int, q: int, d: int):
    fun = itemgetter((..., 0, 0))
    sampler = samplers.halton_uniform()

    initializer = optimizers.initializers.q_batch_nonnegative(
      fun,
      sampler,
      q,
      s,
      n,
    )

    result = initializer(key)

    assert_shape(result, (n, q, d))


if __name__ == '__main__':
  absltest.main()
