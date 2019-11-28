#!/usr/bin/env python2
## -*- coding: utf-8 -*-

from __future__          import print_function
from triton              import *
from unicorn             import *
from unicorn.arm_const   import *

import sys
import pprint
import random

ADDR  = 0x100000
STACK = 0x200000
HEAP  = 0x300000
SIZE  = 5 * 1024 * 1024
CODE  = [
    # ADC -------------------------------------------------------------------- #
    (b"\x02\x00\xa1\xe2", "adc r0, r1, #2"),
    (b"\x02\x00\xa1\x02", "adceq r0, r1, #2"),
    (b"\x02\x00\xa1\x12", "adcne r0, r1, #2"),
    (b"\x02\x00\xa1\x22", "adccs r0, r1, #2"),
    (b"\x02\x00\xa1\x32", "adccc r0, r1, #2"),
    (b"\x02\x00\xa1\x42", "adcmi r0, r1, #2"),
    (b"\x02\x00\xa1\x52", "adcpl r0, r1, #2"),
    (b"\x02\x00\xa1\x62", "adcvs r0, r1, #2"),
    (b"\x02\x00\xa1\x72", "adcvc r0, r1, #2"),
    (b"\x02\x00\xa1\x82", "adchi r0, r1, #2"),
    (b"\x02\x00\xa1\x92", "adcls r0, r1, #2"),
    (b"\x02\x00\xa1\xa2", "adcge r0, r1, #2"),
    (b"\x02\x00\xa1\xb2", "adclt r0, r1, #2"),
    (b"\x02\x00\xa1\xc2", "adcgt r0, r1, #2"),
    (b"\x02\x00\xa1\xd2", "adcle r0, r1, #2"),
    (b"\x02\x00\xa1\xe2", "adcal r0, r1, #2"),

    (b"\x03\x00\xa1\xe0", "adc r0, r1, r3"),
    (b"\x03\x00\xa1\x00", "adceq r0, r1, r3"),
    (b"\x03\x00\xa1\x10", "adcne r0, r1, r3"),
    (b"\x03\x00\xa1\x20", "adccs r0, r1, r3"),
    (b"\x03\x00\xa1\x30", "adccc r0, r1, r3"),
    (b"\x03\x00\xa1\x40", "adcmi r0, r1, r3"),
    (b"\x03\x00\xa1\x50", "adcpl r0, r1, r3"),
    (b"\x03\x00\xa1\x60", "adcvs r0, r1, r3"),
    (b"\x03\x00\xa1\x70", "adcvc r0, r1, r3"),
    (b"\x03\x00\xa1\x80", "adchi r0, r1, r3"),
    (b"\x03\x00\xa1\x90", "adcls r0, r1, r3"),
    (b"\x03\x00\xa1\xa0", "adcge r0, r1, r3"),
    (b"\x03\x00\xa1\xb0", "adclt r0, r1, r3"),
    (b"\x03\x00\xa1\xc0", "adcgt r0, r1, r3"),
    (b"\x03\x00\xa1\xd0", "adcle r0, r1, r3"),
    (b"\x03\x00\xa1\xe0", "adcal r0, r1, r3"),

    # ADC - ASR Shifter
    (b"\x42\x02\xa1\x00", "adceq r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x10", "adcne r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x20", "adccs r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x30", "adccc r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x40", "adcmi r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x50", "adcpl r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x60", "adcvs r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x70", "adcvc r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x80", "adchi r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\x90", "adcls r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\xa0", "adcge r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\xb0", "adclt r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\xc0", "adcgt r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\xd0", "adcle r0, r1, r2, asr #4"),
    (b"\x42\x02\xa1\xe0", "adcal r0, r1, r2, asr #4"),

    (b"\x52\x03\xa1\x00", "adceq r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x10", "adcne r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x20", "adccs r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x30", "adccc r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x40", "adcmi r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x50", "adcpl r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x60", "adcvs r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x70", "adcvc r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x80", "adchi r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\x90", "adcls r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\xa0", "adcge r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\xb0", "adclt r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\xc0", "adcgt r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\xd0", "adcle r0, r1, r2, asr r3"),
    (b"\x52\x03\xa1\xe0", "adcal r0, r1, r2, asr r3"),

    # ADC - LSL Shifter
    (b"\x02\x02\xa1\x00", "adceq r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x10", "adcne r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x20", "adccs r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x30", "adccc r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x40", "adcmi r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x50", "adcpl r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x60", "adcvs r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x70", "adcvc r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x80", "adchi r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\x90", "adcls r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\xa0", "adcge r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\xb0", "adclt r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\xc0", "adcgt r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\xd0", "adcle r0, r1, r2, lsl #4"),
    (b"\x02\x02\xa1\xe0", "adcal r0, r1, r2, lsl #4"),

    (b"\x12\x03\xa1\x00", "adceq r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x10", "adcne r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x20", "adccs r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x30", "adccc r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x40", "adcmi r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x50", "adcpl r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x60", "adcvs r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x70", "adcvc r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x80", "adchi r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\x90", "adcls r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\xa0", "adcge r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\xb0", "adclt r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\xc0", "adcgt r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\xd0", "adcle r0, r1, r2, lsl r3"),
    (b"\x12\x03\xa1\xe0", "adcal r0, r1, r2, lsl r3"),

    # ADC - LSR Shifter
    (b"\x22\x02\xa1\x00", "adceq r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x10", "adcne r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x20", "adccs r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x30", "adccc r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x40", "adcmi r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x50", "adcpl r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x60", "adcvs r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x70", "adcvc r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x80", "adchi r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\x90", "adcls r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\xa0", "adcge r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\xb0", "adclt r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\xc0", "adcgt r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\xd0", "adcle r0, r1, r2, lsr #4"),
    (b"\x22\x02\xa1\xe0", "adcal r0, r1, r2, lsr #4"),

    (b"\x32\x03\xa1\x00", "adceq r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x10", "adcne r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x20", "adccs r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x30", "adccc r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x40", "adcmi r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x50", "adcpl r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x60", "adcvs r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x70", "adcvc r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x80", "adchi r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\x90", "adcls r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\xa0", "adcge r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\xb0", "adclt r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\xc0", "adcgt r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\xd0", "adcle r0, r1, r2, lsr r3"),
    (b"\x32\x03\xa1\xe0", "adcal r0, r1, r2, lsr r3"),

    # ADC - ROR Shifter
    (b"\x62\x02\xa1\x00", "adceq r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x10", "adcne r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x20", "adccs r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x30", "adccc r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x40", "adcmi r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x50", "adcpl r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x60", "adcvs r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x70", "adcvc r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x80", "adchi r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\x90", "adcls r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\xa0", "adcge r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\xb0", "adclt r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\xc0", "adcgt r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\xd0", "adcle r0, r1, r2, ror #4"),
    (b"\x62\x02\xa1\xe0", "adcal r0, r1, r2, ror #4"),

    (b"\x72\x03\xa1\x00", "adceq r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x10", "adcne r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x20", "adccs r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x30", "adccc r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x40", "adcmi r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x50", "adcpl r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x60", "adcvs r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x70", "adcvc r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x80", "adchi r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\x90", "adcls r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\xa0", "adcge r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\xb0", "adclt r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\xc0", "adcgt r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\xd0", "adcle r0, r1, r2, ror r3"),
    (b"\x72\x03\xa1\xe0", "adcal r0, r1, r2, ror r3"),

    # ADC - RRX Shifter
    (b"\x62\x00\xa1\x00", "adceq r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x10", "adcne r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x20", "adccs r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x30", "adccc r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x40", "adcmi r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x50", "adcpl r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x60", "adcvs r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x70", "adcvc r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x80", "adchi r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\x90", "adcls r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\xa0", "adcge r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\xb0", "adclt r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\xc0", "adcgt r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\xd0", "adcle r0, r1, r2, rrx"),
    (b"\x62\x00\xa1\xe0", "adcal r0, r1, r2, rrx"),

    # ADCS ------------------------------------------------------------------- #
    (b"\x02\x00\xb1\xe2", "adcs r0, r1, #2"),
    (b"\x02\x00\xb1\x02", "adcseq r0, r1, #2"),
    (b"\x02\x00\xb1\x12", "adcsne r0, r1, #2"),
    (b"\x02\x00\xb1\x22", "adcscs r0, r1, #2"),
    (b"\x02\x00\xb1\x32", "adcscc r0, r1, #2"),
    (b"\x02\x00\xb1\x42", "adcsmi r0, r1, #2"),
    (b"\x02\x00\xb1\x52", "adcspl r0, r1, #2"),
    (b"\x02\x00\xb1\x62", "adcsvs r0, r1, #2"),
    (b"\x02\x00\xb1\x72", "adcsvc r0, r1, #2"),
    (b"\x02\x00\xb1\x82", "adcshi r0, r1, #2"),
    (b"\x02\x00\xb1\x92", "adcsls r0, r1, #2"),
    (b"\x02\x00\xb1\xa2", "adcsge r0, r1, #2"),
    (b"\x02\x00\xb1\xb2", "adcslt r0, r1, #2"),
    (b"\x02\x00\xb1\xc2", "adcsgt r0, r1, #2"),
    (b"\x02\x00\xb1\xd2", "adcsle r0, r1, #2"),
    (b"\x02\x00\xb1\xe2", "adcsal r0, r1, #2"),

    (b"\x03\x00\xb1\xe0", "adcs r0, r1, r3"),
    (b"\x03\x00\xb1\x00", "adcseq r0, r1, r3"),
    (b"\x03\x00\xb1\x10", "adcsne r0, r1, r3"),
    (b"\x03\x00\xb1\x20", "adcscs r0, r1, r3"),
    (b"\x03\x00\xb1\x30", "adcscc r0, r1, r3"),
    (b"\x03\x00\xb1\x40", "adcsmi r0, r1, r3"),
    (b"\x03\x00\xb1\x50", "adcspl r0, r1, r3"),
    (b"\x03\x00\xb1\x60", "adcsvs r0, r1, r3"),
    (b"\x03\x00\xb1\x70", "adcsvc r0, r1, r3"),
    (b"\x03\x00\xb1\x80", "adcshi r0, r1, r3"),
    (b"\x03\x00\xb1\x90", "adcsls r0, r1, r3"),
    (b"\x03\x00\xb1\xa0", "adcsge r0, r1, r3"),
    (b"\x03\x00\xb1\xb0", "adcslt r0, r1, r3"),
    (b"\x03\x00\xb1\xc0", "adcsgt r0, r1, r3"),
    (b"\x03\x00\xb1\xd0", "adcsle r0, r1, r3"),
    (b"\x03\x00\xb1\xe0", "adcsal r0, r1, r3"),

    # ADCS - ASR Shifter
    (b"\x42\x02\xb1\x00", "adcseq r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x10", "adcsne r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x20", "adcscs r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x30", "adcscc r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x40", "adcsmi r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x50", "adcspl r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x60", "adcsvs r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x70", "adcsvc r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x80", "adcshi r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\x90", "adcsls r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\xa0", "adcsge r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\xb0", "adcslt r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\xc0", "adcsgt r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\xd0", "adcsle r0, r1, r2, asr #4"),
    (b"\x42\x02\xb1\xe0", "adcsal r0, r1, r2, asr #4"),

    (b"\x52\x03\xb1\x00", "adcseq r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x10", "adcsne r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x20", "adcscs r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x30", "adcscc r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x40", "adcsmi r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x50", "adcspl r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x60", "adcsvs r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x70", "adcsvc r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x80", "adcshi r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\x90", "adcsls r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\xa0", "adcsge r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\xb0", "adcslt r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\xc0", "adcsgt r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\xd0", "adcsle r0, r1, r2, asr r3"),
    (b"\x52\x03\xb1\xe0", "adcsal r0, r1, r2, asr r3"),

    # ADCS - LSL Shifter
    (b"\x02\x02\xb1\x00", "adcseq r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x10", "adcsne r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x20", "adcscs r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x30", "adcscc r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x40", "adcsmi r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x50", "adcspl r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x60", "adcsvs r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x70", "adcsvc r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x80", "adcshi r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\x90", "adcsls r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\xa0", "adcsge r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\xb0", "adcslt r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\xc0", "adcsgt r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\xd0", "adcsle r0, r1, r2, lsl #4"),
    (b"\x02\x02\xb1\xe0", "adcsal r0, r1, r2, lsl #4"),

    (b"\x12\x03\xb1\x00", "adcseq r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x10", "adcsne r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x20", "adcscs r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x30", "adcscc r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x40", "adcsmi r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x50", "adcspl r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x60", "adcsvs r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x70", "adcsvc r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x80", "adcshi r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\x90", "adcsls r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\xa0", "adcsge r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\xb0", "adcslt r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\xc0", "adcsgt r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\xd0", "adcsle r0, r1, r2, lsl r3"),
    (b"\x12\x03\xb1\xe0", "adcsal r0, r1, r2, lsl r3"),

    # ADCS - LSR Shifter
    (b"\x22\x02\xb1\x00", "adcseq r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x10", "adcsne r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x20", "adcscs r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x30", "adcscc r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x40", "adcsmi r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x50", "adcspl r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x60", "adcsvs r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x70", "adcsvc r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x80", "adcshi r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\x90", "adcsls r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\xa0", "adcsge r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\xb0", "adcslt r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\xc0", "adcsgt r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\xd0", "adcsle r0, r1, r2, lsr #4"),
    (b"\x22\x02\xb1\xe0", "adcsal r0, r1, r2, lsr #4"),

    (b"\x32\x03\xb1\x00", "adcseq r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x10", "adcsne r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x20", "adcscs r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x30", "adcscc r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x40", "adcsmi r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x50", "adcspl r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x60", "adcsvs r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x70", "adcsvc r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x80", "adcshi r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\x90", "adcsls r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\xa0", "adcsge r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\xb0", "adcslt r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\xc0", "adcsgt r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\xd0", "adcsle r0, r1, r2, lsr r3"),
    (b"\x32\x03\xb1\xe0", "adcsal r0, r1, r2, lsr r3"),

    # ADCS - ROR Shifter
    (b"\x62\x02\xb1\x00", "adcseq r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x10", "adcsne r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x20", "adcscs r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x30", "adcscc r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x40", "adcsmi r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x50", "adcspl r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x60", "adcsvs r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x70", "adcsvc r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x80", "adcshi r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\x90", "adcsls r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\xa0", "adcsge r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\xb0", "adcslt r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\xc0", "adcsgt r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\xd0", "adcsle r0, r1, r2, ror #4"),
    (b"\x62\x02\xb1\xe0", "adcsal r0, r1, r2, ror #4"),

    (b"\x72\x03\xb1\x00", "adcseq r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x10", "adcsne r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x20", "adcscs r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x30", "adcscc r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x40", "adcsmi r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x50", "adcspl r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x60", "adcsvs r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x70", "adcsvc r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x80", "adcshi r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\x90", "adcsls r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\xa0", "adcsge r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\xb0", "adcslt r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\xc0", "adcsgt r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\xd0", "adcsle r0, r1, r2, ror r3"),
    (b"\x72\x03\xb1\xe0", "adcsal r0, r1, r2, ror r3"),

    # ADCS - RRX Shifter
    (b"\x62\x00\xb1\x00", "adcseq r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x10", "adcsne r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x20", "adcscs r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x30", "adcscc r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x40", "adcsmi r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x50", "adcspl r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x60", "adcsvs r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x70", "adcsvc r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x80", "adcshi r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\x90", "adcsls r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\xa0", "adcsge r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\xb0", "adcslt r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\xc0", "adcsgt r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\xd0", "adcsle r0, r1, r2, rrx"),
    (b"\x62\x00\xb1\xe0", "adcsal r0, r1, r2, rrx"),

    # ADC|S - Misc
    (b"\x01\x00\xa2\xe0", "adc r0, r2, r1"),
    (b"\x01\x00\xa1\xe0", "adc r0, r1, r1"),
    (b"\x01\x10\xa1\xe0", "adc r1, r1, r1"),
    (b"\x11\x01\xa2\xe0", "adc r0, r2, r1, lsl r1"),
    (b"\x11\x01\xa1\xe0", "adc r0, r1, r1, lsl r1"),
    (b"\x11\x11\xa1\xe0", "adc r1, r1, r1, lsl r1"),
    (b"\xc1\x1f\xa1\xe0", "adc r1, r1, r1, asr #31"),
    (b"\x81\x1f\xa1\xe0", "adc r1, r1, r1, lsl #31"),
    (b"\xa1\x1f\xa1\xe0", "adc r1, r1, r1, lsr #31"),
    (b"\xe1\x1f\xa1\xe0", "adc r1, r1, r1, ror #31"),

    # TODO (cnheitman): Test also with PC as a source and as destination
    # operand.
    # ADD -------------------------------------------------------------------- #
    (b"\x02\x00\x81\xe2", "add r0, r1, #2"),
    (b"\x02\x00\x81\x02", "addeq r0, r1, #2"),
    (b"\x02\x00\x81\x12", "addne r0, r1, #2"),
    (b"\x02\x00\x81\x22", "addcs r0, r1, #2"),
    (b"\x02\x00\x81\x32", "addcc r0, r1, #2"),
    (b"\x02\x00\x81\x42", "addmi r0, r1, #2"),
    (b"\x02\x00\x81\x52", "addpl r0, r1, #2"),
    (b"\x02\x00\x81\x62", "addvs r0, r1, #2"),
    (b"\x02\x00\x81\x72", "addvc r0, r1, #2"),
    (b"\x02\x00\x81\x82", "addhi r0, r1, #2"),
    (b"\x02\x00\x81\x92", "addls r0, r1, #2"),
    (b"\x02\x00\x81\xa2", "addge r0, r1, #2"),
    (b"\x02\x00\x81\xb2", "addlt r0, r1, #2"),
    (b"\x02\x00\x81\xc2", "addgt r0, r1, #2"),
    (b"\x02\x00\x81\xd2", "addle r0, r1, #2"),
    (b"\x02\x00\x81\xe2", "addal r0, r1, #2"),

    (b"\x03\x00\x81\xe0", "add r0, r1, r3"),
    (b"\x03\x00\x81\x00", "addeq r0, r1, r3"),
    (b"\x03\x00\x81\x10", "addne r0, r1, r3"),
    (b"\x03\x00\x81\x20", "addcs r0, r1, r3"),
    (b"\x03\x00\x81\x30", "addcc r0, r1, r3"),
    (b"\x03\x00\x81\x40", "addmi r0, r1, r3"),
    (b"\x03\x00\x81\x50", "addpl r0, r1, r3"),
    (b"\x03\x00\x81\x60", "addvs r0, r1, r3"),
    (b"\x03\x00\x81\x70", "addvc r0, r1, r3"),
    (b"\x03\x00\x81\x80", "addhi r0, r1, r3"),
    (b"\x03\x00\x81\x90", "addls r0, r1, r3"),
    (b"\x03\x00\x81\xa0", "addge r0, r1, r3"),
    (b"\x03\x00\x81\xb0", "addlt r0, r1, r3"),
    (b"\x03\x00\x81\xc0", "addgt r0, r1, r3"),
    (b"\x03\x00\x81\xd0", "addle r0, r1, r3"),
    (b"\x03\x00\x81\xe0", "addal r0, r1, r3"),

    # ADD - ASR Shifter
    (b"\x42\x02\x81\x00", "addeq r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x10", "addne r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x20", "addcs r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x30", "addcc r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x40", "addmi r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x50", "addpl r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x60", "addvs r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x70", "addvc r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x80", "addhi r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\x90", "addls r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\xa0", "addge r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\xb0", "addlt r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\xc0", "addgt r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\xd0", "addle r0, r1, r2, asr #4"),
    (b"\x42\x02\x81\xe0", "addal r0, r1, r2, asr #4"),

    (b"\x52\x03\x81\x00", "addeq r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x10", "addne r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x20", "addcs r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x30", "addcc r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x40", "addmi r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x50", "addpl r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x60", "addvs r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x70", "addvc r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x80", "addhi r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\x90", "addls r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\xa0", "addge r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\xb0", "addlt r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\xc0", "addgt r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\xd0", "addle r0, r1, r2, asr r3"),
    (b"\x52\x03\x81\xe0", "addal r0, r1, r2, asr r3"),

    # ADD - LSL Shifter
    (b"\x02\x02\x81\x00", "addeq r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x10", "addne r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x20", "addcs r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x30", "addcc r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x40", "addmi r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x50", "addpl r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x60", "addvs r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x70", "addvc r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x80", "addhi r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\x90", "addls r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\xa0", "addge r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\xb0", "addlt r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\xc0", "addgt r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\xd0", "addle r0, r1, r2, lsl #4"),
    (b"\x02\x02\x81\xe0", "addal r0, r1, r2, lsl #4"),

    (b"\x12\x03\x81\x00", "addeq r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x10", "addne r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x20", "addcs r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x30", "addcc r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x40", "addmi r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x50", "addpl r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x60", "addvs r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x70", "addvc r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x80", "addhi r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\x90", "addls r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\xa0", "addge r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\xb0", "addlt r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\xc0", "addgt r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\xd0", "addle r0, r1, r2, lsl r3"),
    (b"\x12\x03\x81\xe0", "addal r0, r1, r2, lsl r3"),

    # ADD - LSR Shifter
    (b"\x22\x02\x81\x00", "addeq r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x10", "addne r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x20", "addcs r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x30", "addcc r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x40", "addmi r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x50", "addpl r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x60", "addvs r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x70", "addvc r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x80", "addhi r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\x90", "addls r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\xa0", "addge r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\xb0", "addlt r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\xc0", "addgt r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\xd0", "addle r0, r1, r2, lsr #4"),
    (b"\x22\x02\x81\xe0", "addal r0, r1, r2, lsr #4"),

    (b"\x32\x03\x81\x00", "addeq r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x10", "addne r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x20", "addcs r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x30", "addcc r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x40", "addmi r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x50", "addpl r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x60", "addvs r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x70", "addvc r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x80", "addhi r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\x90", "addls r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\xa0", "addge r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\xb0", "addlt r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\xc0", "addgt r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\xd0", "addle r0, r1, r2, lsr r3"),
    (b"\x32\x03\x81\xe0", "addal r0, r1, r2, lsr r3"),

    # ADD - ROR Shifter
    (b"\x62\x02\x81\x00", "addeq r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x10", "addne r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x20", "addcs r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x30", "addcc r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x40", "addmi r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x50", "addpl r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x60", "addvs r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x70", "addvc r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x80", "addhi r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\x90", "addls r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\xa0", "addge r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\xb0", "addlt r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\xc0", "addgt r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\xd0", "addle r0, r1, r2, ror #4"),
    (b"\x62\x02\x81\xe0", "addal r0, r1, r2, ror #4"),

    (b"\x72\x03\x81\x00", "addeq r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x10", "addne r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x20", "addcs r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x30", "addcc r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x40", "addmi r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x50", "addpl r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x60", "addvs r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x70", "addvc r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x80", "addhi r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\x90", "addls r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\xa0", "addge r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\xb0", "addlt r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\xc0", "addgt r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\xd0", "addle r0, r1, r2, ror r3"),
    (b"\x72\x03\x81\xe0", "addal r0, r1, r2, ror r3"),

    # ADD - RRX Shifter
    (b"\x62\x00\x81\x00", "addeq r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x10", "addne r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x20", "addcs r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x30", "addcc r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x40", "addmi r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x50", "addpl r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x60", "addvs r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x70", "addvc r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x80", "addhi r0, r1, r2, rrx"),
    (b"\x62\x00\x81\x90", "addls r0, r1, r2, rrx"),
    (b"\x62\x00\x81\xa0", "addge r0, r1, r2, rrx"),
    (b"\x62\x00\x81\xb0", "addlt r0, r1, r2, rrx"),
    (b"\x62\x00\x81\xc0", "addgt r0, r1, r2, rrx"),
    (b"\x62\x00\x81\xd0", "addle r0, r1, r2, rrx"),
    (b"\x62\x00\x81\xe0", "addal r0, r1, r2, rrx"),

    # ADDS ------------------------------------------------------------------- #
    (b"\x02\x00\x91\xe2", "adds r0, r1, #2"),
    (b"\x02\x00\x91\x02", "addseq r0, r1, #2"),
    (b"\x02\x00\x91\x12", "addsne r0, r1, #2"),
    (b"\x02\x00\x91\x22", "addscs r0, r1, #2"),
    (b"\x02\x00\x91\x32", "addscc r0, r1, #2"),
    (b"\x02\x00\x91\x42", "addsmi r0, r1, #2"),
    (b"\x02\x00\x91\x52", "addspl r0, r1, #2"),
    (b"\x02\x00\x91\x62", "addsvs r0, r1, #2"),
    (b"\x02\x00\x91\x72", "addsvc r0, r1, #2"),
    (b"\x02\x00\x91\x82", "addshi r0, r1, #2"),
    (b"\x02\x00\x91\x92", "addsls r0, r1, #2"),
    (b"\x02\x00\x91\xa2", "addsge r0, r1, #2"),
    (b"\x02\x00\x91\xb2", "addslt r0, r1, #2"),
    (b"\x02\x00\x91\xc2", "addsgt r0, r1, #2"),
    (b"\x02\x00\x91\xd2", "addsle r0, r1, #2"),
    (b"\x02\x00\x91\xe2", "addsal r0, r1, #2"),

    (b"\x03\x00\x91\xe0", "adds r0, r1, r3"),
    (b"\x03\x00\x91\x00", "addseq r0, r1, r3"),
    (b"\x03\x00\x91\x10", "addsne r0, r1, r3"),
    (b"\x03\x00\x91\x20", "addscs r0, r1, r3"),
    (b"\x03\x00\x91\x30", "addscc r0, r1, r3"),
    (b"\x03\x00\x91\x40", "addsmi r0, r1, r3"),
    (b"\x03\x00\x91\x50", "addspl r0, r1, r3"),
    (b"\x03\x00\x91\x60", "addsvs r0, r1, r3"),
    (b"\x03\x00\x91\x70", "addsvc r0, r1, r3"),
    (b"\x03\x00\x91\x80", "addshi r0, r1, r3"),
    (b"\x03\x00\x91\x90", "addsls r0, r1, r3"),
    (b"\x03\x00\x91\xa0", "addsge r0, r1, r3"),
    (b"\x03\x00\x91\xb0", "addslt r0, r1, r3"),
    (b"\x03\x00\x91\xc0", "addsgt r0, r1, r3"),
    (b"\x03\x00\x91\xd0", "addsle r0, r1, r3"),
    (b"\x03\x00\x91\xe0", "addsal r0, r1, r3"),

    # ADDS - ASR Shifter
    (b"\x42\x02\x91\x00", "addseq r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x10", "addsne r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x20", "addscs r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x30", "addscc r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x40", "addsmi r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x50", "addspl r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x60", "addsvs r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x70", "addsvc r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x80", "addshi r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\x90", "addsls r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\xa0", "addsge r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\xb0", "addslt r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\xc0", "addsgt r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\xd0", "addsle r0, r1, r2, asr #4"),
    (b"\x42\x02\x91\xe0", "addsal r0, r1, r2, asr #4"),

    (b"\x52\x03\x91\x00", "addseq r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x10", "addsne r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x20", "addscs r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x30", "addscc r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x40", "addsmi r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x50", "addspl r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x60", "addsvs r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x70", "addsvc r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x80", "addshi r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\x90", "addsls r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\xa0", "addsge r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\xb0", "addslt r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\xc0", "addsgt r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\xd0", "addsle r0, r1, r2, asr r3"),
    (b"\x52\x03\x91\xe0", "addsal r0, r1, r2, asr r3"),

    # ADDS - LSL Shifter
    (b"\x02\x02\x91\x00", "addseq r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x10", "addsne r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x20", "addscs r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x30", "addscc r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x40", "addsmi r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x50", "addspl r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x60", "addsvs r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x70", "addsvc r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x80", "addshi r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\x90", "addsls r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\xa0", "addsge r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\xb0", "addslt r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\xc0", "addsgt r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\xd0", "addsle r0, r1, r2, lsl #4"),
    (b"\x02\x02\x91\xe0", "addsal r0, r1, r2, lsl #4"),

    (b"\x12\x03\x91\x00", "addseq r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x10", "addsne r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x20", "addscs r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x30", "addscc r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x40", "addsmi r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x50", "addspl r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x60", "addsvs r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x70", "addsvc r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x80", "addshi r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\x90", "addsls r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\xa0", "addsge r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\xb0", "addslt r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\xc0", "addsgt r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\xd0", "addsle r0, r1, r2, lsl r3"),
    (b"\x12\x03\x91\xe0", "addsal r0, r1, r2, lsl r3"),

    # ADDS - LSR Shifter
    (b"\x22\x02\x91\x00", "addseq r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x10", "addsne r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x20", "addscs r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x30", "addscc r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x40", "addsmi r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x50", "addspl r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x60", "addsvs r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x70", "addsvc r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x80", "addshi r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\x90", "addsls r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\xa0", "addsge r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\xb0", "addslt r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\xc0", "addsgt r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\xd0", "addsle r0, r1, r2, lsr #4"),
    (b"\x22\x02\x91\xe0", "addsal r0, r1, r2, lsr #4"),

    (b"\x32\x03\x91\x00", "addseq r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x10", "addsne r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x20", "addscs r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x30", "addscc r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x40", "addsmi r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x50", "addspl r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x60", "addsvs r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x70", "addsvc r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x80", "addshi r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\x90", "addsls r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\xa0", "addsge r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\xb0", "addslt r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\xc0", "addsgt r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\xd0", "addsle r0, r1, r2, lsr r3"),
    (b"\x32\x03\x91\xe0", "addsal r0, r1, r2, lsr r3"),

    # ADDS - ROR Shifter
    (b"\x62\x02\x91\x00", "addseq r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x10", "addsne r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x20", "addscs r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x30", "addscc r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x40", "addsmi r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x50", "addspl r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x60", "addsvs r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x70", "addsvc r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x80", "addshi r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\x90", "addsls r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\xa0", "addsge r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\xb0", "addslt r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\xc0", "addsgt r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\xd0", "addsle r0, r1, r2, ror #4"),
    (b"\x62\x02\x91\xe0", "addsal r0, r1, r2, ror #4"),

    (b"\x72\x03\x91\x00", "addseq r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x10", "addsne r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x20", "addscs r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x30", "addscc r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x40", "addsmi r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x50", "addspl r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x60", "addsvs r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x70", "addsvc r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x80", "addshi r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\x90", "addsls r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\xa0", "addsge r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\xb0", "addslt r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\xc0", "addsgt r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\xd0", "addsle r0, r1, r2, ror r3"),
    (b"\x72\x03\x91\xe0", "addsal r0, r1, r2, ror r3"),

    # ADDS - RRX Shifter
    (b"\x62\x00\x91\x00", "addseq r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x10", "addsne r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x20", "addscs r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x30", "addscc r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x40", "addsmi r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x50", "addspl r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x60", "addsvs r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x70", "addsvc r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x80", "addshi r0, r1, r2, rrx"),
    (b"\x62\x00\x91\x90", "addsls r0, r1, r2, rrx"),
    (b"\x62\x00\x91\xa0", "addsge r0, r1, r2, rrx"),
    (b"\x62\x00\x91\xb0", "addslt r0, r1, r2, rrx"),
    (b"\x62\x00\x91\xc0", "addsgt r0, r1, r2, rrx"),
    (b"\x62\x00\x91\xd0", "addsle r0, r1, r2, rrx"),
    (b"\x62\x00\x91\xe0", "addsal r0, r1, r2, rrx"),

    # ADD|S misc
    (b"\x01\x00\x82\xe0", "add r0, r2, r1"),
    (b"\x01\x00\x81\xe0", "add r0, r1, r1"),
    (b"\x01\x10\x81\xe0", "add r1, r1, r1"),
    (b"\x11\x01\x82\xe0", "add r0, r2, r1, lsl r1"),
    (b"\x11\x01\x81\xe0", "add r0, r1, r1, lsl r1"),
    (b"\x11\x11\x81\xe0", "add r1, r1, r1, lsl r1"),
    (b"\xc1\x1f\x81\xe0", "add r1, r1, r1, asr #31"),
    (b"\x81\x1f\x81\xe0", "add r1, r1, r1, lsl #31"),
    (b"\xa1\x1f\x81\xe0", "add r1, r1, r1, lsr #31"),
    (b"\xe1\x1f\x81\xe0", "add r1, r1, r1, ror #31"),

    # ADD|S  with SP --------------------------------------------------------- #
    (b"\x02\x00\x9d\xe2", "adds r0, sp, #2"),
    (b"\x02\x00\x9d\x02", "addseq r0, sp, #2"),
    (b"\x02\x00\x9d\x12", "addsne r0, sp, #2"),
    (b"\x02\x00\x9d\x22", "addscs r0, sp, #2"),
    (b"\x02\x00\x9d\x32", "addscc r0, sp, #2"),
    (b"\x02\x00\x9d\x42", "addsmi r0, sp, #2"),
    (b"\x02\x00\x9d\x52", "addspl r0, sp, #2"),
    (b"\x02\x00\x9d\x62", "addsvs r0, sp, #2"),
    (b"\x02\x00\x9d\x72", "addsvc r0, sp, #2"),
    (b"\x02\x00\x9d\x82", "addshi r0, sp, #2"),
    (b"\x02\x00\x9d\x92", "addsls r0, sp, #2"),
    (b"\x02\x00\x9d\xa2", "addsge r0, sp, #2"),
    (b"\x02\x00\x9d\xb2", "addslt r0, sp, #2"),
    (b"\x02\x00\x9d\xc2", "addsgt r0, sp, #2"),
    (b"\x02\x00\x9d\xd2", "addsle r0, sp, #2"),
    (b"\x02\x00\x9d\xe2", "addsal r0, sp, #2"),

    (b"\x03\x00\x9d\xe0", "adds r0, sp, r3"),
    (b"\x03\x00\x9d\x00", "addseq r0, sp, r3"),
    (b"\x03\x00\x9d\x10", "addsne r0, sp, r3"),
    (b"\x03\x00\x9d\x20", "addscs r0, sp, r3"),
    (b"\x03\x00\x9d\x30", "addscc r0, sp, r3"),
    (b"\x03\x00\x9d\x40", "addsmi r0, sp, r3"),
    (b"\x03\x00\x9d\x50", "addspl r0, sp, r3"),
    (b"\x03\x00\x9d\x60", "addsvs r0, sp, r3"),
    (b"\x03\x00\x9d\x70", "addsvc r0, sp, r3"),
    (b"\x03\x00\x9d\x80", "addshi r0, sp, r3"),
    (b"\x03\x00\x9d\x90", "addsls r0, sp, r3"),
    (b"\x03\x00\x9d\xa0", "addsge r0, sp, r3"),
    (b"\x03\x00\x9d\xb0", "addslt r0, sp, r3"),
    (b"\x03\x00\x9d\xc0", "addsgt r0, sp, r3"),
    (b"\x03\x00\x9d\xd0", "addsle r0, sp, r3"),
    (b"\x03\x00\x9d\xe0", "addsal r0, sp, r3"),

    (b"\x02\xd0\x9d\xe2", "adds sp, sp, #2"),
    (b"\x02\xd0\x9d\x02", "addseq sp, sp, #2"),
    (b"\x02\xd0\x9d\x12", "addsne sp, sp, #2"),
    (b"\x02\xd0\x9d\x22", "addscs sp, sp, #2"),
    (b"\x02\xd0\x9d\x32", "addscc sp, sp, #2"),
    (b"\x02\xd0\x9d\x42", "addsmi sp, sp, #2"),
    (b"\x02\xd0\x9d\x52", "addspl sp, sp, #2"),
    (b"\x02\xd0\x9d\x62", "addsvs sp, sp, #2"),
    (b"\x02\xd0\x9d\x72", "addsvc sp, sp, #2"),
    (b"\x02\xd0\x9d\x82", "addshi sp, sp, #2"),
    (b"\x02\xd0\x9d\x92", "addsls sp, sp, #2"),
    (b"\x02\xd0\x9d\xa2", "addsge sp, sp, #2"),
    (b"\x02\xd0\x9d\xb2", "addslt sp, sp, #2"),
    (b"\x02\xd0\x9d\xc2", "addsgt sp, sp, #2"),
    (b"\x02\xd0\x9d\xd2", "addsle sp, sp, #2"),
    (b"\x02\xd0\x9d\xe2", "addsal sp, sp, #2"),

    (b"\x03\xd0\x9d\xe0", "adds sp, sp, r3"),
    (b"\x03\xd0\x9d\x00", "addseq sp, sp, r3"),
    (b"\x03\xd0\x9d\x10", "addsne sp, sp, r3"),
    (b"\x03\xd0\x9d\x20", "addscs sp, sp, r3"),
    (b"\x03\xd0\x9d\x30", "addscc sp, sp, r3"),
    (b"\x03\xd0\x9d\x40", "addsmi sp, sp, r3"),
    (b"\x03\xd0\x9d\x50", "addspl sp, sp, r3"),
    (b"\x03\xd0\x9d\x60", "addsvs sp, sp, r3"),
    (b"\x03\xd0\x9d\x70", "addsvc sp, sp, r3"),
    (b"\x03\xd0\x9d\x80", "addshi sp, sp, r3"),
    (b"\x03\xd0\x9d\x90", "addsls sp, sp, r3"),
    (b"\x03\xd0\x9d\xa0", "addsge sp, sp, r3"),
    (b"\x03\xd0\x9d\xb0", "addslt sp, sp, r3"),
    (b"\x03\xd0\x9d\xc0", "addsgt sp, sp, r3"),
    (b"\x03\xd0\x9d\xd0", "addsle sp, sp, r3"),
    (b"\x03\xd0\x9d\xe0", "addsal sp, sp, r3"),

    (b"\x1d\xdd\x8d\xe0", "add sp, sp, sp, lsl sp"),
    (b"\x1d\xdd\x9d\xe0", "adds sp, sp, sp, lsl sp"),
    (b"\x3d\xdd\x8d\xe0", "add sp, sp, sp, lsr sp"),
    (b"\x3d\xdd\x9d\xe0", "adds sp, sp, sp, lsr sp"),
    (b"\x5d\xdd\x8d\xe0", "add sp, sp, sp, asr sp"),
    (b"\x5d\xdd\x9d\xe0", "adds sp, sp, sp, asr sp"),
    (b"\x5d\xdd\x8d\xe0", "add sp, sp, sp, asr sp"),
    (b"\x5d\xdd\x9d\xe0", "adds sp, sp, sp, asr sp"),
    (b"\x7d\xdd\x8d\xe0", "add sp, sp, sp, ror sp"),
    (b"\x7d\xdd\x9d\xe0", "adds sp, sp, sp, ror sp"),
    (b"\x7d\xdd\x8d\xe0", "add sp, sp, sp, ror sp"),
    (b"\x7d\xdd\x9d\xe0", "adds sp, sp, sp, ror sp"),
]

def emu_with_unicorn(opcode, istate):
    # Initialize emulator in arm32 mode
    mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)

    # map memory for this emulation
    mu.mem_map(ADDR, SIZE)

    # write machine code to be emulated to memory
    index = 0
    for op, _ in CODE:
        mu.mem_write(ADDR+index, op)
        index += len(op)

    apsr = mu.reg_read(UC_ARM_REG_APSR)
    nzcv = istate['n'] << 31 | istate['z'] << 30 | istate['c'] << 29 | istate['v'] << 28

    mu.mem_write(STACK,                bytes(istate['stack']))
    mu.mem_write(HEAP,                 bytes(istate['heap']))
    mu.reg_write(UC_ARM_REG_R0,        istate['r0'])
    mu.reg_write(UC_ARM_REG_R1,        istate['r1'])
    mu.reg_write(UC_ARM_REG_R2,        istate['r2'])
    mu.reg_write(UC_ARM_REG_R3,        istate['r3'])
    mu.reg_write(UC_ARM_REG_R4,        istate['r4'])
    mu.reg_write(UC_ARM_REG_R5,        istate['r5'])
    mu.reg_write(UC_ARM_REG_R6,        istate['r6'])
    mu.reg_write(UC_ARM_REG_R7,        istate['r7'])
    mu.reg_write(UC_ARM_REG_R8,        istate['r8'])
    mu.reg_write(UC_ARM_REG_R9,        istate['r9'])
    mu.reg_write(UC_ARM_REG_R10,       istate['r10'])
    mu.reg_write(UC_ARM_REG_R11,       istate['r11'])
    mu.reg_write(UC_ARM_REG_R12,       istate['r12'])
    mu.reg_write(UC_ARM_REG_SP,        istate['sp'])
    mu.reg_write(UC_ARM_REG_R14,       istate['r14'])
    mu.reg_write(UC_ARM_REG_PC,        istate['pc'])
    mu.reg_write(UC_ARM_REG_APSR,      apsr & 0x0fffffff | nzcv)

    # emulate code in infinite time & unlimited instructions
    mu.emu_start(istate['pc'], istate['pc'] + len(opcode))

    ostate = {
        "stack": mu.mem_read(STACK, 0x100),
        "heap":  mu.mem_read(HEAP, 0x100),
        "r0":    mu.reg_read(UC_ARM_REG_R0),
        "r1":    mu.reg_read(UC_ARM_REG_R1),
        "r2":    mu.reg_read(UC_ARM_REG_R2),
        "r3":    mu.reg_read(UC_ARM_REG_R3),
        "r4":    mu.reg_read(UC_ARM_REG_R4),
        "r5":    mu.reg_read(UC_ARM_REG_R5),
        "r6":    mu.reg_read(UC_ARM_REG_R6),
        "r7":    mu.reg_read(UC_ARM_REG_R7),
        "r8":    mu.reg_read(UC_ARM_REG_R8),
        "r9":    mu.reg_read(UC_ARM_REG_R9),
        "r10":   mu.reg_read(UC_ARM_REG_R10),
        "r11":   mu.reg_read(UC_ARM_REG_R11),
        "r12":   mu.reg_read(UC_ARM_REG_R12),
        "sp":    mu.reg_read(UC_ARM_REG_SP),
        "r14":   mu.reg_read(UC_ARM_REG_R14),
        "pc":    mu.reg_read(UC_ARM_REG_PC),
        "n":   ((mu.reg_read(UC_ARM_REG_APSR) >> 31) & 1),
        "z":   ((mu.reg_read(UC_ARM_REG_APSR) >> 30) & 1),
        "c":   ((mu.reg_read(UC_ARM_REG_APSR) >> 29) & 1),
        "v":   ((mu.reg_read(UC_ARM_REG_APSR) >> 28) & 1),
    }
    return ostate

def emu_with_triton(opcode, istate):
    ctx = TritonContext()
    ctx.setArchitecture(ARCH.ARM32)

    inst = Instruction(opcode)
    inst.setAddress(istate['pc'])

    ctx.setConcreteMemoryAreaValue(STACK,           bytes(istate['stack']))
    ctx.setConcreteMemoryAreaValue(HEAP,            bytes(istate['heap']))
    ctx.setConcreteRegisterValue(ctx.registers.r0,  istate['r0'])
    ctx.setConcreteRegisterValue(ctx.registers.r1,  istate['r1'])
    ctx.setConcreteRegisterValue(ctx.registers.r2,  istate['r2'])
    ctx.setConcreteRegisterValue(ctx.registers.r3,  istate['r3'])
    ctx.setConcreteRegisterValue(ctx.registers.r4,  istate['r4'])
    ctx.setConcreteRegisterValue(ctx.registers.r5,  istate['r5'])
    ctx.setConcreteRegisterValue(ctx.registers.r6,  istate['r6'])
    ctx.setConcreteRegisterValue(ctx.registers.r7,  istate['r7'])
    ctx.setConcreteRegisterValue(ctx.registers.r8,  istate['r8'])
    ctx.setConcreteRegisterValue(ctx.registers.r9,  istate['r9'])
    ctx.setConcreteRegisterValue(ctx.registers.r10, istate['r10'])
    ctx.setConcreteRegisterValue(ctx.registers.r11, istate['r11'])
    ctx.setConcreteRegisterValue(ctx.registers.r12, istate['r12'])
    ctx.setConcreteRegisterValue(ctx.registers.sp,  istate['sp'])
    ctx.setConcreteRegisterValue(ctx.registers.r14, istate['r14'])
    ctx.setConcreteRegisterValue(ctx.registers.pc,  istate['pc'])
    ctx.setConcreteRegisterValue(ctx.registers.n,   istate['n'])
    ctx.setConcreteRegisterValue(ctx.registers.z,   istate['z'])
    ctx.setConcreteRegisterValue(ctx.registers.c,   istate['c'])
    ctx.setConcreteRegisterValue(ctx.registers.v,   istate['v'])

    ctx.processing(inst)

    # print()
    # print(inst)
    # for x in inst.getSymbolicExpressions():
    #    print(x)
    # print()

    ostate = {
        "stack": ctx.getConcreteMemoryAreaValue(STACK, 0x100),
        "heap":  ctx.getConcreteMemoryAreaValue(HEAP, 0x100),
        "r0":    ctx.getSymbolicRegisterValue(ctx.registers.r0),
        "r1":    ctx.getSymbolicRegisterValue(ctx.registers.r1),
        "r2":    ctx.getSymbolicRegisterValue(ctx.registers.r2),
        "r3":    ctx.getSymbolicRegisterValue(ctx.registers.r3),
        "r4":    ctx.getSymbolicRegisterValue(ctx.registers.r4),
        "r5":    ctx.getSymbolicRegisterValue(ctx.registers.r5),
        "r6":    ctx.getSymbolicRegisterValue(ctx.registers.r6),
        "r7":    ctx.getSymbolicRegisterValue(ctx.registers.r7),
        "r8":    ctx.getSymbolicRegisterValue(ctx.registers.r8),
        "r9":    ctx.getSymbolicRegisterValue(ctx.registers.r9),
        "r10":   ctx.getSymbolicRegisterValue(ctx.registers.r10),
        "r11":   ctx.getSymbolicRegisterValue(ctx.registers.r11),
        "r12":   ctx.getSymbolicRegisterValue(ctx.registers.r12),
        "sp":    ctx.getSymbolicRegisterValue(ctx.registers.sp),
        "r14":   ctx.getSymbolicRegisterValue(ctx.registers.r14),
        "pc":    ctx.getSymbolicRegisterValue(ctx.registers.pc),
        "n":     ctx.getSymbolicRegisterValue(ctx.registers.n),
        "z":     ctx.getSymbolicRegisterValue(ctx.registers.z),
        "c":     ctx.getSymbolicRegisterValue(ctx.registers.c),
        "v":     ctx.getSymbolicRegisterValue(ctx.registers.v),
    }
    return ostate

def diff_state(state1, state2):
    for k, v in list(state1.items()):
        if (k == 'heap' or k == 'stack') and v != state2[k]:
            print('\t%s: (UC) != (TT)' %(k))
        elif not (k == 'heap' or k == 'stack') and v != state2[k]:
            print('\t%s: %#x (UC) != %#x (TT)' %(k, v, state2[k]))
    return

def print_state(istate, uc_ostate, tt_ostate):
    for k in sorted(istate.keys()):
        if k in ['stack', 'heap']:
            continue

        diff = "!=" if uc_ostate[k] != tt_ostate[k] else "=="

        print("{:>3s}: {:08x} | {:08x} {} {:08x}".format(k, istate[k], uc_ostate[k], diff, tt_ostate[k]))


if __name__ == '__main__':
    # initial state
    state = {
        "stack": b"".join([bytes(255 - i) for i in range(256)]),
        "heap":  b"".join([bytes(i) for i in range(256)]),
        "r0":    random.randint(0x0, 0xffffffff),
        "r1":    random.randint(0x0, 0xffffffff),
        "r2":    random.randint(0x0, 0xffffffff),
        "r3":    random.randint(0x0, 0xffffffff),
        "r4":    random.randint(0x0, 0xffffffff),
        "r5":    random.randint(0x0, 0xffffffff),
        "r6":    random.randint(0x0, 0xffffffff),
        "r7":    random.randint(0x0, 0xffffffff),
        "r8":    random.randint(0x0, 0xffffffff),
        "r9":    random.randint(0x0, 0xffffffff),
        "r10":   random.randint(0x0, 0xffffffff),
        "r11":   random.randint(0x0, 0xffffffff),
        "r12":   random.randint(0x0, 0xffffffff),
        "sp":    STACK,
        "r14":   random.randint(0x0, 0xffffffff),
        "pc":    ADDR,
        "n":     random.randint(0x0, 0x1),
        "z":     random.randint(0x0, 0x1),
        "c":     random.randint(0x0, 0x1),
        "v":     random.randint(0x0, 0x1),
    }

    for opcode, disassembly in CODE:
        try:
            uc_state = emu_with_unicorn(opcode, state)
            tt_state = emu_with_triton(opcode, state)
        except Exception as e:
            print('[KO] %s' %(disassembly))
            print('\t%s' %(e))
            sys.exit(-1)

        uc_state['pc'] = tt_state['pc']     # FIXME: Check why UC does not update PC.

        if uc_state != tt_state:
            print('[KO] %s %s' %(" ".join(["%02x" % ord(b) for b in opcode]), disassembly))
            diff_state(uc_state, tt_state)
            print_state(state, uc_state, tt_state)
            sys.exit(-1)

        print('[OK] %s' %(disassembly))
        state = tt_state

    sys.exit(0)