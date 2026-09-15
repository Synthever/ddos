#!/usr/bin/env python3
"""Merge all proxy lists, dedupe, test each against target, keep only working ones."""
import concurrent.futures, os, sys, socket

PROXY_DIR = "files/proxys"
OUTPUT = "files/proxys/alive.txt"
TARGET_HOST = "ai.tamandata.com"
TARGET_PORT = 443
TIMEOUT = 3

def collect():
    proxies = set()
    for f in os.listdir(PROXY_DIR):
        fp = os.path.join(PROXY_DIR, f)
        if not f.endswith(".txt") or f == "alive.txt":
            continue
        with open(fp) as fh:
            for line in fh:
                line = line.strip()
                if line and ":" in line:
                    proxies.add(line)
    return list(proxies)

def test_proxy(proxy):
    """Try TCP connect through proxy (HTTP CONNECT) to target."""
    ip, port = proxy.split(":")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((ip, int(port)))
        # HTTP CONNECT to target
        s.send(f"CONNECT {TARGET_HOST}:{TARGET_PORT} HTTP/1.1\r\nHost: {TARGET_HOST}\r\n\r\n".encode())
        resp = s.recv(1024)
        s.close()
        if b"200" in resp or b"Connection established" in resp:
            return proxy
    except:
        pass
    return None

if __name__ == "__main__":
    proxies = collect()
    print(f"Total collected: {len(proxies)}")

    alive = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
        for i, result in enumerate(ex.map(test_proxy, proxies)):
            if result:
                alive.append(result)
            if (i + 1) % 500 == 0:
                print(f"Checked {i+1}/{len(proxies)}, alive: {len(alive)}")

    alive = sorted(set(alive))
    with open(OUTPUT, "w") as f:
        f.write("\n".join(alive) + "\n")
    print(f"\nAlive: {len(alive)} / {len(proxies)}")
    print(f"Saved to {OUTPUT}")
