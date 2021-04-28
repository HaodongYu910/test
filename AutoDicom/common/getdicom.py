# coding=utf-8
import os
import random

import pydicom
from tqdm import tqdm
import time
import logging

logger = logging.getLogger(__name__)

def getDicomServe(**kwargs):
    PID = kwargs['PID'],
    destIP = kwargs['destIP']
    destUSR = kwargs['destUSR']
    destPSW = kwargs['destPSW']


    return
