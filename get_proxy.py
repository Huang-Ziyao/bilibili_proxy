#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动获取免费HTTP代理工具
从多个免费代理源获取代理并保存到 proxy.txt
"""

import requests
import re


def get_proxy_from_geonode():
    """
    从 geonode 获取免费代理 (API方式，最可靠)
    """
    print("正在从 geonode 获取代理...")
    
    url = "https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=http"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            proxies = []
            
            for proxy in data.get('data', []):
                ip = proxy.get('ip')
                port = proxy.get('port')
                protocols = proxy.get('protocols', [])
                
                if ip and port and 'http' in protocols:
                    proxies.append(f"{ip}:{port}")
            
            print(f"✓ 从 geonode 获取 {len(proxies)} 个代理")
            return proxies
        else:
            print(f"✗ geonode 请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"✗ geonode 获取失败：{e}")
        return []


def get_proxy_from_proxy_list_download():
    """
    从 proxy-list.download 获取代理
    """
    print("正在从 proxy-list.download 获取代理...")
    
    url = "https://www.proxy-list.download/api/v1/get?type=http"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            proxy_list = response.text.strip().split('\n')
            proxies = [p.strip() for p in proxy_list if ':' in p.strip()]
            print(f"✓ 从 proxy-list.download 获取 {len(proxies)} 个代理")
            return proxies
        else:
            print(f"✗ proxy-list.download 请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"✗ proxy-list.download 获取失败：{e}")
        return []


def get_proxy_from_openproxylist():
    """
    从 openproxylist.xyz 获取代理
    """
    print("正在从 openproxylist.xyz 获取代理...")
    
    urls = [
        "https://openproxylist.xyz/http.txt",
        "https://openproxylist.xyz/https.txt"
    ]
    
    proxies = []
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                proxy_list = response.text.strip().split('\n')
                valid = [p.strip() for p in proxy_list if ':' in p.strip()]
                proxies.extend(valid)
        except Exception as e:
            pass
    
    if proxies:
        print(f"✓ 从 openproxylist.xyz 获取 {len(proxies)} 个代理")
    else:
        print(f"✗ openproxylist.xyz 获取失败")
    
    return proxies


def get_proxy_from_freeproxylists():
    """
    从 freeproxylists.net 获取代理
    """
    print("正在从 freeproxylists.net 获取代理...")
    
    url = "https://www.freeproxylists.net/zh/?page=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # 解析HTML获取代理
            pattern = r'<td class="ipport">([\d\.]+:\d+)</td>'
            matches = re.findall(pattern, response.text)
            proxies = list(set(matches))  # 去重
            print(f"✓ 从 freeproxylists.net 获取 {len(proxies)} 个代理")
            return proxies
        else:
            print(f"✗ freeproxylists.net 请求失败，状态码：{response.status_code}")
            return []
    except Exception as e:
        print(f"✗ freeproxylists.net 获取失败：{e}")
        return []


def validate_proxy(proxy):
    """
    验证代理格式是否正确
    """
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'
    return bool(re.match(pattern, proxy))


def save_proxies(proxies, filename="proxy.txt"):
    """
    保存代理到文件
    """
    # 去重
    unique_proxies = list(set(proxies))
    
    # 验证格式
    valid_proxies = [p for p in unique_proxies if validate_proxy(p)]
    
    with open(filename, 'w', encoding='utf-8') as f:
        for proxy in valid_proxies:
            f.write(proxy + '\n')
    
    print(f"\n✓ 已保存 {len(valid_proxies)} 个有效代理到 {filename}")
    return len(valid_proxies)


def main():
    print("=" * 60)
    print(" " * 18 + "自动代理获取工具")
    print("=" * 60)
    print()
    
    all_proxies = []
    
    # 从多个源获取代理
    sources = [
        get_proxy_from_geonode,
        get_proxy_from_proxy_list_download,
        get_proxy_from_openproxylist,
        get_proxy_from_freeproxylists,
    ]
    
    for source_func in sources:
        proxies = source_func()
        all_proxies.extend(proxies)
        print()
    
    if all_proxies:
        count = save_proxies(all_proxies)
        print(f"\n总共获取 {count} 个可用代理")
        print("\n前10个代理示例:")
        for i, proxy in enumerate(all_proxies[:10], 1):
            print(f"  {i}. {proxy}")
        
        print(f"\n提示：运行 python bilibili_proxy.py 使用这些代理刷播放量")
    else:
        print("\n✗ 未能获取到任何代理，请稍后重试")
        print("可能原因:")
        print("  1. 网络连接问题")
        print("  2. 代理源暂时不可用")
        print("  3. 需要更换其他代理源")


if __name__ == "__main__":
    main()
