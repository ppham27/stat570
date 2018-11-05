"""Implements a Gibbs sampler for use with TensorFlow Probability."""

import collections
import functools
from typing import List, Callable, NamedTuple, Tuple

import tensorflow as tf
import tensorflow_probability as tfp

GibbsSamplingKernelResults = NamedTuple(
    'GibbsSamplingKernelResults',
    [
        ('log_acceptance_correction', tf.Tensor),
        ('target_log_prob', tf.Tensor),
        ('steps_completed', tf.Tensor),
    ])

class GibbsSamplingKernel(tfp.mcmc.TransitionKernel):
    """Makes a transition kernel that does sequential Gibbs sampling.
    
    Args:
      samplers: A list of samplers that take a slice of state and return a
        distribution.
      target_log_prob_fn: A function to compute the log probability of state.            
    """
    def __init__(self,
                 samplers: List[Callable[[List[tf.Tensor]], tfp.distributions.Distribution]],
                 target_log_prob_fn: Callable[[List[tf.Tensor]], tf.Tensor],
                 name='gibbs_sampling_kernel') -> None:
        self._name = name
        self._samplers = samplers
        self._target_log_prob_fn = target_log_prob_fn
    
    def one_step(self,
                 current_state: List[tf.Tensor],
                 previous_kernel_results: GibbsSamplingKernelResults) -> Tuple[
                     List[tf.Tensor], GibbsSamplingKernelResults]:
        """Progress one step in the chain.

        Each step only updates one element of state. Consider specifying
        `num_steps_between_results` in tfp.mcmc.sample_chain as len(samplers) - 1
        to obtain entirely new states for each result.
        """
        def update_state(current_state: List[tf.Tensor], i: int):
            """Updates the ith slice of state."""
            head, tail = current_state[:i], current_state[(i + 1):]
            return head + [self._samplers[i](*(head + tail)).sample()] + tail

        num_samplers = len(self._samplers)
        previous_target_log_prob = previous_kernel_results.target_log_prob
        steps_completed = previous_kernel_results.steps_completed

        with tf.name_scope(''.join([self._name, 'bootstrap_results']),
                           values=current_state + [previous_target_log_prob, steps_completed]):            
            pred_fn_pairs = [
                (tf.equal(tf.mod(steps_completed, num_samplers), i),
                 functools.partial(update_state, current_state, i))
                for i in range(num_samplers)]
            next_state = tf.case(pred_fn_pairs)
        
            target_log_prob = self._target_log_prob_fn(*next_state)        
            kernel_results = GibbsSamplingKernelResults(
                target_log_prob=target_log_prob,
                log_acceptance_correction=previous_target_log_prob - target_log_prob,
                steps_completed=steps_completed + 1)
        
            return next_state, kernel_results
    
    def bootstrap_results(self, init_state: List[tf.Tensor]) -> GibbsSamplingKernelResults:
        """Initiates results based off of initial state.

        Args:
          init_state: Initial state, usually specified in `current_state` of
            tfp.mcmc.sample_chain.

        Returns:
          Initial accumulated results to begin the chain.
        """
        with tf.name_scope(
            '_'.join([self._name, 'bootstrap_results']),
            values=init_state):
            target_log_prob = self._target_log_prob_fn(*init_state)
            return GibbsSamplingKernelResults(
                log_acceptance_correction=tf.zeros_like(target_log_prob),
                target_log_prob=target_log_prob,
                steps_completed=tf.constant(0, dtype=tf.int64))
    
    @property
    def is_calibrated(self) -> bool:
        """Returns False even though Gibbs sampling always accepts.

        GibbsSamplingKernel is actually calibrated, but set as False to avoid
        warning when used with tfp.mcmc.MetropolisHastings.
        """
        return False
