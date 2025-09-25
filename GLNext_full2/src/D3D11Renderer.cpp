#include "D3D11Renderer.hpp"
#include "Buffer.hpp" // your Buffer class
#include <d3dcompiler.h>
#include <vector>
#include <stdexcept>

// link libs (MSVC) - in CMake you can link d3d11 dxgi d3dcompiler
#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")
#pragma comment(lib, "d3dcompiler.lib")

using Microsoft::WRL::ComPtr;

struct Vertex { float x,y,z,u,v; };

static const char* vs_src = R"(
cbuffer cb : register(b0) {}
struct VS_IN { float3 pos : POSITION; float2 uv : TEXCOORD0; };
struct PS_IN { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
PS_IN main(VS_IN vin) {
    PS_IN o; o.pos = float4(vin.pos, 1.0f); o.uv = vin.uv; return o;
}
)";

static const char* ps_src = R"(
Texture2D tex : register(t0);
SamplerState samp : register(s0);
struct PS_IN { float4 pos : SV_POSITION; float2 uv : TEXCOORD0; };
float4 main(PS_IN i) : SV_TARGET {
    return tex.Sample(samp, i.uv);
}
)";

D3D11Renderer::D3D11Renderer() {}
D3D11Renderer::~D3D11Renderer() { shutdown(); }

bool D3D11Renderer::init(HWND hwnd, int width, int height) {
    if (!createDeviceAndSwapChain(hwnd, width, height)) return false;
    return createResources(width, height);
}

bool D3D11Renderer::createDeviceAndSwapChain(HWND hwnd, int width, int height) {
    DXGI_SWAP_CHAIN_DESC sd{};
    sd.BufferCount = 1;
    sd.BufferDesc.Width = width;
    sd.BufferDesc.Height = height;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hwnd;
    sd.SampleDesc.Count = 1;
    sd.Windowed = TRUE;

    UINT flags = 0;
#ifdef _DEBUG
    flags |= D3D11_CREATE_DEVICE_DEBUG;
#endif

    D3D_FEATURE_LEVEL fl;
    HRESULT hr = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, flags,
        nullptr, 0, D3D11_SDK_VERSION, &sd, &swapchain_,
        &device_, &fl, &ctx_);

    if (FAILED(hr)) return false;

    // create RTV for backbuffer
    ComPtr<ID3D11Texture2D> backbuf;
    hr = swapchain_->GetBuffer(0, IID_PPV_ARGS(&backbuf));
    if (FAILED(hr)) return false;
    hr = device_->CreateRenderTargetView(backbuf.Get(), nullptr, &rtv_);
    if (FAILED(hr)) return false;

    width_ = width; height_ = height;
    ctx_->OMSetRenderTargets(1, rtv_.GetAddressOf(), nullptr);
    return true;
}

bool D3D11Renderer::createResources(int width, int height) {
    // Create a dynamic texture that we'll Map each frame (BGRA)
    D3D11_TEXTURE2D_DESC td{};
    td.Width = width;
    td.Height = height;
    td.MipLevels = 1;
    td.ArraySize = 1;
    td.Format = DXGI_FORMAT_B8G8R8A8_UNORM; // BGRA8
    td.SampleDesc.Count = 1;
    td.Usage = D3D11_USAGE_DYNAMIC;
    td.BindFlags = D3D11_BIND_SHADER_RESOURCE;
    td.CPUAccessFlags = D3D11_CPU_ACCESS_WRITE;

    HRESULT hr = device_->CreateTexture2D(&td, nullptr, &texture_);
    if (FAILED(hr)) return false;

    D3D11_SHADER_RESOURCE_VIEW_DESC srvd{};
    srvd.Format = td.Format;
    srvd.ViewDimension = D3D11_SRV_DIMENSION_TEXTURE2D;
    srvd.Texture2D.MipLevels = 1;
    hr = device_->CreateShaderResourceView(texture_.Get(), &srvd, &srv_);
    if (FAILED(hr)) return false;

    // sampler
    D3D11_SAMPLER_DESC smd{};
    smd.Filter = D3D11_FILTER_MIN_MAG_MIP_LINEAR;
    smd.AddressU = D3D11_TEXTURE_ADDRESS_CLAMP;
    smd.AddressV = D3D11_TEXTURE_ADDRESS_CLAMP;
    smd.AddressW = D3D11_TEXTURE_ADDRESS_CLAMP;
    device_->CreateSamplerState(&smd, &sampler_);

    // compile shaders
    ComPtr<ID3DBlob> vsb, psb, err;
    D3DCompile(vs_src, strlen(vs_src), nullptr, nullptr, nullptr, "main", "vs_4_0", 0, 0, &vsb, &err);
    D3DCompile(ps_src, strlen(ps_src), nullptr, nullptr, nullptr, "main", "ps_4_0", 0, 0, &psb, &err);

    device_->CreateVertexShader(vsb->GetBufferPointer(), vsb->GetBufferSize(), nullptr, &vs_);
    device_->CreatePixelShader(psb->GetBufferPointer(), psb->GetBufferSize(), nullptr, &ps_);

    // input layout
    D3D11_INPUT_ELEMENT_DESC ied[] = {
        {"POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, offsetof(Vertex,x), D3D11_INPUT_PER_VERTEX_DATA, 0},
        {"TEXCOORD", 0, DXGI_FORMAT_R32G32_FLOAT, 0, offsetof(Vertex,u), D3D11_INPUT_PER_VERTEX_DATA, 0}
    };
    device_->CreateInputLayout(ied, 2, vsb->GetBufferPointer(), vsb->GetBufferSize(), &inputLayout_);

    // fullscreen quad vertex buffer (two triangles)
    Vertex quad[] = {
        {-1,-1,0, 0.0f,1.0f},
        {-1, 1,0, 0.0f,0.0f},
        { 1,-1,0, 1.0f,1.0f},
        { 1, 1,0, 1.0f,0.0f}
    };
    D3D11_BUFFER_DESC bd{};
    bd.Usage = D3D11_USAGE_IMMUTABLE;
    bd.ByteWidth = sizeof(quad);
    bd.BindFlags = D3D11_BIND_VERTEX_BUFFER;
    D3D11_SUBRESOURCE_DATA sdv{};
    sdv.pSysMem = quad;
    device_->CreateBuffer(&bd, &sdv, &vb_);

    // input assembly & viewport set later in render
    return true;
}

void D3D11Renderer::resize(int width, int height) {
    if (!swapchain_) return;
    ctx_->OMSetRenderTargets(0, nullptr, nullptr);
    rtv_.Reset();
    swapchain_->ResizeBuffers(0, width, height, DXGI_FORMAT_UNKNOWN, 0);
    ComPtr<ID3D11Texture2D> backbuf;
    swapchain_->GetBuffer(0, IID_PPV_ARGS(&backbuf));
    device_->CreateRenderTargetView(backbuf.Get(), nullptr, &rtv_);
    ctx_->OMSetRenderTargets(1, rtv_.GetAddressOf(), nullptr);
    width_ = width; height_ = height;
}

void D3D11Renderer::render(const Buffer &buf) {
    if (!ctx_ || !texture_) return;
    // map texture and copy pixels
    D3D11_MAPPED_SUBRESOURCE mapped;
    HRESULT hr = ctx_->Map(texture_.Get(), 0, D3D11_MAP_WRITE_DISCARD, 0, &mapped);
    if (FAILED(hr)) return;

    // assume Buffer provides width(), height() and getPixels() returning pointer to uint32_t
    // If buffer pixel format is ARGB, swap bytes to BGRA here.
    const uint32_t* src = buf.dataPointer(); // implement this accessor in Buffer
    int bw = buf.width(), bh = buf.height();
    // copy row-by-row taking into account pitch
    for (int y = 0; y < bh; ++y) {
        uint8_t* destRow = reinterpret_cast<uint8_t*>(mapped.pData) + y * mapped.RowPitch;
        const uint8_t* srcRow = reinterpret_cast<const uint8_t*>(src + y * bw);
        // If needed, convert ARGB -> BGRA per pixel:
        for (int x = 0; x < bw; ++x) {
            uint32_t pix = *(const uint32_t*)(srcRow + x*4);
            // Example conversion from ARGB (A R G B) to BGRA (B G R A):
            uint8_t a = (pix >> 24) & 0xFF;
            uint8_t r = (pix >> 16) & 0xFF;
            uint8_t g = (pix >> 8) & 0xFF;
            uint8_t b = (pix      ) & 0xFF;
            uint32_t out = (b) | (g<<8) | (r<<16) | (a<<24);
            reinterpret_cast<uint32_t*>(destRow)[x] = out;
        }
    }
    ctx_->Unmap(texture_.Get(), 0);

    // Clear RTV
    float clearColor[4] = {0.f,0.f,0.f,1.f};
    ctx_->ClearRenderTargetView(rtv_.Get(), clearColor);

    // set pipeline
    UINT stride = sizeof(Vertex);
    UINT offset = 0;
    ctx_->IASetInputLayout(inputLayout_.Get());
    ctx_->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP);
    ctx_->IASetVertexBuffers(0, 1, vb_.GetAddressOf(), &stride, &offset);
    ctx_->VSSetShader(vs_.Get(), nullptr, 0);
    ctx_->PSSetShader(ps_.Get(), nullptr, 0);
    ctx_->PSSetShaderResources(0, 1, srv_.GetAddressOf());
    ctx_->PSSetSamplers(0,1, sampler_.GetAddressOf());

    // set viewport
    D3D11_VIEWPORT vp; vp.TopLeftX=0; vp.TopLeftY=0; vp.Width=(float)width_; vp.Height=(float)height_; vp.MinDepth=0; vp.MaxDepth=1;
    ctx_->RSSetViewports(1,&vp);

    // draw 4 vertices (triangle-strip)
    ctx_->Draw(4,0);
}

void D3D11Renderer::present() {
    if (swapchain_) swapchain_->Present(1,0);
}

void D3D11Renderer::shutdown() {
    rtv_.Reset(); srv_.Reset(); texture_.Reset(); vb_.Reset(); ps_.Reset(); vs_.Reset(); inputLayout_.Reset();
    sampler_.Reset(); ctx_.Reset(); device_.Reset(); swapchain_.Reset();
}
