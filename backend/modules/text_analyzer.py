"""
Module 3: Text Analyzer
Analyzes webpage text content for phishing indicators using NLP and AI.
"""

from transformers import pipeline
import re

class TextAnalyzer:
    """Analyzes text content using Natural Language Processing and AI."""

    def __init__(self):
        """Initialize the text analyzer with sentiment analysis model."""
        print("Loading text analysis model...")

        # Use a lightweight sentiment analysis model
        # DistilBERT is fast and works well on CPU
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            print("✅ Text analysis model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Could not load sentiment model: {e}")
            self.sentiment_analyzer = None

        # Phishing keyword patterns
        self.urgency_keywords = [
            'urgent', 'immediately', 'asap', 'right now', 'hurry',
            'limited time', 'expires', 'act now', 'don\'t wait',
            'deadline', 'time is running out', 'within 24 hours'
        ]

        self.fear_keywords = [
            'suspended', 'locked', 'blocked', 'terminated', 'closed',
            'violated', 'unauthorized', 'fraud', 'alert', 'warning',
            'security breach', 'compromised', 'hacked', 'stolen'
        ]

        self.action_keywords = [
            'verify', 'confirm', 'update', 'click here', 'login',
            'sign in', 'enter your', 'provide', 'validate',
            'authenticate', 'submit', 'respond', 'action required'
        ]

        self.credential_keywords = [
            'password', 'username', 'credit card', 'ssn', 'social security',
            'account number', 'pin', 'cvv', 'security code',
            'billing information', 'payment details', 'bank account'
        ]

        self.too_good_keywords = [
            'winner', 'congratulations', 'you\'ve won', 'prize',
            'free money', 'lottery', 'million dollars', 'inheritance',
            'claim your', 'selected', 'lucky'
        ]

    def analyze(self, text, url=None):
        """
        Analyze text content for phishing indicators.

        Args:
            text (str): The text content to analyze
            url (str, optional): URL for context

        Returns:
            dict: Analysis results with risk score and details
        """
        try:
            if not text or len(text.strip()) < 10:
                return self._error_result("Text too short or empty")

            # Normalize text
            text_lower = text.lower()

            # Initialize risk score
            risk_score = 0
            flags = []

            # Analysis 1: Urgency detection
            urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in text_lower)
            if urgency_count >= 3:
                risk_score += 25
                flags.append(f"⚠️ Multiple urgency indicators ({urgency_count} found)")
            elif urgency_count > 0:
                risk_score += 10
                flags.append(f"⚠️ Urgency language detected")

            # Analysis 2: Fear/threat detection
            fear_count = sum(1 for keyword in self.fear_keywords if keyword in text_lower)
            if fear_count >= 3:
                risk_score += 30
                flags.append(f"⚠️ Multiple fear/threat tactics ({fear_count} found)")
            elif fear_count > 0:
                risk_score += 15
                flags.append(f"⚠️ Threat language detected")

            # Analysis 3: Action pressure
            action_count = sum(1 for keyword in self.action_keywords if keyword in text_lower)
            if action_count >= 3:
                risk_score += 20
                flags.append(f"⚠️ Pressure to take action ({action_count} calls to action)")
            elif action_count > 0:
                risk_score += 8
                flags.append(f"⚠️ Action requested")

            # Analysis 4: Credential requests
            cred_count = sum(1 for keyword in self.credential_keywords if keyword in text_lower)
            if cred_count >= 2:
                risk_score += 25
                flags.append(f"⚠️ Requests sensitive information ({cred_count} types)")
            elif cred_count > 0:
                risk_score += 10
                flags.append(f"⚠️ Asks for credentials")

            # Analysis 5: Too good to be true
            tgtb_count = sum(1 for keyword in self.too_good_keywords if keyword in text_lower)
            if tgtb_count >= 2:
                risk_score += 20
                flags.append(f"⚠️ Unrealistic offers/claims")
            elif tgtb_count > 0:
                risk_score += 10
                flags.append(f"⚠️ Suspicious claims detected")

            # Analysis 6: Grammar and spelling (phishing often has poor grammar)
            grammar_issues = self._check_grammar(text)
            if grammar_issues > 5:
                risk_score += 15
                flags.append(f"⚠️ Multiple grammar/spelling issues")
            elif grammar_issues > 0:
                risk_score += 5
                flags.append(f"⚠️ Some grammar issues detected")

            # Analysis 7: Sentiment analysis (if model is loaded)
            if self.sentiment_analyzer:
                sentiment_risk = self._analyze_sentiment(text)
                risk_score += sentiment_risk
                if sentiment_risk > 0:
                    flags.append(f"⚠️ Negative/aggressive tone detected")

            # Analysis 8: Length analysis
            word_count = len(text.split())
            if word_count < 50:
                risk_score += 10
                flags.append("⚠️ Very short content (suspicious)")
            elif word_count > 1000:
                # Very long text might be trying to hide something
                if fear_count > 0 or urgency_count > 0:
                    risk_score += 5
                    flags.append("⚠️ Very long content with suspicious elements")

            # Analysis 9: ALL CAPS detection (aggressive/unprofessional)
            caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
            if caps_ratio > 0.3:
                risk_score += 15
                flags.append("⚠️ Excessive use of CAPITAL LETTERS")
            elif caps_ratio > 0.15:
                risk_score += 5
                flags.append("⚠️ Frequent capital letters (aggressive tone)")

            # Analysis 10: Exclamation marks (!!!!)
            exclamation_count = text.count('!')
            if exclamation_count > 5:
                risk_score += 10
                flags.append(f"⚠️ Excessive exclamation marks ({exclamation_count}!!!)")

            # Cap risk score at 100
            risk_score = min(100, risk_score)

            # Determine verdict
            if risk_score >= 70:
                verdict = "PHISHING"
                verdict_color = "🔴"
            elif risk_score >= 40:
                verdict = "SUSPICIOUS"
                verdict_color = "🟡"
            else:
                verdict = "SAFE"
                verdict_color = "🟢"

            return {
                'risk_score': risk_score,
                'verdict': verdict,
                'verdict_color': verdict_color,
                'flags': flags,
                'details': {
                    'urgency_count': urgency_count,
                    'fear_count': fear_count,
                    'action_count': action_count,
                    'credential_count': cred_count,
                    'too_good_count': tgtb_count,
                    'grammar_issues': grammar_issues,
                    'word_count': word_count,
                    'caps_ratio': round(caps_ratio, 2),
                    'exclamation_count': exclamation_count
                }
            }

        except Exception as e:
            return self._error_result(f"Error during analysis: {str(e)}")

    def _check_grammar(self, text):
        """
        Simple grammar check (counts basic issues).
        Real implementation would use more sophisticated NLP.

        Returns:
            int: Number of potential grammar issues
        """
        issues = 0

        # Multiple spaces
        if '  ' in text:
            issues += text.count('  ')

        # No space after punctuation
        patterns = [r'\.[a-zA-Z]', r',[a-zA-Z]', r'![a-zA-Z]']
        for pattern in patterns:
            issues += len(re.findall(pattern, text))

        # Common spelling mistakes in phishing
        common_mistakes = [
            'recieve', 'occured', 'untill', 'seperate', 'succesful',
            'neccessary', 'occassion', 'tommorow', 'independant'
        ]
        text_lower = text.lower()
        for mistake in common_mistakes:
            if mistake in text_lower:
                issues += 1

        return min(issues, 10)  # Cap at 10

    def _analyze_sentiment(self, text):
        """
        Analyze sentiment for aggressive/negative tone.

        Returns:
            int: Risk score contribution (0-15)
        """
        try:
            if not self.sentiment_analyzer:
                return 0

            # Truncate text if too long (model limit)
            text_sample = text[:512]

            result = self.sentiment_analyzer(text_sample)[0]

            # Phishing often has negative sentiment
            if result['label'] == 'NEGATIVE':
                # Higher confidence = more risk
                confidence = result['score']
                if confidence > 0.8:
                    return 15
                elif confidence > 0.6:
                    return 10
                else:
                    return 5

            return 0

        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 0

    def _error_result(self, error_message):
        """Return error result format."""
        return {
            'risk_score': 50,
            'verdict': 'ERROR',
            'verdict_color': '⚠️',
            'flags': [f'⚠️ {error_message}'],
            'details': {'error': error_message}
        }


# Test function
def test_text_analyzer():
    """Test the text analyzer with sample texts."""
    print("=" * 80)
    print("TEXT ANALYZER TEST")
    print("=" * 80)

    # Initialize analyzer
    analyzer = TextAnalyzer()

    # Test cases
    test_texts = [
        {
            'name': 'Legitimate Email',
            'text': '''Dear Customer,
                      Your order has been confirmed and will be shipped within 3-5 business days.
                      You can track your order using the tracking number provided.
                      Thank you for your purchase!'''
        },
        {
            'name': 'Phishing Email 1 (Urgency)',
            'text': '''URGENT! Your account will be SUSPENDED in 24 hours!
                      Click here IMMEDIATELY to verify your account or you will lose access FOREVER!
                      ACT NOW before it's too late!!!'''
        },
        {
            'name': 'Phishing Email 2 (Credentials)',
            'text': '''Security Alert: Unusual activity detected.
                      Please verify your account by entering your username, password, and credit card details.
                      Click here to confirm your identity immediately.'''
        },
        {
            'name': 'Normal Website',
            'text': '''Welcome to our website. We offer quality products at affordable prices.
                      Browse our catalog and find what you need. Free shipping on orders over $50.'''
        }
    ]

    for test in test_texts:
        print(f"\n{'=' * 80}")
        print(f"Test: {test['name']}")
        print(f"{'=' * 80}")
        print(f"Text: {test['text'][:100]}...")

        result = analyzer.analyze(test['text'])

        print(f"\nVerdict: {result['verdict_color']} {result['verdict']}")
        print(f"Risk Score: {result['risk_score']}%")
        print("\nFlags:")
        for flag in result['flags']:
            print(f"  {flag}")

        print("\nDetails:")
        for key, value in result['details'].items():
            print(f"  {key}: {value}")

    print("\n" + "=" * 80)
    print("✅ Text Analyzer is working!")
    print("=" * 80)


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_text_analyzer()
