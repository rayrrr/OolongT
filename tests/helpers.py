""" Test Helpers """
from random import shuffle


def snip(val, max_len=20, separator=' ', ellip="..."):
    """Truncate text

    Arguments:
        val {str} -- string to snip

    Keyword Arguments:
        max_len {int} -- maximum length of string (default: {20})
        separator {str} -- if list passed,
            string to join members (default: {' '})
        ellip {str} -- filler text if truncated (default: {"..."})

    Returns:
        str -- text, truncated if necessary
    """

    text = val

    if isinstance(val, list):
        text = separator.join(val)

    if len(text) <= max_len:
        return text

    return text[:max_len-len(ellip)] + ellip


def randomize_list(src):
    """Reorder a copy of the supplied list

    Arguments:
        src {list} -- source list

    Returns:
        list -- copy of source list in different order
    """
    dupe = list(src)
    while dupe == src:
        shuffle(dupe)

    return dupe


def compare_float(val1, val2):
    """Compare two floating point values

    Arguments:
        val1 {float} -- value 1
        val2 {float} -- value 2

    Returns:
        bool -- the two values are close enough
    """
    return (abs(val1 * 100000 - val2 * 100000) < 2.0)


def compare_list(left, right):
    """Compare left to right, generate diff

    Arguments:
        left {List[Any]} - reference list
        right {List[Any]} - list to compare against

    Returns:
        str -- length of left list, REPR of exclusive values

    >>> compare_list([1, 2, 3], [2, 3, 4])
    "len: 3, exclusive: ['1']"
    >>> compare_list([1, 2, 3], [1, 2, 3, 4])
    'len: 3, exclusive: []'
    """
    len_str = 'len: ' + str(len(left))
    diff_str = 'exclusive: ' + str([repr(x) for x in left if x not in right])

    return ', '.join([len_str, diff_str])


def compare_dict(left, right, keys=False):
    """Compare left to right

    Arguments:
        left {Dict} -- lowest common denominator Dict
        right {Dict} -- Dict that should contain the same values

    Keyword Arguments:
        keys {List[any]} -- keys to compare instead of left.keys()
    >>> compare_dict({1: 1}, {1: 1})
    True
    >>> compare_dict({1: 1}, {1: 1, 2: 2})
    True
    >>> compare_dict({1: 1, 2: 2}, {1: 1})
    False
    >>> compare_dict({1: 1, 2: 2}, {1: 1}, keys=[1])
    True
    """
    keys = keys or left.keys()
    same = True

    for key in keys:
        comp = right.get(key, None)

        if isinstance(left[key], float) or isinstance(comp, float):
            same = compare_float(left[key], comp)
        else:
            same = (left[key] == comp)

        if not same:
            break

    return same


def assert_ex(msg, result, expected, hint=None):
    """Generate detailed AssertionError exceptions

    Arguments:
        msg {str} -- description of error
        result {any} -- outcome of test
        expected {any} -- expected outcome of test

    Returns:
        bool -- tested condition

    >>> rv = [0]
    >>> ev = [1]
    >>> assert_ex('Mismatch', rv, ev)[:63]
    "Mismatch\\nresult   > len: 1, exclusive: ['0']\\nexpected > len: 1,"
    >>> rv = int(1)
    >>> rc = len(str(rv))
    >>> ev = float(1)
    >>> ec = len(str(ev))
    >>> assert_ex('Precision', rv, ev, hint='float')
    "Precision ('float')\\nresult   > 1\\nexpected > 1.0"
    """
    if hint is not None:
        hint = ' (' + repr(hint) + ')'
    else:
        hint = ''

    res_str = str(result)
    exp_str = str(expected)

    if isinstance(result, list) and isinstance(expected, list):
        res_str = compare_list(result, expected)
        exp_str = compare_list(expected, result)

    return '\n'.join([
        msg + hint,
        'result   > ' + res_str,
        'expected > ' + exp_str])
