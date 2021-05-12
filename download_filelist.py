# Script to download CopernicusDSM from the AWS API:
# https://registry.opendata.aws/copernicus-dem
#
# Peter Uhe 10/05/2021

import subprocess,os

outdir = 'tiles'

# First get a list of the tiles to download
flist = 'filelist.txt'
if not os.path.exists(flist):
	with open(flist,'w') as f:
		cmd = ['aws','s3','ls','s3://copernicus-dem-30m/','--no-sign-request']
		subprocess.run(cmd,stdout=f)

# Now loop over all the files
with open(flist,'r') as f:
	for line in f:
		try:
			tilename=line.split()[-1][:-1]
			
			# Only download tiles (not readme files etc)
			if tilename[:10]!='Copernicus':
				continue
				
			# skip far south:
			ns_str = tilename.split('_')[4]
			if ns_str[0]=='S' and int(ns_str[1:])>60:
				print('skipping far south',tilename)
				continue
			
			print(tilename)
			fname = tilename+'.tif'
			fpath = os.path.join(outdir,fname)
			if not os.path.exists(fpath):
				# Call AWS API to download file
				cmd = ['aws','s3','cp','--no-sign-request','s3://copernicus-dem-30m/'+tilename+'/'+tilename+'.tif',outdir]
				print(' '.join(cmd))
				retval = subprocess.run(cmd,check=True)
		except Exception as e:
			print('Error, line:',line)
			#print(e)
			raise
