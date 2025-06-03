#!/usr/bin/env python3
import dns.resolver
import requests
import subprocess
import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Load subdomains from a txt file
def load_subdomains_from_file(filepath="subdomains.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        print(f"📄 Loaded {len(lines)} subdomains from {filepath}")
        return lines
    except FileNotFoundError:
        print(f"⚠️ File {filepath} not found. Using default list.")
        return []

# Resolve subdomain to IP address
def resolve_subdomain(domain, subdomain):
    full_domain = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(full_domain, 'A')
        return [rdata.to_text() for rdata in answers]
    except:
        return []

# Check if IP is behind Cloudflare
def is_behind_cloudflare(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/org", timeout=5)
        return "Cloudflare" in r.text
    except:
        return True

# Perform fast port scan using masscan
def scan_ports_masscan(ip):
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

# Use nmap to identify services on open ports
def scan_services_nmap(ip):
    try:
        result = subprocess.check_output([
            "nmap", "-sV", "-p-", "--min-rate", "500", "-T4", ip
        ], stderr=subprocess.DEVNULL).decode()
        return result
    except:
        return "N/A"

# Generate HTML report using Jinja2
def generate_report(domain, results):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")
    output = template.render(domain=domain, results=results)
    Path("report.html").write_text(output, encoding="utf-8")
    print("✅ HTML report created: report.html")

def main():
    domain = input("🔍 Enter a domain to scan (e.g., example.com): ").strip()
    subdomains = load_subdomains_from_file()
    final_results = []

    for sub in subdomains:
        ips = resolve_subdomain(domain, sub)
        for ip in ips:
            behind_cf = is_behind_cloudflare(ip)
            ports = scan_ports_masscan(ip) if not behind_cf else []
            nmap_result = scan_services_nmap(ip) if not behind_cf else "Protected by Cloudflare"
            final_results.append({
                "subdomain": f"{sub}.{domain}",
                "ip": ip,
                "behind_cf": behind_cf,
                "ports": ports,
                "nmap_result": nmap_result
            })

    generate_report(domain, final_results)

if __name__ == "__main__":
    main()
