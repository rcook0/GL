#pragma once
#include <vector>
#include <cstdint>
class Buffer {
public:
    Buffer(int w=128,int h=128): w_(w), h_(h), data_(w*h,0) {}
    void resize(int w,int h){ w_=w; h_=h; data_.assign(w*h,0); }
    int width() const{return w_;}
    int height() const{return h_;}
    const uint32_t* dataPointer() const{return data_.data();}
    uint32_t* dataPointer(){ return data_.data(); }
    std::vector<uint32_t>& data() { return data_; }
private:
    int w_, h_;
    std::vector<uint32_t> data_;
};