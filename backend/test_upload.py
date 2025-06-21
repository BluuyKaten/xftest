#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def test_file_paths():
    """测试文件路径处理"""
    
    # 模拟上传的文件路径
    upload_folder = 'uploads'
    filename = '20250621_114735_audio1.wav'
    
    # 构建文件路径
    filepath = os.path.join(upload_folder, filename)
    abs_filepath = os.path.abspath(filepath)
    
    print(f"上传文件夹: {upload_folder}")
    print(f"文件名: {filename}")
    print(f"相对路径: {filepath}")
    print(f"绝对路径: {abs_filepath}")
    
    # 检查文件是否存在
    print(f"相对路径存在: {os.path.exists(filepath)}")
    print(f"绝对路径存在: {os.path.exists(abs_filepath)}")
    
    # 测试basename提取
    basename = os.path.basename(filepath)
    print(f"提取的文件名: {basename}")
    
    # 测试在uploads目录中查找
    uploads_path = os.path.join(upload_folder, basename)
    print(f"uploads目录中的路径: {uploads_path}")
    print(f"uploads路径存在: {os.path.exists(uploads_path)}")

if __name__ == "__main__":
    test_file_paths() 