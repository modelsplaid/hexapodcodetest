models="fisheye_det;fisheye_seg;front_28;front_64;tsr_2nd;front_120;side;mosaic;linedet;ParkingSlot;topview"
models=($(echo $models | tr ";" "\\n"))
echo ${models[@]}

echo "------------------"
for i in "${models[@]}" 

do 
	echo $i
	
done

