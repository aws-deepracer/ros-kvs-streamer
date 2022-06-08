#!/bin/sh

echo "[kvs]: clone utils-common"
git clone https://github.com/aws-robotics/utils-common
cd utils-common || exit
echo "[kvs]: checkout commit b70e9416968ca5a56fd263ff9c96c80793a7230f for utils-common"
git checkout b70e9416968ca5a56fd263ff9c96c80793a7230f
git apply ../patch/utils-common.patch
cd ..

echo "[kvs]: clone utils-ros1"
git clone https://github.com/aws-robotics/utils-ros1
cd utils-ros1 || exit
echo "[kvs]: checkout commit d4d64f73727149fd8885f13581a74d5ca6dcfb6c"
git checkout d4d64f73727149fd8885f13581a74d5ca6dcfb6c
git apply ../patch/utils-ros1.patch
cd ..

echo "[kvs]: clone kinesisvideo-encoder-common"
git clone https://github.com/aws-robotics/kinesisvideo-encoder-common
cd kinesisvideo-encoder-common || exit
echo "[kvs]: checkout commit b798a06cca43891170d33da3aa329648c864a418"
git checkout b798a06cca43891170d33da3aa329648c864a418
git apply ../patch/kinesisvideo-encoder-common.patch
cd ..

echo "[kvs]: clone kinesisvideo-encoder-ros1"
git clone https://github.com/aws-robotics/kinesisvideo-encoder-ros1
cd kinesisvideo-encoder-ros1 || exit
echo "[kvs]: checkout commit d2e3fb3e72fc481e18b8c29e4d831707e453d276"
git checkout d2e3fb3e72fc481e18b8c29e4d831707e453d276
git apply ../patch/kinesisvideo-encoder-ros1.patch
cd ..

echo "[kvs]: clone kinesisvideo-common"
git clone https://github.com/aws-robotics/kinesisvideo-common
cd kinesisvideo-common || exit
echo "[kvs]: checkout commit b0b4d9f011454a22957383cf3ef5c781e2384a96"
git checkout b0b4d9f011454a22957383cf3ef5c781e2384a96
git apply ../patch/kinesisvideo-common.patch
cd ..

echo "[kvs]: clone kinesisvideo-ros1"
git clone https://github.com/aws-robotics/kinesisvideo-ros1
cd kinesisvideo-ros1 || exit
echo "[kvs]: checkout commit ad9014035ca16d5b212c4f58ffcbb346a53b441b"
git checkout ad9014035ca16d5b212c4f58ffcbb346a53b441b
git apply ../patch/kinesisvideo-ros1.patch
cd ..
