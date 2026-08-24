cmake_minimum_required(VERSION 3.16)
project(nlcs_brx_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(nlcs_brx_core STATIC
    src/nlcs_block_index.cpp
)
target_include_directories(nlcs_brx_core PUBLIC include)
set_target_properties(nlcs_brx_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

option(NLCS_BUILD_TESTS "Build the SDK-independent BRX core tests" ON)
if(NLCS_BUILD_TESTS)
    enable_testing()
    add_executable(nlcs_block_index_test tests/nlcs_block_index_test.cpp)
    target_link_libraries(nlcs_block_index_test PRIVATE nlcs_brx_core)
    add_test(
        NAME nlcs_block_index_test
        COMMAND nlcs_block_index_test
            ${CMAKE_CURRENT_SOURCE_DIR}/../data/nlcs/tabellen/publicatie/5.02-symbolen.csv
            ${CMAKE_CURRENT_SOURCE_DIR}/../data/nlcs/symbolen/autocad
    )
endif()

set(BRX26_SDK_PATH "$ENV{BRX26_SDK_PATH}" CACHE PATH
    "Path to the BricsCAD V26 BRX SDK")
set(BRX26_RUNTIME_PATH "$ENV{BRX26_RUNTIME_PATH}" CACHE PATH
    "Path to the installed BricsCAD V26 Linux runtime")
option(NLCS_BUILD_BRX "Build the BricsCAD V26 Linux module" ON)
option(NLCS_ENABLE_QT_PANEL "Enable experimental Qt panel (may conflict with BricsCAD Qt)" OFF)

if(NLCS_BUILD_BRX)
    if(NOT BRX26_RUNTIME_PATH)
        set(BRX26_RUNTIME_PATH "/opt/bricsys/bricscad/v26")
    endif()
    if(NOT BRX26_SDK_PATH OR NOT EXISTS "${BRX26_SDK_PATH}/inc/arxHeaders.h")
        message(STATUS "BRX26_SDK_PATH not set; skipping nlcs_brx.lrx")
    elseif(NOT EXISTS "${BRX26_RUNTIME_PATH}/libbrx26.so")
        message(STATUS "BricsCAD Linux runtime not found; skipping nlcs_brx.lrx")
    else()
        set(NLCS_BRX_SOURCES src/nlcs_brx_entry.cpp)
        if(NLCS_ENABLE_QT_PANEL)
            find_package(Qt5 COMPONENTS Widgets REQUIRED)
            list(APPEND NLCS_BRX_SOURCES src/nlcs_panel.cpp)
        endif()
        add_library(nlcs_brx MODULE ${NLCS_BRX_SOURCES})
        target_compile_definitions(nlcs_brx PRIVATE
            BRX_APP _ACRXAPP BRX_APP __BRXTARGET=26 _FILE_OFFSET_BITS=64
            NLCS_DEFAULT_ROOT="${CMAKE_CURRENT_SOURCE_DIR}/.."
        )
        target_compile_options(nlcs_brx PRIVATE -fPIC)
        if(NLCS_ENABLE_QT_PANEL)
            target_compile_definitions(nlcs_brx PRIVATE NLCS_ENABLE_QT_PANEL)
            target_link_libraries(nlcs_brx PRIVATE Qt5::Widgets)
        endif()
        target_include_directories(nlcs_brx PRIVATE
            "${CMAKE_CURRENT_SOURCE_DIR}/include"
            "${BRX26_SDK_PATH}/inc"
            "${BRX26_SDK_PATH}/inc/Platform/substitutes"
        )
        target_link_options(nlcs_brx PRIVATE
            "-Wl,-whole-archive,${BRX26_RUNTIME_PATH}/libdrx_entrypoint.a"
            "-Wl,-no-whole-archive"
        )
        target_link_libraries(nlcs_brx PRIVATE
            nlcs_brx_core
            "${BRX26_RUNTIME_PATH}/libbrx26.so"
        )
        set_target_properties(nlcs_brx PROPERTIES PREFIX "" SUFFIX ".lrx")
    endif()
endif()
