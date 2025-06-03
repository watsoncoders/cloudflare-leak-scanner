# 🔍 Cloudflare Leak Scanner

**An advanced tool to discover origin IP addresses of websites that are (or should be) protected by Cloudflare.**

Developed by: **Pablo Rotem / פבלו רותם**  
🌐 Website: [https://pablo-guides.com](https://pablo-guides.com)

---

## 🧠 What This Tool Does

Cloudflare protects websites by hiding their real server IP addresses. However, due to DNS misconfigurations or leftover subdomains, some IPs might still be exposed.

This tool helps you:

- Scan common subdomains for a given domain.
- Resolve each subdomain's IP address.
- Determine whether the IP is protected by Cloudflare or exposed.
- Scan open ports on exposed IPs using `masscan`.
- Generate a full HTML report (RTL + Hebrew support).

---

## 📦 Installation & Usage Instructions

```bash
# 🔹 Clone the repository
git clone https://github.com/watsoncoders/cloudflare-leak-scanner.git
cd cloudflare-leak-scanner

# 🔹 Install Python dependencies
pip install dnspython jinja2 requests

# 🔹 Install system tools
sudo apt install masscan      # For fast port scanning
sudo apt install nmap         # (Optional) For advanced service detection
```

---

## 🚀 How to Run the Scanner

```bash
python3 cloudflare_scanner.py
```

You will be prompted to enter a domain (e.g., `example.com`).

What happens next:
1. Common subdomains are resolved to IP addresses.
2. Each IP is checked to see if it’s protected by Cloudflare.
3. If the IP is exposed, it is scanned with `masscan` for open ports.
4. A styled HTML report in Hebrew is saved as `report.html`.

---

## 📁 Output Example (HTML Report)

| Subdomain           | IP Address     | Cloudflare Protected | Open Ports    |
|---------------------|----------------|-----------------------|---------------|
| www.example.com      | 104.21.35.34   | ✅ Yes                | -             |
| cpanel.example.com   | 198.51.100.20  | ❌ No                 | 80, 443, 22   |

The `report.html` file is:
- Fully RTL (Hebrew) and printable
- Color-coded for safety (green = safe, red = leak)
- Can be opened in any modern browser

---

## 🧾 Template Customization

You can edit the report's visual style by modifying:

```
templates/report_template.html
```

The layout is clean, mobile-friendly, and designed for RTL Hebrew use.

---

## 🔧 Future Features (Ideas)

- Use `nmap -sV` to detect services and versions on leaked IPs.
- Add CSV and PDF export options.
- Historical DNS leak check via APIs (e.g., SecurityTrails, Censys).
- CLI flags for automation:
  ```bash
  python3 cloudflare_scanner.py --domain example.com --out html
  ```
- Web UI with Flask or Django.

---

## 👨‍💻 Developer Info

**Pablo Rotem / פבלו רותם**  
🌐 Website: [https://pablo-guides.com](https://pablo-guides.com)

If you like this project, please ⭐ star the repo and share it!

---

## 📜 License

MIT License.  
Feel free to use, modify, and improve this tool responsibly.
