#! /bin/bash
# start the master and the slaves
start-all.sh

# submit applications to spark cluster

spark-submit \
--class main \
--master spark://192.103.8.7:7077 \
--driver-memory 4g \
--executor-memory 2g \
--executor-cores 4 \
/home/spark/test_spark_sjr/fire_risk_assessment/fill_nan_value.py file:/home/spark/test_spark_sjr/fire_risk_assessment/sample_libsvm_data.txt method_of_fill file:///home/spark/test_spark_sjr/fire_risk_assessment/data_save/data_fill

# stop the master and the slaves
stop-all.sh



