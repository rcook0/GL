#pragma once
#include <memory>
struct GLFWwindow;

namespace glnext {

enum class Backend { D3D12, Vulkan, D3D11 };

class Renderer {
public:
    static std::unique_ptr<Renderer> Create(Backend b);
    virtual bool init(GLFWwindow* window) = 0;
    virtual void beginFrame() = 0;
    virtual void endFrame() = 0;
    virtual void present() = 0;
    virtual ~Renderer() = default;
};

} // namespace glnext
