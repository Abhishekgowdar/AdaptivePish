"""
Module 1: URL Analyzer
Analyzes URLs for phishing indicators using rule-based detection.
"""

import re
from urllib.parse import urlparse
from datetime import datetime

class URLAnalyzer:
    """Analyzes URLs for suspicious patterns that indicate phishing."""

    def __init__(self):
        """Initialize the URL analyzer with suspicious patterns."""
        # Suspicious top-level domains often used by phishers
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']

        # Common legitimate domains (whitelist)
        self.legitimate_domains = [
            'google.com', 'facebook.com', 'amazon.com', 'microsoft.com',
            'apple.com', 'paypal.com', 'netflix.com', 'linkedin.com',
            'twitter.com', 'instagram.com', 'github.com', 'stackoverflow.com'
        ]

        # Suspicious keywords often in phishing URLs
        self.suspicious_keywords = [
            'verify', 'account', 'update', 'secure', 'banking', 'confirm',
            'login', 'signin', 'password', 'suspended', 'locked', 'alert'
        ]

    def analyze(self, url):
        """
        Main analysis function - checks URL for phishing indicators.

        Args:
            url (str): The URL to analyze

        Returns:
            dict: Analysis results with risk score and details
        """
        try:
            # Parse the URL
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()

            # Initialize risk score (0-100, higher = more suspicious)
            risk_score = 0
            flags = []

            # Check 1: URL Length (phishing URLs are often very long)
            if len(url) > 75:
                risk_score += 20
                flags.append(f"⚠️ Very long URL ({len(url)} characters)")
            elif len(url) > 54:
                risk_score += 10
                flags.append(f"⚠️ Long URL ({len(url)} characters)")

            # Check 2: HTTPS (no HTTPS is suspicious)
            if not url.startswith('https://'):
                risk_score += 15
                flags.append("⚠️ No HTTPS (insecure connection)")

            # Check 3: IP Address instead of domain name
            if self._is_ip_address(domain):
                risk_score += 25
                flags.append("⚠️ Using IP address instead of domain name")

            # Check 4: Suspicious TLD
            for tld in self.suspicious_tlds:
                if domain.endswith(tld):
                    risk_score += 20
                    flags.append(f"⚠️ Suspicious domain ending: {tld}")
                    break

            # Check 5: Too many subdomains
            subdomain_count = domain.count('.') - 1
            if subdomain_count > 3:
                risk_score += 15
                flags.append(f"⚠️ Too many subdomains ({subdomain_count})")
            elif subdomain_count > 2:
                risk_score += 8
                flags.append(f"⚠️ Multiple subdomains ({subdomain_count})")

            # Check 6: Special characters (@ symbol, --, etc.)
            if '@' in url:
                risk_score += 25
                flags.append("⚠️ Contains '@' symbol (redirect trick)")

            if '//' in parsed.path:
                risk_score += 10
                flags.append("⚠️ Contains '//' in path")

            if url.count('-') > 3:
                risk_score += 10
                flags.append(f"⚠️ Too many hyphens ({url.count('-')})")

            # Check 7: Suspicious keywords in URL
            suspicious_found = []
            url_lower = url.lower()
            for keyword in self.suspicious_keywords:
                if keyword in url_lower:
                    suspicious_found.append(keyword)

            if len(suspicious_found) >= 3:
                risk_score += 15
                flags.append(f"⚠️ Multiple suspicious keywords: {', '.join(suspicious_found[:3])}")
            elif len(suspicious_found) > 0:
                risk_score += 5
                flags.append(f"⚠️ Suspicious keyword: {suspicious_found[0]}")

            # Check 8: Legitimate domain check
            is_legitimate = False
            for legit_domain in self.legitimate_domains:
                if legit_domain in domain:
                    is_legitimate = True
                    # But check if it's EXACTLY that domain or a subdomain
                    if not (domain == legit_domain or domain.endswith('.' + legit_domain)):
                        # Fake! Like "google.com.phishing.tk"
                        risk_score += 30
                        flags.append(f"⚠️ FAKE DOMAIN: Contains '{legit_domain}' but isn't legitimate")
                        is_legitimate = False
                    break

            # If it's a verified legitimate domain, reduce risk
            if is_legitimate:
                risk_score = max(0, risk_score - 20)
                flags.append(f"✅ Recognized legitimate domain")

            # Check 9: Homograph attack detection (e.g., paypa1 vs paypal)
            if self._has_homograph_chars(domain):
                risk_score += 15
                flags.append("⚠️ Contains look-alike characters")

            # Check 10: Port number (suspicious if non-standard)
            if parsed.port and parsed.port not in [80, 443]:
                risk_score += 10
                flags.append(f"⚠️ Non-standard port: {parsed.port}")

            # Cap risk score at 100
            risk_score = min(100, risk_score)

            # Determine verdict based on risk score
            if risk_score >= 70:
                verdict = "PHISHING"
                verdict_color = "🔴"
            elif risk_score >= 40:
                verdict = "SUSPICIOUS"
                verdict_color = "🟡"
            else:
                verdict = "SAFE"
                verdict_color = "🟢"

            # Return comprehensive results
            return {
                'url': url,
                'risk_score': risk_score,
                'verdict': verdict,
                'verdict_color': verdict_color,
                'flags': flags,
                'details': {
                    'domain': domain,
                    'has_https': url.startswith('https://'),
                    'url_length': len(url),
                    'subdomain_count': subdomain_count,
                    'is_legitimate': is_legitimate
                }
            }

        except Exception as e:
            # If URL parsing fails, it's probably malformed
            return {
                'url': url,
                'risk_score': 80,
                'verdict': 'SUSPICIOUS',
                'verdict_color': '🟡',
                'flags': [f'⚠️ Error parsing URL: {str(e)}'],
                'details': {'error': str(e)}
            }

    def _is_ip_address(self, domain):
        """Check if domain is an IP address."""
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        return bool(ip_pattern.match(domain))

    def _has_homograph_chars(self, text):
        """Check for common homograph attack characters."""
        # Common substitutions: 0 for o, 1 for l, etc.
        suspicious_patterns = [
            r'paypa1',  # paypal with 1
            r'g00gle',  # google with zeros
            r'micr0soft',  # microsoft with zero
            r'amaz0n',  # amazon with zero
        ]

        text_lower = text.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower):
                return True
        return False


# Test function
def test_url_analyzer():
    """Test the URL analyzer with sample URLs."""
    analyzer = URLAnalyzer()

    # Test URLs
    test_urls = [
        "https://www.google.com",  # Legitimate
        "http://paypa1-secure.tk/login",  # Phishing
        "https://192.168.1.1/admin",  # IP address
        "http://microsoft-account-verify-security-alert.xyz",  # Suspicious
        "https://www.amazon.com",  # Legitimate
        "http://www.bank-of-america-secure-login-verify.ml",  # Phishing
    ]

    print("=" * 80)
    print("URL ANALYZER TEST")
    print("=" * 80)

    for url in test_urls:
        result = analyzer.analyze(url)
        print(f"\nURL: {url}")
        print(f"Verdict: {result['verdict_color']} {result['verdict']} (Risk: {result['risk_score']}%)")
        if result['flags']:
            print("Flags:")
            for flag in result['flags']:
                print(f"  {flag}")
        print("-" * 80)


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_url_analyzer()
