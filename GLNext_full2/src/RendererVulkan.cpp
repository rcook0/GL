#include <glnext/Renderer.hpp>
#include <vulkan/vulkan.h>
#include <GLFW/glfw3.h>
#include <vector>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <algorithm>

namespace glnext {

static void vkchk(VkResult r, const char* where) {
    if (r != VK_SUCCESS) {
        std::cerr << "Vulkan error at " << where << " (" << r << ")\n";
        throw std::runtime_error("Vulkan failure");
    }
}

class RendererVulkan : public Renderer {
public:
    bool init(GLFWwindow* window) override {
        createInstance(window);
        createSurface(window);
        pickPhysicalDevice();
        createDevice();
        createSwapchain();
        createImageViews();
        createRenderPass();
        createFramebuffers();
        createCommandPool();
        allocateCommandBuffers();
        recordCommandBuffers();
        createSync();
        return true;
    }

    void beginFrame() override {
        vkWaitForFences(device, 1, &inFlight, VK_TRUE, UINT64_MAX);
        vkResetFences(device, 1, &inFlight);
        vkchk(vkAcquireNextImageKHR(device, swapchain, UINT64_MAX, imageAvailable, VK_NULL_HANDLE, &currentImage), "AcquireNextImageKHR");
    }

    void endFrame() override {
        VkPipelineStageFlags waitStages[] = { VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT };
        VkSubmitInfo si{ VK_STRUCTURE_TYPE_SUBMIT_INFO };
        si.waitSemaphoreCount = 1;
        si.pWaitSemaphores = &imageAvailable;
        si.pWaitDstStageMask = waitStages;
        si.commandBufferCount = 1;
        si.pCommandBuffers = &cmdBufs[currentImage];
        si.signalSemaphoreCount = 1;
        si.pSignalSemaphores = &renderFinished;
        vkchk(vkQueueSubmit(queue, 1, &si, inFlight), "QueueSubmit");
    }

    void present() override {
        VkPresentInfoKHR pi{ VK_STRUCTURE_TYPE_PRESENT_INFO_KHR };
        pi.waitSemaphoreCount = 1;
        pi.pWaitSemaphores = &renderFinished;
        pi.swapchainCount = 1;
        pi.pSwapchains = &swapchain;
        pi.pImageIndices = &currentImage;
        vkQueuePresentKHR(queue, &pi);
    }

    ~RendererVulkan() override {
        if (device) {
            vkDeviceWaitIdle(device);
            vkDestroySemaphore(device, renderFinished, nullptr);
            vkDestroySemaphore(device, imageAvailable, nullptr);
            vkDestroyFence(device, inFlight, nullptr);
            vkDestroyCommandPool(device, cmdPool, nullptr);
            for (auto fb : framebuffers) vkDestroyFramebuffer(device, fb, nullptr);
            vkDestroyRenderPass(device, renderPass, nullptr);
            for (auto iv : imageViews) vkDestroyImageView(device, iv, nullptr);
            vkDestroySwapchainKHR(device, swapchain, nullptr);
            vkDestroyDevice(device, nullptr);
        }
        if (surface) vkDestroySurfaceKHR(instance, surface, nullptr);
        if (instance) vkDestroyInstance(instance, nullptr);
    }

private:
    VkInstance instance{};
    VkSurfaceKHR surface{};
    VkPhysicalDevice phys{};
    VkDevice device{};
    uint32_t queueFamily{};
    VkQueue queue{};
    VkSwapchainKHR swapchain{};
    std::vector<VkImage> images;
    std::vector<VkImageView> imageViews;
    VkFormat swapFormat{};
    VkExtent2D extent{};
    VkRenderPass renderPass{};
    std::vector<VkFramebuffer> framebuffers;
    VkCommandPool cmdPool{};
    std::vector<VkCommandBuffer> cmdBufs;
    VkSemaphore imageAvailable{};
    VkSemaphore renderFinished{};
    VkFence inFlight{};
    uint32_t currentImage{};

    void createInstance(GLFWwindow* /*window*/) {
        VkApplicationInfo app{ VK_STRUCTURE_TYPE_APPLICATION_INFO };
        app.pApplicationName = "GLNext Demo";
        app.apiVersion = VK_API_VERSION_1_1;

        uint32_t extCount = 0;
        const char** glfwExts = glfwGetRequiredInstanceExtensions(&extCount);

        VkInstanceCreateInfo ci{ VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO };
        ci.pApplicationInfo = &app;
        ci.enabledExtensionCount = extCount;
        ci.ppEnabledExtensionNames = glfwExts;

        vkchk(vkCreateInstance(&ci, nullptr, &instance), "CreateInstance");
    }

    void createSurface(GLFWwindow* window) {
        if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS)
            throw std::runtime_error("glfwCreateWindowSurface failed");
    }

    void pickPhysicalDevice() {
        uint32_t count=0; vkEnumeratePhysicalDevices(instance, &count, nullptr);
        if (count == 0) throw std::runtime_error("No Vulkan devices");
        std::vector<VkPhysicalDevice> devs(count);
        vkEnumeratePhysicalDevices(instance, &count, devs.data());
        for (auto d : devs) {
            uint32_t qcount=0; vkGetPhysicalDeviceQueueFamilyProperties(d, &qcount, nullptr);
            std::vector<VkQueueFamilyProperties> qfp(qcount);
            vkGetPhysicalDeviceQueueFamilyProperties(d, &qcount, qfp.data());
            for (uint32_t i=0;i<qcount;++i) {
                VkBool32 present = VK_FALSE;
                vkGetPhysicalDeviceSurfaceSupportKHR(d, i, surface, &present);
                if ((qfp[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) && present) {
                    phys = d; queueFamily = i; return;
                }
            }
        }
        throw std::runtime_error("No suitable Vulkan device");
    }

    void createDevice() {
        float prio = 1.0f;
        VkDeviceQueueCreateInfo qci{ VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO };
        qci.queueFamilyIndex = queueFamily;
        qci.queueCount = 1;
        qci.pQueuePriorities = &prio;

        const char* devExts[] = { VK_KHR_SWAPCHAIN_EXTENSION_NAME };
        VkDeviceCreateInfo dci{ VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO };
        dci.queueCreateInfoCount = 1;
        dci.pQueueCreateInfos = &qci;
        dci.enabledExtensionCount = 1;
        dci.ppEnabledExtensionNames = devExts;

        vkchk(vkCreateDevice(phys, &dci, nullptr, &device), "CreateDevice");
        vkGetDeviceQueue(device, queueFamily, 0, &queue);
    }

    void createSwapchain() {
        VkSurfaceCapabilitiesKHR caps{}; vkGetPhysicalDeviceSurfaceCapabilitiesKHR(phys, surface, &caps);
        uint32_t fmtCount=0; vkGetPhysicalDeviceSurfaceFormatsKHR(phys, surface, &fmtCount, nullptr);
        std::vector<VkSurfaceFormatKHR> formats(fmtCount);
        vkGetPhysicalDeviceSurfaceFormatsKHR(phys, surface, &fmtCount, formats.data());
        VkSurfaceFormatKHR chosen = formats[0];
        for (auto& f : formats) if (f.format == VK_FORMAT_B8G8R8A8_UNORM) { chosen = f; break; }
        swapFormat = chosen.format;
        extent = caps.currentExtent;
        if (extent.width == 0 || extent.height == 0) { extent = {800,600}; }

        VkSwapchainCreateInfoKHR sci{ VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR };
        sci.surface = surface;
        sci.minImageCount = std::max(caps.minImageCount, 2u);
        sci.imageFormat = swapFormat;
        sci.imageColorSpace = chosen.colorSpace;
        sci.imageExtent = extent;
        sci.imageArrayLayers = 1;
        sci.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
        sci.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
        sci.preTransform = caps.currentTransform;
        sci.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
        sci.presentMode = VK_PRESENT_MODE_FIFO_KHR;
        sci.clipped = VK_TRUE;
        vkchk(vkCreateSwapchainKHR(device, &sci, nullptr, &swapchain), "CreateSwapchain");

        uint32_t imgCount=0; vkGetSwapchainImagesKHR(device, swapchain, &imgCount, nullptr);
        images.resize(imgCount);
        vkGetSwapchainImagesKHR(device, swapchain, &imgCount, images.data());
    }

    void createImageViews() {
        imageViews.resize(images.size());
        for (size_t i=0;i<images.size();++i) {
            VkImageViewCreateInfo vi{ VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO };
            vi.image = images[i];
            vi.viewType = VK_IMAGE_VIEW_TYPE_2D;
            vi.format = swapFormat;
            vi.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
            vi.subresourceRange.levelCount = 1;
            vi.subresourceRange.layerCount = 1;
            vkchk(vkCreateImageView(device, &vi, nullptr, &imageViews[i]), "CreateImageView");
        }
    }

    void createRenderPass() {
        VkAttachmentDescription color{};
        color.format = swapFormat;
        color.samples = VK_SAMPLE_COUNT_1_BIT;
        color.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
        color.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
        color.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
        color.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;

        VkAttachmentReference colorRef{ 0, VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL };

        VkSubpassDescription sub{};
        sub.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
        sub.colorAttachmentCount = 1;
        sub.pColorAttachments = &colorRef;

        VkRenderPassCreateInfo rp{ VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO };
        rp.attachmentCount = 1;
        rp.pAttachments = &color;
        rp.subpassCount = 1;
        rp.pSubpasses = &sub;

        vkchk(vkCreateRenderPass(device, &rp, nullptr, &renderPass), "CreateRenderPass");
    }

    void createFramebuffers() {
        framebuffers.resize(imageViews.size());
        for (size_t i=0;i<imageViews.size();++i) {
            VkImageView atts[] = { imageViews[i] };
            VkFramebufferCreateInfo fi{ VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO };
            fi.renderPass = renderPass;
            fi.attachmentCount = 1;
            fi.pAttachments = atts;
            fi.width = extent.width;
            fi.height= extent.height;
            fi.layers= 1;
            vkchk(vkCreateFramebuffer(device, &fi, nullptr, &framebuffers[i]), "CreateFramebuffer");
        }
    }

    void createCommandPool() {
        VkCommandPoolCreateInfo pci{ VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO };
        pci.queueFamilyIndex = queueFamily;
        pci.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        vkchk(vkCreateCommandPool(device, &pci, nullptr, &cmdPool), "CreateCommandPool");
    }

    void allocateCommandBuffers() {
        cmdBufs.resize(images.size());
        VkCommandBufferAllocateInfo ai{ VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO };
        ai.commandPool = cmdPool;
        ai.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        ai.commandBufferCount = (uint32_t)cmdBufs.size();
        vkchk(vkAllocateCommandBuffers(device, &ai, cmdBufs.data()), "AllocateCommandBuffers");
    }

    void recordCommandBuffers() {
        for (size_t i=0;i<cmdBufs.size();++i) {
            VkCommandBufferBeginInfo bi{ VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO };
            vkBeginCommandBuffer(cmdBufs[i], &bi);

            VkClearValue clear{};
            clear.color = { { 0.39f, 0.58f, 0.93f, 1.0f } };

            VkRenderPassBeginInfo rpb{ VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO };
            rpb.renderPass = renderPass;
            rpb.framebuffer = framebuffers[i];
            rpb.renderArea.offset = {0,0};
            rpb.renderArea.extent = extent;
            rpb.clearValueCount = 1;
            rpb.pClearValues = &clear;

            vkCmdBeginRenderPass(cmdBufs[i], &rpb, VK_SUBPASS_CONTENTS_INLINE);
            vkCmdEndRenderPass(cmdBufs[i]);

            vkchk(vkEndCommandBuffer(cmdBufs[i]), "EndCommandBuffer");
        }
    }

    void createSync() {
        VkSemaphoreCreateInfo si{ VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO };
        vkCreateSemaphore(device, &si, nullptr, &imageAvailable);
        vkCreateSemaphore(device, &si, nullptr, &renderFinished);

        VkFenceCreateInfo fi{ VK_STRUCTURE_TYPE_FENCE_CREATE_INFO };
        fi.flags = VK_FENCE_CREATE_SIGNALED_BIT;
        vkCreateFence(device, &fi, nullptr, &inFlight);
    }
};

std::unique_ptr<Renderer> Renderer::Create(Backend b) {
    if (b == Backend::Vulkan)
        return std::make_unique<RendererVulkan>();
    return nullptr;
}

} // namespace glnext
