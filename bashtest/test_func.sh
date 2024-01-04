function tom() {
	model=$1
	cur_dir=pwd
	echo "ls --config ${cur_dir} ${model}"

}

tom "This is to test function "
