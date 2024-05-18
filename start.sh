#!/bin/bash
   docker run -it -p 5000:5000 \
   -v /home/sudonuma/Documents/mlruns:/app/mlruns \
   -v /home/sudonuma/Documents/DataLabelledRice:/app/DataLabelledRice \
   testui