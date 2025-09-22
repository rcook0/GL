set(SOURCES
    RendererD3D12.cpp
    RendererVulkan.cpp
    Scene.cpp
    RenderGraph.cpp
)

add_library(glnext STATIC ${SOURCES})
target_include_directories(glnext PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${Vulkan_INCLUDE_DIRS}
)
target_link_libraries(glnext PUBLIC
    ${Vulkan_LIBRARIES}
    glfw
)
if(WIN32)
  target_link_libraries(glnext PUBLIC d3d12 dxgi)
endif()

# Demo executable
add_executable(glnext_demo main.cpp)
target_link_libraries(glnext_demo PRIVATE glnext)
