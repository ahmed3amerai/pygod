# -*- coding: utf-8 -*-
"""
Metrics used to evaluate the anomaly detection performance
"""
# Author: Yingtong Dou <ytongdou@gmail.com>
# License: BSD 2 clause

import numpy as np
from sklearn.metrics import roc_auc_score


def eval_rocauc(labels, pred):
    """
    Description
    -----------
    ROC-AUC score for binary classification.

    Parameters
    ----------
    labels : numpy.array
        Labels in shape of ``(N, )``, where 1 represents outliers,
        0 represents normal nodes.
    pred : numpy.array
        Outlier scores in shape of ``(N, )``.

    Returns
    -------
    rocauc : float
        Average ROC-AUC score across different labels.
    """

    # anomaly detection is a binary classification problem
    return roc_auc_score(y_true=labels, y_score=pred[:, 1])


def eval_recall_at_k(labels, pred, k):
    """
    Description
    -----------
    Recall score for top k instances with the highest outlier scores.

    Parameters
    ----------
    labels : numpy.array
        Labels in shape of ``(N, )``, where 1 represents outliers,
        0 represents normal nodes.
    pred : numpy.array
        Outlier scores in shape of ``(N, )``.
    k : int
        The number of instances to evaluate.

    Returns
    -------
    recall_at_k : float
        Recall for top k instances with the highest outlier scores.
    """

    scores = [(s, l) for s, l in zip(pred, labels)]
    scores.sort(reverse=True, key=lambda x: x[0])
    threshold = 0.5

    # Number of true outliers
    n_true = sum(l for (_, l) in scores)

    # Number of true positive instances in top k
    n_true_and_pred_k = sum((l and (s >= threshold)) for (s, l) in scores[:k])

    recall_at_k = n_true_and_pred_k / n_true if n_true != 0 else 0

    return recall_at_k


def eval_precision_at_k(labels, pred, k):
    """
    Description
    -----------
    Precision score for top k instances with the highest outlier scores.

    Parameters
    ----------
    labels : numpy.array
        Labels in shape of ``(N, )``, where 1 represents outliers,
        0 represents normal nodes.
    pred : numpy.array
        Outlier scores in shape of ``(N, )``.
    k : int
        The number of instances to evaluate.

    Returns
    -------
    precision_at_k : float
        Precision for top k instances with the highest outlier scores.
    """

    scores = [(s, l) for s, l in zip(pred, labels)]
    scores.sort(reverse=True, key=lambda x: x[0])
    threshold = 0.5

    # Number of predicted outliers in top k
    n_pred_k = sum((s >= threshold) for (s, _) in scores[:k])

    # Number of true positive instances in top k
    n_true_and_pred_k = sum((l and (s >= threshold)) for (s, l) in scores[:k])

    precision_at_k = n_true_and_pred_k / n_pred_k if n_pred_k != 0 else 0

    return precision_at_k
