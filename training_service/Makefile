KERNEL_NAME=hugoce/vmt-training
KERNEL_DIR=kernel_files
OUTPUT_DIR=output

pull:
	kaggle kernels pull ${KERNEL_NAME} -p ${KERNEL_DIR} -m
	
push:
	kaggle kernels push -p ${KERNEL_DIR}

status:
	kaggle kernels status ${KERNEL_NAME}

files:
	kaggle kernels files ${KERNEL_NAME}

get-output:
	kaggle kernels output ${KERNEL_NAME} -p ${OUTPUT_DIR}