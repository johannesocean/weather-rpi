#!/usr/bin/env python3
"""
Created on 2021-11-21 18:22

@author: johannes
"""
import pandas as pd


class QCRanges:
    """Doc."""

    def __init__(self, serie, qc_range):
        self.serie = serie.copy()
        self.qc_range = qc_range
        # print(serie.name, self.qc_range)

    def __call__(self):
        """Return a QC checked pd.Series."""
        boolean = (self.serie < float(self.qc_range[0])) | (self.serie > float(self.qc_range[1]))
        if boolean.any():
            self.serie[boolean] = None
        return self.serie
