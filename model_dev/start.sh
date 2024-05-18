#!/bin/bash
   docker run -it -p 5000:5000 \
   -v /home/sudonuma/Documents/RiceLeafClassification/app/mlruns:/ap/mlruns \
   -v /home/user/Documents/DataLabelledRice:/app/DataLabelledRice \
   testapp