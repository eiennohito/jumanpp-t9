add_executable(jumanpp_t9 jumanpp_t9.cc)
target_link_libraries(jumanpp_t9 jpp_core)

include(../jumanpp/cmake/JumanppStaticFeatures.cmake)
jumanpp_gen_static(jumanpp_t9.spec JppT9Static JPP_T9_CGDIR JPP_T9_CG_SRC)

add_executable(jumanpp_t9_s jumanpp_t9_static.cc ${JPP_T9_CG_SRC})
target_include_directories(jumanpp_t9_s PRIVATE ${JPP_T9_CGDIR})
target_link_libraries(jumanpp_t9_s jpp_core)