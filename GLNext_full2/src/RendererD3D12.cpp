#include <glnext/Renderer.hpp>
#include <iostream>

namespace glnext {

class RendererD3D12 : public Renderer {
public:
    bool init(GLFWwindow* /*window*/) override { return true; }
    void beginFrame() override {}
    void endFrame() override {}
    void present() override { std::cout << "[D3D12 stub] Use Vulkan backend for now.\n"; }
};

} // namespace glnext
