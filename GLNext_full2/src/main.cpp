#include <GLFW/glfw3.h>
#include <glnext/Renderer.hpp>
#include <iostream>
using namespace glnext;

int main() {
    if (!glfwInit()) { std::cerr << "Failed to init GLFW\n"; return -1; }
    glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
    GLFWwindow* window = glfwCreateWindow(800, 600, "GLNext Demo", nullptr, nullptr);
    if (!window) { std::cerr << "Failed to create window\n"; glfwTerminate(); return -1; }
    auto renderer = Renderer::Create(Backend::Vulkan);
    if (!renderer) { std::cerr << "Failed to create renderer\n"; glfwDestroyWindow(window); glfwTerminate(); return -1; }
    if (!renderer->init(window)) { std::cerr << "Renderer init failed\n"; glfwDestroyWindow(window); glfwTerminate(); return -1; }

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
        renderer->beginFrame();
        renderer->endFrame();
        renderer->present();
    }
    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
