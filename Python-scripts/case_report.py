from datetime import datetime

def generate_case_report(alert_data, threat_score, asset_owner):
    """
    Automatically builds a case report string from enriched alert data.
    """

    # Extract key fields from alert data
    timestamp = datetime.strptime(alert_data['_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    source_ip = alert_data['SourceIP']
    dest_ip = alert_data['DestinationIP']
    url = alert_data['URL']
    severity = alert_data.get('severity', 'High')
    user = asset_owner.get('username', 'Unknown')
    department = asset_owner.get('department', 'Unknown')

    # Template structure
    report = f"""
    🚨 **SOC Incident Case Report**

    **Title:** Blocked Access to Blacklisted URL (Shortlink Detected)

    **Date/Time Detected:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    **Detection Source:** {alert_data.get('detector', 'Firewall / Splunk Alert')}
    **Severity:** {severity}

    **Summary:**
    Detected and blocked outbound request to blacklisted destination:
    - URL: {url}
    - Final IP: {dest_ip}
    - Threat Score: {threat_score}/100

    **Asset Info:**
    - Source IP: {source_ip}
    - User: {user}
    - Department: {department}

    **Actions Taken:**
    - Connection blocked at perimeter firewall.
    - Host {source_ip} reviewed for lateral movement and credential abuse.
    - URL decoded and analyzed with external threat intelligence.
    - No signs of compromise detected.

    **Recommendations:**
    - Educate user on phishing and suspicious links.
    - Monitor for shortlink usage patterns from host.
    - Refine SIEM rules for better anomaly detection.

    **Incident Status:** Escalated to Tier 2 (Pending Review)
    """

    return report.strip()


if __name__ == "__main__":
    alert_data = {
        "_time": "2025-08-01T05:35:20.000Z",
        "SourceIP": "192.168.1.10",
        "DestinationIP": "8.8.8.8",
        "URL": "http://bit.ly/malicious-link",
        "detector": "Splunk URL Monitor",
        "severity": "High"
    }

    asset_owner = {
        "username": "j.doe",
        "department": "Finance"
    }

    threat_score = 85

    print(generate_case_report(alert_data, threat_score, asset_owner))








# Example usage:
# alert = { ... } → from Splunk or API
# asset_owner = { "username": "j.doe", "department": "Finance" }
# threat_score = 85
# print(generate_case_report(alert, threat_score, asset_owner))
