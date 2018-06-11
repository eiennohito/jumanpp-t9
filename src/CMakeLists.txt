function(jumanpp_gen_static spec sources)
  set(CODEGEN_OUTDIR "${CMAKE_CURRENT_BINARY_DIR}/codegen/")
  set()
  add_custom_command(
    COMMAND jumanpp_tool
    ARGS static-features
    DEPENDS ${spec} ${jumanpp_tool}
    OUTPUT ${CG_OUT_SRC} ${CG_OUT_HDR}
  )
endfunction()

add_executable(jumanpp_t9 jumanpp_t9.cc)
target_link_libraries(jumanpp_t9 jpp_core)