module load nco
source ../set_env.sh
template_dir=../TOOLS/interp-files/namelist-templates/

cd glodap
cp $EXE_DIR/{scripgrid.exe,scrip.exe,scripinterp.exe} .
cp $EXE_DIR/sosie3.x .
ln -s $DOM_DIR/mesh_mask.nc .
ln -s $SOURCE_DIR/{} .

python interp_glodap.py $template_dir > glodap_interp.log

cd ../woa18
cp $EXE_DIR/{scripgrid.exe,scrip.exe,scripinterp.exe} .
cp $EXE_DIR/sosie3.x .
ln -s $DOM_DIR/mesh_mask.nc .
ln -s $SOURCE_DIR/{} .

python interp_woa18.py $template_dir > woa18_interp.log
mkdir $OUT_DIR/LBC
cd ..
