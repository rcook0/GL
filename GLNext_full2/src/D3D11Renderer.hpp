#pragma once
#include <d3d11.h>
#include <wrl.h>
#include <cstdint>

class Buffer; // forward

class D3D11Renderer {
public:
    D3D11Renderer();
    ~D3D11Renderer();

    // Initialize with HWND of your window (Win32). Returns false on failure.
    bool init(HWND hwnd, int width, int height);

    // Call when window resized
    void resize(int width, int height);

    // Upload buffer pixels and render
    void render(const Buffer &buf);

    // Present swapchain
    void present();

    // Cleanup
    void shutdown();

private:
    bool createDeviceAndSwapChain(HWND hwnd, int width, int height);
    bool createResources(int width, int height);

    Microsoft::WRL::ComPtr<ID3D11Device>           device_;
    Microsoft::WRL::ComPtr<ID3D11DeviceContext>    ctx_;
    Microsoft::WRL::ComPtr<IDXGISwapChain>         swapchain_;
    Microsoft::WRL::ComPtr<ID3D11RenderTargetView> rtv_;
    Microsoft::WRL::ComPtr<ID3D11Texture2D>        texture_; // texture backing Buffer
    Microsoft::WRL::ComPtr<ID3D11ShaderResourceView> srv_;
    Microsoft::WRL::ComPtr<ID3D11SamplerState>     sampler_;
    Microsoft::WRL::ComPtr<ID3D11VertexShader>     vs_;
    Microsoft::WRL::ComPtr<ID3D11PixelShader>      ps_;
    Microsoft::WRL::ComPtr<ID3D11InputLayout>      inputLayout_;
    Microsoft::WRL::ComPtr<ID3D11Buffer>           vb_; // fullscreen quad
    int width_{0}, height_{0};
};
