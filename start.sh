#!/bin/bash
   docker run -it -p 5000:5000 \
   -v /home/user/Documents/mlruns:/app/mlruns \
   -v /home/user/Documents/DataLabelledRice:/app/DataLabelledRice \
   riceleaf