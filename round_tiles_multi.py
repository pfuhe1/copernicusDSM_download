# Python script to round CopernicusDSM files to nearest 1cm
# Uses gdal_calc.py for computation
# Assumes filenames match cloud optimized geotiffs downloaded from AWS
#
# Peter Uhe 10/5/2021
# 

import os,sys,glob,subprocess
from multiprocessing import Pool 

outdir = 'tiles_rounded'
numthreads = 8

with Pool(numthreads) as p:
	for ftile in glob.glob('tiles/*.tif'):
		fend = os.path.basename(ftile).split('Copernicus_DSM_COG')[-1]
		fround = 'Copernicus_DSM_rounded'+fend
		fout = os.path.join(outdir,fround)
		if not os.path.exists(fout):
			cmd = ['gdal_calc.py','--co','COMPRESS=DEFLATE','-A',ftile,'--A_band','1','--outfile',fout,'--calc', 'around(A,2)']
			print(cmd)
			#subprocess.run(cmd,check=True)
			ret = p.apply_async(subprocess.run,(cmd,),{'check':True})
			
	#print(ret.get())
