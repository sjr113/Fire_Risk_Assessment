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
/home/spark/test_spark_sjr/fire_risk_assessment/lr_on_data_set.py file:/home/spark/test_spark_sjr/fire_risk_assessment/sample_libsvm_data.txt file:/home/spark/test_spark_sjr/fire_risk_assessment/model_save file:/home/spark/test_spark_sjr/fire_risk_assessment/result_save

# stop the master and the slaves
stop-all.sh



