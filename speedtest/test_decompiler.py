from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
from androguard.decompiler.decompiler import DecompilerDAD
import sys
import os
import time

import cProfile, pstats
from io import StringIO


def source(d, limit=-1):
    t0 = 0
    tsum = 0
    if limit == -1:
        cl = d.get_classes()
    else:
        cl = d.get_classes()[:limit]

    for i, x in enumerate(cl):
        tic = time.time()
        x.get_source()
        toc = time.time()
        t0 = (t0 + (toc - tic)) / 2.0
        tsum += toc - tic
        if i % 100 == 0:
            print(i, t0, tsum)

    print("average:", t0, "sum:", tsum)

tic = time.time()
a = APK(sys.argv[1])
print("APK Bytecode", time.time() - tic)
tic = time.time()
d = DalvikVMFormat(a)
print("Dalvik Bytecode", time.time() - tic)
tic = time.time()
dx = Analysis(d)
print("DVM Analysis", time.time() - tic)
d.set_vmanalysis(dx)

tic = time.time()
decompile = DecompilerDAD(d, dx)
print("Decompilation", time.time() - tic)
d.set_decompiler(decompile)

print("Number of classes", len(d.get_classes()))


pr = cProfile.Profile()

pr.enable()  # start profiling

source(d)
pr.disable()  # end profiling
s = StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
