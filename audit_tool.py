import os
import platform
import csv
import subprocess

def check_os_version():
    """Get operating system details"""
    return platform.platform()

def check_firewall_status():
    """Check firewall staus for Windows or Linux"""
    try:
        if os.name == 'nt': # Windows
            result = subprocess.run (['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True)
            if 'ON' in result.stdout:
                return "Enabled"
            else:
                return "Disabled"
        else: #Linux

            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            if 'active' in result.stdout:
                return "Enabled"
            else:
                return "Disabled"
    except Exception as e:
        return f"Error: {e}"
    
def check_users():
    if os.name == 'nt':
        result = subprocess.run(['net', 'user'], capture_output=True, text=True)
    else:
        result = subprocess.run(['cat', '/etc/passwd'], capture_output=True, text=True)
    return result.stdout


def main():
    results = []
    
    print("Running System Audit...\n")
    
    os_version = check_os_version()
    firewall_status = check_firewall_status()
    user = check_users()
    
    results.append(["Control", "Result"])
    results.append(["Operating System", os_version])
    results.append(["Firewall Status", firewall_status])
    results.append(["Users", user])

    # write results to csv
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)
    
    print("Audit completed! Results saved in results.csv")

if __name__ == "__main__":
    main()    
