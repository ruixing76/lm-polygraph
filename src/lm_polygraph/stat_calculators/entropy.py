import numpy as np

from typing import Dict, List, Tuple

from .stat_calculator import StatCalculator
from lm_polygraph.utils.model import WhiteboxModel


class EntropyCalculator(StatCalculator):
    """
    Calculates entropy of probabilities at each token position in the generation of a Whitebox model.
    """

    @staticmethod
    def meta_info() -> Tuple[List[str], List[str]]:
        """
        Returns the statistics and dependencies for the calculator.
        """

        return ["entropy"], ["greedy_log_probs"]

    def __init__(self):
        super().__init__()

    def __call__(
        self,
        dependencies: Dict[str, np.array],
        texts: List[str] = None,
        model: WhiteboxModel = None,
        max_new_tokens: int = 100,
        **kwargs,
    ) -> Dict[str, np.ndarray]:
        """
        Calculates the entropy of probabilities at each token position in the generation.

        Parameters:
            dependencies (Dict[str, np.ndarray]): input statistics, which includes:
                * 'greedy_log_probs' (List[List[float]]): log-probabilities of the generation tokens.
            texts (List[str]): Input texts batch used for model generation.
            model (Model): Model used for generation.
            max_new_tokens (int): Maximum number of new tokens at model generation. Default: 100.
        Returns:
            Dict[str, np.ndarray]: dictionary with List[List[float]] entropies calculated at 'entropy' key.
        """
        logprobs = dependencies["greedy_log_probs"]
        entropies = []
        for s_lp in logprobs:
            entropies.append([])
            for lp in s_lp:
                mask = ~np.isinf(lp)
                entropies[-1].append(-np.sum(np.array(lp[mask]) * np.exp(lp[mask])))
        return {"entropy": entropies}
