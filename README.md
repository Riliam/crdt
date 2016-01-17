Here is trivial single-threaded emulation of a few CRDT objects, described in
[A comprehensive study of Convergent and Commutative Replicated Data Types](http://hal.upmc.fr/inria-00555588/document).

Also, WordCountMap object is built on top of concepts introduced by paper.
Example usage:


    In [1]: from datatypes import WordCountMap

    In [2]: a = WordCountMap()

    In [3]: b = WordCountMap()

    In [4]: c = WordCountMap()

    In [5]: a.add('a b c d e f')

    In [6]: a.get_top(10)
    Out[6]: [('c', 1), ('d', 1), ('f', 1), ('e', 1), ('a', 1), ('b', 1)]

    In [7]: b.get_top(10)
    Out[7]: [('e', 1), ('d', 1), ('f', 1), ('c', 1), ('a', 1), ('b', 1)]

    In [8]: c.add('a b c d')

    In [9]: a.get_top(10)
    Out[9]: [('c', 2), ('d', 2), ('a', 2), ('b', 2), ('f', 1), ('e', 1)]

    In [10]: c.get_top(10)
    Out[10]: [('d', 2), ('c', 2), ('a', 2), ('b', 2), ('e', 1), ('f', 1)]
