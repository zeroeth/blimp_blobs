Building
========

    brew install opencv
    g++ source_file.cpp -o output_executable `pkg-config --cflags opencv` `pkg-config --libs opencv`
