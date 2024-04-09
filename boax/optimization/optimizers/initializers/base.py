# Copyright 2023 The Boax Authors.
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

"""Base interface for initializers."""

from typing import Protocol

from boax.utils.typing import Array, PRNGKey


class Initializer(Protocol):
  """
  A callable type for the initialization step of an `Optimizer`.
  """

  def __call__(
    self, key: PRNGKey, x: Array, y: Array, num_restarts: int
  ) -> Array:
    """
    The initialization function.

    Args:
      key: A PRNG key.
      x: The initial index points.
      y: The initial scores.
      num_restarts: The number of restarts.

    Returns:
      The initial set of candidates.
    """
