# cmake 的最小版本要求
cmake_minimum_required(VERSION 3.12)

# 这个CMakeLists管理的工程名称
project(cmakeTest)

# 设置C++标准为 C++ 11
set(CMAKE_CXX_STANDARD 17)

#设定头文件目录,主程序中的#include的.h文件坐在的目录
INCLUDE_DIRECTORIES( ${PROJECT_SOURCE_DIR}/include)

#生成可执行程序 语法:add_executable(可执行程序名 要编译的cpp)
add_executable(cmakeTest main.cpp )
