__all__ = ()


def merge_results(results_0, results_1):
    """
    Merges results.
    
    Parameters
    ----------
    results_0 : `None | list<NotificationSettings>`
        Results to merge.
    results_1 : `None | list<NotificationSettings>`
        Results to merge.
    
    Returns
    -------
    results : `None | list<NotificationSettings>`
    """
    if results_0 is None:
        return results_1
    
    if results_1 is None:
        return results_0
    
    results_0.extend(results_1)
    return results_0
