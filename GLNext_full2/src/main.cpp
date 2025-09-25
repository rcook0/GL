\
#include <windows.h>
#include <chrono>
#include "D3D11Renderer.hpp"
#include "Buffer.hpp"
#include <thread>
#include <vector>
using namespace std::chrono;

static D3D11Renderer renderer;
static Buffer buf(256,256);

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
    case WM_SIZE:
        renderer.resize(LOWORD(lParam), HIWORD(lParam));
        return 0;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hwnd,msg,wParam,lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    WNDCLASS wc{};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"D3DTestWindow";
    RegisterClass(&wc);
    HWND hwnd = CreateWindowEx(0, wc.lpszClassName, L"D3D11 Renderer Test", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, nullptr, nullptr, hInstance, nullptr);
    ShowWindow(hwnd, nCmdShow);

    if (!renderer.init(hwnd, 800, 600)) {
        MessageBox(hwnd, L"Failed to init D3D11", L"Error", MB_OK);
        return -1;
    }

    int w = buf.width(), h = buf.height();
    for (int y=0;y<h;++y) for (int x=0;x<w;++x) {
        uint8_t r = (uint8_t)(x*255/w);
        uint8_t g = (uint8_t)(y*255/h);
        uint8_t b = 128;
        buf.data()[y*w + x] = (255u<<24) | (r<<16) | (g<<8) | b;
    }

    MSG msg{};
    auto last = high_resolution_clock::now();
    while (true) {
        while (PeekMessage(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message==WM_QUIT) goto exit;
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        auto now = high_resolution_clock::now();
        double t = duration_cast<milliseconds>(now-last).count()/1000.0;
        for (int y=0;y<h;++y) for (int x=0;x<w;++x) {
            uint32_t p = buf.data()[y*w + x];
            uint8_t r = (p>>16)&0xFF;
            uint8_t g = (p>>8)&0xFF;
            uint8_t b = p&0xFF;
            uint8_t nr = (uint8_t)((r + (int)(t*30))%256);
            buf.data()[y*w + x] = (255u<<24) | (nr<<16) | (g<<8) | b;
        }
        renderer.renderTexture(buf);
        std::vector<Vertex> tri = { { -0.5f, -0.5f, 0.0f, 0.0f, 0.0f }, { 0.5f,-0.5f,0.0f,1.0f,0.0f }, {0.0f,0.5f,0.0f,0.5f,1.0f} };
        renderer.renderPrimitives(tri, D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
        renderer.present();
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }
exit:
    renderer.shutdown();
    return 0;
}
