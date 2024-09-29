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

"""Base interface for evaluator functions."""

from typing import Generic, NamedTuple, Protocol, TypeVar

from boax.utils.typing import Numeric

T = TypeVar('T')


class InitFn(Protocol, Generic[T]):
  """
  A callable type for policy evaluator's init functions.

  An init function returns the initial set of parameters.
  """

  def __call__(self) -> T:
    """
    Initialise the parameters.

    Returns:
      The initial parameters.
    """


class UpdateFn(Protocol, Generic[T]):
  """
  A callable type for policy evaluator's update functions.

  An update function takes a set of parameters of type `T`,
  the selected variant, and a reward as input and returns an updated set of parameters.
  """

  def __call__(self, params: T, variant: Numeric, reward: Numeric) -> T:
    """
    Update the parameters.

    Args:
      params: The policy's parameters.
      variant: The selected variant.
      reward: The received reward.

    Returns:
      The updated paramters.
    """


class Evaluator(NamedTuple, Generic[T]):
  """
  A policy evaluator.

  The evaluator is defined by a set of an `init` and an `update` function.
  """

  init: InitFn[T]
  update: UpdateFn[T]
