import subprocess,os
for s in range(1,60):
    for e in range(0,180):
        tilename='Copernicus_DSM_COG_10_N'+str(s).zfill(2)+'_00_W'+str(e).zfill(3)+'_00_DEM'
        fname = tilename+'.tif'
        if not os.path.exists(fname):
            cmd = ['aws','s3','cp','--no-sign-request','s3://copernicus-dem-30m/'+tilename+'/'+tilename+'.tif','.']
            print(' '.join(cmd))
            subprocess.call(cmd)
