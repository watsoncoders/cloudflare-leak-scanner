import dns.resolver
import requests
import subprocess
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

common_subdomains = [
    "www", "mail", "ftp", "direct", "server", "cpanel", "webmail",
    "ns1", "ns2", "admin", "dev", "test", "api", "origin"
]

def resolve_subdomain(domain, subdomain):
    full_domain = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(full_domain, 'A')
        return [rdata.to_text() for rdata in answers]
    except:
        return []

def is_behind_cloudflare(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/org", timeout=5)
        return "Cloudflare" in r.text
    except:
        return True  # assume protected if timeout

def scan_ports(ip):
    try:
        result = subprocess.check_output([
            "masscan", ip, "-p1-1000", "--rate", "1000"
        ], stderr=subprocess.DEVNULL).decode()
        ports = []
        for line in result.splitlines():
            if "Discovered open port" in line:
                parts = line.split()
                ports.append(parts[3])
        return sorted(set(ports))
    except:
        return []

def generate_report(domain, results):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")
    output = template.render(domain=domain, results=results)
    Path("report.html").write_text(output, encoding="utf-8")
    print("✅ דוח נוצר: report.html")

def main():
    domain = input("🔍 הכנס דומיין לבדיקה (למשל example.com): ").strip()
    final_results = []
    for sub in common_subdomains:
        ips = resolve_subdomain(domain, sub)
        for ip in ips:
            behind_cf = is_behind_cloudflare(ip)
            ports = scan_ports(ip) if not behind_cf else []
            final_results.append({
                "subdomain": f"{sub}.{domain}",
                "ip": ip,
                "behind_cf": behind_cf,
                "ports": ports
            })
    generate_report(domain, final_results)

if __name__ == "__main__":
    main()
