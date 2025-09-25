#pragma once
#include <d3d11.h>
#include <wrl.h>
#include <cstdint>
#include <vector>

class Buffer; // forward

struct Vertex { float x,y,z; float u,v; };

class D3D11Renderer {
public:
    D3D11Renderer();
    ~D3D11Renderer();

    bool init(HWND hwnd, int width, int height);
    void resize(int width, int height);
    void renderTexture(const Buffer &buf); // upload buffer as texture and draw quad
    void renderPrimitives(const std::vector<Vertex>& verts, D3D11_PRIMITIVE_TOPOLOGY topo = D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
    void present();
    void shutdown();

private:
    bool createDeviceAndSwapChain(HWND hwnd, int width, int height);
    bool createResources(int width, int height);
    bool ensureDynamicVB(size_t byteSize);

    Microsoft::WRL::ComPtr<ID3D11Device>           device_;
    Microsoft::WRL::ComPtr<ID3D11DeviceContext>    ctx_;
    Microsoft::WRL::ComPtr<IDXGISwapChain>         swapchain_;
    Microsoft::WRL::ComPtr<ID3D11RenderTargetView> rtv_;
    Microsoft::WRL::ComPtr<ID3D11Texture2D>        texture_;
    Microsoft::WRL::ComPtr<ID3D11ShaderResourceView> srv_;
    Microsoft::WRL::ComPtr<ID3D11SamplerState>     sampler_;
    Microsoft::WRL::ComPtr<ID3D11VertexShader>     vs_;
    Microsoft::WRL::ComPtr<ID3D11PixelShader>      ps_;
    Microsoft::WRL::ComPtr<ID3D11InputLayout>      inputLayout_;
    Microsoft::WRL::ComPtr<ID3D11Buffer>           vb_; // fullscreen quad
    Microsoft::WRL::ComPtr<ID3D11Buffer>           dynVB_; // dynamic vertex buffer for primitives
    Microsoft::WRL::ComPtr<ID3D11Buffer>           ib_; // index buffer if needed
    int width_{0}, height_{0};
    size_t dynVBSize_{0};
};