#!/usr/bin/env python3
"""
Created on 2021-11-21 18:22

@author: johannes
"""


class QCRanges:

    def __init__(self, serie, qc_range):
        self.serie = serie
        self.lower = float(qc_range[0])
        self.upper = float(qc_range[1])

    def __call__(self):
        """Return a QC checked data list.

        Replaces pandas boolean functionality.
        """
        # boolean = (self.serie < self.lower) | (self.serie > self.upper)
        # if boolean.any():
        #     self.serie[boolean] = None
        # return self.serie
        return [value if (self.lower < value < self.upper) else None for value in self.serie]
