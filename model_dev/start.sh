#!/bin/bash
   docker run -it -p 5000:5000 \
   -v /home/sudonuma/Documents/RiceLeafClassification/mlruns:/model_dev/mlruns \
   -v /home/sudonuma/Documents/DataLabelledRice:/model_dev/DataLabelledRice \
   model_development